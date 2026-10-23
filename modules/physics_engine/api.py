# =============================================
#              MODULE IMPORTS
# =============================================

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandapower as pp
import uvicorn
import os
import sys
from pathlib import Path
import warnings
import datetime
import asyncio
import copy
import time
import math
import pandas as pd
import random

# Ignore specific internal pandapower deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandapower")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandapower")

# --- Path Routing ---
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

from twin_model import TwinModel
from grid_metrics import get_resilience_index, get_security_metrics, get_health_metrics
from scenario_engine import simulate_generator_wear,simulate_transformer_aging, simulate_breaker_degradation, simulate_relay_degradation, simulate_generator_trip, simulate_weather_event


from modules.event_store import log_event, get_events

# =============================================
#              API ARCHITECTURE
# =============================================
# NOTE: This file is the DIGITAL TWIN service only. It has zero knowledge of LangGraph, Gemini, RAG, or anything else in the AI architecture. 
# It exposes physics (topology, telemetry, contingency testing, actuation) over plain HTTP/WebSocket so that ANY external client 
# - the AI agent service, a human operator's browser, a test harness - can drive it purely through this API.

app = FastAPI(title="Digital Twin API")

# CORS Middleware to allow the React frontend (and the separate AI service) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# 1. Instantiate the grid objects globally (Unified State)
grids = {
    "39": TwinModel(grid_type="39"),
    "118": TwinModel(grid_type="118")
}

# 2. Run baselines and apply scenarios before the server opens
print("Setting up grid scenarios...")
grids["39"].run_baseline_simulation()

'''
STARTUP STRESS LEVEL for IEEE-118. derate_multiplier=0.05 means every line's thermal rating is cut to 5% of nominal 
- extremely aggressive, which is why nudging a single bus's load by any large amount tends to blow past 100% loading or fail to converge at all. 
Raise this (e.g. to 0.15-0.25) for more headroom to test bigger interventions without the grid being perpetually on the edge of collapse. 
Lower it for overload scenarios to be trivially easy to trigger for demos.
'''

STARTUP_DERATE_MULTIPLIER = float(os.getenv("SWING_STARTUP_DERATE", "0.25"))
STARTUP_LOAD_MULTIPLIER = float(os.getenv("SWING_STARTUP_LOAD_MULT", "1.2"))

grids["118"].apply_scenario(load_multiplier=STARTUP_LOAD_MULTIPLIER, derate_multiplier=STARTUP_DERATE_MULTIPLIER)
grids["118"].run_baseline_simulation()


@app.get('/')
def read_root():
    return {'message': 'Digital Twin Engine is Online'}


# =============================================
#      N-1 CONTINGENCY SCANNER (BACKGROUND)
# =============================================
# Continuously simulates the loss of each line and each generator, one at a time, on a deep copy of the live grid 
# - never the live grid itself - and caches whether the system stays secure (converges, no line >100% loading) under each contingency.

# IMPORTANT PERFORMANCE NOTE: pp.runpp() is synchronous, CPU-bound code.
# Scanning ~170+ contingencies (118 lines + ~54 gens on the 118-bus case) takes several real seconds. 
# Running that directly inside an `async def` body would monopolize the single-threaded event loop for that whole stretch, 
# freezing the WebSocket telemetry stream and any HTTP request (like /change_load) that arrives during the scan. 
# To avoid that, the actual scanning work is a plain synchronous function, and the async loop only ever calls it via asyncio.to_thread(), 
# which runs it on a worker thread and lets the event loop keep serving telemetry and requests concurrently.

contingency_cache = {grid_key: {} for grid_key in grids.keys()}


def _scan_contingencies_sync(grid_key: str) -> dict:
    base_net = grids[grid_key].net
    
    # --- FIX: CHECK BASE GRID CONVERGENCE FIRST ---
    # If the grid is already collapsed from a catastrophic trip, 
    # trying to run 170 contingencies will hang the background thread.
    try:
        pp.runpp(copy.deepcopy(base_net), solver='nr')
    except pp.LoadflowNotConverged:
        return {
            "lines": {},
            "generators": {},
            "n_minus_1_secure": False,
            "insecure_contingency_count": "FATAL (Base Grid Collapsed)",
            "last_scan_timestamp": time.time()
        }
    # ----------------------------------------------

    # NOTE: tripping a line or generator can strand part of the network
    # with no slack bus (an "island"). Depending on pandapower version/
    # solver path, that does NOT always raise pp.LoadflowNotConverged --
    # it can just as easily raise numpy.linalg.LinAlgError (singular
    # Jacobian), a UserWarning-turned-error, or a bare pandapower
    # exception from the topology/island-detection step. Any one of those
    # escaping this loop propagates out of _scan_contingencies_sync,
    # gets caught by the broad `except Exception` in
    # contingency_scanner_loop, and silently aborts the ENTIRE scan for
    # this cycle -- contingency_cache[grid_key] is never written, so the
    # frontend is stuck showing "Scanning..." forever, and since the same
    # topology is rescanned every interval, the same contingency fails
    # the same way every single time. Catching Exception per-contingency
    # (instead of only pp.LoadflowNotConverged) means one bad contingency
    # is recorded as insecure/non-converged and the scan continues.

    line_results = {}
    for line_idx in base_net.line.index:
        test_net = copy.deepcopy(base_net)
        test_net.line.at[line_idx, 'in_service'] = False
        try:
            pp.runpp(test_net, solver='nr')
            max_loading = float(test_net.res_line.loading_percent.max())
            line_results[int(line_idx)] = {
                "converged": True,
                "max_loading_percent": round(max_loading, 2),
                "secure": bool(max_loading <= 100.0)
            }
        except pp.LoadflowNotConverged:
            line_results[int(line_idx)] = {"converged": False, "max_loading_percent": None, "secure": False}
        except Exception as e:
            print(f"[N-1 SCANNER] grid {grid_key} line {line_idx} contingency raised {type(e).__name__}: {e}")
            line_results[int(line_idx)] = {
                "converged": False, "max_loading_percent": None, "secure": False,
                "error": f"{type(e).__name__}: {e}"
            }

    gen_results = {}
    for gen_idx in base_net.gen.index:
        test_net = copy.deepcopy(base_net)
        test_net.gen.at[gen_idx, 'in_service'] = False
        try:
            pp.runpp(test_net, solver='nr')
            max_loading = float(test_net.res_line.loading_percent.max())
            gen_results[int(gen_idx)] = {
                "converged": True,
                "max_loading_percent": round(max_loading, 2),
                "secure": bool(max_loading <= 100.0)
            }
        except pp.LoadflowNotConverged:
            gen_results[int(gen_idx)] = {"converged": False, "max_loading_percent": None, "secure": False}
        except Exception as e:
            print(f"[N-1 SCANNER] grid {grid_key} gen {gen_idx} contingency raised {type(e).__name__}: {e}")
            gen_results[int(gen_idx)] = {
                "converged": False, "max_loading_percent": None, "secure": False,
                "error": f"{type(e).__name__}: {e}"
            }

    insecure_count = sum(
        1 for r in list(line_results.values()) + list(gen_results.values()) if not r["secure"]
    )

    return {
        "lines": line_results,
        "generators": gen_results,
        "n_minus_1_secure": insecure_count == 0,
        "insecure_contingency_count": insecure_count,
        "last_scan_timestamp": time.time()
    }


