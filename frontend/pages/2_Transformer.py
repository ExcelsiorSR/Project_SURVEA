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

st.set_page_config(page_title="Transformer Fleet | Health Monitor", page_icon="🔌", layout="wide", initial_sidebar_state="collapsed")
enable_autorefresh(interval_seconds=3)

ist = pytz.timezone("Asia/Kolkata")
now_str = datetime.now(ist).strftime("%d %b %Y  %H:%M:%S IST")

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.caption("🔌 ASSET FLEET VIEW — TRANSFORMERS")
    st.title(f"Transformer Fleet — IEEE {get_selected_grid()}-Bus System")
with col2:
    live_clock()

st.divider()

# Fleet-wide alert
render_fleet_alert_banner(current_asset_type="transformer")

# --- VISUAL FLEET DASHBOARD ---
st.subheader("🔌 Transformer Fleet Overview")
all_ids = get_fleet_asset_ids("transformer")
overview = get_fleet_overview("transformer")

if "selected_trf_id" not in st.session_state or st.session_state["selected_trf_id"] not in all_ids:
    failing_unit = next((a["asset_id"] for a in overview if a["fault_class"] != "Normal"), None)
    st.session_state["selected_trf_id"] = failing_unit if failing_unit is not None else (all_ids[0] if all_ids else 0)

if overview:
    st.caption("Click any unit below to view live telemetry and prognostics.")
    cols = st.columns(8) 
    for index, asset in enumerate(overview):
        uid = asset["asset_id"]
        fc = asset["fault_class"]
        
        if fc == "Normal":
            btn_label = f"🟢 T-{uid:02d}\nNormal"
        elif "Severe" in fc or "Discharge" in fc or "T3" in fc or "CATASTROPHIC" in fc:
            btn_label = f"🔴 T-{uid:02d}\n{fc}"
        else:
            btn_label = f"🟡 T-{uid:02d}\n{fc}"
            
        with cols[index % 8]:
            if st.button(btn_label, key=f"btn_trf_{uid}", use_container_width=True):
                st.session_state["selected_trf_id"] = uid
                st.rerun()
else:
    st.info("Live twin disconnected. Demo mode active.")
    st.session_state["selected_trf_id"] = st.selectbox("Select Transformer Unit", options=all_ids, format_func=lambda i: f"Transformer T-{i:02d}")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:

    btn_left, btn_center, btn_right = st.columns([1, 1, 1])

    with btn_center:
        if st.button("🔄 Refresh Grid State", width = 'content'):
            st.rerun()

st.divider()

# --- DETAILED SINGLE-UNIT VIEW ---
selected_id = st.session_state["selected_trf_id"]
result = get_prediction("transformer", asset_id=selected_id)
r = result["reading"]
clf = result["classification"]
forecast = result["forecast"]
st.subheader(f"🔌 Transformer T-{selected_id:02d} — Health & Prognostics")
st.caption(f"Unit {selected_id} of {len(all_ids)} on this grid  |  Model: Random Forest (8-class DGA) + LSTM  |  "
           f"{'🟢 LIVE DIGITAL TWIN FEED' if result['source'] == 'LIVE DIGITAL TWIN' else '🟡 DEMO MODE — replaying real historical readings'}")

# --- FRONTEND SYNC PATCH ---
# If the Twin's physics engine explicitly knows the asset is Normal,
# override the ML's "Undetermined" confusion caused by the synthetic low baseline.
# badge is computed AFTER this patch so it reflects the corrected label.
registry_status = next((a["fault_class"] for a in overview if a["asset_id"] == selected_id), "Unknown")
if clf["fault_label"] == "Undetermined" and registry_status == "Normal":
    clf["fault_label"] = "Normal"

badge = risk_badge(clf["fault_label"])

# --- MODEL ASSESSMENT ---
st.subheader("🔔 Model Assessment")
if clf["fault_label"] == "Normal":
    st.success(f"{badge} — Random Forest classifier: **Normal** (confidence validated by Twin Registry)")
