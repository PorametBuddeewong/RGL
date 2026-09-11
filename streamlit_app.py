import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import io

# Import ReportLab components safely
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# =============================================================================
# 1. PAGE SETUP & CONFIGURATION
# =============================================================================
st.set_page_config(
    layout="wide", 
    page_title="RGL Specialist Procurement Dashboard", 
    page_icon="🧪"
)

st.markdown("""
    <style>
    html, body, [class*="css"], p, label, span, li, input {
        font-size: 16px !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        font-size: 18px !important;
        padding: 10px !important;
    }
    .stForm {
        padding: 25px !important;
        border-radius: 12px !important;
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
    }
    .section-container {
        background-color: #1E293B;
        color: #FFFFFF;
        padding: 18px 24px;
        border-radius: 8px;
        margin-top: 30px;
        margin-bottom: 20px;
        font-weight: 700;
        font-size: 22px !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 32px !important;
        font-weight: bold !important;
    }
    .stDataFrame th, .stDataFrame td {
        padding: 12px 16px !important;
        font-size: 16px !important;
    }
    div[data-baseweb="select"] { font-size: 18px !important; }
    div[data-baseweb="select"] > div { min-height: 48px !important; display: flex !important; align-items: center !important; }
    ul[role="listbox"] li { white-space: normal !important; word-break: break-word !important; font-size: 18px !important; padding: 12px 16px !important; }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. STATE MANAGEMENT & PRESETS 
# =============================================================================
PRESET_SUPPLIERS = {
    "Custom (Manual Input)": {"conv": 0.8600, "naoh": 1.20, "fac": 0.50, "rac": 1.90, "elec": 122.0, "water": 3.90, "fuel": 1.40, "n2": 1.50, "biogas": 109.0, "ygl": 1.0, "glr": 3.90, "ds": 3.1},
    "CGL ME2": {"conv": 0.8600, "naoh": 1.20, "fac": 0.50, "rac": 1.90, "elec": 122.0, "water": 3.90, "fuel": 1.40, "n2": 1.50, "biogas": 109.0, "ygl": 1.0, "glr": 3.90, "ds": 3.1},
    "New Bio": {"conv": 0.8204, "naoh": 1.14, "fac": 0.53, "rac": 2.14, "elec": 116.404, "water": 3.749, "fuel": 1.339, "n2": 1.446, "biogas": 104.391, "ygl": 1.0, "glr": 5.088, "ds": 2.95726},
    "East Bio": {"conv": 0.7850, "naoh": 1.10, "fac": 0.51, "rac": 2.04, "elec": 111.384, "water": 3.587, "fuel": 1.281, "n2": 1.384, "biogas": 99.889, "ygl": 1.0, "glr": 6.149, "ds": 2.82972},
    "Bangchak Bio": {"conv": 0.8164, "naoh": 1.14, "fac": 0.53, "rac": 2.13, "elec": 115.837, "water": 3.731, "fuel": 1.333, "n2": 1.439, "biogas": 103.882, "ygl": 1.0, "glr": 5.208, "ds": 2.94284},
    "Seastar-Indo": {"conv": 0.7747, "naoh": 1.08, "fac": 0.50, "rac": 2.02, "elec": 109.914, "water": 3.540, "fuel": 1.264, "n2": 1.366, "biogas": 98.571, "ygl": 1.0, "glr": 6.460, "ds": 2.79237},
    "Seastar-2 SEA": {"conv": 0.7666, "naoh": 1.07, "fac": 0.50, "rac": 2.00, "elec": 108.771, "water": 3.503, "fuel": 1.251, "n2": 1.351, "biogas": 97.545, "ygl": 1.0, "glr": 6.702, "ds": 2.76333},
    "Itochu (PPP)": {"conv": 0.7712, "naoh": 1.08, "fac": 0.50, "rac": 2.01, "elec": 109.423, "water": 3.524, "fuel": 1.259, "n2": 1.359, "biogas": 98.131, "ygl": 1.0, "glr": 6.564, "ds": 2.77991},
    "Sojit (LDC)": {"conv": 0.8175, "naoh": 1.14, "fac": 0.53, "rac": 2.13, "elec": 115.988, "water": 3.736, "fuel": 1.334, "n2": 1.441, "biogas": 104.018, "ygl": 1.0, "glr": 5.176, "ds": 2.94667},
    "Agri oil 1": {"conv": 0.8609, "naoh": 1.20, "fac": 0.56, "rac": 2.24, "elec": 122.151, "water": 3.934, "fuel": 1.405, "n2": 1.518, "biogas": 109.545, "ygl": 1.0, "glr": 3.873, "ds": 3.10324},
    "Agri oil 2": {"conv": 0.8247, "naoh": 1.15, "fac": 0.54, "rac": 2.15, "elec": 117.014, "water": 3.769, "fuel": 1.346, "n2": 1.454, "biogas": 104.938, "ygl": 1.0, "glr": 4.959, "ds": 2.97276},
    "PPP (High pH)-Jan25": {"conv": 0.7473, "naoh": 1.11, "fac": 0.49, "rac": 1.95, "elec": 115.988, "water": 3.542, "fuel": 1.223, "n2": 1.600, "biogas": 102.156, "ygl": 1.0, "glr": 7.281, "ds": 2.69371}
}

if "suppliers" not in st.session_state:
    st.session_state.suppliers = []
else:
    for s in st.session_state.suppliers:
        if "ds" not in s:
            s["ds"] = PRESET_SUPPLIERS.get(s["name"], {}).get("ds", 0.0)

# =============================================================================
# 3. GLOBAL VARIABLES AND SIDEBAR INPUTS
# =============================================================================
st.title("🧪 RGL Specialist Executive Dashboard")

with st.sidebar:
    st.header("⚙️ Cost Parameters")
    st.markdown("---")
    
    with st.expander("💰 1. Market & By-product Prices", expanded=True):
        ygl_p_usd = st.number_input("YGL Selling Price (USD/MT)", value=643.0)
        gl_res_p_usd = st.number_input("GL Residue Selling Price (USD/MT)", value=31.98)
        fx = st.number_input("Exchange Rate FX (THB/USD)", value=31.25)
        
    with st.expander("🧪 2. Chemical Cost Parameters", expanded=False):
        naoh_p = st.number_input("NaOH (THB/kg)", value=9.68)
        fac_p_usd = st.number_input("Fresh Active Carbon(USD/MT)", value=4730.46)
        rac_p_usd = st.number_input("Regen Active Carbon(USD/MT)", value=1216.0)
        
    with st.expander("⚡ 3. Utility Cost Parameters", expanded=False):
        elec_p = st.number_input("Electricity Cost (THB/kWh)", value=3.51)
        water_p = st.number_input("Clarified Water Cost (THB/m3)", value=25.0)
        fuel_p = st.number_input("Fuel Oil Cost (THB/Ton)", value=14514.0)
        biogas_p = st.number_input("Biogas Cost (THB/m3)", value=6.41)
        n2_p = st.number_input("Nitrogen Gas Cost (THB/m3)", value=6.18)
        ds_p = st.number_input("Diesel Cost (THB/L)", value=30.00)

    with st.expander("🏭 4. Rayong Operational Cost Parameters", expanded=False):
        cgl_80_p_usd = st.number_input("CGL 80% Price (USD/MT)", value=777.89)
        dmw_p_usd = st.number_input("DMW Price (USD/unit)", value=2.019)
        bfw_p_usd = st.number_input("BFW Price (USD/unit)", value=6.368)

    with st.expander("🏗️ 5. Other Parameter", expanded=False):
        ovc_ext_usd_mt_rgl1 = st.number_input("ME1 Other Variable Cost / OVC (USD/MT RGL)", value=89.00)
        ovc_ext_usd_mt_rgl2 = st.number_input("ME2 Other Variable Cost / OVC (USD/MT RGL)", value=8.00)
        ovc_ext_usd_mt_rgl12 = st.number_input("ME2 to ME1 Delivery Cost (USD/MT CGL)", value=40.00)

# =============================================================================
# 4. CALCULATION ENGINE
# =============================================================================
def calculate_rgl_external(suppliers, rgl_p_thb):
    results = []
    for s in suppliers:
        feed = s["qty"]
        conv = s["conv"]
        cgl_price = s["price"]
        
        if feed <= 0:
            continue
            
        naoh_cost = feed * (s["naoh"] * naoh_p)
        fac_cost  = feed * (s["fac"] * fac_p_usd * fx / 1000)
        rac_cost  = feed * (s["rac"] * rac_p_usd * fx / 1000)
        chem_cost = naoh_cost + fac_cost + rac_cost
        
        elec_cost   = feed * (s["elec"] * elec_p)
        water_cost  = feed * (s["water"] * water_p)
        fuel_cost   = feed * (s["fuel"] * fuel_p) / 72
        n2_cost     = feed * (s["n2"] * n2_p)
        biogas_cost = feed * (s["biogas"] * biogas_p)
        Diesel_cost = feed * (s.get("ds", 0.0) * ds_p)
        util_cost   = elec_cost + water_cost + fuel_cost + n2_cost + biogas_cost + Diesel_cost
        
        ygl_cr    = feed * (s["ygl_conv"] / 100) * ygl_p_usd * fx
        gl_res_cr = feed * (s["gl_res_conv"] / 100) * gl_res_p_usd * fx
        bp_credit = ygl_cr + gl_res_cr

        rgl_out = feed * conv

        # Disposal Cost Calculation
        gr_sl = feed - rgl_out - feed * (s["ygl_conv"] / 100) - feed * (s["gl_res_conv"] / 100) 
        dis_cost = gr_sl * 2950
        
        feed_cost = feed * cgl_price * 1000
        ovc_total_thb = rgl_out * ovc_ext_usd_mt_rgl2 * fx
        
        # Total cost inclusive of disposal
        total_cost = feed_cost + chem_cost + util_cost + ovc_total_thb - bp_credit + dis_cost
        revenue = rgl_p_thb * rgl_out * 1000
        
        cm_thb_kg = (revenue - total_cost) / (rgl_out * 1000) if rgl_out > 0 else 0
        cm_usd_mt = cm_thb_kg * 1000 / fx if rgl_out > 0 else 0

        results.append({
            "name": s["name"], "feed": feed, "rgl_out": rgl_out,
            "feed_cost": feed_cost, "chem_cost": chem_cost,
            "util_cost": util_cost, "bp_credit": bp_credit,
            "ovc_total_thb": ovc_total_thb, "dis_cost": dis_cost,
            "total_cost": total_cost, "cm": cm_thb_kg, "cm_usd": cm_usd_mt,
            "conv": conv
        })
    return results

def calculate_rgl_rayong(suppliers, rgl_p_usd):
    results = []
    rayong_conv = 0.75500
    logistics_cost_usd_mt_cgl = ovc_ext_usd_mt_rgl12
    ovc_usd_mt_rgl = ovc_ext_usd_mt_rgl1
    
    for s in suppliers:
        feed = s["qty"]
        if feed <= 0:
            continue
            
        cgl_price_usd_mt = (s["price"] * 1000) / fx
        feed_cost_usd = feed * cgl_price_usd_mt
        logistics_cost_usd = feed * logistics_cost_usd_mt_cgl
        
        n2_cost_usd = feed * 5.37803 * (n2_p / fx)
        cfw_cost_usd = feed * 0.84234 * (water_p / fx)
        dmw_cost_usd = feed * 0.09955 * dmw_p_usd
        bfw_cost_usd = feed * 0.32987 * bfw_p_usd
        util1_cost = n2_cost_usd + cfw_cost_usd + dmw_cost_usd + bfw_cost_usd
        
        naoh_cost_usd = feed * 0.02356 * (naoh_p * 1000 / fx) 
        fac_cost_usd = feed * 0.00088 * fac_p_usd
        rac_cost_usd = feed * 0.00377 * rac_p_usd
        chem1_cost = naoh_cost_usd + fac_cost_usd + rac_cost_usd
        
        variable_costs_usd = util1_cost + chem1_cost
        rgl_out = feed * rayong_conv
        ovc_total_usd = rgl_out * ovc_usd_mt_rgl

        wasteres_vol = 0.0282 * feed
        dis1_cost = wasteres_vol * 2950 / fx
        
        total_vc_usd = variable_costs_usd + ovc_total_usd + dis1_cost
        
        ygl_credit_usd = feed * 0.1450 * ygl_p_usd
        gl_res_credit_usd = feed * 0.0360 * gl_res_p_usd
        cgl_80_credit_usd = feed * 0.0358 * cgl_80_p_usd
        total_bp_credit_usd = ygl_credit_usd + gl_res_credit_usd + cgl_80_credit_usd
        
        revenue_usd = rgl_out * rgl_p_usd
        net_operational_cost_usd = feed_cost_usd + logistics_cost_usd + total_vc_usd - total_bp_credit_usd
        
        cm_usd_mt = (revenue_usd - net_operational_cost_usd) / rgl_out if rgl_out > 0 else 0
        cm_thb_kg = cm_usd_mt * fx / 1000
        
        results.append({
            "name": s["name"], "feed": feed, "rgl_out": rgl_out,
            "feed_cost_usd": feed_cost_usd, "logistics_cost_usd": logistics_cost_usd,
            "vc_usd": total_vc_usd, "bp_credit_usd": total_bp_credit_usd,
            "cm_usd": cm_usd_mt, "cm_thb": cm_thb_kg, "conv": rayong_conv,
            "variable_costs_usd": variable_costs_usd, "ovc_total_usd": ovc_total_usd
        })
    return results

# =============================================================================
# 5. EXECUTE CORE CALCULATIONS
# =============================================================================
rgl_p_usd = st.session_state.get("rgl_p_usd_input", 1120.0) 
rgl_p_thb = rgl_p_usd * fx / 1000

ext_results = calculate_rgl_external(st.session_state.suppliers, rgl_p_thb)
total_ext_feed = sum(r["feed"] for r in ext_results)
total_ext_rgl = sum(r["rgl_out"] for r in ext_results)

if total_ext_rgl > 0:
    weighted_conv_rate = total_ext_rgl / total_ext_feed
    
    # FIX: Added dis_cost into total fixed operational costs calculation
    tot_ext_fixed_costs = sum(r["chem_cost"] + r["util_cost"] + r["ovc_total_thb"] + r["dis_cost"] - r["bp_credit"] for r in ext_results)
    
    p2f_thb_kg = rgl_p_thb - (sum(r["feed_cost"] for r in ext_results) / (total_ext_rgl * 1000))
    p2f_usd_mt = p2f_thb_kg * 1000 / fx
    
    vc_thb_kg = sum(r["chem_cost"] + r["util_cost"] + r["ovc_total_thb"] + r["dis_cost"] for r in ext_results) / (total_ext_rgl * 1000)
    vc_usd_mt = vc_thb_kg * 1000 / fx
    
    bp_thb_kg = sum(r["bp_credit"] for r in ext_results) / (total_ext_rgl * 1000)
    bp_usd_mt = bp_thb_kg * 1000 / fx
    
    overall_cm_thb = sum(r["cm"] * r["rgl_out"] for r in ext_results) / total_ext_rgl
    overall_cm_usd = overall_cm_thb * 1000 / fx
    
    fixed_costs_per_kg_feed = tot_ext_fixed_costs / (total_ext_feed * 1000)
    be_cgl_purchase_price_thb = (rgl_p_thb * weighted_conv_rate) - fixed_costs_per_kg_feed
else:
    weighted_conv_rate = 0.0; tot_ext_fixed_costs = 0.0; p2f_thb_kg = 0.0; p2f_usd_mt = 0.0
    vc_thb_kg = 0.0; vc_usd_mt = 0.0; bp_thb_kg = 0.0; bp_usd_mt = 0.0
    overall_cm_thb = 0.0; overall_cm_usd = 0.0; be_cgl_purchase_price_thb = 0.0

rayong_results = calculate_rgl_rayong(st.session_state.suppliers, rgl_p_usd)
total_rayong_feed = sum(r["feed"] for r in rayong_results)
total_rayong_rgl = sum(r["rgl_out"] for r in rayong_results)

if total_rayong_rgl > 0:
    rayong_weighted_conv = 0.75500
    tot_rayong_logistics_usd = sum(r["logistics_cost_usd"] for r in rayong_results)
    tot_rayong_vc_usd = sum(r["vc_usd"] for r in rayong_results)
    tot_rayong_bp_usd = sum(r["bp_credit_usd"] for r in rayong_results)
    
    rayong_logistics_usd_mt_rgl = tot_rayong_logistics_usd / total_rayong_rgl
    rayong_vc_usd_mt_rgl = tot_rayong_vc_usd / total_rayong_rgl
    rayong_bp_usd_mt_rgl = tot_rayong_bp_usd / total_rayong_rgl
    
    rayong_overall_cm_usd = sum(r["cm_usd"] * r["rgl_out"] for r in rayong_results) / total_rayong_rgl
    rayong_overall_cm_thb = rayong_overall_cm_usd * fx / 1000
    
    be_rayong_cgl_price_usd_mt = (rgl_p_usd * rayong_weighted_conv) - ovc_ext_usd_mt_rgl12 - (tot_rayong_vc_usd / total_rayong_feed) + (tot_rayong_bp_usd / total_rayong_feed)
    be_rayong_cgl_purchase_price_thb = be_rayong_cgl_price_usd_mt * fx / 1000
else:
    rayong_weighted_conv = 0.75500; rayong_logistics_usd_mt_rgl = 0.0; rayong_vc_usd_mt_rgl = 0.0; rayong_bp_usd_mt_rgl = 0.0
    rayong_overall_cm_usd = 0.0; rayong_overall_cm_thb = 0.0; be_rayong_cgl_purchase_price_thb = 0.0; tot_rayong_vc_usd = 0.0; tot_rayong_bp_usd = 0.0

# FIX: Aligned Sensitivity formulas with full cost structure
def calc_sens_cgl_current(target_cm_usd):
    if total_ext_feed <= 0: return 0.0
    target_cm_thb = target_cm_usd * fx / 1000
    cost_fixed_per_kg_rgl = tot_ext_fixed_costs / (total_ext_feed * weighted_conv_rate * 1000)
    return float(weighted_conv_rate * (rgl_p_thb - cost_fixed_per_kg_rgl - target_cm_thb))

def calc_sens_cgl_rayong(target_cm_usd):
    if total_rayong_feed <= 0: return 0.0
    vc_per_cgl = tot_rayong_vc_usd / total_rayong_feed
    credits_per_cgl = tot_rayong_bp_usd / total_rayong_feed
    # FIX: Replaced hardcoded 40.00 with dynamic variable ovc_ext_usd_mt_rgl12
    max_cgl_usd_mt = (rgl_p_usd - target_cm_usd) * rayong_weighted_conv - ovc_ext_usd_mt_rgl12 - vc_per_cgl + credits_per_cgl
    return float(max_cgl_usd_mt * fx / 1000)

# =============================================================================
# 6. USER INTERFACE WORKFLOW
# =============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🗂️ Step 1: Data Setup & Supplier Management",
    "📊 Step 2: Overview & Break-Even Analysis",
    "📈 Step 3: CGL Price Sensitivity Analysis",
    "📑 Step 4: Audit Trail & Calculation Details"
])

with tab1:
    st.markdown('<div class="section-container">1. Primary Market Pricing Framework</div>', unsafe_allow_html=True)
    col_p1, col_p2 = st.columns([2, 2])
    with col_p1:
        rgl_p_usd = st.number_input("Finished Refined Glycerin (RGL) Selling Price (USD/MT)", value=1120.0, key="rgl_p_usd_input")
    with col_p2:
        st.metric(label="ICIS Recommended Price Benchmark", value="1,120 USD/MT")
    
    selected_preset_name = st.selectbox("📋 Load Consumption Structure from Data Base (Supplier Preset)", options=list(PRESET_SUPPLIERS.keys()))
    preset = PRESET_SUPPLIERS[selected_preset_name]
    
    with st.form("add_supplier_form_v3", clear_on_submit=False):
        st.markdown("### 🔹 Base Feed Variables")
        col1, col2, col3 = st.columns(3)
        s_name = col1.text_input("Supplier Entity Name", value="" if selected_preset_name == "Custom (Manual Input)" else selected_preset_name)
        s_price = col2.number_input("CGL Purchase Price (THB/kg)", value=20.50, step=0.01, format="%.2f")
        s_qty = col3.number_input("Supply Volume (MT)", value=10.0, step=1.0)
        s_conv = col1.number_input("RGL Yield Conversion Rate", value=preset["conv"], format="%.4f")
        
        st.markdown("---")
        st.markdown("### 🔹 Chemical Consumption Rates (kg / MT CGL feed)")
        c_col1, c_col2, c_col3 = st.columns(3)
        s_naoh = c_col1.number_input("NaOH", value=float(preset["naoh"]), format="%.4f")
        s_fac = c_col2.number_input("Fresh Active Carbon", value=float(preset["fac"]), format="%.4f")
        s_rac = c_col3.number_input("Regenerated Active Carbon", value=float(preset["rac"]), format="%.4f")
        
        st.markdown("---")
        st.markdown("### 🔹 Utility Consumption Rates (unit / MT CGL feed)")
        u_col1, u_col2, u_col3, u_col4, u_col5 = st.columns(5)
        s_elec = u_col1.number_input("Electricity (kWh)", value=float(preset["elec"]), format="%.3f")
        s_water = u_col2.number_input("Clarified Water (m3)", value=float(preset["water"]), format="%.3f")
        s_fuel = u_col3.number_input("Fuel Oil(Ton)", value=float(preset["fuel"]), format="%.3f")
        s_n2 = u_col4.number_input("Nitrogen Gas (Nm3)", value=float(preset["n2"]), format="%.3f")
        s_bio = u_col5.number_input("Biogas(m3)", value=float(preset["biogas"]), format="%.3f")
        s_ds = u_col1.number_input("Diesel (L)", value=float(preset.get("ds", 3.1)), format="%.3f")
        
        st.markdown("---")
        st.markdown("### 🔹 By-product Credit Matrix (% conversion from CGL feed)")
        b_col1, b_col2 = st.columns(2)
        s_ygl = b_col1.number_input("Yellow Glycerin Output(%)", value=float(preset["ygl"]), format="%.3f")
        s_glr = b_col2.number_input("Glycerin Waste Residue(%)", value=float(preset["glr"]), format="%.3f")
        
        submitted = st.form_submit_button("➕ Save / Update Supplier Configuration", use_container_width=True)
        if submitted:
            if not s_name.strip():
                st.error("❌ Configuration Error: Supplier Entity Name field cannot be left blank.")
            else:
                st.session_state.suppliers = [s for s in st.session_state.suppliers if s["name"].lower() != s_name.strip().lower()]
                st.session_state.suppliers.append({
                    "name": s_name.strip(), "price": s_price, "qty": s_qty, "conv": s_conv,
                    "naoh": s_naoh, "fac": s_fac, "rac": s_rac,
                    "elec": s_elec, "water": s_water, "fuel": s_fuel, "n2": s_n2, "biogas": s_bio, "ds": s_ds,
                    "ygl_conv": s_ygl, "gl_res_conv": s_glr
                })
                st.success(f"🎉 Configuration updated successfully for entity: {s_name.strip()}")
                st.rerun()

    if ext_results:
        st.markdown("### 📋 Active External Suppliers Procurement Manifest")
        df_ext = pd.DataFrame(ext_results)
        st.dataframe(
            df_ext[["name", "feed", "rgl_out", "feed_cost", "cm", "cm_usd"]].rename(columns={
                "name": "Supplier Profile Name", "feed": "Input Volume Feed (MT)", "rgl_out": "Production Output (MT)",
                "feed_cost": "Total Capital Cost (THB)", "cm": "CM (THB/kg)", "cm_usd": "CM (USD/MT)"
            }).style.format({
                "Input Volume Feed (MT)": "{:.1f}", "Production Output (MT)": "{:.1f}", 
                "Total Capital Cost (THB)": "{:,.2f}", "CM (THB/kg)": "{:.3f}", "CM (USD/MT)": "{:.2f}"
            }), use_container_width=True
        )
        if st.button("🗑️ Clear All Operational Procurement Records"):
            st.session_state.suppliers = []
            st.rerun()

with tab2:
    st.markdown('<div class="section-container">📊 Summary & Break-Even Optimization Analysis</div>', unsafe_allow_html=True)
    avg_ext_cm_usd = overall_cm_usd
    avg_ext_cm_thb = overall_cm_thb
    
    if avg_ext_cm_usd < 60:
        card_bg = "#FEE2E2"; card_border = "#EF4444"; card_text = "#991B1B"
        status_lbl = "🚨 Status: Current Setup Margin Below Critical Safety Threshold (Action Required)"
    elif avg_ext_cm_usd > 120:
        card_bg = "#DCFCE7"; card_border = "#22C55E"; card_text = "#166534"
        status_lbl = "🟢 Status: Current Setup Margin Achieving Optimal Target Performance"
    else:
        card_bg = "#EFF6FF"; card_border = "#3B82F6"; card_text = "#1E40AF"
        status_lbl = "🟡 Status: Current Setup Margin within Stable / Warning Range"
        
    st.markdown(f"""
        <div style="background-color: {card_bg}; border: 3px solid {card_border}; padding: 25px; border-radius: 12px; margin-bottom: 25px;">
            <p style="color: {card_text}; margin: 0px; font-size: 18px; font-weight: bold;">{status_lbl}</p>
            <h1 style="color: {card_text}; margin: 5px 0px 0px 0px; font-size: 46px;">{avg_ext_cm_usd:,.2f} <span style="font-size: 24px;">USD/MT</span></h1>
            <p style="color: {card_text}; margin: 0px; font-size: 18px;">Weighted Contribution Margin across elements: <b>{avg_ext_cm_thb:,.3f} THB/kg</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📈 Financial Component Breakdown (Current Setup)")
    met_col1, met_col2, met_col3, met_col4 = st.columns(4)
    with met_col1:
        st.markdown(f"""<div style="background-color: #F8FAFC; padding: 18px; border-radius: 10px; border: 1px solid #CBD5E1; text-align: center;">
            <p style="margin:0; font-size:15px; color:#475569; font-weight: 700;">1. Product to Feedstock (P2F)</p>
            <h3 style="margin:8px 0; color:#0F172A; font-size:24px; font-weight:bold;">{p2f_usd_mt:,.2f} USD/MT</h3>
            <p style="margin:0; color:#64748B; font-size:15px;">{p2f_thb_kg:,.3f} THB/kg</p></div>""", unsafe_allow_html=True)
    with met_col2:
        st.markdown(f"""<div style="background-color: #F8FAFC; padding: 18px; border-radius: 10px; border: 1px solid #CBD5E1; text-align: center;">
            <p style="margin:0; font-size:15px; color:#475569; font-weight: 700;">2. Variable Cost incl. OVC (VC)</p>
            <h3 style="margin:8px 0; color:#DC2626; font-size:24px; font-weight:bold;">{vc_usd_mt:,.2f} USD/MT</h3>
            <p style="margin:0; color:#991B1B; font-size:15px;">{vc_thb_kg:,.3f} THB/kg</p></div>""", unsafe_allow_html=True)
    with met_col3:
        st.markdown(f"""<div style="background-color: #F8FAFC; padding: 18px; border-radius: 10px; border: 1px solid #CBD5E1; text-align: center;">
            <p style="margin:0; font-size:15px; color:#475569; font-weight: 700;">3. By-product Credit</p>
            <h3 style="margin:8px 0; color:#16A34A; font-size:24px; font-weight:bold;">{bp_usd_mt:,.2f} USD/MT</h3>
            <p style="margin:0; color:#166534; font-size:15px;">{bp_thb_kg:,.3f} THB/kg</p></div>""", unsafe_allow_html=True)
    with met_col4:
        st.markdown(f"""<div style="background-color: #EFF6FF; padding: 18px; border-radius: 10px; border: 2px solid #3B82F6; text-align: center;">
            <p style="margin:0; font-size:15px; color:#1E40AF; font-weight: 700;">4. Contribution Margin (CM)</p>
            <h3 style="margin:8px 0; color:#1E3A8A; font-size:24px; font-weight:bold;">{overall_cm_usd:,.2f} USD/MT</h3>
            <p style="margin:0; color:#2563EB; font-size:15px; font-weight:600;">{overall_cm_thb:,.3f} THB/kg</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔄 Cross-Operational Model Comparison Matrix")
    comparison_data = {
        "Key Financial Indicator Model": ["Yield  (CGL ➔ RGL)", "Maximum Break-Even External CGL Purchase Price Limit", "Logistics Cost", "Variable Costs ", "By-product Credits ", "Contribution Margin (CM)"],
        "ME2 Setup": [f"{weighted_conv_rate * 100:.2f}%", f"{be_cgl_purchase_price_thb:,.2f} THB/kg", "0.00 USD/MT", f"{vc_usd_mt:,.2f} USD/MT", f"{bp_usd_mt:,.2f} USD/MT", f"{overall_cm_usd:,.2f} USD/MT"],
        "ME1 Setup": [f"{0.75500 * 100:.2f}%", f"{be_rayong_cgl_purchase_price_thb:,.2f} THB/kg", f"{ovc_ext_usd_mt_rgl12:,.2f} USD/MT CGL", f"{rayong_vc_usd_mt_rgl:,.2f} USD/MT", f"{rayong_bp_usd_mt_rgl:,.2f} USD/MT", f"{rayong_overall_cm_usd:,.2f} USD/MT"]
    }
    st.table(pd.DataFrame(comparison_data).set_index("Key Financial Indicator Model"))

    st.markdown("---")
    st.markdown("### 📥 Management Performance Report Export")
    
    def generate_pdf():
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        story = []
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=12, textColor=colors.HexColor('#1E293B'))
        h2_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=12, spaceBefore=14, spaceAfter=8, textColor=colors.HexColor('#0F172A'))
        body_style = ParagraphStyle('ReportBody', parent=styles['Normal'], fontSize=10, spaceBefore=4, spaceAfter=4, leading=14)
        
        story.append(Paragraph("<b>PERFORMANCE REPORT: RGL PROCUREMENT SPECIFICATION MODEL</b>", title_style))
        story.append(Paragraph(f"<b>Report Generation Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("1. Core Performance Report Indicators", h2_style))
        supplier_names_str = ", ".join([r['name'] for r in ext_results])
        
        metrics_summary_data = [
            ["Key Parameter Indicator Model", "Calculated Performance Value System"],
            ["RGL Benchmark Target Price Valuation", f"{rgl_p_usd:,.2f} USD/MT"],
            ["Active Supplier Profiles Analyzed", supplier_names_str],
            ["ME2 Break-Even Purchase Price", f"{be_cgl_purchase_price_thb:,.2f} THB/kg"],
            ["ME1 Break-Even Purchase Price", f"{be_rayong_cgl_purchase_price_thb:,.2f} THB/kg"]
        ]
        t_metrics = Table(metrics_summary_data, colWidths=[240, 260])
        t_metrics.setStyle(TableStyle([('BACKGROUND', (0,0), (1,0), colors.HexColor('#1E293B')), ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1'))]))
        story.append(t_metrics)
        story.append(Spacer(1, 12))

        story.append(Paragraph("3. Target Margin Sensitivity Analysis (Required CGL Purchase Price Limits)", h2_style))
        sens_data = [
            ["Target RGL CM", "ME2 Setup CGL Price", "ME1 Setup CGL Price", "Risk Assessment Tier"],
            ["150.00 USD/MT", f"{calc_sens_cgl_current(150):,.2f} THB/kg", f"{calc_sens_cgl_rayong(150):,.2f} THB/kg", "Premium Target Window"],
            ["120.00 USD/MT", f"{calc_sens_cgl_current(120):,.2f} THB/kg", f"{calc_sens_cgl_rayong(120):,.2f} THB/kg", "Optimal Target Boundary"],
            ["90.00 USD/MT", f"{calc_sens_cgl_current(90):,.2f} THB/kg", f"{calc_sens_cgl_rayong(90):,.2f} THB/kg", "Acceptable Window"],
            ["60.00 USD/MT", f"{calc_sens_cgl_current(60):,.2f} THB/kg", f"{calc_sens_cgl_rayong(60):,.2f} THB/kg", "Critical Safety Floor"],
            ["0.00 USD/MT", f"{calc_sens_cgl_current(0):,.2f} THB/kg", f"{calc_sens_cgl_rayong(0):,.2f} THB/kg", "Break-Even Limit"]
        ]
        t_sens = Table(sens_data, colWidths=[110, 135, 135, 120])
        t_sens.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#475569')), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1'))]))
        story.append(t_sens)

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    if len(ext_results) > 0:
        pdf_data = generate_pdf()
        st.download_button(label="📥 Download Executive Summary Report (PDF)", data=pdf_data, file_name="RGL_Procurement_Report.pdf", mime="application/pdf", use_container_width=True)

with tab3:
    st.markdown('<div class="section-container">3. Raw Material Purchase Sensitivity Validation Graph Evaluation</div>', unsafe_allow_html=True)
    if total_ext_rgl > 0 and total_rayong_rgl > 0:
        current_avg_cgl_p = sum(s["price"] * s["qty"] for s in st.session_state.suppliers) / total_ext_feed
        cgl_prices = np.linspace(max(0, current_avg_cgl_p - 6), current_avg_cgl_p + 6, 100)
        
        cm_usd_current = []
        cm_usd_rayong = []
        for cp in cgl_prices:
            total_cost_thb = (total_ext_feed * cp * 1000) + tot_ext_fixed_costs
            revenue_thb = total_ext_rgl * rgl_p_thb * 1000
            cm_thb_kg = (revenue_thb - total_cost_thb) / (total_ext_rgl * 1000)
            cm_usd_current.append(cm_thb_kg * 1000 / fx)
            
            feed_cost_usd_rayong = total_rayong_feed * ((cp * 1000) / fx)
            net_cost_usd_rayong = feed_cost_usd_rayong + tot_rayong_logistics_usd + tot_rayong_vc_usd - tot_rayong_bp_usd
            rev_usd_rayong = total_rayong_rgl * rgl_p_usd
            cm_usd_r_mt = (rev_usd_rayong - net_cost_usd_rayong) / total_rayong_rgl
            cm_usd_rayong.append(cm_usd_r_mt)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cgl_prices, y=cm_usd_current, mode='lines', name='Current Setup CM Curve', line=dict(color='#2563EB', width=4)))
        fig.add_trace(go.Scatter(x=cgl_prices, y=cm_usd_rayong, mode='lines', name='Rayong Setup CM Curve', line=dict(color='#9333EA', width=4, dash='dash')))
        fig.add_hline(y=60, line_dash="dot", line_color="#EF4444", opacity=0.5, annotation_text="Critical Margin Floor (60 USD)")
        fig.add_hline(y=120, line_dash="dot", line_color="#22C55E", opacity=0.5, annotation_text="Optimal Target Window (120 USD)")
        fig.add_hline(y=0, line_color="#000000", line_width=1.5)
        
        fig.update_layout(title="Comparative Price Sensitivity Mapping", xaxis_title="External CGL Purchase Price (THB/kg)", yaxis_title="Simulated CM (USD/MT Finished RGL)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown('<div class="section-container">📑 Step 4: Audit Trail & Granular Calculation Details</div>', unsafe_allow_html=True)
    if st.session_state.suppliers:
        _RAYONG_CONV = 0.75500
        _LOGISTICS_USD_MT_CGL = ovc_ext_usd_mt_rgl12
        _OVC_USD_MT_RGL = ovc_ext_usd_mt_rgl1

        current_rows = []
        for s in st.session_state.suppliers:
            feed = s["qty"]
            if feed <= 0: continue

            feed_cost_thb = feed * s["price"] * 1000
            total_chem_thb = (feed * s["naoh"] * naoh_p) + (feed * s["fac"] * fac_p_usd * fx / 1000) + (feed * s["rac"] * rac_p_usd * fx / 1000)
            total_util_thb = (feed * s["elec"] * elec_p) + (feed * s["water"] * water_p) + (feed * s["fuel"] * fuel_p / 72) + (feed * s["n2"] * n2_p) + (feed * s["biogas"] * biogas_p) + (feed * s.get("ds", 0.0) * ds_p)
            total_bp_thb = (feed * (s["ygl_conv"] / 100) * ygl_p_usd * fx) + (feed * (s["gl_res_conv"] / 100) * gl_res_p_usd * fx)

            rgl_output_mt = feed * s["conv"]
            gr_sl = feed - rgl_output_mt - feed * (s["ygl_conv"] / 100) - feed * (s["gl_res_conv"] / 100)
            dis_cost = gr_sl * 2950
            ovc_cost_thb = rgl_output_mt * ovc_ext_usd_mt_rgl2 * fx

            total_capital_cost_thb = feed_cost_thb + total_chem_thb + total_util_thb + ovc_cost_thb + dis_cost - total_bp_thb
            total_revenue_thb = rgl_p_thb * rgl_output_mt * 1000

            cm_thb_kg = (total_revenue_thb - total_capital_cost_thb) / (rgl_output_mt * 1000) if rgl_output_mt > 0 else 0.0
            cm_usd_mt = cm_thb_kg * 1000 / fx if rgl_output_mt > 0 else 0.0

            current_rows.append({
                "Supplier Name": s["name"], "Feed Quantity (MT)": feed, "Feed Price (THB/kg)": s["price"],
                "Total Feed Cost (THB)": feed_cost_thb, "Total Chemical Cost (THB)": total_chem_thb,
                "Total Utility Cost (THB)": total_util_thb, "Disposal Cost (THB)": dis_cost,
                "Total By-Product Credit (THB)": total_bp_thb, "RGL Output (MT)": rgl_output_mt,
                "OVC Cost (THB)": ovc_cost_thb, "Total Capital Cost (THB)": total_capital_cost_thb,
                "Contribution Margin (USD/MT)": cm_usd_mt
            })

        st.dataframe(pd.DataFrame(current_rows), use_container_width=True)