async def contingency_scanner_loop(grid_key: str, interval_seconds: int = 30):
    while True:
        try:
            result = await asyncio.to_thread(_scan_contingencies_sync, grid_key)
            contingency_cache[grid_key] = result
        except Exception as e:
            # This is the outer safety net -- with the per-contingency
            # try/except above in place, this should now only fire for
            # something truly unexpected (e.g. grids[grid_key] missing).
            # Print the full traceback so a real bug here is visible in
            # the server logs instead of just a one-line summary.
            import traceback
            print(f"[N-1 SCANNER] Error scanning grid {grid_key}: {e}")
            traceback.print_exc()
        await asyncio.sleep(interval_seconds)


@app.on_event("startup")
async def launch_background_scanners():
    for grid_key in grids.keys():
        asyncio.create_task(contingency_scanner_loop(grid_key, interval_seconds=30))


@app.get("/rl_status")
def get_rl_status():
    '''
    Reports which RL policies actually exist on disk, for both grids and both RL-eligible action types. 
    '''
    models_dir = Path(__file__).resolve().parent.parent.parent / "models"
    grids_to_check = ["39", "118"]
    actions_to_check = ["shed_load", "redispatch_gen"]

    status = {}
    for g in grids_to_check:
        status[g] = {}
        for a in actions_to_check:
            path = models_dir / f"rl_optimizer_{a}_{g}.zip"
            if path.exists():
                stat = path.stat()
                status[g][a] = {
                    "trained": True,
                    "size_kb": round(stat.st_size / 1024, 1),
                    "last_trained": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            else:
                status[g][a] = {"trained": False}

    return status


@app.get("/contingency/{grid}")
def get_contingency_status(grid: str):
    '''Returns the latest N-1 security scan for the given grid. May be empty
    for a few seconds after startup until the first background scan completes.'''
    if grid not in contingency_cache:
        raise HTTPException(status_code=404, detail='Grid not Found')
    return contingency_cache[grid]


# ==============================================================
#      PHYSICS ORACLE (validate-only, no actuation)
# ==============================================================
# A pure physics test: "if this action were applied, would the grid stay secure?" 
# This endpoint NEVER mutates the live grid - it always tests against a deep copy, exactly like the contingency scanner above. 
# This is the one endpoint the AI architecture's Physics Validator agent calls; the Digital Twin has no idea an LLM exists on the other end of that call, 
# it's just answering a physics question over HTTP.

class ActionRequest(BaseModel):
    action_type: str   # "SHED_LOAD", "REDISPATCH_GEN", or "LOAD_REDISTRIBUTION"
    target_bus: int
    mw_amount: float
    secondary_bus: int = None  # only used by LOAD_REDISTRIBUTION


def _apply_action(test_net, action_type: str, target_bus: int, mw_amount: float, secondary_bus: int = None) -> bool:
    """
    Mutates test_net (a deep copy, never the live grid) to reflect the given action. 
    Returns False if the action_type/bus combination is invalid (e.g. no matching facility), True if applied. 
    Shared by _test_action and the GRI-recompute step in /validate_action so both are guaranteed to apply the exact same physics change.
    """
    if action_type == "SHED_LOAD":
        matching = test_net.load[test_net.load.bus == target_bus].index
        if matching.empty:
            return False
        idx = matching[0]
        current_mw = test_net.load.at[idx, "p_mw"]
        test_net.load.at[idx, "p_mw"] = max(0.0, current_mw - mw_amount)
        return True

    elif action_type == "REDISPATCH_GEN":
        matching = test_net.gen[test_net.gen.bus == target_bus].index
        if matching.empty:
            return False
        idx = matching[0]
        test_net.gen.at[idx, "p_mw"] += mw_amount
        return True

    elif action_type == "LOAD_REDISTRIBUTION":
        '''
        Moves mw_amount of load FROM target_bus TO secondary_bus - net zero change in total system demand. 
        This is the action type that actually does what "relieve an overloaded corridor by shifting load elsewhere" means, 
        as opposed to SHED_LOAD which just reduces total demand outright.
        '''
        if secondary_bus is None:
            return False
        source_matching = test_net.load[test_net.load.bus == target_bus].index
        dest_matching = test_net.load[test_net.load.bus == secondary_bus].index
        if source_matching.empty or dest_matching.empty:
            return False
        source_idx = source_matching[0]
        dest_idx = dest_matching[0]
        current_source_mw = test_net.load.at[source_idx, "p_mw"]
        actual_shift = min(mw_amount, current_source_mw)  # can't shift more than the source bus is carrying
        test_net.load.at[source_idx, "p_mw"] = current_source_mw - actual_shift
        test_net.load.at[dest_idx, "p_mw"] += actual_shift
        return True

    return False


def _test_action(base_net, action_type: str, target_bus: int, mw_amount: float, secondary_bus: int = None):
    """
    Shared physics-testing core used by BOTH /validate_action and  /optimize_action. 
    Always operates on a deep copy - base_net itself is never mutated. 
    Returns (converged: bool|None, max_loading_percent: float|None). 
    converged=None means the action_type/target_bus itself was invalid (e.g. no matching facility), not a power-flow failure.
    """
    test_net = copy.deepcopy(base_net)

    if not _apply_action(test_net, action_type, target_bus, mw_amount, secondary_bus):
        return None, None

    try:
        pp.runpp(test_net, solver="nr")
        return True, float(test_net.res_line.loading_percent.max())
    except pp.LoadflowNotConverged:
        return False, None


@app.post("/validate_action/{grid}")
def validate_action(grid: str, action: ActionRequest):
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    base_net = grids[grid].net
    gri_before = get_resilience_index(base_net)["grid_resilience_index"]

    converged, max_loading = _test_action(base_net, action.action_type, action.target_bus, action.mw_amount, action.secondary_bus)

    if converged is None:
        return {"valid": False, "resulting_max_loading_percent": None,
                "gri_before": gri_before, "gri_after": None, "gri_improvement": None,
                "error": f"Bus {action.target_bus} (or secondary bus {action.secondary_bus}) has no matching facility for '{action.action_type}'."}

    if not converged:
        return {"valid": False, "resulting_max_loading_percent": None,
                "gri_before": gri_before, "gri_after": None, "gri_improvement": None,
                "error": "Power flow did not converge for this action."}

    # Recompute GRI on the same post-action state used for the loading check
    test_net = copy.deepcopy(base_net)
    _apply_action(test_net, action.action_type, action.target_bus, action.mw_amount, action.secondary_bus)
    pp.runpp(test_net, solver="nr")
    gri_after = get_resilience_index(test_net)["grid_resilience_index"]

    # Allow a micro-tolerance of 100.2% to account for pandapower float precision formatting
    secure = max_loading <= 100.2
    return {
        "valid": secure,
        "resulting_max_loading_percent": round(max_loading, 2),
        "gri_before": gri_before,
        "gri_after": gri_after,
        "gri_improvement": round(gri_after - gri_before, 2),
        "error": None if secure else f"Max line loading {max_loading:.1f}% -- still overloaded."
    }


# =============================================
#             OPTIMIZATION ENGINE 
# =============================================
# The Decision Agent (LLM) decides the STRATEGY -- which action_type, which bus (or bus PAIR, for LOAD_REDISTRIBUTION). 
# It should NOT be guessing the exact MW value; that's a physics optimization problem, not a language one. 
# This endpoint runs a bisection search over mw_amount to find the MINIMUM value that clears the overload (max line loading <= 100%), 
# so the agent always proposes the smallest corrective action that actually  works - no more, no less. 
# Every trial point goes through _test_action on a deep copy; the live grid is never touched by this search.


def _emergency_grid_rescue(base_net):
    """
    Iteratively sheds 10% of total grid load globally until the 
    Newton-Raphson power flow matrix regains mathematical stability.
    """
    rescue_net = copy.deepcopy(base_net)
    total_original_load = float(rescue_net.load['p_mw'].sum())
    
    for iteration in range(1, 10):
        # Scale the active power load vector down by 10%
        rescue_net.load['p_mw'] *= 0.90
        
        try:
            pp.runpp(rescue_net, solver="nr")
            # If we reach here, the Jacobian matrix is no longer singular!
            current_load = float(rescue_net.load['p_mw'].sum())
            total_mw_shed = total_original_load - current_load
            max_loading = float(rescue_net.res_line.loading_percent.max())
            
            return True, total_mw_shed, max_loading
        except pp.LoadflowNotConverged:
            continue
            
    return False, 0.0, None


@app.get('/grid_status')
def get_grid_status(grid: str = '39'):
    '''
    Returns topological stats, current MW capacity, AND a live resilience snapshot (GRI + security metrics) for the given grid. 
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')
        
    target_grid = grids[grid].net
    total_demand_mw = float(target_grid.load['p_mw'].sum())
    total_gen_capacity_mw = float(target_grid.gen['p_mw'].sum()) if len(target_grid.gen) else 0.0
    resilience = get_resilience_index(target_grid)
    security = get_security_metrics(target_grid)

    # --- Compute per-bus loads to pass to the AI Agent ---
    bus_loads = {str(idx): 0.0 for idx in target_grid.bus.index}
    for _, row in target_grid.load.iterrows():
        bus_id = str(int(row['bus']))
        if bus_id in bus_loads:
            bus_loads[bus_id] += row['p_mw']

    return {
        'active_grid': f'IEEE {grid}-Bus',
        'buses': len(target_grid.bus),
        'lines': len(target_grid.line),
        'total_demand_mw': round(total_demand_mw, 2),
        'total_generation_capacity_mw': round(total_gen_capacity_mw, 2),
        # capacity_max_mw is the reference the Risk Assessment Agent compares forecast p90 against - current total system load, 
        # not nameplate generation capacity, since that's what "the grid is at X% of what it's currently carrying" should be measured against.
        'capacity_max_mw': round(total_demand_mw, 2),
        'resilience': resilience,
        'security': security,
        'bus_loads': bus_loads,
    }


@app.post('/redistribute_load/{grid}')
def redistribute_load(grid: str, source_bus: int, destination_bus: int, mw_amount: float):
    '''
    Moves mw_amount of load FROM source_bus TO destination_bus in ONE atomic power-flow solve - net zero change in total system demand.
    This is the actuation counterpart to the LOAD_REDISTRIBUTION action type: relieves a specific overloaded corridor by shifting load away
    from it rather than curtailing demand outright.
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    twin = grids[grid]
    try:
        source_matching = twin.net.load[twin.net.load.bus == source_bus].index
        dest_matching = twin.net.load[twin.net.load.bus == destination_bus].index
        if source_matching.empty:
            raise Exception(f"Source bus {source_bus} has no load facility.")
        if dest_matching.empty:
            raise Exception(f"Destination bus {destination_bus} has no load facility.")

        source_idx = source_matching[0]
        dest_idx = dest_matching[0]
        current_source_mw = twin.net.load.at[source_idx, "p_mw"]
        actual_shift = min(mw_amount, current_source_mw)

        twin.net.load.at[source_idx, "p_mw"] = current_source_mw - actual_shift
        twin.net.load.at[dest_idx, "p_mw"] += actual_shift

        pp.runpp(twin.net, solver='nr')
        summary = twin.get_current_state()
        twin.update_state(summary, "COMPLETED", f"Redistributed {actual_shift:.1f} MW: Bus {source_bus} -> Bus {destination_bus}")
        log_event("digital_twin", grid, "LOAD_REDISTRIBUTION", {
            "source_bus": source_bus, "destination_bus": destination_bus, "mw_amount": actual_shift
        })

        return {
            'status': 'Command Received',
            'action': f'Redistributed {actual_shift:.1f} MW from Bus {source_bus} to Bus {destination_bus}'
        }

    except pp.LoadflowNotConverged:
        raise HTTPException(status_code=400, detail="Redistribution caused a non-convergent power flow.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/topology")
def get_topology(grid: str = '118'):
    net = grids[grid].net

    # Which buses are actually generation, transformer-connected, or pure transmission junctions - computed once, not per-node, 
    # since it's the same set of buses regardless of which bus we're currently labeling.
    generator_buses = set(net.gen['bus'].tolist())
    transformer_buses = set(net.trafo['hv_bus'].tolist()) | set(net.trafo['lv_bus'].tolist())

    bus_to_gen_id = {int(row['bus']): idx for idx, row in net.gen.iterrows()}
    
    bus_to_trafo_id = {}
    for idx, row in net.trafo.iterrows():
        bus_to_trafo_id.setdefault(int(row['hv_bus']), idx)
        bus_to_trafo_id.setdefault(int(row['lv_bus']), idx)

    # Include current load in the node data
    nodes = []
    for idx, row in net.bus.iterrows():
        # Find if this bus has a load
        bus_loads = net.load[net.load.bus == idx]
        current_load = bus_loads['p_mw'].sum() if not bus_loads.empty else 0

        # Classify the node - generator takes priority over transformer. 
        # If a bus happens to be both (rare, but generators are the more visually/operationally significant fact about that bus).
        if idx in generator_buses:
            node_type = "GENERATOR"
        elif idx in transformer_buses:
            node_type = "TRANSFORMER"
        elif current_load > 0:
            node_type = "LOAD"
        else:
            node_type = "JUNCTION"

        node_data = {
            'id': str(idx), 'label': f'Bus {idx}', 'load': current_load, 'node_type': node_type,
            # relay_id == bus id directly (asset_registry["relays"] is keyed 1:1 by bus index already); 
            # gen_id/trafo_id are None when this bus isn't that asset type.
            'relay_id': int(idx),
            'gen_id': int(bus_to_gen_id[idx]) if idx in bus_to_gen_id else None,
            'trafo_id': int(bus_to_trafo_id[idx]) if idx in bus_to_trafo_id else None,
        }
        nodes.append({'data': node_data})
        
    edges = [{'data': {'id': f'line{idx}', 'source': str(int(row['from_bus'])), 'target': str(int(row['to_bus']))}} 
             for idx, row in net.line.iterrows()]
             
    return {'nodes': nodes, 'edges': edges}

@app.post('/inject_fault/{line_id}')
def trigger_fault(line_id: int, grid: str = '39'):
    '''Trips a line on the specifically requested grid.'''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')
        
    grids[grid].inject_line_fault(line_id)
    log_event("digital_twin", grid, "FAULT_INJECTED", {"line_id": line_id})
    return {'status': 'Command Received', 'action': f'Tripped Line {line_id} on IEEE {grid}'}

@app.post('/change_load/{bus_id}')
def update_grid_load(bus_id: int, new_mw: float, grid: str = '118'):
    '''
    Updates the MW load on a specific bus ID. This is the sole actuation surface for load-side actions - called by the React dashboard directly,
    or by the separate AI agent service once a human has approved its proposal. The Digital Twin doesn't care which one calls it.
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')
        
    try:
        # change_load() already does its own correct lookup by BUS NUMBER internally - calling it directly with the original bus_id 
        # (not a load-table row index) is both simpler and correct.
        grids[grid].change_load(bus_id, new_mw)
        log_event("digital_twin", grid, "LOAD_CHANGE", {"bus_id": bus_id, "new_mw": new_mw})
        
        return {'status': 'Command Received', 'action': f'Updated Facility {bus_id} to {new_mw}MW'}
    except Exception as e:
        # Pass the exact error string to the frontend
        raise HTTPException(status_code=400, detail=str(e))


class StressTestRequest(BaseModel):
    load_multiplier: float = 1.0     # 1.0 = 100% of nameplate load
    derate_multiplier: float = 1.0   # 1.0 = 100% of nominal line thermal capacity


@app.post('/stress_test/{grid}')
def apply_stress_test(grid: str, request: StressTestRequest):
    '''
    Sets the grid's load and line capacity to an absolute percentage of its ORIGINAL baseline - the endpoint behind the frontend's stress-test slider. 
    Unlike /change_load (single bus) or the startup-only /apply_scenario logic, this is idempotent: 
    calling it repeatedly with different values always means "X% of nameplate," never compounds.
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    if request.load_multiplier <= 0 or request.derate_multiplier <= 0:
        raise HTTPException(status_code=400, detail='Multipliers must be positive.')

    twin = grids[grid]
    twin.apply_stress_test(request.load_multiplier, request.derate_multiplier)
    log_event("digital_twin", grid, "STRESS_TEST_APPLIED", {
        "load_multiplier": request.load_multiplier,
        "derate_multiplier": request.derate_multiplier
    })

    if twin.simulation_status == "FAILED":
        raise HTTPException(status_code=422, detail="Grid collapsed (power flow did not converge) at this stress level.")

    return {
        "status": "Stress Test Applied",
        "load_multiplier": request.load_multiplier,
        "derate_multiplier": request.derate_multiplier,
        "max_line_loading_percent": round(float(twin.net.res_line.loading_percent.max()), 2)
    }


@app.post('/redispatch_gen/{bus_id}')
def redispatch_generator(bus_id: int, delta_mw: float, grid: str = '118'):
    '''
    Adjusts generator output at a specific bus by delta_mw (+/-). 
    This is the generator-side counterpart to /change_load - the other half of the actuation surface an approved REDISPATCH_GEN action commits through.
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    try:
        twin = grids[grid]
        matching_gens = twin.net.gen[twin.net.gen.bus == bus_id].index
        if matching_gens.empty:
            raise Exception(f"Bus {bus_id} has no generator to redispatch.")

        gen_idx = matching_gens[0]
        twin.net.gen.at[gen_idx, "p_mw"] += delta_mw

        pp.runpp(twin.net, solver='nr')
        summary = twin.get_current_state()
        twin.update_state(summary, "COMPLETED", f"Generator redispatched at Bus {bus_id} by {delta_mw} MW")
        log_event("digital_twin", grid, "GEN_REDISPATCH", {"bus_id": bus_id, "delta_mw": delta_mw})

        return {'status': 'Command Received', 'action': f'Redispatched Bus {bus_id} by {delta_mw}MW'}

    except pp.LoadflowNotConverged:
        raise HTTPException(status_code=400, detail="Redispatch caused a non-convergent power flow.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.websocket("/ws/telemetry/{grid}")
async def grid_telemetry(websocket: WebSocket, grid: str):
    # 1. Accept the incoming connection from the frontend
    await websocket.accept()
    
    # Verify grid exists
    if grid not in grids:
        await websocket.close(code=1008)
        return
        
    try:
        # 2. Enter the infinite telemetry loop
        while True:
            # 3. Grab the latest state dictionary from the unified dictionary
            current_state = grids[grid].get_current_state()
            
            # 4. Map the actual Bus IDs to their current loads
            net = grids[grid].net
            # Initialize all buses to 0.0 MW
            bus_loads = {str(idx): 0.0 for idx in net.bus.index}
            
            # Add the actual loads to their respective physical buses
            for _, row in net.load.iterrows():
                bus_id = str(int(row['bus']))
                if bus_id in bus_loads:
                    bus_loads[bus_id] += row['p_mw']
                    
            current_state['bus_loads'] = bus_loads

            # --- CALCULATE AND APPEND LINE METRICS ---
            line_metrics = {}
            if "res_line" in net and not net.res_line.empty:
                for line_idx in net.line.index:
                    try:
                        # Extract active (P) and reactive (Q) power
                        p = float(net.res_line.p_from_mw.at[line_idx])
                        q = float(net.res_line.q_from_mvar.at[line_idx])
                        
                        # Calculate apparent power (S) and Power Factor (PF)
                        s = math.sqrt(p**2 + q**2)
                        pf = abs(p) / s if s > 0 else 1.0
                        
                        # Extract loading and current
                        loading = float(net.res_line.loading_percent.at[line_idx])
                        current = float(net.res_line.i_from_ka.at[line_idx])
                        
                        line_metrics[str(line_idx)] = {
                            "loading_percent": loading if not pd.isna(loading) else 0.0,
                            "i_ka": current if not pd.isna(current) else 0.0,
                            "pf": pf
                        }
                    except Exception:
                        # Fallback for disconnected or non-converged lines
                        line_metrics[str(line_idx)] = {"loading_percent": 0.0, "i_ka": 0.0, "pf": 1.0}
                        
            current_state["line_metrics"] = line_metrics

            # --- CALCULATE AND APPEND BUS METRICS ---
            bus_metrics = {}
            if "res_bus" in net and not net.res_bus.empty:
                for bus_idx in net.bus.index:
                    try:
                        v_pu = float(net.res_bus.vm_pu.at[bus_idx])
                        v_ang = float(net.res_bus.va_degree.at[bus_idx])
                        
                        bus_metrics[str(bus_idx)] = {
                            "v_pu": v_pu if not pd.isna(v_pu) else 0.0,
                            "v_ang": v_ang if not pd.isna(v_ang) else 0.0
                        }
                    except Exception:
                        bus_metrics[str(bus_idx)] = {"v_pu": 0.0, "v_ang": 0.0}
                        
            current_state["bus_metrics"] = bus_metrics
            
            # 5. Push it through the socket as JSON
            await websocket.send_json(current_state)
            
            # 6. Rest for 1 second before sending the next frame
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"Client disconnected from IEEE {grid}: {e}")

@app.get("/asset_health/{grid}")
def get_asset_health(grid: str):
    '''
    Dedicated read endpoint for drid's assets testing harness: returns both the raw per-asset registry (dga_score, vibration_amp, tccs_delay_ms,
    logic_integrity, rul_days, fault_class for every transformer/generator/ circuit_breaker/relay) and the aggregated health rollup. 
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    twin = grids[grid]
    return {
        "asset_registry": twin.asset_registry,
        "health": get_health_metrics(twin.net, twin.asset_registry),
    }