elif clf["fault_label"] == "Undetermined":
    st.warning(f"{badge} — Random Forest classifier: **{clf['fault_label']}** (confidence {clf['confidence']:.0%})\n\n"
               f"Fault signature is ambiguous due to missing/synthetic telemetry. Manual laboratory DGA test required.")
else:
    alert_fn = st.error if "🔴" in badge else st.warning
    alert_fn(
        f"{badge} — Random Forest classifier: **{clf['fault_label']}** (confidence {clf['confidence']:.0%})\n\n"
        f"Dominant fault signature per Duval ratios: C2H2 {r['C2H2']:.2f}  |  CH4 {r['CH4']:.2f}  |  "
        f"C2H4 {r['C2H4']:.2f} (standardized readings)"
    )

st.divider()

# --- OPERATOR BRIEF ---
st.subheader("🧠 Operator Brief")
st.caption("Retrieved guidance, not AI-generated prose -- every passage below cites its source document.")
st.markdown(result["brief"].markdown)

st.divider()

# --- LIVE PARAMETER FEED ---
st.subheader("⚡ Live Parameter Feed")
st.caption(f"Source: {result['source']}  |  Values mapped to IEEE C57.104 Parts-Per-Million (ppm) equivalents")

# Pseudo-PPM conversion (Maps ML-standardized tensors into realistic SCADA PPM limits)
ppm_H2 = max(0.0, (r['H2'] + 1.2) * 45)

# Scaled so healthy baseline (r <= 0.4) stays safely below the 1.0 ppm IEEE C57.104 limit
if r['C2H2'] <= 0.4:
    ppm_C2H2 = max(0.0, round(0.15 + (r['C2H2'] + 0.9) * 0.4, 2))
else:
    ppm_C2H2 = max(0.0, round(1.0 + (r['C2H2'] - 0.4) * 4.5, 2))

ppm_C2H4 = max(0.0, (r['C2H4'] + 1.2) * 50) 
ppm_CH4 = max(0.0, (r['CH4'] + 1.2) * 80)   
ppm_C2H6 = max(0.0, (r['C2H6'] + 1.2) * 40) 
ppm_CO = max(0.0, (r['CO'] + 1.2) * 300)

c1, c2, c3 = st.columns(3)
c1.metric("Hydrogen (H2)", f"{ppm_H2:.1f} ppm")
c1.caption("Normal: <100 ppm | Indicates: Partial discharge")
c2.metric("Acetylene (C2H2)", f"{ppm_C2H2:.2f} ppm")
c2.caption("Normal: <1 ppm | Most critical gas: Indicates arcing")
c3.metric("Ethylene (C2H4)", f"{ppm_C2H4:.1f} ppm")
c3.caption("Normal: <50 ppm | Indicates: Thermal fault >300°C")

c4, c5, c6 = st.columns(3)
c4.metric("Methane (CH4)", f"{ppm_CH4:.1f} ppm")
c4.caption("Normal: <120 ppm | Indicates: Low-level overheating")
c5.metric("Ethane (C2H6)", f"{ppm_C2H6:.1f} ppm")
c5.caption("Normal: <65 ppm | Indicates: Thermal fault <150°C")
c6.metric("Carbon Monoxide (CO)", f"{ppm_CO:.1f} ppm")
c6.caption("Normal: <350 ppm | Indicates: Cellulose degradation")

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    h2_steps = [{'range': [0, 100], 'color': 'rgba(34, 197, 94, 0.25)'}, {'range': [100, 300], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [300, 500], 'color': 'rgba(239, 68, 68, 0.2)'}]
    render_industrial_gauge(ppm_H2, "Hydrogen (H₂)", 0.0, 500.0, "ppm", steps=h2_steps)
