"""
Shared data-access layer for every Streamlit page. Replaces the old
`get_live_data()` random.uniform() generators with real numbers from one of
two sources:

  1. LIVE MODE -- if the Digital Twin (the separate testing-environment repo)
     is reachable at DigitalTwinClient's base_url, pull its current
     simulated telemetry for the given asset and run it through the trained
     models.
  2. DEMO MODE -- if the twin isn't running, sample a real row from that
     asset's own historical CSV (not fabricated noise) and run THAT through
     the trained models instead. The frontend still always shows real,
     dataset-grounded numbers -- it just falls back to historical replay
     instead of a live simulation when nothing is running on port 8001.

Every Streamlit page imports from here; no page talks to the Digital Twin,
loads a model, or reads a CSV directly.

This module also owns three things that used to be missing entirely:
  - grid selection (IEEE 39-bus vs 118-bus), persisted in st.session_state
    so it carries across every page in the multipage app;
  - per-grid asset ID enumeration, so a page can list ALL generators/
    transformers/breakers/relays actually present on the selected grid
    instead of only ever showing a single hardcoded asset_id=0;
  - a fast, fleet-wide fault scan (using the twin's raw asset_registry
    fault_class fields directly, NOT the trained RF classifiers) cheap
    enough to run every autorefresh tick, which is what powers the
    cross-page "another asset is in fault" alert banner.
"""

import random

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

from src.config import ASSETS
from src.data.loaders import load_asset_raw
from src.inference.predictor import load_predictor
from src.advisory.brief_generator import build_brief
from src.live_feed.digital_twin_client import DigitalTwinClient

# Real, verified asset counts per grid (pandapower's IEEE test case
# definitions -- confirmed by direct inspection, not estimated) used ONLY
# as the demo-mode fallback when the live twin can't be reached to report
# its own registry's actual keys.
_DEMO_ASSET_COUNTS = {
    "39": {"generator": 9, "transformer": 11, "circuit_breaker": 35, "relay": 39},
    "118": {"generator": 53, "transformer": 13, "circuit_breaker": 173, "relay": 118},
}

_REGISTRY_KEY = {
    "transformer": "transformers", "generator": "generators",
    "circuit_breaker": "circuit_breakers", "relay": "relays",
}


def enable_autorefresh(interval_seconds: float = 3.0, key: str = "twin_autorefresh"):
    '''
    Reruns the page automatically every interval_seconds -- without this,
    Streamlit only recomputes get_prediction() on user interaction (a
    click, a widget change), so injecting a fault on the Digital Twin's own
    UI wouldn't show up here until the next click. Uses the small
    streamlit-autorefresh package (a single st_autorefresh() call, no other
    API surface) rather than a manual time.sleep()+st.rerun() loop, which
    blocks widget state handling and is a known anti-pattern in Streamlit.

    If streamlit-autorefresh isn't installed, this degrades to a no-op --
    the page still works correctly, it just requires a manual
    interaction/refresh to see live twin changes, same as before this was
    added.
    '''
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=int(interval_seconds * 1000), key=key)
    except ImportError:
        pass


def live_clock(height: int = 40):
    '''
    A genuinely ticking clock, updated once per second entirely in the
    browser via components.v1.html -- NOT dependent on enable_autorefresh's
    3-second full-page rerun. Streamlit has no first-party live-clock
    widget; a static datetime.now() string only ever updates when the
    whole page reruns, which is why the clock looked "static" before this.
    This renders as a small HTML/JS component instead, so the seconds
    genuinely advance between page reruns.
    '''
    components.html(
        """
        <div style="font-family: 'Segoe UI', sans-serif; font-size: 15px;
                    color: #38bdf8; text-align: right; padding-top: 4px;">
          <span id="live-clock-ist">--:--:--</span> IST
        </div>
        <script>
          function tick() {
            const now = new Date();
            // IST = UTC+5:30, computed client-side so this works regardless
            // of the viewer's own browser timezone.
            const utcMs = now.getTime() + (now.getTimezoneOffset() * 60000);
            const ist = new Date(utcMs + (5.5 * 60 * 60000));
            const hh = String(ist.getHours()).padStart(2, '0');
            const mm = String(ist.getMinutes()).padStart(2, '0');
            const ss = String(ist.getSeconds()).padStart(2, '0');
            const el = document.getElementById('live-clock-ist');
            if (el) el.textContent = hh + ':' + mm + ':' + ss;
          }
          tick();
          setInterval(tick, 1000);
        </script>
        """,
        height=height,
    )