class DegradeAssetRequest(BaseModel):
    asset_type: str        # "transformer" | "generator" | "circuit_breaker" | "relay"
    asset_id: int
    severity: float = 1.0


@app.post("/degrade_asset/{grid}")
def degrade_asset(grid: str, request: DegradeAssetRequest):
    '''
    Pushes ONE named asset toward failure - e.g. {"asset_type": "transformer", "asset_id": 0, "severity": 3.0} to drive a transformer toward HIGH_ENERGY_ARCING. 
    This is the endpoint behind reproducible, targeted test-scenario generation for Random Forest/LSTM models, as opposed to /tick_assets below which ages everything uniformly.
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    twin = grids[grid]
    try:
        twin.degrade_asset(request.asset_type, request.asset_id, request.severity)
        log_event("digital_twin", grid, "ASSET_DEGRADED", {
            "asset_type": request.asset_type, "asset_id": request.asset_id, "severity": request.severity
        })
        return {
            "status": "Command Received",
            "action": f"Degraded {request.asset_type} {request.asset_id} by {request.severity}x severity",
            "asset_registry": twin.asset_registry,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class TickAssetsRequest(BaseModel):
    severity: float = 1.0


@app.post("/tick_assets/{grid}")
def tick_assets(grid: str, payload: dict):
    if grid not in grids:
        return {"error": "Grid not found"}
        
    net = grids[grid].net
    registry = grids[grid].asset_registry
    severity = payload.get("severity", 1.0)

    # 1. Run the power flow physics engine first to get the REAL current stress levels
    try:
        import pandapower as pp
        pp.runpp(net, solver="nr")
    except pp.LoadflowNotConverged:
        pass # The grid is collapsing, handle as needed

    # 2. Extract load factors and age TRANSFORMERS
    for trafo_id in list(registry.get("transformers", {}).keys()):
        try:
            # loading_percent is calculated natively by pandapower
            loading = net.res_trafo.at[int(trafo_id), 'loading_percent']
            lf = loading / 100.0 if not pd.isna(loading) else 1.0
        except Exception:
            lf = 1.0
        simulate_transformer_aging(registry, int(trafo_id), severity, load_factor=lf)

    # 3. Extract load factors and age CIRCUIT BREAKERS (mapped to transmission lines)
    for cb_id in list(registry.get("circuit_breakers", {}).keys()):
        try:
            loading = net.res_line.at[int(cb_id), 'loading_percent']
            lf = loading / 100.0 if not pd.isna(loading) else 1.0
        except Exception:
            lf = 1.0
        simulate_breaker_degradation(registry, int(cb_id), friction_factor=severity, load_factor=lf)

    # 4. Extract load factors and age GENERATORS
    for gen_id in list(registry.get("generators", {}).keys()):
        try:
            # For generators, load factor is actual output / max rated capacity
            actual_mw = abs(net.res_gen.at[int(gen_id), 'p_mw'])
            max_mw = net.gen.at[int(gen_id), 'max_p_mw']
            
            if pd.isna(max_mw) or max_mw <= 0:
                lf = 1.0
            else:
                lf = actual_mw / max_mw
        except Exception:
            lf = 1.0
        simulate_generator_wear(registry, int(gen_id), wear_rate=severity, load_factor=lf)

    # 5. Extract load factors and age RELAYS (mapped to buses)
    for bus_id in list(registry.get("relays", {}).keys()):
        try:
            # Relays sit on buses; we estimate bus stress via voltage deviation
            # A 5% voltage drop (0.95 p.u.) creates a load factor of 1.05
            v_pu = net.res_bus.at[int(bus_id), 'vm_pu']
            if pd.isna(v_pu):
                lf = 1.0
            else:
                lf = 1.0 + abs(1.0 - v_pu)
        except Exception:
            lf = 1.0
        simulate_relay_degradation(registry, int(bus_id), noise_factor=severity, load_factor=lf)

    twin = grids[grid]
    registry = twin.asset_registry
    net = twin.net

    # 1. AUTO-TRIP GENERATORS (Mechanical/Thermal Failure)
    for gen_id, gen_data in registry.get("generators", {}).items():
        if (gen_data.get("Bearing_Amplitude_mm_s", 0) >= 11.0 or 
            gen_data.get("Temperature_C", 0) >= 110.0 or 
            gen_data.get("Bearing_Frequency_Hz", 50.0) >= 80.0): # New 80Hz limit
            
            if int(gen_id) in net.gen.index and net.gen.at[int(gen_id), 'in_service']:
                twin.trip_generator(int(gen_id), "CATASTROPHIC FAILURE")

    # 2. AUTO-TRIP TRANSFORMERS (Severe Arcing / Thermal Degradation)
    for trafo_id, trafo_data in registry.get("transformers", {}).items():
        # High Energy Discharge (C2H2 > 2.0) or Severe Thermal Fault (T3)
        if trafo_data.get("C2H2", 0) >= 2.0 or max(trafo_data.get("CH4", 0), trafo_data.get("C2H4", 0)) >= 2.0:
            if int(trafo_id) in net.trafo.index and net.trafo.at[int(trafo_id), 'in_service']:
                net.trafo.at[int(trafo_id), 'in_service'] = False # Disconnect transformer
                trafo_data["fault_class"] = "CATASTROPHIC FAILURE"
                trafo_data["rul_days"] = 0.0

    # 3. AUTO-TRIP RELAYS (Spurious Trip via Logic Failure)
    for relay_id, relay_data in registry.get("relays", {}).items():
        # If impedance collapses below 0.15, the relay maloperates and spuriously trips its connected lines
        if relay_data.get("Impedance_Z", 1.4) <= 0.15:
            bus_id = int(relay_id)
            connected_lines = net.line[(net.line.from_bus == bus_id) | (net.line.to_bus == bus_id)].index
            for line_id in connected_lines:
                net.line.at[line_id, 'in_service'] = False # Relay falsely opens the breakers
            relay_data["fault_class"] = "CATASTROPHIC MISOPERATION"
            relay_data["rul_days"] = 0.0

    return {"status": "success", "action": "Assets aged with dynamic load coupling"}


class WeatherEventRequest(BaseModel):
    event_type: str = "HEATWAVE"   # HEATWAVE | STORM | COLD_SNAP
    severity: float = 1.0


@app.post("/weather_event/{grid}")
def weather_event(grid: str, request: WeatherEventRequest):
    '''
    Applies a grid-wide weather stress scenario. This method already existed on TwinModel (apply_weather_event) but had no API route calling it 
    - it's a useful realistic combined stressor for exercising both the Digital Twin's electrical metrics and SURVEA's asset-health classifiers
    at once (HEATWAVE derates lines + ages transformers, STORM derates lines harder + wears breakers, COLD_SNAP spikes load).
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    twin = grids[grid]
    try:
        twin.apply_weather_event(request.event_type, request.severity)
        log_event("digital_twin", grid, "WEATHER_EVENT", {
            "event_type": request.event_type, "severity": request.severity
        })
        if twin.simulation_status == "FAILED":
            raise HTTPException(status_code=422, detail="Grid collapsed (power flow did not converge) under this weather event.")
        return {"status": "Command Received", "action": twin.current_scenario}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class TripGeneratorRequest(BaseModel):
    trip_type: str = "FORCED_OUTAGE"