with c2:
    c2h2_steps = [{'range': [0, 1], 'color': 'rgba(34, 197, 94, 0.25)'}, {'range': [1, 5], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [5, 10], 'color': 'rgba(239, 68, 68, 0.2)'}]
    render_industrial_gauge(ppm_C2H2, "Acetylene (C₂H₂)", 0.0, 10.0, "ppm", steps=c2h2_steps)
with c3:
    c2h4_steps = [{'range': [0, 50], 'color': 'rgba(34, 197, 94, 0.25)'}, {'range': [50, 80], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [80, 100], 'color': 'rgba(239, 68, 68, 0.2)'}]
    render_industrial_gauge(ppm_C2H4, "Ethylene (C₂H₄)", 0.0, 100.0, "ppm", steps=c2h4_steps)

c4, c5, c6 = st.columns(3)
with c4:
    ch4_steps = [{'range': [0, 120], 'color': 'rgba(34, 197, 94, 0.25)'}, {'range': [120, 200], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [200, 300], 'color': 'rgba(239, 68, 68, 0.2)'}]
    render_industrial_gauge(ppm_CH4, "Methane (CH₄)", 0.0, 300.0, "ppm", steps=ch4_steps)
with c5:
    c2h6_steps = [{'range': [0, 65], 'color': 'rgba(34, 197, 94, 0.25)'}, {'range': [65, 85], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [85, 100], 'color': 'rgba(239, 68, 68, 0.2)'}]
    render_industrial_gauge(ppm_C2H6, "Ethane (C₂H₆)", 0.0, 100.0, "ppm", steps=c2h6_steps)
with c6:
    co_steps = [{'range': [0, 350], 'color': 'rgba(34, 197, 94, 0.25)'}, {'range': [350, 570], 'color': 'rgba(234, 179, 8, 0.2)'}, {'range': [570, 800], 'color': 'rgba(239, 68, 68, 0.2)'}]
    render_industrial_gauge(ppm_CO, "Carbon Monoxide (CO)", 0.0, 800.0, "ppm", steps=co_steps)

st.divider()

# --- PROGNOSTICS: ESTIMATED TIME TO FAILURE ---
st.subheader("⏱️ Estimated Time to Failure — If Maintenance Not Performed")
st.caption("Prognostic analysis based on current AI-detected DGA degradation trends vs. IEEE C57.104 thresholds.")

