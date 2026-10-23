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

st.set_page_config(page_title="Circuit Breaker Fleet | Health Monitor", page_icon="🎚️", layout="wide", initial_sidebar_state="collapsed")
enable_autorefresh(interval_seconds=3)

ist = pytz.timezone("Asia/Kolkata")
now_str = datetime.now(ist).strftime("%d %b %Y  %H:%M:%S IST")

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.caption("🎚️ ASSET FLEET VIEW — CIRCUIT BREAKERS")
    st.title(f"Circuit Breaker Fleet — IEEE {get_selected_grid()}-Bus System")
with col2:
    live_clock()

st.divider()
render_fleet_alert_banner(current_asset_type="circuit_breaker")

# --- VISUAL FLEET DASHBOARD ---
st.subheader("🎚️ Circuit Breaker Fleet Overview")
st.caption("One breaker is modelled per transmission line on this grid.")
all_ids = get_fleet_asset_ids("circuit_breaker")
overview = get_fleet_overview("circuit_breaker")

if "selected_cb_id" not in st.session_state or st.session_state["selected_cb_id"] not in all_ids:
    failing_unit = next((a["asset_id"] for a in overview if a["fault_class"] != "Normal"), None)
    st.session_state["selected_cb_id"] = failing_unit if failing_unit is not None else (all_ids[0] if all_ids else 0)

if overview:
    st.caption("Click any unit below to view live telemetry and prognostics.")
    cols = st.columns(8) 
    for index, asset in enumerate(overview):
        uid = asset["asset_id"]
        fc = asset["fault_class"]
        
        if fc == "Normal":
            btn_label = f"🟢 G-{uid:02d}\nNormal"
        elif "Severe" in fc or "Jamming" in fc:
            btn_label = f"🔴 CB-{uid:02d}\n{fc}"
        else:
            btn_label = f"🟡 CB-{uid:02d}\n{fc}"
            
        with cols[index % 8]:
            if st.button(btn_label, key=f"btn_cb_{uid}", use_container_width=True):
                st.session_state["selected_cb_id"] = uid
                st.rerun()
else:
    st.info("Live twin disconnected. Demo mode active.")
    st.session_state["selected_cb_id"] = st.selectbox("Select Circuit Breaker", options=all_ids, format_func=lambda i: f"Circuit Breaker CB-{i:02d}")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:

    btn_left, btn_center, btn_right = st.columns([1, 1, 1])

    with btn_center:
        if st.button("🔄 Refresh Grid State", width = 'content'):
            st.rerun()


st.divider()

# --- DETAILED SINGLE-UNIT VIEW ---
selected_id = st.session_state["selected_cb_id"]
result = get_prediction("circuit_breaker", asset_id=selected_id)
r = result["reading"]
clf = result["classification"]
forecast = result["forecast"]
badge = risk_badge(clf["fault_label"])

st.subheader(f"⚡ Circuit Breaker CB-{selected_id:02d} (Line {selected_id}) — Health & Prognostics")
st.caption(f"Unit {selected_id} of {len(all_ids)} on this grid  |  Model: Random Forest (6-class) + LSTM  |  "
           f"{'🟢 LIVE DIGITAL TWIN FEED' if result['source'] == 'LIVE DIGITAL TWIN' else '🟡 DEMO MODE — replaying real historical readings'}")

# --- MODEL ASSESSMENT ---
st.subheader("🔔 Model Assessment")
if clf["fault_label"] == "Normal":
    st.success(f"{badge} — Random Forest classifier: **{clf['fault_label']}** (confidence {clf['confidence']:.0%})")
else:
    alert_fn = st.error if "🔴" in badge else st.warning
    alert_fn(
        f"{badge} — Random Forest classifier: **{clf['fault_label']}** (confidence {clf['confidence']:.0%})\n\n"
        f"Contact travel {r['Contact_Travel_Time_ms']:.1f} ms  |  TCCS duration {r['TCCS_Duration_ms']:.1f} ms  |  "
        f"SF6 pressure {r['Gas_Pressure_bar']:.2f} bar"
    )

st.divider()

# --- OPERATOR BRIEF ---
st.subheader("🧠 Operator Brief")
st.caption("Retrieved guidance, not AI-generated prose -- every passage below cites its source document.")
st.markdown(result["brief"].markdown)