@app.post("/trip_generator/{grid}/{gen_id}")
def trip_generator_endpoint(grid: str, gen_id: int, request: TripGeneratorRequest = TripGeneratorRequest()):
    '''
    Forces a generator out of service and stamps a run-to-failure label onto its asset_registry entry. 
    Like /weather_event, TwinModel.trip_generator already existed but had no route calling it.
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    twin = grids[grid]
    if gen_id not in twin.net.gen.index:
        raise HTTPException(status_code=404, detail=f"Generator {gen_id} not found.")

    twin.trip_generator(gen_id, request.trip_type)
    log_event("digital_twin", grid, "GEN_TRIPPED", {"gen_id": gen_id, "trip_type": request.trip_type})

    if twin.simulation_status == "FAILED":
        raise HTTPException(status_code=422, detail="Grid collapsed (power flow did not converge) after this generator trip.")

    return {"status": "Command Received", "action": f"Tripped generator {gen_id} ({request.trip_type})"}


@app.post("/trip_transformer/{grid}/{trafo_id}")
def trip_transformer_endpoint(grid: str, trafo_id: int, request: TripGeneratorRequest = TripGeneratorRequest()):
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    twin = grids[grid]
    if trafo_id not in twin.net.trafo.index:
        raise HTTPException(status_code=404, detail=f"Transformer {trafo_id} not found.")

    # Physically disconnect it
    twin.net.trafo.at[trafo_id, 'in_service'] = False
    
    # Stamp the registry
    if trafo_id in twin.asset_registry["transformers"]:
        twin.asset_registry["transformers"][trafo_id]["fault_class"] = request.trip_type
        twin.asset_registry["transformers"][trafo_id]["rul_days"] = 0.0

    log_event("digital_twin", grid, "TRAFO_TRIPPED", {"trafo_id": trafo_id, "trip_type": request.trip_type})
    return {"status": "Command Received", "action": f"Tripped transformer {trafo_id}"}

@app.get("/asset_detail/{grid}/{asset_type}/{asset_id}")
def get_asset_detail(grid: str, asset_type: str, asset_id: int):
    '''
    On-demand single-asset fetch for the frontend's Asset Inspector panel - lets a click on a generator/transformer node show its full feature record immediately, 
    without waiting for the next websocket telemetry tick or pulling the whole asset_registry.
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    key_map = {
        "transformer": "transformers", "transformers": "transformers",
        "generator": "generators", "generators": "generators",
        "circuit_breaker": "circuit_breakers", "circuit_breakers": "circuit_breakers", "breaker": "circuit_breakers",
        "relay": "relays", "relays": "relays",
    }
    registry_key = key_map.get(asset_type.lower())
    if registry_key is None:
        raise HTTPException(status_code=400, detail="asset_type must be transformer, generator, circuit_breaker, or relay.")

    registry = grids[grid].asset_registry[registry_key]
    if asset_id not in registry:
        raise HTTPException(status_code=404, detail=f"{asset_type} {asset_id} not found.")

    return {"asset_type": registry_key, "asset_id": asset_id, "detail": registry[asset_id]}


