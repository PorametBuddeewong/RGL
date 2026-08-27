import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(layout="wide", page_title="Factory Operational Model")

# --- Custom CSS for Layout ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { min-width: 22%; max-width: 22%; }
    .main-title { font-size: 26px; font-weight: bold; color: #1E3D59; border-bottom: 2px solid #1E3D59; padding-bottom: 10px; }
    .unit-header { background-color: #2c3e50; color: white; padding: 10px; border-radius: 5px; font-weight: bold; margin-top: 25px; margin-bottom: 10px; }
    .sub-section { color: #2980b9; font-weight: bold; margin-top: 15px; border-left: 4px solid #2980b9; padding-left: 10px; }
    .dataframe-container { margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (20-22%) ---
with st.sidebar:
    st.title("⚙️ Variables Input")
    
    with st.expander("💰 หมวดราคา (Price)", expanded=True):
        st.subheader("Product Price")
        me_p = st.number_input("ME Price (THB/kg)", value=37.17)
        rgl_p = st.number_input("RGL Price (THB/kg)", value=35.00)
        
        st.subheader("By-Product Price")
        me_res_p = st.number_input("ME Residue Price (THB/kg)", value=16.69)
        cgl_p_in = st.number_input("CGL Price (THB/kg)", value=20.56)
        fa_p = st.number_input("Fatty acid Price (THB/kg)", value=9.38)
        ygl_p_usd = st.number_input("YGL Price (USD/MT)", value=643.0)
        gl_res_p_usd = st.number_input("GL Residue Price (USD/MT)", value=31.98)
        
        st.subheader("Raw Material Price")
        cpo_a_p = st.number_input("CPO A Price (THB/kg)", value=35.00)
        cpo_b_p = st.number_input("CPO B Price (THB/kg)", value=32.83)
        pfad_p = st.number_input("PFAD Price (THB/kg)", value=31.57)
        ps_p = st.number_input("PS Price (THB/kg)", value=35.31)
        meoh_p = st.number_input("MeOH Price (THB/kg)", value=9.98)
        
        st.subheader("Chemical Price")
        h3po4_p = st.number_input("Phosphoric acid (THB/kg)", value=41.0)
        clay_p = st.number_input("Bleaching clay (THB/kg)", value=7.25)
        na_meth_p = st.number_input("Na-Methylate (THB/kg)", value=20.49)
        naoh_p = st.number_input("NaOH (THB/kg)", value=9.68)
        hcl_p = st.number_input("HCL (THB/kg)", value=1.37)
        bht_p = st.number_input("BHT (THB/kg)", value=160.0)
        fac_p_usd = st.number_input("Fresh Activated Carbon (USD/MT)", value=4730.46)
        rac_p_usd = st.number_input("Regen Activated Carbon (USD/MT)", value=1216.0)
        rgl_chem_p = st.number_input("RGL Chem (THB/kg)", value=30.26)
        
        st.subheader("Utility Price")
        elec_p = st.number_input("Electricity (THB/unit)", value=3.51)
        water_p = st.number_input("Clarified Water (THB/unit)", value=25.0)
        fuel_p = st.number_input("Fuel Oil (THB/Ton)", value=14514.0)
        biogas_p = st.number_input("Bio gas (THB/m3)", value=6.41)
        n2_p = st.number_input("Nitrogen (THB/m3)", value=6.18)
        
        fx = st.number_input("Fx (THB/USD)", value=31.25)

    with st.expander("📈 หมวด Conversion rate"):
        c_rpo = st.number_input("conv to RPO rate", value=1.004016, format="%.6f")
        c_me = st.number_input("conv to ME rate", value=0.9693, format="%.4f")
        c_me_res = st.number_input("conv to ME Residue rate", value=0.0194, format="%.4f")
        c_fa = st.number_input("conv to Fatty acid rate", value=0.0043, format="%.4f")
        c_cgl = st.number_input("conv to CGL rate", value=0.1299, format="%.4f")
        c_rgl_yield = st.number_input("conv to RGL rate", value=0.86, format="%.2f")

    with st.expander("🛡️ หมวด Constraint"):
        ffa_limit = st.number_input("FFA mix feed (%)", value=10.0)
        max_pre_cap_val = st.number_input("max cap pretreatment (MT/day)", value=0.91*600)
        cpo_b_pct = st.slider("%CPO B", 0.0, 40.0, 40.0) / 100
        pfad_ex_pct = st.slider("%PFAD Extra", 0.0, 2.0, 2.0) / 100
        max_me_cap_val = st.number_input("max cap ME (MT/day)", value=600.0)
        ps_pct_max = st.slider("Max %PS limit", 10.0, 30.0, 30.0) / 100
        ps_supply_weekly = st.number_input("PS Supply (MT/week)", value=1500.0)
        
    # --- NEW: หมวด Consumption ---
    with st.expander("🧪 หมวด Consumption (kg/kg feed)"):
        st.subheader("Pretreatment Unit")
        cons_rgl_chem = st.number_input("RGL Consumption", value=0.0259, format="%.4f")
        cons_h3po4_a = st.number_input("H3PO4 (CPO A/PFAD)", value=0.0008, format="%.4f")
        cons_h3po4_b = st.number_input("H3PO4 (CPO B)", value=0.0010, format="%.4f")
        cons_clay_a = st.number_input("Bleaching clay (CPO A/PFAD)", value=0.0076, format="%.4f")
        cons_clay_b = st.number_input("Bleaching clay (CPO B)", value=0.0121, format="%.4f")
        
        st.subheader("ME Unit")
        cons_meoh = st.number_input("Methanol Consumption", value=0.1090, format="%.4f")
        cons_na_meth = st.number_input("Na-Methylate Consumption", value=0.0110, format="%.4f")
        cons_naoh_me = st.number_input("NaOH Consumption (ME)", value=0.0004, format="%.4f")
        cons_hcl = st.number_input("HCL Consumption", value=0.0066, format="%.4f")
        cons_bht = st.number_input("BHT Consumption", value=0.00005, format="%.5f")
        
        st.subheader("RGL Unit")
        cons_naoh_rgl = st.number_input("NaOH Consumption (RGL)", value=0.0012, format="%.4f")
        cons_fac = st.number_input("Fresh Activated Carbon Consumption", value=0.0005, format="%.4f")
        cons_rac = st.number_input("Regen Activated Carbon Consumption", value=0.0019, format="%.4f")

# --- CALCULATION ENGINE ---

# 1. Base Targets
me_production = max_me_cap_val
me_total_feed = me_production / c_me

# --------------------------------------------------------------------------------
# --- DECISION LOGIC: PS vs RPO ---
# --------------------------------------------------------------------------------
rem_ratio = 1.0 - cpo_b_pct - pfad_ex_pct
target_ffa = ffa_limit
rhs = (target_ffa * (1.0 - pfad_ex_pct)) - (10.0 * cpo_b_pct)
pfad_ratio = (rhs - (5.0 * rem_ratio)) / (80.0 - 5.0)
if pfad_ratio < 0: pfad_ratio = 0
cpo_a_ratio = rem_ratio - pfad_ratio

mock_rpo_demand = max_pre_cap_val
mock_pre_feed = mock_rpo_demand * c_rpo
mock_cpo_a = mock_pre_feed * cpo_a_ratio
mock_cpo_b = mock_pre_feed * cpo_b_pct
mock_pfad = mock_pre_feed * pfad_ratio
mock_pfad_ex = mock_pre_feed * pfad_ex_pct

mock_fs_cost = (mock_cpo_a*cpo_a_p + mock_cpo_b*cpo_b_p + mock_pfad*pfad_p + mock_pfad_ex*pfad_p) * 1000

# Using dynamic consumption variables for Mock Pretreatment
mock_chem_cost = (mock_pre_feed * cons_rgl_chem * rgl_chem_p * 1000) + \
                 ((cons_h3po4_a*mock_cpo_a + cons_h3po4_b*mock_cpo_b + cons_h3po4_a*mock_pfad) * h3po4_p * 1000) + \
                 ((cons_clay_a*mock_cpo_a + cons_clay_b*mock_cpo_b + cons_clay_a*mock_pfad) * clay_p * 1000)

mock_util_cost = (35.118 * (100**-0.892) * elec_p * mock_rpo_demand) + \
                 (0.2814 * (100**-0.673) * water_p * mock_rpo_demand) + \
                 (2.7718 * fuel_p) + \
                 (0.1667 * mock_pre_feed * n2_p) + \
                 (31.6348 * mock_pre_feed * biogas_p)

mock_rpo_cost_kg = (mock_fs_cost + mock_chem_cost + mock_util_cost) / (mock_rpo_demand * 1000)

max_ps_allowed = min(me_total_feed * ps_pct_max, ps_supply_weekly / 7.0)

# เทียบราคาเพื่อกำหนดสัดส่วน
if mock_rpo_cost_kg <= ps_p:
    rpo_demand = min(me_total_feed, max_pre_cap_val)
    ps_qty = me_total_feed - rpo_demand
else:
    ps_qty = max_ps_allowed
    rpo_demand = me_total_feed - ps_qty
    if rpo_demand > max_pre_cap_val:
        rpo_demand = max_pre_cap_val
        ps_qty = me_total_feed - rpo_demand

# --------------------------------------------------------------------------------
# 2. Pretreatment Unit Calculation (Actual)
# --------------------------------------------------------------------------------
pre_total_feed = rpo_demand * c_rpo
q_cpo_a = pre_total_feed * cpo_a_ratio
q_cpo_b = pre_total_feed * cpo_b_pct
q_pfad = pre_total_feed * pfad_ratio
q_pfad_ex = pre_total_feed * pfad_ex_pct

# --- DataFrames for Pretreatment ---
df_pre_fs = pd.DataFrame({
    "Feed Type": ["CPO A", "CPO B", "PFAD", "PFAD Extra", "TOTAL"],
    "Ratio (%)": [cpo_a_ratio*100, cpo_b_pct*100, pfad_ratio*100, pfad_ex_pct*100, 100.0],
    "MT/Day": [q_cpo_a, q_cpo_b, q_pfad, q_pfad_ex, pre_total_feed],
    "Cost (kTHB)": [(q_cpo_a*cpo_a_p), (q_cpo_b*cpo_b_p), (q_pfad*pfad_p), (q_pfad_ex*pfad_p), 0] 
})
fs_cost_pre = df_pre_fs["Cost (kTHB)"].iloc[:-1].sum() * 1000
df_pre_fs.loc[4, "Cost (kTHB)"] = fs_cost_pre / 1000

# Using dynamic consumption variables
df_pre_chem = pd.DataFrame({
    "Chemical Item": ["RGL Chem", "Phosphoric acid (H3PO4)", "Bleaching clay", "TOTAL"],
    "Qty Usage": [
        pre_total_feed * cons_rgl_chem * 1000, 
        (cons_h3po4_a*q_cpo_a + cons_h3po4_b*q_cpo_b + cons_h3po4_a*q_pfad) * 1000, 
        (cons_clay_a*q_cpo_a + cons_clay_b*q_cpo_b + cons_clay_a*q_pfad) * 1000, 
        0
    ],
    "Unit": ["kg", "kg", "kg", "kg"],
    "Cost (kTHB)": [
        (pre_total_feed * cons_rgl_chem * rgl_chem_p * 1000) / 1000,
        ((cons_h3po4_a*q_cpo_a + cons_h3po4_b*q_cpo_b + cons_h3po4_a*q_pfad) * h3po4_p * 1000) / 1000,
        ((cons_clay_a*q_cpo_a + cons_clay_b*q_cpo_b + cons_clay_a*q_pfad) * clay_p * 1000) / 1000,
        0
    ]
})
df_pre_chem.loc[3, "Qty Usage"] = df_pre_chem["Qty Usage"].iloc[:-1].sum()
chem_cost_pre = df_pre_chem["Cost (kTHB)"].iloc[:-1].sum() * 1000
df_pre_chem.loc[3, "Cost (kTHB)"] = chem_cost_pre / 1000

pre_util_pct = (rpo_demand / 600) * 100
df_pre_util = pd.DataFrame({
    "Utility Item": ["Electricity", "Water", "Fuel Oil", "Nitrogen", "Biogas", "TOTAL"],
    "Cost (kTHB)": [
        (35.118 * (pre_util_pct**-0.892) * elec_p * rpo_demand) / 1000,
        (0.2814 * (pre_util_pct**-0.673) * water_p * rpo_demand) / 1000,
        (2.7718 * fuel_p) / 1000,
        (0.1667 * pre_total_feed * n2_p) / 1000,
        (31.6348 * pre_total_feed * biogas_p) / 1000,
        0
    ]
})
util_cost_pre = df_pre_util["Cost (kTHB)"].iloc[:-1].sum() * 1000
df_pre_util.loc[5, "Cost (kTHB)"] = util_cost_pre / 1000

rpo_cost_kg = (fs_cost_pre + chem_cost_pre + util_cost_pre) / (rpo_demand * 1000)

# --------------------------------------------------------------------------------
# 3. ME Unit Calculation
# --------------------------------------------------------------------------------
df_me_fs = pd.DataFrame({
    "Feed Type": ["RPO", "Palm Stearin (PS)", "TOTAL"],
    "Ratio (%)": [rpo_demand/me_total_feed*100, ps_qty/me_total_feed*100, 100],
    "MT/Day": [rpo_demand, ps_qty, me_total_feed],
    "Cost (kTHB)": [(rpo_demand * rpo_cost_kg), (ps_qty * ps_p), 0]
})
fs_cost_me = df_me_fs["Cost (kTHB)"].iloc[:-1].sum() * 1000
df_me_fs.loc[2, "Cost (kTHB)"] = fs_cost_me / 1000

# Using dynamic consumption variables for ME
df_me_chem = pd.DataFrame({
    "Chemical Item": ["MeOH", "Na-Methylate", "NaOH", "HCL", "BHT", "TOTAL"],
    "Qty (kg)": [
        cons_meoh * me_total_feed * 1000, 
        cons_na_meth * me_total_feed * 1000, 
        cons_naoh_me * me_total_feed * 1000, 
        cons_hcl * me_total_feed * 1000, 
        cons_bht * me_total_feed * 1000, 
        0
    ],
    "Cost (kTHB)": [
        (cons_meoh * me_total_feed * 1000 * meoh_p) / 1000,
        (cons_na_meth * me_total_feed * 1000 * na_meth_p) / 1000,
        (cons_naoh_me * me_total_feed * 1000 * naoh_p) / 1000,
        (cons_hcl * me_total_feed * 1000 * hcl_p) / 1000,
        (cons_bht * me_total_feed * 1000 * bht_p) / 1000,
        0
    ]
})
df_me_chem.loc[5, "Qty (kg)"] = df_me_chem["Qty (kg)"].iloc[:-1].sum()
chem_cost_me = df_me_chem["Cost (kTHB)"].iloc[:-1].sum() * 1000
df_me_chem.loc[5, "Cost (kTHB)"] = chem_cost_me / 1000

me_util_pct = (me_production / max_me_cap_val) * 100
df_me_util = pd.DataFrame({
    "Utility Item": ["Electricity", "Water", "Fuel Oil", "Nitrogen", "Biogas", "TOTAL"],
    "Cost (kTHB)": [
        (35.85 * (me_util_pct**-0.768) * elec_p * me_total_feed) / 1000,
        (0.6255 * (me_util_pct**-0.688) * water_p * me_total_feed) / 1000,
        (2.171 * fuel_p) / 1000,
        (1.5693 * me_total_feed * n2_p) / 1000,
        (31.4548 * me_total_feed * biogas_p) / 1000,
        0
    ]
})
util_cost_me = df_me_util["Cost (kTHB)"].iloc[:-1].sum() * 1000
df_me_util.loc[5, "Cost (kTHB)"] = util_cost_me / 1000

df_me_bp = pd.DataFrame({
    "By-Product": ["ME Residue", "Fatty Acid", "CGL", "TOTAL"],
    "Qty (MT)": [c_me_res * me_total_feed, c_fa * me_total_feed, c_cgl * me_total_feed, 0],
    "Credit (kTHB)": [
        (c_me_res * me_total_feed * me_res_p),
        (c_fa * me_total_feed * fa_p),
        (c_cgl * me_total_feed * cgl_p_in),
        0
    ]
})
df_me_bp.loc[3, "Qty (MT)"] = df_me_bp["Qty (MT)"].iloc[:-1].sum()
bp_credit_me = df_me_bp["Credit (kTHB)"].iloc[:-1].sum() * 1000
df_me_bp.loc[3, "Credit (kTHB)"] = bp_credit_me / 1000

me_fs_kg = (fs_cost_me + (cons_meoh * meoh_p * me_total_feed * 1000)) / (me_production * 1000)
me_var_kg = (chem_cost_me - (cons_meoh*meoh_p*me_total_feed*1000) + util_cost_me) / (me_production * 1000)
me_bp_kg = bp_credit_me / (me_production * 1000)
me_p2f = me_p - me_fs_kg
me_cm = me_p2f - me_var_kg - 0.39276587 + me_bp_kg

# --------------------------------------------------------------------------------
# 4. RGL Unit Calculation
# --------------------------------------------------------------------------------
rgl_feed = c_cgl * me_total_feed
rgl_prod = rgl_feed * c_rgl_yield
fs_cost_rgl = rgl_feed * cgl_p_in * 1000

# Using dynamic consumption variables for RGL
df_rgl_chem = pd.DataFrame({
    "Chemical Item": ["NaOH", "Fresh Activated Carbon", "Regen Activated Carbon", "TOTAL"],
    "Qty (kg)": [
        cons_naoh_rgl * rgl_feed * 1000,
        cons_fac * rgl_feed * 1000,
        cons_rac * rgl_feed * 1000,
        0
    ],
    "Cost (kTHB)": [
        (cons_naoh_rgl * naoh_p * rgl_feed * 1000) / 1000,
        (cons_fac * (fac_p_usd * fx / 1000) * rgl_feed * 1000) / 1000,
        (cons_rac * (rac_p_usd * fx / 1000) * rgl_feed * 1000) / 1000,
        0
    ]
})
df_rgl_chem.loc[3, "Qty (kg)"] = df_rgl_chem["Qty (kg)"].iloc[:-1].sum()
chem_cost_rgl = df_rgl_chem["Cost (kTHB)"].iloc[:-1].sum() * 1000
df_rgl_chem.loc[3, "Cost (kTHB)"] = chem_cost_rgl / 1000

df_rgl_util = pd.DataFrame({
    "Utility Item": ["Electricity", "Water", "Fuel Oil", "Nitrogen", "Biogas", "TOTAL"],
    "Cost (kTHB)": [
        (122.023 * elec_p * rgl_feed) / 1000,
        (3.93 * water_p * rgl_feed) / 1000,
        (1.4037 * fuel_p) / 1000,
        (1.516 * n2_p * rgl_feed) / 1000,
        (109.43 * biogas_p * rgl_feed) / 1000,
        0
    ]
})
util_cost_rgl = df_rgl_util["Cost (kTHB)"].iloc[:-1].sum() * 1000
df_rgl_util.loc[5, "Cost (kTHB)"] = util_cost_rgl / 1000

ygl_credit = (0.01 * rgl_feed * (ygl_p_usd * fx / 1000) * 1000) 
gl_res_credit = (0.039 * rgl_feed * (gl_res_p_usd * fx / 1000) * 1000)
bp_credit_rgl = ygl_credit + gl_res_credit

df_rgl_bp = pd.DataFrame({
    "By-Product": ["Yellow Gly", "GL Residue", "TOTAL"],
    "Qty (MT)": [0.01 * rgl_feed, 0.039 * rgl_feed, 0],
    "Credit (kTHB)": [ygl_credit / 1000, gl_res_credit / 1000, bp_credit_rgl / 1000]
})
df_rgl_bp.loc[2, "Qty (MT)"] = df_rgl_bp["Qty (MT)"].iloc[:-1].sum()

waste_rgl = rgl_feed - rgl_prod - (0.01 * rgl_feed) - (0.039 * rgl_feed)
disposal_cost_rgl = waste_rgl * 2.950

rgl_fs_kg = fs_cost_rgl / (rgl_prod * 1000)
rgl_var_kg = (chem_cost_rgl + util_cost_rgl + (disposal_cost_rgl * 1000)) / (rgl_prod * 1000)
rgl_bp_kg = bp_credit_rgl / (rgl_prod * 1000)
rgl_p2f = rgl_p - rgl_fs_kg
rgl_cm = rgl_p2f - rgl_var_kg + rgl_bp_kg

# --- MAIN DISPLAY (80%) ---
st.markdown('<p class="main-title">🏭 Factory Scenario Analysis Dashboard</p>', unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# 1. Pretreatment Unit Result
# --------------------------------------------------------------------------------
st.markdown('<div class="unit-header">1. Pretreatment Unit Analysis</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Utilization", f"{pre_util_pct:.2f}%")
col2.metric("RPO Feed Stock Cost", f"{fs_cost_pre/rpo_demand/1000:.3f}", help="THB/kg")
col3.metric("RPO Variable Cost", f"{(chem_cost_pre + util_cost_pre)/(rpo_demand*1000):.3f}", help="THB/kg")
col4.metric("RPO Prod Cost", f"{rpo_cost_kg:.3f}", help="THB/kg")

st.markdown('<p class="sub-section">Data Breakdown (Pretreatment)</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Feedstock**")
    st.dataframe(df_pre_fs.style.format({"Ratio (%)": "{:.2f}", "MT/Day": "{:.1f}", "Cost (kTHB)": "{:,.1f}"}), use_container_width=True)
with c2:
    st.markdown("**Chemicals Summary**")
    st.dataframe(df_pre_chem.style.format({"Qty Usage": "{:,.2f}", "Cost (kTHB)": "{:,.1f}"}), use_container_width=True)

# --- EXPANDER รายละเอียดการคำนวณ Pretreatment ---
with st.expander("🔍 ดูรายละเอียดการคำนวณ (Cost Breakdown - Pretreatment)"):
    col_u, col_c = st.columns(2)

    with col_u:
        st.markdown("**Utility Cost Itemized**")
        st.dataframe(df_pre_util.style.format({"Cost (kTHB)": "{:,.2f}"}), use_container_width=True)
    with col_c:
        st.markdown("**RPO Cost Breakdown**")
        df_pre_cost = pd.DataFrame({
    "Item": ["RPO Production","Feed Stock Cost", "Chemical Cost", "Utility Cost", "TOTAL"],
    "Qty": [
        rpo_demand, 
        fs_cost_pre/rpo_demand/1000, 
        chem_cost_pre/rpo_demand/1000, 
        util_cost_pre/rpo_demand/1000, 
        fs_cost_pre/rpo_demand/1000+chem_cost_pre/rpo_demand/1000+util_cost_pre/rpo_demand/1000, 
    ],
    "Unit": ["MT", "THB/Kg", "THB/Kg", "THB/Kg", "THB/Kg"],
})
        st.dataframe(df_pre_cost.style.format({"Qty": "{:,.3f}"}), use_container_width=True)


# --------------------------------------------------------------------------------
# 2. ME Unit Result
# --------------------------------------------------------------------------------
st.markdown('<div class="unit-header">2. ME (B100) Unit Analysis</div>', unsafe_allow_html=True)

if mock_rpo_cost_kg <= ps_p:
    st.info(f"💡 **Decision:** RPO Cost ({mock_rpo_cost_kg:.4f} THB/kg) <= PS Price ({ps_p:.4f} THB/kg) ➡️ **Maximize Pretreatment usage.**")
else:
    st.warning(f"💡 **Decision:** PS Price ({ps_p:.4f} THB/kg) < RPO Cost ({mock_rpo_cost_kg:.4f} THB/kg) ➡️ **Maximize PS usage (Limited by constraints).**")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Utilization", f"{me_util_pct:.2f}%")
col2.metric("ME Feed Cost", f"{me_fs_kg:.3f}", help="THB/kg")
col3.metric("P2F ME", f"{me_p2f:.3f}", help="THB/kg")
col4.metric("ME CM", f"{me_cm:.3f}", help="THB/kg")

st.markdown('<p class="sub-section">Data Breakdown (ME)</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Feedstock**")
    st.dataframe(df_me_fs.style.format({"Ratio (%)": "{:.2f}","MT/Day": "{:.2f}", "Cost (kTHB)": "{:,.1f}"}), use_container_width=True)
with c2:
    st.markdown("**By-Products Credit**")
    st.dataframe(df_me_bp.style.format({"Qty (MT)": "{:.2f}", "Credit (kTHB)": "{:,.1f}"}), use_container_width=True)

# --- EXPANDER รายละเอียดการคำนวณ ME ---
with st.expander("🔍 ดูรายละเอียดการคำนวณ (Cost Breakdown - ME)"):
    col_c, col_u = st.columns(2)
    with col_c:
        st.markdown("**Chemical Cost Itemized**")
        st.dataframe(df_me_chem.style.format({"Qty (kg)": "{:,.2f}", "Cost (kTHB)": "{:,.2f}"}), use_container_width=True)
    with col_u:
        st.markdown("**Utility Cost Itemized**")
        st.dataframe(df_me_util.style.format({"Cost (kTHB)": "{:,.2f}"}), use_container_width=True)

    col_me, = st.columns(1)
    with col_me:
        st.markdown("**ME Cost Breakdown**")
        df_ME_cost = pd.DataFrame({
    "Item": ["ME Production","ME Selling Price","Feed Stock Cost (inclde Methanol)", "P2F","Chemical Cost", "Utility Cost","Other Variable Cost","By-Product Credit", "TOTAL"],
    "Qty": [
        me_production,
        me_p, 
        me_fs_kg, 
        me_p2f,
        (chem_cost_me - (cons_meoh*meoh_p*me_total_feed*1000)) / (me_production * 1000), 
        util_cost_me / (me_production * 1000),
        0.39276587,
        me_bp_kg,
        me_cm,
    ],
    "Unit": ["MT","THB/Kg", "THB/Kg", "THB/Kg","THB/Kg", "THB/Kg", "THB/Kg", "THB/Kg", "THB/Kg"],
})
        st.dataframe(df_ME_cost.style.format({"Qty": "{:,.3f}"}), use_container_width=True)



# --------------------------------------------------------------------------------
# 3. RGL Unit Result
# --------------------------------------------------------------------------------
st.markdown('<div class="unit-header">3. RGL Unit Analysis</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("RGL Prod", f"{rgl_prod:.2f} MT")
col2.metric("RGL Price", f"{rgl_p:.2f}", help="THB/kg")
col3.metric("RGL P2F", f"{rgl_p2f:.3f}", help="THB/kg")
col4.metric("RGL CM", f"{rgl_cm:.3f}", help="THB/kg")

st.markdown('<p class="sub-section">Data Breakdown (RGL)</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Chemicals Summary**")
    st.dataframe(df_rgl_chem.style.format({"Qty (kg)": "{:,.2f}", "Cost (kTHB)": "{:,.1f}"}), use_container_width=True)
    
with c2:
    st.markdown("**By-Products Credit**")
    st.dataframe(df_rgl_bp.style.format({"Qty (MT)": "{:.2f}", "Credit (kTHB)": "{:,.1f}"}), use_container_width=True)

# --- EXPANDER รายละเอียดการคำนวณ RGL ---
with st.expander("🔍 ดูรายละเอียดการคำนวณ (Cost Breakdown - RGL)"):
    col_u, col_co = st.columns(2)

    with col_u:
        st.markdown("**Utility Cost Itemized**")
        st.dataframe(df_rgl_util.style.format({"Cost (kTHB)": "{:,.2f}"}), use_container_width=True)
    with col_co:
        st.markdown("**RGL Cost Breakdown**")
        df_pre_cost = pd.DataFrame({
    "Item": ["RGL Selling Price","FeedStock Cost","P2F", "Chemical Cost", "Utility Cost", "Disposal Cost", "By-Product Credit", "CM RGL"],
    "Qty (THB/Kg)": [
        rgl_p, 
        rgl_fs_kg, 
        rgl_p2f, 
        (chem_cost_rgl) / (rgl_prod * 1000),
        util_cost_rgl / (rgl_prod * 1000),
        (disposal_cost_rgl * 1000) / (rgl_prod * 1000),
        rgl_bp_kg,
        rgl_cm, 
    ],
    "Qty (USD/MT)": [
        rgl_p*fx, 
        rgl_fs_kg*fx, 
        rgl_p2f*fx, 
        (chem_cost_rgl) / (rgl_prod * 1000)*fx,
        util_cost_rgl / (rgl_prod * 1000)*fx,
        (disposal_cost_rgl * 1000) / (rgl_prod * 1000)*fx,
        rgl_bp_kg*fx,
        rgl_cm*fx, 
        ],
})
        st.dataframe(df_pre_cost.style.format({"Qty (THB/Kg)": "{:,.3f}", "Qty (USD/MT)": "{:,.1f}"}), use_container_width=True)


# --------------------------------------------------------------------------------
# 4. Total Summary
# --------------------------------------------------------------------------------
st.markdown('<div class="unit-header" style="background-color:#16a085;">4. Overall Performance</div>', unsafe_allow_html=True)
total_cm_val = me_cm + rgl_cm*rgl_prod/me_production
st.subheader(f"Total Contribution Margin: {total_cm_val:,.3f} THB/Kg", help="ME + RGL")
