# =============================================
#              MODULE IMPORTS
# =============================================

import pandapower as pp
import pandapower.networks as nw

# =============================================
#              GRID METRICS
# =============================================


def get_topology_metrics(net):
    
    topology_metrics = {}

    topology_metrics["total_buses"] = len(net.bus)
    topology_metrics["total_lines"] = len(net.line)
    topology_metrics["total_loads"] = len(net.load)
    topology_metrics["total_generators"] = len(net.gen)
    topology_metrics["total_transformers"] = len(net.trafo) +len(net.trafo3w)

    return topology_metrics

def get_electrical_metrics(net):

    electrical_metrics = {}

    electrical_metrics['current_demand_mw'] = net.res_load["p_mw"].sum()
    electrical_metrics['total_generation_mw'] = net.res_gen["p_mw"].sum()
    electrical_metrics['max_line_loading_percent'] = net.res_line['loading_percent'].max()
    electrical_metrics["min_voltage_pu"] = net.res_bus.vm_pu.min()
    electrical_metrics["max_volateg_pu"] = net.res_bus.vm_pu.max()

    return electrical_metrics
    

def get_security_metrics(net):
    '''
    A non-convergent power flow leaves loading_percent entirely NaN, and `NaN > 100` is always False in pandas, 
    so a genuinely collapsed grid would otherwise report ZERO overloaded lines here. 
    Report every line as insecure instead - "unknown" is the honest answer, 
    and unknown-during-collapse should never be silently read as "fine."
    '''
    if len(net.line) > 0 and net.res_line.loading_percent.isna().all():
        return {
            "overloaded_line_count": len(net.line),
            "overloaded_line_ids": list(net.line.index),
            "collapsed": True,
        }

    overloaded_lines = net.res_line[net.res_line.loading_percent > 100]

    security_metrics = { 
    "overloaded_line_count" : len(overloaded_lines),
    "overloaded_line_ids" : list(overloaded_lines.index),
    "collapsed": False,
    }

    return security_metrics

def _summarize_asset_class(records):
    """
    Rolls up one asset class's slice of the asset_registry into:
    how many assets are in a non-NORMAL fault state, which specific asset is
    closest to failure (lowest RUL), and the distribution of fault classes present.
    """
    if not records:
        return {
            "count": 0,
            "min_rul_days": None,
            "worst_asset_id": None,
            "worst_asset_detail": None,
            "fault_distribution": {},
            "critical_count": 0,
        }

    fault_distribution = {}
    min_rul = None
    worst_id = None
    worst_detail = None
    critical_count = 0

    for asset_id, rec in records.items():
        fault_class = rec.get("fault_class", "Normal")
        fault_distribution[fault_class] = fault_distribution.get(fault_class, 0) + 1
        if fault_class.strip().lower() != "normal":
            critical_count += 1

        rul = rec.get("rul_days")
        if rul is not None and (min_rul is None or rul < min_rul):
            min_rul = rul
            worst_id = asset_id
            worst_detail = rec

    return {
        "count": len(records),
        "min_rul_days": round(min_rul, 2) if min_rul is not None else None,
        "worst_asset_id": worst_id,
        # Full feature record for the worst asset -- so a dashboard card can render it
        # directly without a second lookup into the raw asset_registry.
        "worst_asset_detail": worst_detail,
        "fault_distribution": fault_distribution,
        "critical_count": critical_count,
    }


def get_health_metrics(net, asset_registry=None):
    """
    Aggregates the AI-facing asset_registry (populated by scenario_engine's
    simulate_* functions) into a single health view for the four IEEE-493
    critical asset classes: transformers, generators, circuit breakers, and relays.
    """
    if asset_registry is None:
        return {"grid_health": "UNKNOWN", "asset_summary": {}}

    transformers = _summarize_asset_class(asset_registry.get("transformers", {}))
    generators = _summarize_asset_class(asset_registry.get("generators", {}))
    circuit_breakers = _summarize_asset_class(asset_registry.get("circuit_breakers", {}))
    relays = _summarize_asset_class(asset_registry.get("relays", {}))

    total_critical = (
        transformers["critical_count"]
        + generators["critical_count"]
        + circuit_breakers["critical_count"]
        + relays["critical_count"]
    )

    if total_critical == 0:
        grid_health = "HEALTHY"
    elif total_critical <= 2:
        grid_health = "DEGRADED"
    else:
        grid_health = "CRITICAL"

    return {
        "grid_health": grid_health,
        "total_assets_in_fault": total_critical,
        "asset_summary": {
            "transformers": transformers,
            "generators": generators,
            "circuit_breakers": circuit_breakers,
            "relays": relays,
        },
    }

print("grid_metrics imported successfully")

def get_observation_vector(net):
    # Extract and clean voltages
    voltages = net.res_bus.vm_pu.fillna(0).tolist()

    # Extract, clean, and normalize line loadings
    loadings = (net.res_line.loading_percent.fillna(0) / 100.0).tolist()

    # Concatenate into a single 1D vector
    observation_vector = voltages + loadings

    return observation_vector


def _clamp(value, low=0.0, high=100.0):
    return max(low, min(high, value))


def get_resilience_index(net):
    """
    Computes a composite Grid Resilience Index (GRI) on a 0-100 scale from three sub-scores:

    - voltage_score:  100 at nominal (1.0 pu), decays to 0 at +/-0.10 pu deviation
    - loading_score:  100 up to 80% max line loading, decays to 0 at 130%
    - security_score: 100 with no overloaded lines, -15 pts per overloaded line

    Weights (0.35 / 0.40 / 0.25) favor thermal loading slightly, since overloads are
    the most immediate cause of cascading trips, followed by voltage collapse risk.
    The discrete overload count is weighted least since it's already partially
    captured by loading_score.
    """

    has_lines = len(net.line) > 0
    collapsed = has_lines and net.res_line.loading_percent.isna().all()

    if collapsed:
        return {
            "grid_resilience_index": 0.0,
            "voltage_score": 0.0,
            "loading_score": 0.0,
            "security_score": 0.0,
            "collapsed": True,
        }

    voltages = net.res_bus.vm_pu.dropna()
    if voltages.empty:
        voltage_score = 0.0
    else:
        max_deviation = (voltages - 1.0).abs().max()
        voltage_score = _clamp(100.0 - (max_deviation / 0.10) * 100.0)

    loadings = net.res_line.loading_percent.dropna()
    if loadings.empty:
        loading_score = 100.0
    else:
        max_loading = loadings.max()
        loading_score = _clamp(100.0 - max(0.0, max_loading - 80.0) * 2.0)

    overloaded_count = len(net.res_line[net.res_line.loading_percent > 100])
    security_score = _clamp(100.0 - (overloaded_count * 15.0))

    gri = (0.35 * voltage_score) + (0.40 * loading_score) + (0.25 * security_score)

    return {
        "grid_resilience_index": round(gri, 2),
        "collapsed": False,
        "voltage_score": round(voltage_score, 2),
        "loading_score": round(loading_score, 2),
        "security_score": round(security_score, 2),
    }