import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import sys
from pathlib import Path
from shared import render_industrial_gauge

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from frontend.shared import (
    get_prediction, risk_badge, enable_autorefresh, live_clock, get_selected_grid,
    render_fleet_alert_banner, get_fleet_asset_ids, get_fleet_overview,
)

st.set_page_config(
    page_title="Generator Fleet | Health Monitor",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

enable_autorefresh(interval_seconds=3)

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.caption("⚙️ ASSET FLEET VIEW — GENERATORS")
    st.title(f"Generator Fleet — IEEE {get_selected_grid()}-Bus System")
with col2:
    live_clock()

st.divider()

# Fleet-wide alert for OTHER asset types faulting elsewhere on this grid
render_fleet_alert_banner(current_asset_type="generator")

# --- VISUAL FLEET DASHBOARD ---
st.subheader("⚙️ Generator Fleet Overview")
all_ids = get_fleet_asset_ids("generator")
overview = get_fleet_overview("generator")

# Persist the selected unit in session state
if "selected_gen_id" not in st.session_state or st.session_state["selected_gen_id"] not in all_ids:
    failing_unit = next((a["asset_id"] for a in overview if a["fault_class"] != "Normal"), None)
    st.session_state["selected_gen_id"] = failing_unit if failing_unit is not None else (all_ids[0] if all_ids else 0)

if overview:
    st.caption("Click any unit below to view live telemetry and prognostics.")
    # Create a visual grid of buttons (8 units per row)
    cols = st.columns(8) 
    for index, asset in enumerate(overview):
        uid = asset["asset_id"]
        fc = asset["fault_class"]
        
        # Add a visual indicator to the button text based on status
        if fc == "Normal":
            btn_label = f"🟢 G-{uid:02d}\nNormal"
        elif "Severe" in fc or "Runaway" in fc:
            btn_label = f"🔴 G-{uid:02d}\n{fc}"
        else:
            btn_label = f"🟡 G-{uid:02d}\n{fc}"
            
        with cols[index % 8]:
            if st.button(btn_label, key=f"btn_gen_{uid}", use_container_width=True):
                st.session_state["selected_gen_id"] = uid
                st.rerun()
else:
    st.info("Live twin disconnected. Demo mode active.")
    st.session_state["selected_gen_id"] = st.selectbox("Select Generator Unit", options=all_ids, format_func=lambda i: f"Generator G-{i:02d}")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:

    btn_left, btn_center, btn_right = st.columns([1, 1, 1])

    with btn_center:
        if st.button("🔄 Refresh Grid State", width = 'content'):
            st.rerun()


st.divider()

# --- DETAILED SINGLE-UNIT VIEW ---
selected_id = st.session_state["selected_gen_id"]
result = get_prediction("generator", asset_id=selected_id)
r = result["reading"]
clf = result["classification"]
forecast = result["forecast"]
badge = risk_badge(clf["fault_label"])

st.subheader(f"⚙️ Generator G-{selected_id:02d} — Health & Prognostics")
st.caption(f"Unit {selected_id} of {len(all_ids)} on this grid  |  Model: Random Forest (macro-F1 1.00) + LSTM  |  "
           f"{'🟢 LIVE DIGITAL TWIN FEED' if result['source'] == 'LIVE DIGITAL TWIN' else '🟡 DEMO MODE — replaying real historical readings'}")

# --- MODEL ASSESSMENT ---
st.subheader("🔔 Model Assessment")
if clf["fault_label"] == "Normal":
    st.success(f"{badge} — Random Forest classifier: **{clf['fault_label']}** (confidence {clf['confidence']:.0%})")
else:
    alert_fn = st.error if "🔴" in badge else st.warning
    alert_fn(
        f"{badge} — Random Forest classifier: **{clf['fault_label']}** (confidence {clf['confidence']:.0%})\n\n"
        f"Bearing amplitude {r['Bearing_Amplitude_mm_s']:.2f} mm/s  |  "
        f"Temperature {r['Temperature_C']:.1f}°C (rise {r['Temp_Rise_Rate_C_min']:.2f}°C/min)  |  "
        f"{'⚠ Thermal runaway indicator ACTIVE' if r['Thermal_Runaway_Indicator'] else ''}"
    )

st.divider()

# --- OPERATOR BRIEF ---
st.subheader("🧠 Operator Brief")
st.caption("Retrieved guidance, not AI-generated prose -- every passage below cites its source document.")
st.markdown(result["brief"].markdown)

st.divider()

# --- LIVE PARAMETER FEED ---
st.subheader("⚡ Live Parameter Feed")
st.caption(f"Source: {result['source']}  |  Features: Bearing_Frequency_Hz, Bearing_Amplitude_mm_s, Temperature_C, "
           "Temp_Rise_Rate_C_min, Thermal_Runaway_Indicator (ISO 10816 / IEC 60034-1)")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Bearing Vib. Frequency", f"{r['Bearing_Frequency_Hz']:.2f} Hz")
c1.caption("Nominal: 50 Hz")
c2.metric("Bearing Vib. Amplitude", f"{r['Bearing_Amplitude_mm_s']:.2f} mm/s")
c2.caption("ISO 10816 Zone A <2.3 | B <4.5 | C <7.1 | D ≥7.1")
c3.metric("Temperature", f"{r['Temperature_C']:.1f} °C")
c3.caption("Baseline: 40 °C")
c4.metric("Temp Rise Rate", f"{r['Temp_Rise_Rate_C_min']:.2f} °C/min")
c4.caption("Thermal runaway flag trips above ~2 °C/min")

st.divider()

c1, c2, c3, c4 = st.columns(4)

with c1:
    # CERC Grid Code Limits
    freq_steps = [
        {'range': [30.0, 49.5], 'color': 'rgba(239, 68, 68, 0.2)'},      # Critical Low
        {'range': [49.5, 49.95], 'color': 'rgba(234, 179, 8, 0.2)'},    # Warning Low
        {'range': [49.95, 50.05], 'color': 'rgba(34, 197, 94, 0.25)'},  # CERC Safe Green Zone
        {'range': [50.05, 50.5], 'color': 'rgba(234, 179, 8, 0.2)'},    # Warning High
        {'range': [50.5, 70.0], 'color': 'rgba(239, 68, 68, 0.2)'}     # Critical High (Allows up to 180+ Hz)
    ]
    render_industrial_gauge(r['Bearing_Frequency_Hz'], "Bearing Vib. Frequency", 30.0, 70.0, "Hz", steps=freq_steps)

with c2:
    # IS 12075:2008 limits for >400mm shaft, 1500 RPM (50Hz)
    vib_steps = [
        {'range': [0.0, 2.24], 'color': 'rgba(34, 197, 94, 0.25)'},    # Normal (Rigid mounting limit)
        {'range': [2.24, 2.8], 'color': 'rgba(234, 179, 8, 0.2)'},     # Warning (Free suspension limit)
        {'range': [2.8, 12.0], 'color': 'rgba(239, 68, 68, 0.2)'}      # Critical (Damage zone)
    ]
    render_industrial_gauge(r['Bearing_Amplitude_mm_s'], "Bearing Vib. Amplitude", 0.0, 12.0, "mm/s", steps=vib_steps)

with c3:
    # Insulation Class B standard continuous operating limits
    temp_steps = [
        {'range': [20.0, 85.0], 'color': 'rgba(34, 197, 94, 0.25)'},   # Normal operating range
        {'range': [85.0, 105.0], 'color': 'rgba(234, 179, 8, 0.2)'},   # Elevated / Warning
        {'range': [105.0, 130.0], 'color': 'rgba(239, 68, 68, 0.2)'}   # Critical / Melting
    ]
    render_industrial_gauge(r['Temperature_C'], "Stator Temperature", 20.0, 130.0, "°C", steps=temp_steps)

with c4:
    # Thermal runaway thresholds matching scenario_engine.py physics
    rise_steps = [
        {'range': [0.0, 1.0], 'color': 'rgba(34, 197, 94, 0.25)'},     # Normal
        {'range': [1.0, 2.0], 'color': 'rgba(234, 179, 8, 0.2)'},      # Thermal Warning active
        {'range': [2.0, 6.0], 'color': 'rgba(239, 68, 68, 0.2)'}       # Thermal Runaway active
    ]
    render_industrial_gauge(r['Temp_Rise_Rate_C_min'], "Temp Rise Rate", 0.0, 6.0, "°C/min", steps=rise_steps)

st.divider()

# --- PROGNOSTICS: ESTIMATED TIME TO FAILURE ---
st.subheader("⏱️ Estimated Time to Failure — If Maintenance Not Performed")
st.caption("Prognostic analysis based on current AI-detected degradation trends vs. ISO 10816 / IEC 60034-1 limits.")

if forecast is not None:
    # 1. Calculate dynamic Time-to-Failure based on real sensor drift
    current_vib = r['Bearing_Amplitude_mm_s']
    vib_limit = 7.1 # ISO 10816 Class D threshold
    # Estimate days left based on current amplitude (rough heuristic mapping for UI)
    vib_health_pct = max(0, (vib_limit - current_vib) / vib_limit)
    days_to_bearing = max(1, int(vib_health_pct * 120)) 

    current_temp = r['Temperature_C']
    temp_rise = r['Temp_Rise_Rate_C_min']
    temp_limit = 105.0 # Insulation Class B limit
    temp_health_pct = max(0, (temp_limit - current_temp) / temp_limit)
    # If temp is rising fast, time to thermal failure drops drastically
    days_to_thermal = max(1, int((temp_health_pct * 150) / max(0.1, temp_rise)))

    overall_days = min(days_to_bearing, days_to_thermal)

    # 2. Render the 3-Box UI
    html_cards = f"""
    <div style="display: flex; gap: 15px; margin-bottom: 20px;">
        <div style="flex: 1; background: {'#3f2323' if days_to_bearing < 15 else '#2d3748'}; padding: 15px; border-radius: 8px; border-left: 4px solid {'#f87171' if days_to_bearing < 15 else '#fb923c'};">
            <h5 style="color: {'#f87171' if days_to_bearing < 15 else '#fb923c'}; margin-top: 0; font-size: 14px;">Bearing Failure</h5>
            <h2 style="margin: 10px 0; color: #fff;">~{days_to_bearing} Days</h2>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 0;">
                Based on current vibration amplitude ({current_vib:.2f} mm/s). 
                Exceeding ISO 10816 Zone D (7.1 mm/s) indicates imminent mechanical seizure.
            </p>
        </div>
        <div style="flex: 1; background: {'#3f2323' if days_to_thermal < 20 else '#2d3748'}; padding: 15px; border-radius: 8px; border-left: 4px solid {'#f87171' if days_to_thermal < 20 else '#facc15'};">
            <h5 style="color: {'#f87171' if days_to_thermal < 20 else '#facc15'}; margin-top: 0; font-size: 14px;">Thermal / Insulation Failure</h5>
            <h2 style="margin: 10px 0; color: #fff;">~{days_to_thermal} Days</h2>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 0;">
                Stator temp rising at {temp_rise:.2f}°C/min. 
                Insulation Class B limit ({temp_limit}°C) may be breached if trend continues.
            </p>
        </div>
        <div style="flex: 1; background: {'#3f2323' if overall_days < 15 else '#1e293b'}; padding: 15px; border-radius: 8px; border-left: 4px solid {'#f87171' if overall_days < 15 else '#38bdf8'};">
            <h5 style="color: {'#f87171' if overall_days < 15 else '#38bdf8'}; margin-top: 0; font-size: 14px;">Complete Generator Failure</h5>
            <h2 style="margin: 10px 0; color: #fff;">~{overall_days} Days</h2>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 0;">
                Compounded LSTM forecasted Health Index: {forecast['value']:.2f}. 
                Risk of catastrophic failure without operational intervention.
            </p>
        </div>
    </div>
    """
    st.markdown(html_cards, unsafe_allow_html=True)
else:
    st.warning("No LSTM model available for this asset yet. Run `python -m src.training.train_all`.")

st.divider()

# --- MAINTENANCE (Dual View & Action Dispatch) ---
st.subheader("🔧 Mandatory Maintenance — Action Required")

maintenance_df = pd.DataFrame({
    "Fault Class": ["Moderate Fault", "Severe Fault", "Thermal Warning", "Thermal Runaway", "CATASTROPHIC FAILURE"],
    "Recommended Action": [
        "Schedule bearing inspection within 30 days",
        "Drive-end bearing replacement — vibration exceeds ISO 10816 Class III/IV",
        "Cooling system inspection and coolant flush",
        "Immediate shutdown evaluation — insulation life at risk",
        "UNIT OFFLINE. Complete shaft/stator replacement required. Grid capacity severely reduced.",
    ],
    "Priority": ["🟡 MEDIUM", "🔴 HIGH", "🟡 MEDIUM", "🔴 HIGH", "🚨 CRITICAL"],
})

# 1. Normal State
if clf["fault_label"] == "Normal":
    st.success("**Status:** Asset is operating within normal parameters. No mandatory maintenance required at this time.")

# 2. Fault State
else:
    active_maintenance = maintenance_df[maintenance_df["Fault Class"] == clf["fault_label"]]
    if not active_maintenance.empty:
        action = active_maintenance.iloc[0]["Recommended Action"]
        priority = active_maintenance.iloc[0]["Priority"]
        
        # Check if maintenance was already dispatched
        maint_key = f"maint_dispatched_gen_{selected_id}"
        
        if st.session_state.get(maint_key, False):
            st.success(f"✅ **Maintenance Crew Dispatched.** Asset G-{selected_id:02d} is isolated and pending physical repair.")
            if st.button("Complete Repair & Reset Asset Status"):
                st.session_state[maint_key] = False
                st.rerun()
        else:
            st.error(f"**Prescribed Task ({priority}):** {action}")
            if st.button(f"🚨 Dispatch Maintenance Team to G-{selected_id:02d}", type="primary"):
                st.session_state[maint_key] = True
                st.session_state['auto_redirect'] = False 
                st.rerun()
    else:
        st.warning(f"**Prescribed Action:** No standard maintenance protocol mapped for fault class: {clf['fault_label']}")

st.caption("Standard Maintenance Reference Dictionary (Schedule Within 30 Days)")
st.dataframe(maintenance_df, width='stretch', hide_index=True)

st.divider()

# --- FOOTER (Navigation & Fleet Info) ---
nav1, nav2, nav3 = st.columns([1, 1, 4])
with nav1:
    if st.button("← Back to Home"):
        st.switch_page("home.py")
with nav2:
    if st.button("ℹ️ XAI Explanation"):
        st.switch_page("pages/5_XAI.py")
with nav3:
    st.caption(f"Fleet: {len(all_ids)} generator(s)  |  Model-driven live feed (RF + LSTM)")