# ------------------------------------------------------------
# GRID SELECTION -- persisted in session_state so it carries across every
# page in the multipage app without needing to be re-selected each time.
# ------------------------------------------------------------
def get_selected_grid() -> str:
    return st.session_state.get("selected_grid", "118")


def set_selected_grid(grid: str):
    st.session_state["selected_grid"] = grid


def grid_selector_widget(location=st):
    '''Renders the IEEE 39-bus / 118-bus picker. Meant to be called once,
    prominently, on the home page -- every other page just reads
    get_selected_grid() and shows the current choice, since re-picking a
    grid mid-session on a detail page would be an easy way to lose track of
    which network you're actually looking at.'''
    current = get_selected_grid()
    choice = location.radio(
        "Active Grid (Digital Twin)",
        options=["39", "118"],
        index=["39", "118"].index(current),
        format_func=lambda g: f"IEEE {g}-Bus System",
        horizontal=True,
        key="grid_selector_radio",
    )
    set_selected_grid(choice)
    return choice


@st.cache_resource
def get_predictor():
    return load_predictor()


@st.cache_resource(hash_funcs={str: lambda g: g})
def _twin_client_for(grid: str):
    return DigitalTwinClient(grid=grid)


def get_twin_client():
    return _twin_client_for(get_selected_grid())


@st.cache_data(ttl=30)
def _demo_row_pool(asset_type: str, n: int = 500):
    """Caches a small pool of real historical rows per asset so demo mode
    doesn't re-read a 68MB CSV on every Streamlit rerun."""
    schema = ASSETS[asset_type]
    df = load_asset_raw(asset_type).dropna(subset=schema["feature_columns"])
    return df.sample(n=min(n, len(df)), random_state=None).to_dict("records")


def is_twin_live() -> bool:
    return get_twin_client().is_reachable()


def get_fleet_asset_ids(asset_type: str) -> list:
    '''
    Every real asset_id of this type on the CURRENTLY SELECTED grid.
    Previously every page hardcoded asset_id=0, which meant a 118-bus grid
    with 53 real generators only ever showed the first one. Live mode asks
    the twin directly (so this is always exactly right, including after a
    topology change); demo mode falls back to the real, verified per-grid
    counts in _DEMO_ASSET_COUNTS above, since historical CSV replay has no
    concept of "this grid's" topology to query.
    '''
    grid = get_selected_grid()
    if is_twin_live():
        try:
            return get_twin_client().get_asset_ids(asset_type, grid=grid)
        except Exception:
            pass
    return list(range(_DEMO_ASSET_COUNTS[grid][asset_type]))


def get_current_reading(asset_type: str, asset_id: int = 0) -> tuple[dict, str]:
    """Returns (feature_dict, source_label) where source_label is
    'LIVE DIGITAL TWIN' or 'DEMO (historical replay)' -- the frontend should
    always show this so nobody mistakes a demo-mode replay for a live feed."""
    schema = ASSETS[asset_type]

    if is_twin_live():
        try:
            reading = get_twin_client().get_reading(asset_type, asset_id, grid=get_selected_grid())
            return reading, "LIVE DIGITAL TWIN"
        except Exception:
            pass  # fall through to demo mode below

    pool = _demo_row_pool(asset_type)
    row = random.choice(pool)
    reading = {col: row[col] for col in schema["feature_columns"]}
    return reading, "DEMO (historical replay)"


