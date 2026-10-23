import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from frontend.shared import (
    get_prediction, risk_badge, is_twin_live, enable_autorefresh, live_clock,
    grid_selector_widget, get_selected_grid, render_fleet_alert_banner, get_fleet_asset_ids,
)

st.set_page_config(
    page_title="Asset Health Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

enable_autorefresh(interval_seconds=3)

col1, col2 = st.columns([3, 1])
with col1:
    st.caption("⚡ AI-DRIVEN INTEGRATED FRAMEWORK")
    st.title("Critical Assets Health Monitoring & Prognostics")
with col2:
    st.info("🟢 LIVE DIGITAL TWIN" if is_twin_live() else "🟡 DEMO MODE (historical replay)")
    live_clock()

st.divider()

# GRID SELECTION -- this is the entry point for choosing which network
# (IEEE 39-bus or 118-bus) every other page will operate against. Previously
# there was no way to switch grids at all; the frontend silently always
# targeted the 118-bus network regardless of what the Digital Twin operator
# was actually testing against.
st.subheader("🔌 Select Active Grid")
st.caption("This choice persists across every page -- switch here to test against a different network.")
selected_grid = grid_selector_widget()

col1, col2, col3 = st.columns([1, 1, 1])

with col2:

    btn_left, btn_center, btn_right = st.columns([1, 1, 1])

    with btn_center:
        if st.button("🔄 Refresh Grid State", width = 'content'):
            st.rerun()


if is_twin_live():
    st.caption(f"Connected to live Digital Twin -- grid IEEE {selected_grid}-Bus "
               f"({len(get_fleet_asset_ids('generator'))} generators, "
               f"{len(get_fleet_asset_ids('transformer'))} transformers, "
               f"{len(get_fleet_asset_ids('circuit_breaker'))} breakers, "
               f"{len(get_fleet_asset_ids('relay'))} relays).")
else:
    st.caption("Digital Twin not reachable -- asset counts below are the known IEEE reference "
               "topology sizes for this grid, used only to size the demo-mode fleet lists.")

st.divider()

# FLEET-WIDE ALERT -- shows regardless of which asset type is selected below,
# so a transformer fault is visible here even before drilling into that page.
render_fleet_alert_banner()

# One real prediction per asset TYPE (asset_id=0, or the first real ID on
# this grid) for the overview cards -- the full per-asset fleet table lives
# on each asset's own page.
def _first_id(asset_type):
    ids = get_fleet_asset_ids(asset_type)
    return ids[0] if ids else 0

gen = get_prediction("generator", asset_id=_first_id("generator"))
trf = get_prediction("transformer", asset_id=_first_id("transformer"))
rly = get_prediction("relay", asset_id=_first_id("relay"))
cb = get_prediction("circuit_breaker", asset_id=_first_id("circuit_breaker"))

st.subheader("🔧 Equipment Overview")
st.caption(f"Data source: {gen['source']}  |  Click 'Open Details' for the full fleet view and prognostics.")

c1, c2, c3, c4 = st.columns(4)

for col, name, asset_key, result, page, icon in [
    (c1, "Generator", "generator", gen, "pages/1_Generator.py", "⚙️"),
    (c2, "Transformer", "transformer", trf, "pages/2_Transformer.py", "🔌"),
    (c3, "Relay", "relay", rly, "pages/3_Relay.py", "🛡️"),
    (c4, "Circuit Breaker", "circuit_breaker", cb, "pages/4_Circuit_Breaker.py", "🎚️"),
]:
    with col:
        st.markdown(f"#### {icon} {name}")
        st.caption(f"{len(get_fleet_asset_ids(asset_key))} unit(s) on this grid")
        label = result["classification"]["fault_label"]
        confidence = result["classification"]["confidence"]

        # If the Twin registry says Normal but the RF returned Undetermined,
        # trust the physics engine -- same override as the Transformer detail page.
        from frontend.shared import get_fleet_overview
        overview = get_fleet_overview(asset_key)
        first_id = _first_id(asset_key)
        registry_status = next((a["fault_class"] for a in overview if a["asset_id"] == first_id), "Unknown")
        if label == "Undetermined" and registry_status == "Normal":
            label = "Normal"

        badge = risk_badge(label)

        if label == "Normal":
            st.success(badge)
        elif "🔴" in badge:
            st.error(badge)
        else:
            st.warning(badge)

        st.metric(f"Unit #{_first_id(asset_key)} State", label, f"{confidence:.0%} confidence", delta_color="off")

        forecast = result["forecast"]
        if forecast is not None:
            st.caption(f"Forecast {forecast['target_name']}: {forecast['value']:.2f}")
        else:
            st.caption("No RUL/trend forecast for this asset's dataset")

        if st.button("Open Details →", key=f"{asset_key}_btn"):
            st.switch_page(page)
        if st.button("ℹ️", key=f"{asset_key}_info", help=f"View XAI explanation for {name} parameters"):
            st.switch_page("pages/5_XAI.py")

st.divider()
fc1, fc2 = st.columns([3, 1])
with fc1:
    st.caption("Model-driven live feed (Random Forest + LSTM, real datasets)")
with fc2:
    if st.button("ℹ️  About XAI & Parameters", key="home_xai"):
        st.switch_page("pages/5_XAI.py")

# --- ACADEMIC DISCLAIMER ---
st.markdown(
    """
    <div style='text-align: center; color: #64748b; font-size: 12px; margin-top: 20px;'>
        <strong>⚠️ Academic Disclaimer:</strong> This dashboard and its integrated AI framework are developed as part of a 
        university research project for educational and proof-of-concept purposes. It is not intended for active deployment 
        in live, physical power system environments without comprehensive safety validation and regulatory certification.
    </div>
    """, 
    unsafe_allow_html=True
)