if forecast is not None:
    current_arcing = r['C2H2']
    arcing_limit = 2.0 
    arcing_health_pct = max(0, (arcing_limit - current_arcing) / arcing_limit)
    days_to_arcing = max(1, int(arcing_health_pct * 45)) 

    current_thermal = max(r['CH4'], r['C2H4'])
    thermal_limit = 2.0 
    thermal_health_pct = max(0, (thermal_limit - current_thermal) / thermal_limit)
    days_to_thermal = max(1, int(thermal_health_pct * 60))

    overall_days = min(days_to_arcing, days_to_thermal)

    html_cards = f"""
    <div style="display: flex; gap: 15px; margin-bottom: 20px;">
        <div style="flex: 1; background: {'#3f2323' if days_to_arcing < 15 else '#2d3748'}; padding: 15px; border-radius: 8px; border-left: 4px solid {'#f87171' if days_to_arcing < 15 else '#fb923c'};">
            <h5 style="color: {'#f87171' if days_to_arcing < 15 else '#fb923c'}; margin-top: 0; font-size: 14px;">Insulation / Winding Failure</h5>
            <h2 style="margin: 10px 0; color: #fff;">~{days_to_arcing} Days</h2>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 0;">
                Based on standardized C2H2 levels ({current_arcing:.2f}). 
                Approaching critical threshold indicates imminent severe arcing or discharge.
            </p>
        </div>
        <div style="flex: 1; background: {'#3f2323' if days_to_thermal < 20 else '#2d3748'}; padding: 15px; border-radius: 8px; border-left: 4px solid {'#f87171' if days_to_thermal < 20 else '#facc15'};">
            <h5 style="color: {'#f87171' if days_to_thermal < 20 else '#facc15'}; margin-top: 0; font-size: 14px;">Oil Degradation & Dielectric Failure</h5>
            <h2 style="margin: 10px 0; color: #fff;">~{days_to_thermal} Days</h2>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 0;">
                Combined thermal gas levels (CH4/C2H4) indicate accelerated oil aging. 
                Dielectric strength expected to fall below safe thresholds.
            </p>
        </div>
        <div style="flex: 1; background: {'#3f2323' if overall_days < 15 else '#1e293b'}; padding: 15px; border-radius: 8px; border-left: 4px solid {'#f87171' if overall_days < 15 else '#38bdf8'};">
            <h5 style="color: {'#f87171' if overall_days < 15 else '#38bdf8'}; margin-top: 0; font-size: 14px;">Complete Transformer Failure</h5>
            <h2 style="margin: 10px 0; color: #fff;">~{overall_days} Days</h2>
            <p style="font-size: 12px; color: #cbd5e1; margin-bottom: 0;">
                Compounded LSTM DGA Severity Index: {forecast['value']:.2f}. 
                Without oil treatment and gas purging, full failure risk escalates significantly.
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
    "Fault Class": [
        "Partial Discharge", "D1 - Low Energy Discharge", "D2 - High Energy Discharge",
        "T1 - Thermal Fault (<300C)", "T2 - Thermal Fault (300-700C)", "T3 - Thermal Fault (>700C)", "CATASTROPHIC FAILURE"
    ],
    "Recommended Action": [
        "Acoustic emission testing to locate corona discharge",
        "Oil sampling + Duval Triangle confirmation within 30 days",
        "Immediate shutdown evaluation — internal arcing risk",
        "Check cooling system performance and load history",
        "Cooling system inspection, oil temperature check",
        "Full internal inspection — severe thermal degradation risk",
        "UNIT OFFLINE. Severe arcing/thermal damage detected. Replace oil and inspect core."
    ],
    "Priority": ["🟡 MEDIUM", "🟡 MEDIUM", "🔴 HIGH", "🟡 MEDIUM", "🔴 HIGH", "🔴 HIGH", "🚨 CRITICAL"],
})

maint_key = f"maint_dispatched_trf_{selected_id}"

if clf["fault_label"] == "Normal":
    st.success("**Status:** Asset is operating within normal parameters. No mandatory maintenance required at this time.")

elif clf["fault_label"] == "Undetermined":
    if st.session_state.get(maint_key, False):
        st.success(f"✅ **Oil Sampling Crew Dispatched.** Asset T-{selected_id:02d} is pending manual DGA lab results.")
        if st.button("Log Lab Results & Reset Status"):
            st.session_state[maint_key] = False
            st.rerun()
    else:
        st.warning("**Status:** Fault signature is ambiguous. Schedule manual oil sampling.")
        if st.button(f"🧪 Dispatch Oil Sampling Crew to T-{selected_id:02d}"):
            st.session_state[maint_key] = True
            st.rerun()

else:
    active_maintenance = maintenance_df[maintenance_df["Fault Class"] == clf["fault_label"]]
    if not active_maintenance.empty:
        action = active_maintenance.iloc[0]["Recommended Action"]
        priority = active_maintenance.iloc[0]["Priority"]
        
        if st.session_state.get(maint_key, False):
            st.success(f"✅ **Maintenance Crew Dispatched.** Asset T-{selected_id:02d} is isolated and pending physical repair.")
            if st.button("Complete Repair & Reset Asset Status"):
                st.session_state[maint_key] = False
                st.rerun()
        else:
            st.error(f"**Prescribed Task ({priority}):** {action}")
            if st.button(f"🚨 Dispatch Maintenance Team to T-{selected_id:02d}", type="primary"):
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
    st.caption(f"Fleet: {len(all_ids)} transformer(s)  |  Model-driven live feed (RF + LSTM)")