'''
Decorative-only substation equipment bays - so they're generated deterministically per bus rather than simulated/aged 
like the four monitored asset classes above. Purely for the single-line-diagram-style visual layer on the frontend.
'''
'''
Decorative-only substation equipment bays - now with state tracking!
'''
_EQUIPMENT_BY_NODE_TYPE = {
    "GENERATOR": ["Generator CT", "Generator PT", "Neutral Grounding Resistor", "Excitation Transformer", "Circuit Breaker", "Isolator", "Earth Switch"],
    "TRANSFORMER": ["Lightning Arrestor", "Wave Trap", "Circuit Breaker", "Isolator", "Earth Switch", "Current Transformer (CT)", "Potential Transformer (PT)"],
    "LOAD": ["Circuit Breaker", "Isolator", "Earth Switch", "Current Transformer (CT)", "Potential Transformer (PT)"],
    "JUNCTION": ["Circuit Breaker", "Isolator", "Earth Switch"],
}

# Global cache to remember the toggled state of equipment
equipment_state_cache = {}

@app.get("/substation_equipment/{grid}/{bus_id}")
def get_substation_equipment(grid: str, bus_id: int):
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')

    net = grids[grid].net
    if bus_id not in net.bus.index:
        raise HTTPException(status_code=404, detail=f"Bus {bus_id} not found.")

    generator_buses = set(net.gen['bus'].tolist())
    transformer_buses = set(net.trafo['hv_bus'].tolist()) | set(net.trafo['lv_bus'].tolist())
    bus_loads = net.load[net.load.bus == bus_id]
    has_load = not bus_loads.empty and bus_loads['p_mw'].sum() > 0

    if bus_id in generator_buses:
        node_type = "GENERATOR"
    elif bus_id in transformer_buses:
        node_type = "TRANSFORMER"
    elif has_load:
        node_type = "LOAD"
    else:
        node_type = "JUNCTION"

    rng = random.Random(bus_id) 
    candidates = _EQUIPMENT_BY_NODE_TYPE[node_type]
    equipment = []

    for name in candidates:
        # Create a unique key for this specific piece of equipment
        cache_key = f"{grid}_{bus_id}_{name}"
        
        if cache_key in equipment_state_cache:
            status = equipment_state_cache[cache_key]
        else:
            # Assign logical defaults for the first load
            if name == "Earth Switch":
                status = "OPEN"
            elif name in ["Circuit Breaker", "Isolator"]:
                status = "CLOSED"
            else:
                status = "IN SERVICE" if rng.random() > 0.05 else "MAINTENANCE FLAGGED"
            
            equipment_state_cache[cache_key] = status

        equipment.append({"name": name, "status": status})

    return {"bus_id": bus_id, "node_type": node_type, "equipment": equipment}