st.divider()

# --- LIVE PARAMETER FEED ---
st.subheader("⚡ Live Parameter Feed")
st.caption(f"Source: {result['source']}  |  Features: TCCS current/duration, contact travel/temp, SF6 pressure")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Trip Coil Peak Current", f"{r['TCCS_Peak_Current_A']:.2f} A")
c2.metric("Contact Travel Time", f"{r['Contact_Travel_Time_ms']:.1f} ms")
c2.caption("Increasing indicates friction")
c3.metric("Contact Temperature", f"{r['Contact_Temperature_C']:.1f} °C")
c4.metric("SF6 Gas Pressure", f"{r['Gas_Pressure_bar']:.2f} bar")
c4.caption("Below ~5.5 bar — leakage risk")

st.divider()

c1, c2, c3, c4 = st.columns(4)
with c1:
    tccs_steps = [{'range': [0.0, 4.0], 'color': 'rgba(34, 197, 94, 0.25)'}, {'range': [4.0, 6.0], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [6.0, 10.0], 'color': 'rgba(239, 68, 68, 0.2)'}]
    render_industrial_gauge(r['TCCS_Peak_Current_A'], "Trip Coil Current", 0.0, 10.0, "A", steps=tccs_steps)
with c2:
    travel_steps = [{'range': [0.0, 38.0], 'color': 'rgba(34, 197, 94, 0.25)'}, {'range': [38.0, 45.0], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [45.0, 80.0], 'color': 'rgba(239, 68, 68, 0.2)'}]
    render_industrial_gauge(r['Contact_Travel_Time_ms'], "Contact Travel Time", 0.0, 80.0, "ms", steps=travel_steps)
with c3:
    temp_steps = [{'range': [20.0, 60.0], 'color': 'rgba(34, 197, 94, 0.25)'}, {'range': [60.0, 80.0], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [80.0, 100.0], 'color': 'rgba(239, 68, 68, 0.2)'}]
    render_industrial_gauge(r['Contact_Temperature_C'], "Contact Temp", 20.0, 100.0, "°C", steps=temp_steps)
with c4:
    # SF6 leaks downwards. Below 5.5 is a warning/critical zone.
    sf6_steps = [{'range': [0.0, 4.5], 'color': 'rgba(239, 68, 68, 0.2)'}, {'range': [4.5, 5.5], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [5.5, 10.0], 'color': 'rgba(34, 197, 94, 0.25)'}]
    render_industrial_gauge(r['Gas_Pressure_bar'], "SF6 Pressure", 0.0, 10.0, "bar", steps=sf6_steps)

st.divider()

# --- PROGNOSTICS: ESTIMATED TIME TO FAILURE ---
st.subheader("⏱️ Estimated Time to Failure — If Maintenance Not Performed")
st.caption("Prognostic analysis based on current AI-detected degradation trends vs. physical mechanism thresholds.")