def get_prediction(asset_type: str, asset_id: int = 0) -> dict:
    """One call that a Streamlit page uses to get everything it needs:
    the raw reading, the RF classification, the source label, and (where
    supported) the LSTM's forecast built from a short repeated-reading
    window as a stand-in for a real rolling buffer -- see the module
    docstring in predictor.py for what forecast() expects."""
    from src.config import SEQUENCE_LENGTH

    predictor = get_predictor()
    reading, source = get_current_reading(asset_type, asset_id)
    classification = predictor.classify(asset_type, reading)

    forecast = None
    if ASSETS[asset_type]["supports_lstm"]:
        # A real deployment would buffer SEQUENCE_LENGTH consecutive live
        # ticks; repeating the current snapshot is a reasonable stand-in
        # for a page that re-samples independently on every Streamlit rerun.
        forecast = predictor.forecast(asset_type, [reading] * SEQUENCE_LENGTH)

    brief = build_brief(asset_type, classification, forecast)

    return {
        "reading": reading,
        "classification": classification,
        "forecast": forecast,
        "source": source,
        "brief": brief,
    }


def scan_fleet_alerts(exclude_asset_type: str = None):
    '''
     Scans all asset registries across the grid and returns a list of non-normal assets.
    '''
    grid_id = get_selected_grid()
    try:
        import requests
        res = requests.get(f"http://127.0.0.1:8001/asset_health/{grid_id}")
        if res.status_code != 200:
            return []
        data = res.json().get("asset_registry", {})
    except Exception:
        return []

    alerts = []
    # Map registry keys to clean type names
    type_mapping = {
        "generators": "generator",
        "transformers": "transformer",
        "circuit_breakers": "circuit_breaker",
        "relays": "relay"
    }

    for reg_key, asset_type in type_mapping.items():
        if asset_type == exclude_asset_type:
            continue
        assets_dict = data.get(reg_key, {})
        for aid, asset_data in assets_dict.items():
            fc = asset_data.get("fault_class", "Normal")
            if fc != "Normal":
                alerts.append({
                    "asset_type": asset_type,
                    "asset_id": int(aid),
                    "fault_class": fc
                })
    return alerts