@app.post("/toggle_equipment/{grid}/{bus_id}/{equipment_name}")
def toggle_equipment(grid: str, bus_id: int, equipment_name: str):
    '''Toggles the state of a specific piece of bay equipment'''
    cache_key = f"{grid}_{bus_id}_{equipment_name}"
    current_state = equipment_state_cache.get(cache_key, "CLOSED")
    
    # Toggle logic
    if current_state == "CLOSED":
        new_state = "OPEN"
    elif current_state == "OPEN":
        new_state = "CLOSED"
    elif current_state == "IN SERVICE":
        new_state = "OUT OF SERVICE"
    else:
        new_state = "IN SERVICE"
        
    equipment_state_cache[cache_key] = new_state
    
    log_event("digital_twin", grid, "EQUIPMENT_TOGGLED", {
        "bus_id": bus_id, "equipment": equipment_name, "new_state": new_state
    })
    
    return {"status": "success", "new_state": new_state}


@app.get("/events/{grid}")
def read_event_timeline(grid: str, source: str = None, limit: int = 100):
    '''
    Reads back the shared event timeline (event_store.get_events) for one grid - physics-side (digital_twin) and AI-side (ai_agent) events together, newest first. 
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail='Grid not Found')
    return {"events": get_events(grid_id=grid, source=source, limit=limit)}

@app.post("/restore_line/{grid}/{line_id}")
def restore_line(grid: str, line_id: int):
    '''
    Kept for backward compatibility - delegates to the same close_breaker() path as /close_breaker below, 
    so both routes stay consistent (breaker_state/operation_count bookkeeping, event logging).
    '''

    if grid not in grids:
        raise HTTPException(status_code=404, detail="Grid not found")
        
    twin = grids[grid].net
    if line_id not in twin.line.index:
        raise HTTPException(status_code=404, detail="Line not found")
        
    # Reconnect the line
    try:
        twin.close_breaker(line_id)
        log_event("digital_twin", grid, "BREAKER_CLOSED", {"line_id": line_id})
    except pp.LoadflowNotConverged:
        raise HTTPException(status_code=422, detail="Grid did not converge after restoring this line.")

    return {"status": "restored", "line_id": line_id}


@app.post("/trip_breaker/{grid}/{line_id}")
def trip_breaker(grid: str, line_id: int):
    '''
    Explicit switchgear control: opens the breaker on this line. Same
    physics as /inject_fault, but named for what it actually represents --
    an operator opening a specific breaker, not an abstract "fault."
    Updates breaker_state/operation_count in the circuit_breakers asset
    registry, which /adjacent_breakers and SURVEA's live feed both read.
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail="Grid not found")

    twin = grids[grid]
    if line_id not in twin.net.line.index:
        raise HTTPException(status_code=404, detail="Line not found")

    twin.inject_line_fault(line_id)
    log_event("digital_twin", grid, "BREAKER_TRIPPED", {"line_id": line_id})
    return {"status": "tripped", "line_id": line_id}