if forecast is not None:
    current_travel = r['Contact_Travel_Time_ms']
    travel_limit = 65.0 
    travel_health_pct = max(0, (travel_limit - current_travel) / (travel_limit - 32.0))
    days_to_jam = max(1, int(travel_health_pct * 60)) 

    current_coil = r['TCCS_Duration_ms']
    coil_limit = 30.0 
    coil_health_pct = max(0, (coil_limit - current_coil) / (coil_limit - 10.0))
    days_to_coil = max(1, int(coil_health_pct * 40))

    overall_days = min(days_to_jam, days_to_coil)

    html_cards = f"""
    <div style="display: flex; gap: 15px; margin-bottom: 20px;">
        <div style="flex: 1; background: {'#3f2323' if days_to_jam < 15 else '#2d3748'}; padding: 15px; border-radius: 8px; border-left: 4px solid {'#f87171' if days_to_jam < 15 else '#fb923c'};">
            <h5 style="color: {'#f87171' if days_to_jam < 15 else '#fb923c'}; margin-top: 0; font-size: 14px;">Mechanical Jamming Failure</h5>
            <h2 style="margin: 10px 0; color: #fff;">~{days_to_jam} Days</h2>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 0;">
                Based on Contact Travel Time ({current_travel:.1f} ms). 
                Extended operation times indicate severe friction and imminent failure-to-trip.
            </p>
        </div>
        <div style="flex: 1; background: {'#3f2323' if days_to_coil < 20 else '#2d3748'}; padding: 15px; border-radius: 8px; border-left: 4px solid {'#f87171' if days_to_coil < 20 else '#facc15'};">
            <h5 style="color: {'#f87171' if days_to_coil < 20 else '#facc15'}; margin-top: 0; font-size: 14px;">Trip Coil Degradation</h5>
            <h2 style="margin: 10px 0; color: #fff;">~{days_to_coil} Days</h2>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 0;">
                TCCS Duration extending to {current_coil:.1f} ms. 
                Winding insulation degradation poses risk to electromagnetic latch release.
            </p>
        </div>
        <div style="flex: 1; background: {'#3f2323' if overall_days < 15 else '#1e293b'}; padding: 15px; border-radius: 8px; border-left: 4px solid {'#f87171' if overall_days < 15 else '#38bdf8'};">
            <h5 style="color: {'#f87171' if overall_days < 15 else '#38bdf8'}; margin-top: 0; font-size: 14px;">Complete Breaker Failure</h5>
            <h2 style="margin: 10px 0; color: #fff;">~{overall_days} Days</h2>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 0;">
                Compounded LSTM Health_Index: {forecast['value']:.2f}. 
                High risk of mechanism lockout during a primary network fault.
            </p>
        </div>
    </div>
    """
    st.markdown(html_cards, unsafe_allow_html=True)
else:
    st.warning("No LSTM model available. Run `python -m src.training.train_all`.")

st.divider()

# --- MAINTENANCE (Dual View & Action Dispatch) ---
st.subheader("🔧 Mandatory Maintenance — Action Required")

maintenance_df = pd.DataFrame({
    "Fault Class": [
        "Coil Degradation - Early", "Coil Degradation - Severe", 
        "Friction Wear", "Mechanical Jamming - Mild", "Mechanical Jamming - Severe"
    ],
    "Recommended Action": [
        "Trip coil resistance measurement at next scheduled outage",
        "Immediate trip coil replacement — winding insulation risk",
        "Operating mechanism lubrication and linkage inspection",
        "Schedule mechanism overhaul — increasing failure-to-trip risk",
        "Immediate mechanism inspection — critical failure-to-trip risk",
    ],
    "Priority": ["🟡 MEDIUM", "🔴 HIGH", "🟡 MEDIUM", "🔴 HIGH", "🔴 HIGH"],
})

if clf["fault_label"] == "Normal":
    st.success("**Status:** Breaker mechanism and coil parameters are nominal. No mandatory maintenance required at this time.")
else:
    active_maintenance = maintenance_df[maintenance_df["Fault Class"] == clf["fault_label"]]
    if not active_maintenance.empty:
        action = active_maintenance.iloc[0]["Recommended Action"]
        priority = active_maintenance.iloc[0]["Priority"]
        
        maint_key = f"maint_dispatched_cb_{selected_id}"
        
        if st.session_state.get(maint_key, False):
            st.success(f"✅ **Maintenance Crew Dispatched.** Breaker CB-{selected_id:02d} is isolated and pending physical repair.")
            if st.button("Complete Repair & Reset Asset Status"):
                st.session_state[maint_key] = False
                st.rerun()
        else:
            st.error(f"**Prescribed Task ({priority}):** {action}")
            if st.button(f"🚨 Dispatch Maintenance Team to CB-{selected_id:02d}", type="primary"):
                st.session_state[maint_key] = True
                st.session_state['auto_redirect'] = False 
                st.rerun()
    else:
        st.warning(f"**Prescribed Action:** No standard maintenance protocol mapped for fault class: {clf['fault_label']}")

st.caption("Standard Maintenance Reference Dictionary (Schedule Within 30 Days)")
st.dataframe(maintenance_df, width='stretch', hide_index=True)

st.divider()

# --- FOOTER ---
nav1, nav2, nav3 = st.columns([1, 1, 4])
with nav1:
    if st.button("← Back to Home"):
        st.switch_page("home.py")
with nav2:
    if st.button("ℹ️ XAI Explanation"):
        st.switch_page("pages/5_XAI.py")
with nav3:
    st.caption(f"Fleet: {len(all_ids)} circuit breaker(s)  |  Model-driven live feed (RF + LSTM)")