def render_fleet_alert_banner(current_asset_type: str = None):
    '''
    Renders a flashing red banner if ANY asset on the currently
    selected grid is in a non-Normal state. 
    '''
    alerts = scan_fleet_alerts(exclude_asset_type=current_asset_type)
    
    if not alerts:
        return

    display_names = {
        "transformer": "Transformer", "generator": "Generator",
        "circuit_breaker": "Circuit Breaker", "relay": "Relay",
    }
    
    # Build distinct stacked blocks for each alert
    html_blocks = ""
    for a in alerts:
        name = display_names.get(a['asset_type'], a['asset_type'].capitalize())
        # Using 1-based indexing (+1) for display purposes
        html_blocks += f"<div class='fleet-alert-item'><strong>{name} {a['asset_id'] + 1:02d}</strong> — {a['fault_class']}</div>"

    asset_word = "asset" if len(alerts) == 1 else "assets"
    verb_word = "requires" if len(alerts) == 1 else "require"
    location_text = "elsewhere on this grid" if current_asset_type else "on this grid"

    st.markdown(
        f"""
        <div class="fleet-alert-banner">
          <div style="margin-bottom: 12px; font-size: 15px;">🔴 <strong>FLEET ALERT — {len(alerts)} {asset_word} {location_text} {verb_word} attention:</strong></div>
          {html_blocks}
        </div>
        <style>
        .fleet-alert-banner {{
            background: rgba(231, 76, 60, 0.15);
            border: 2px solid #e74c3c;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
            color: #ffffff;
            animation: fleetAlertPulse 1.4s ease-in-out infinite;
        }}
        .fleet-alert-item {{
            background: rgba(0, 0, 0, 0.3);
            padding: 8px 12px;
            margin-bottom: 8px;
            border-left: 4px solid #ff6b5b;
            border-radius: 4px;
            font-size: 14px;
        }}
        @keyframes fleetAlertPulse {{
            0%, 100% {{ box-shadow: 0 0 6px 0 rgba(231, 76, 60, 0.4); border-color: #e74c3c; }}
            50%      {{ box-shadow: 0 0 18px 6px rgba(231, 76, 60, 0.75); border-color: #ff6b5b; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


if st.sidebar.button("🔄 Reset Entire Fleet & Grid"):
    import requests
    grid_id = get_selected_grid()
    try:
        requests.post(f"http://127.0.0.1:8001/reset_fleet/{grid_id}")
        st.success("Fleet reset successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to reset fleet: {e}")

def render_page_header(title: str, asset_type_for_alerts: str = None):
    '''Common header block every page calls: live clock + grid indicator +
    fleet alert banner, in one place so the 4 asset pages and home.py don't
    each reimplement this differently.'''
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"Active Grid: IEEE {get_selected_grid()}-Bus System")
    with col2:
        live_clock()

    render_fleet_alert_banner(current_asset_type=asset_type_for_alerts)


def get_fleet_overview(asset_type: str) -> list:
    '''
    A fast, fleet-wide "quick glance" list for the overview table at the
    top of each asset page: every asset_id of this type on the current
    grid, with the twin's own raw fault_class (NOT the trained RF
    classifier's verdict). Deliberately cheap for the same reason
    scan_fleet_alerts() is cheap -- one HTTP call regardless of fleet size,
    versus running full RF+LSTM inference on up to 173 breakers every
    autorefresh tick. Selecting one specific asset from this table is what
    triggers the real get_prediction() call for that asset only.

    Returns [] in demo mode: historical CSV replay has no per-grid fleet to
    enumerate, only a pool of independent historical rows, so a fleet table
    would have nothing genuine to show. Pages should treat an empty list as
    "fleet overview unavailable in demo mode," not as "fleet is empty."
    '''
    if not is_twin_live():
        return []
    try:
        registry = get_twin_client().get_raw_registry(grid=get_selected_grid())
    except Exception:
        return []

    key = _REGISTRY_KEY[asset_type]
    return [
        {"asset_id": int(asset_id), "fault_class": record.get("fault_class", "Normal")}
        for asset_id, record in sorted(registry.get(key, {}).items(), key=lambda kv: int(kv[0]))
    ]


def risk_badge(fault_label: str) -> str:
    """Maps a predicted fault label to the same 🔴/🟡/🟢 convention already
    used across the pages, generically (no per-asset hardcoding needed)."""
    normalized = fault_label.strip().lower()
    if normalized == "normal":
        return "🟢 NORMAL"
    if normalized == "undetermined":
        return "🟡 UNDETERMINED"
    if "critical" in normalized or "severe" in normalized or "high energy" in normalized             or "runaway" in normalized or "jamming" in normalized:
        return "🔴 CRITICAL"
    return "🟡 WARNING"

def render_industrial_gauge(value: float, title: str, min_val: float, max_val: float, unit: str = "", steps: list = None):
    """
    Renders an industrial SCADA-style semi-circular gauge with customizable regulatory zones.
    """
    if steps is None:
        steps = [
            {'range': [min_val, min_val + (max_val - min_val) * 0.6], 'color': 'rgba(34, 197, 94, 0.15)'},
            {'range': [min_val + (max_val - min_val) * 0.6, min_val + (max_val - min_val) * 0.85], 'color': 'rgba(234, 179, 8, 0.15)'},
            {'range': [min_val + (max_val - min_val) * 0.85, max_val], 'color': 'rgba(239, 68, 68, 0.15)'}
        ]

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        number = {'suffix': f" {unit}", 'font': {'color': '#ffffff', 'size': 22}},
        title = {'text': title, 'font': {'size': 14, 'color': '#94a3b8'}},
        gauge = {
            'axis': {'range': [min_val, max_val], 'tickcolor': "#94a3b8", 'tickfont': {'color': '#94a3b8'}},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "#1e293b",
            'borderwidth': 1,
            'bordercolor': "#334155",
            'steps': steps,
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=210,
        margin=dict(t=55, b=10, l=25, r=25)
    )
    st.plotly_chart(fig, use_container_width=True)