@app.post("/close_breaker/{grid}/{line_id}")
def close_breaker(grid: str, line_id: int):
    '''
    Explicit switchgear control: closes the breaker on this line (restores the line to service). '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail="Grid not found")

    twin = grids[grid]
    if line_id not in twin.net.line.index:
        raise HTTPException(status_code=404, detail="Line not found")

    try:
        twin.close_breaker(line_id)
        log_event("digital_twin", grid, "BREAKER_CLOSED", {"line_id": line_id})
    except pp.LoadflowNotConverged:
        raise HTTPException(status_code=422, detail="Grid did not converge after closing this breaker.")

    return {"status": "closed", "line_id": line_id}


@app.get("/adjacent_breakers/{grid}/{bus_id}")
def adjacent_breakers(grid: str, bus_id: int):
    '''
    Every line/breaker directly connected to a bus, with each one's current breaker_state and fault_class 
    - what the frontend's Asset Inspector needs to show "breakers around this asset" and let an operator trip or
    close any of them without hunting for the right line on the graph.
    '''
    if grid not in grids:
        raise HTTPException(status_code=404, detail="Grid not Found")

    twin = grids[grid]
    if bus_id not in twin.net.bus.index:
        raise HTTPException(status_code=404, detail=f"Bus {bus_id} not found.")

    return {"bus_id": bus_id, "breakers": twin.get_adjacent_breakers(bus_id)}


# ==================================================
#              TESTING & EXECUTION
# ==================================================

if __name__ == '__main__':
    # Runs the server locally
    print('\nStarting FastAPI Server')
    uvicorn.run(app, host='127.0.0.1', port=8001)