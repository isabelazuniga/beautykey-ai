import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="BeautyKey | Retail Intelligence", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

# ---------- DESIGN SYSTEM ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
:root { --ink:#34202B; --wine:#63283F; --wine-deep:#431A2B; --rose:#B77C8B; --blush:#F3E6E5; --ivory:#FAF7F1; --paper:#FFFEFC; --muted:#82727A; --line:#E8DDD5; --gold:#B69A6A; --sage:#557B6C; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:var(--ivory); color:var(--ink); }
.block-container { max-width:1440px; padding-top:2rem; padding-bottom:3rem; }
[data-testid="stSidebar"] { background:#F1E7E0; border-right:1px solid #E1D2C9; }
[data-testid="stSidebar"] .block-container { padding-top:1.8rem; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 { color:var(--ink); }
h1,h2,h3 { color:var(--ink) !important; }
h1 { font-family:'Playfair Display',serif !important; font-weight:500 !important; font-size:2.8rem !important; letter-spacing:-1.2px !important; line-height:1.1 !important; }
h2 { font-family:'Playfair Display',serif !important; font-size:1.6rem !important; font-weight:500 !important; }
h3 { font-size:1.02rem !important; font-weight:700 !important; }
p, label, .stMarkdown { color:var(--ink); }
.bk-brand { display:flex; align-items:center; gap:12px; margin-bottom:12px; }
.bk-mark { width:44px; height:44px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#FBF6EF; background:var(--wine); font-size:23px; box-shadow:0 4px 12px #63283F20; }
.bk-wordmark { font-family:'Playfair Display',serif; font-size:27px; font-weight:500; color:var(--wine-deep); line-height:1; }
.bk-subbrand { color:var(--muted); font-size:9px; letter-spacing:2.1px; font-weight:700; margin-top:7px; }
.bk-eyebrow { font-size:10px; letter-spacing:2.3px; color:var(--wine); font-weight:700; text-transform:uppercase; }
.bk-hero { position:relative; overflow:hidden; background:linear-gradient(112deg,#F0E1DC 0%,#F8EFE8 52%,#E8D5D2 100%); border:1px solid #E4D2CB; border-radius:4px 24px 4px 24px; padding:34px 36px; margin:18px 0 24px 0; box-shadow:0 8px 28px rgba(67,26,43,.035); }
.bk-hero:after { content:'B'; position:absolute; right:42px; top:-55px; font-family:'Playfair Display',serif; font-size:240px; line-height:1; color:#63283F0B; pointer-events:none; }
.bk-hero-title { font-family:'Playfair Display',serif; font-size:35px; line-height:1.18; color:var(--wine-deep); margin:10px 0 10px 0; max-width:700px; }
.bk-hero-copy { color:#715D65; font-size:13px; max-width:720px; line-height:1.8; }
.bk-pill { display:inline-block; background:var(--wine); color:#FFF8F1; border-radius:2px; padding:7px 11px; font-size:9px; font-weight:700; letter-spacing:1.5px; }
.bk-card { background:var(--paper); border:1px solid var(--line); border-radius:3px 15px 3px 15px; padding:19px 20px; min-height:132px; box-shadow:0 5px 20px rgba(63,35,46,.025); border-top:3px solid #B77C8B; }
.bk-kpi-label { font-size:9px; letter-spacing:1.5px; font-weight:700; color:var(--muted); text-transform:uppercase; }
.bk-kpi-value { font-family:'Playfair Display',serif; font-size:31px; font-weight:500; letter-spacing:-.6px; color:var(--wine-deep); margin:12px 0 7px 0; }
.bk-kpi-note { font-size:11px; color:var(--muted); line-height:1.5; }
.bk-section { background:var(--paper); border:1px solid var(--line); border-radius:4px 18px 4px 18px; padding:22px 24px; margin:12px 0 20px 0; }
.bk-section-title { font-family:'Playfair Display',serif; font-weight:500; font-size:21px; color:var(--wine-deep); margin-bottom:4px; }
.bk-section-sub { color:var(--muted); font-size:11px; margin-bottom:16px; line-height:1.6; }
.bk-callout { background:#F5EBE7; border-left:3px solid var(--wine); border-radius:2px 10px 2px 10px; padding:16px 18px; color:#59414B; font-size:12px; line-height:1.8; }
.bk-disclaimer { color:#94858A; font-size:10px; line-height:1.7; border-top:1px solid var(--line); padding-top:17px; margin-top:30px; }
[data-testid="stMetric"] { background:var(--paper); border:1px solid var(--line); padding:16px 18px; border-radius:3px 14px 3px 14px; }
[data-testid="stMetricLabel"] { color:var(--muted) !important; font-size:10px !important; }
[data-testid="stMetricValue"] { color:var(--wine-deep) !important; font-weight:600; }
.stButton>button { border-radius:3px 10px 3px 10px; border:1px solid var(--wine); background:var(--wine); color:white; font-weight:600; padding:.62rem 1rem; transition:all .15s ease; }
.stButton>button:hover { background:var(--wine-deep); color:white; border-color:var(--wine-deep); }
.stDownloadButton>button { border-radius:3px 10px 3px 10px; }
[data-testid="stTabs"] [role="tab"] { color:var(--muted); font-weight:600; padding:12px 15px; }
[data-testid="stTabs"] [aria-selected="true"] { color:var(--wine) !important; border-bottom-color:var(--wine) !important; }
hr { border-color:var(--line) !important; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:10px; overflow:hidden; }
div[data-baseweb="select"] > div, .stTextInput input { border-radius:5px 10px 5px 10px; }
@media(max-width:800px) { .bk-hero-title {font-size:27px;} .bk-kpi-value {font-size:24px;} h1 {font-size:2.1rem !important;} }
</style>
""", unsafe_allow_html=True)

# ---------- FICTIONAL DEMO DATA ----------
DEMO_DATA = [
    {"Retail Account":"Sephora Spain","Account Type":"Prestige beauty","Monthly Target (€)":52000,"Current Month Sales (€)":46800,"Previous Month Sales (€)":44200,"Stock Cover (weeks)":3.5,"Hero SKU":"Vitamin C Serum","Hero SKU Sales Growth (%)":0.042,"Promotion Planned?":"No","Account Notes":"Strong growth, but below target; serum is a key driver."},
    {"Retail Account":"Douglas Spain","Account Type":"Prestige beauty","Monthly Target (€)":40000,"Current Month Sales (€)":43200,"Previous Month Sales (€)":40500,"Stock Cover (weeks)":4,"Hero SKU":"Barrier Repair Cream","Hero SKU Sales Growth (%)":0.07,"Promotion Planned?":"Yes","Account Notes":"Above target; opportunity to protect momentum and expand hero SKU."},
    {"Retail Account":"Lookfantastic Spain","Account Type":"Online beauty retailer","Monthly Target (€)":30000,"Current Month Sales (€)":24600,"Previous Month Sales (€)":27000,"Stock Cover (weeks)":2.5,"Hero SKU":"Retinol Night Serum","Hero SKU Sales Growth (%)":0.038,"Promotion Planned?":"No","Account Notes":"Sales declined versus previous month; investigate traffic, conversion, and assortment."},
    {"Retail Account":"El Corte Inglés Beauty","Account Type":"Department store","Monthly Target (€)":36000,"Current Month Sales (€)":32400,"Previous Month Sales (€)":31800,"Stock Cover (weeks)":5,"Hero SKU":"Hydrating Cleanser","Hero SKU Sales Growth (%)":0.065,"Promotion Planned?":"Yes","Account Notes":"Near target with positive growth; planned promotion needs ROI review."},
    {"Retail Account":"Primor","Account Type":"Beauty specialist","Monthly Target (€)":45000,"Current Month Sales (€)":40500,"Previous Month Sales (€)":38200,"Stock Cover (weeks)":2,"Hero SKU":"SPF 50 Fluid","Hero SKU Sales Growth (%)":0.025,"Promotion Planned?":"No","Account Notes":"Largest absolute target gap among specialist accounts; stock cover is tight."},
    {"Retail Account":"Druni","Account Type":"Beauty specialist","Monthly Target (€)":28000,"Current Month Sales (€)":29400,"Previous Month Sales (€)":27600,"Stock Cover (weeks)":6,"Hero SKU":"Vitamin C Serum","Hero SKU Sales Growth (%)":0.085,"Promotion Planned?":"No","Account Notes":"Above target with strong growth; potential for cross-sell and replenishment."},
    {"Retail Account":"Perfume's Club","Account Type":"Online beauty retailer","Monthly Target (€)":22000,"Current Month Sales (€)":17600,"Previous Month Sales (€)":19000,"Stock Cover (weeks)":3,"Hero SKU":"Retinol Night Serum","Hero SKU Sales Growth (%)":0.05,"Promotion Planned?":"Yes","Account Notes":"Below target and declining; assess whether planned promotion can recover sales."},
    {"Retail Account":"Marionnaud Spain","Account Type":"Prestige beauty","Monthly Target (€)":25000,"Current Month Sales (€)":23750,"Previous Month Sales (€)":23000,"Stock Cover (weeks)":4,"Hero SKU":"Barrier Repair Cream","Hero SKU Sales Growth (%)":0.045,"Promotion Planned?":"No","Account Notes":"Close to target; opportunity to improve merchandising and staff education."},
]


# Fictional promotion example used when no workbook is uploaded.
DEMO_PROMOTIONS = pd.DataFrame([{
    "Reporting Month":"2026-10", "Retail Account":"Perfume's Club", "Product":"Retinol Night Serum",
    "Mechanic":"Online promotional offer", "Discount Rate":0.20, "Expected Incremental Units":160,
    "Retailer Funding (€)":500, "Brand Funding (€)":1500, "Baseline Units":310,
    "Expected Brand Gross Profit (€)":float("nan"), "Status":"Under review",
    "Decision Notes":"Declining sales; validate stock, margin, traffic and expected incremental units before approval."
}])
promotions_df = DEMO_PROMOTIONS.copy()
product_master_df = pd.DataFrame()
inventory_df = pd.DataFrame()

REQUIRED = ["Retail Account", "Monthly Target (€)", "Current Month Sales (€)", "Previous Month Sales (€)", "Stock Cover (weeks)"]

def prepare_data(frame):
    frame = frame.copy()
    frame = frame.rename(columns={
        "Current Net Sales (€)":"Current Month Sales (€)",
        "Net Sales (€)":"Current Month Sales (€)",
        "Hero SKU Growth (%)":"Hero SKU Sales Growth (%)",
        "Priority Notes":"Account Notes"
    })
    for col in ["Monthly Target (€)", "Current Month Sales (€)", "Previous Month Sales (€)", "Stock Cover (weeks)", "Hero SKU Sales Growth (%)"]:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
    missing = [col for col in REQUIRED if col not in frame.columns]
    if missing:
        return None, missing
    frame["Sales Growth (%)"] = frame["Current Month Sales (€)"].div(frame["Previous Month Sales (€)"].replace(0, float("nan"))) - 1
    frame["Target Attainment (%)"] = frame["Current Month Sales (€)"].div(frame["Monthly Target (€)"].replace(0, float("nan")))
    frame["Gap to Target (€)"] = frame["Monthly Target (€)"] - frame["Current Month Sales (€)"]
    return frame, []

def money(x):
    return f"€{x:,.0f}" if pd.notna(x) else "—"
def percent(x):
    return f"{x:+.1%}" if pd.notna(x) else "—"
def pct_plain(x):
    return f"{x:.1%}" if pd.notna(x) else "—"

def next_step(row):
    gap, growth, stock = row["Gap to Target (€)"], row["Sales Growth (%)"], row["Stock Cover (weeks)"]
    if stock < 3:
        return "Validate replenishment", "Low stock cover may constrain sales recovery."
    if growth < 0 and gap > 0:
        return "Review sales drivers", "The workbook does not identify the cause of the decline."
    if gap > 0:
        return "Build a targeted recovery plan", "Validate margin and incremental sales before any promotion."
    return "Protect momentum and cross-sell", "Validate sell-through and margin before expanding assortment."

# ---------- SIDEBAR / DATA MANAGEMENT ----------
with st.sidebar:
    st.markdown("<div class='bk-brand'><div class='bk-mark'>✦</div><div><div class='bk-wordmark'>BeautyKey</div><div class='bk-subbrand'>RETAIL INTELLIGENCE</div></div></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='bk-eyebrow'>WORKSPACE</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload BeautyKey Excel workbook", type=["xlsx"])
    st.caption("Upload the complete workbook to switch between historical months. Without an upload, the September demo is shown.")

# Demo is the safe default. An uploaded workbook activates the real month selector.
source = "Fictional demonstration dataset"
df = pd.DataFrame(DEMO_DATA)
reporting_period = "September 2026"
with st.sidebar:
    if uploaded_file:
        st.success("Workbook selected")
    else:
        st.info("Using fictional demonstration data")

if uploaded_file:
    try:
        workbook = pd.ExcelFile(uploaded_file)
        if "Promotions" in workbook.sheet_names:
            try:
                promotions_df = pd.read_excel(uploaded_file, sheet_name="Promotions", header=2)
                for numeric_col in ["Discount Rate", "Expected Incremental Units", "Retailer Funding (€)", "Brand Funding (€)", "Baseline Units", "Expected Brand Gross Profit (€)"]:
                    if numeric_col in promotions_df.columns:
                        promotions_df[numeric_col] = pd.to_numeric(promotions_df[numeric_col], errors="coerce")
            except Exception:
                promotions_df = DEMO_PROMOTIONS.copy()
        if "Product Master" in workbook.sheet_names:
            try:
                product_master_df = pd.read_excel(uploaded_file, sheet_name="Product Master", header=2)
                if "Gross Margin Rate" in product_master_df.columns:
                    product_master_df["Gross Margin Rate"] = pd.to_numeric(product_master_df["Gross Margin Rate"], errors="coerce")
            except Exception:
                product_master_df = pd.DataFrame()
        if "Inventory" in workbook.sheet_names:
            try:
                inventory_df = pd.read_excel(uploaded_file, sheet_name="Inventory", header=2)
                for numeric_col in ["On-hand Units", "Avg Weekly Units Sold", "Stock Cover (weeks)", "Reorder Threshold (weeks)"]:
                    if numeric_col in inventory_df.columns:
                        inventory_df[numeric_col] = pd.to_numeric(inventory_df[numeric_col], errors="coerce")
            except Exception:
                inventory_df = pd.DataFrame()
        if "Historical Sales" not in workbook.sheet_names:
            st.error("This workbook does not contain a 'Historical Sales' sheet. Please upload the complete BeautyKey Excel template.")
            st.stop()
        history = pd.read_excel(uploaded_file, sheet_name="Historical Sales", header=2)
        needed_history = {"Reporting Month", "Retail Account", "Net Sales (€)", "Target (€)"}
        if not needed_history.issubset(history.columns):
            st.error("The 'Historical Sales' sheet is missing one or more required columns: Reporting Month, Retail Account, Net Sales (€), Target (€).")
            st.stop()
        history = history.copy()
        history["Reporting Month"] = pd.to_datetime(history["Reporting Month"].astype(str), errors="coerce").dt.to_period("M")
        history["Net Sales (€)"] = pd.to_numeric(history["Net Sales (€)"], errors="coerce")
        history["Target (€)"] = pd.to_numeric(history["Target (€)"], errors="coerce")
        history = history.dropna(subset=["Reporting Month", "Retail Account", "Net Sales (€)", "Target (€)"])
        month_periods = sorted(history["Reporting Month"].unique())
        if not month_periods:
            st.error("No usable monthly records were found in 'Historical Sales'.")
            st.stop()
        month_labels = {str(m): m.strftime("%B %Y") for m in month_periods}
        default_month = str(month_periods[-1])
        with st.sidebar:
            chosen_month = st.selectbox("Reporting period", options=[str(m) for m in month_periods], index=len(month_periods)-1, format_func=lambda m: month_labels[m])
        selected_period = pd.Period(chosen_month, freq="M")
        current = history[history["Reporting Month"] == selected_period].copy()
        previous_period = selected_period - 1
        previous = history[history["Reporting Month"] == previous_period][["Retail Account", "Net Sales (€)"]].rename(columns={"Net Sales (€)":"Previous Month Sales (€)"})
        current = current.rename(columns={"Net Sales (€)":"Current Month Sales (€)", "Target (€)":"Monthly Target (€)"})
        current = current.drop(columns=[c for c in ["Reporting Month", "Account ID", "Target Attainment (%)", "Gap to Target (€)", "Data Status"] if c in current.columns])
        current = current.merge(previous, on="Retail Account", how="left")
        current["Previous Month Sales (€)"] = current["Previous Month Sales (€)"].fillna(current["Current Month Sales (€)"])
        # Account Targets contains current snapshot context (stock, hero SKU and notes), not historical snapshots.
        if "Account Targets" in workbook.sheet_names:
            snapshot = pd.read_excel(uploaded_file, sheet_name="Account Targets", header=2)
            context_cols = [c for c in ["Retail Account", "Account Type", "Stock Cover (weeks)", "Hero SKU", "Hero SKU Growth (%)", "Planned Promotion?", "Priority Notes"] if c in snapshot.columns]
            if "Retail Account" in context_cols:
                snapshot = snapshot[context_cols].drop_duplicates(subset=["Retail Account"])
                current = current.merge(snapshot, on="Retail Account", how="left")
        current = current.rename(columns={"Hero SKU Growth (%)":"Hero SKU Sales Growth (%)", "Priority Notes":"Account Notes", "Planned Promotion?":"Promotion Planned?"})
        if "Stock Cover (weeks)" not in current.columns:
            current["Stock Cover (weeks)"] = 4.0
        current["Stock Cover (weeks)"] = pd.to_numeric(current["Stock Cover (weeks)"], errors="coerce").fillna(4.0)
        if "Hero SKU Sales Growth (%)" not in current.columns:
            current["Hero SKU Sales Growth (%)"] = 0.0
        current["Hero SKU Sales Growth (%)"] = pd.to_numeric(current["Hero SKU Sales Growth (%)"], errors="coerce").fillna(0.0)
        if "Account Notes" not in current.columns:
            current["Account Notes"] = "Review historical sales and validate account context."
        if "Promotion Planned?" not in current.columns:
            current["Promotion Planned?"] = "Unknown"
        df, missing = prepare_data(current)
        if missing:
            st.error("The selected month is missing required fields: " + ", ".join(missing))
            st.stop()
        reporting_period = month_labels[chosen_month]
        source = "Uploaded workbook · Historical Sales"
        st.sidebar.caption("Historical sales and targets change by month. Stock cover and hero-SKU context come from the latest account snapshot in the workbook.")
    except Exception as exc:
        st.error(f"Unable to read the workbook. Please upload the complete BeautyKey .xlsx template. Details: {exc}")
        st.stop()
else:
    with st.sidebar:
        reporting_period = st.selectbox("Reporting period", ["September 2026"], index=0, help="Upload the full Excel workbook to select historical months.")

if df is None:
    st.stop()
df, missing = prepare_data(df)
if missing:
    st.error("The data is missing required columns: " + ", ".join(missing))
    st.stop()
df = df.dropna(subset=["Monthly Target (€)", "Current Month Sales (€)", "Previous Month Sales (€)"])
df = df[df["Monthly Target (€)"] > 0]
if df.empty:
    st.error("No valid account rows found for the selected month. Check the Historical Sales sheet.")
    st.stop()

# Priority scoring is deliberately transparent and heuristic.
df["Priority score"] = (
    (df["Gap to Target (€)"].clip(lower=0) / df["Monthly Target (€)"]) * 0.55
    + (-df["Sales Growth (%)"]).clip(lower=0) * 0.30
    + df.get("Hero SKU Sales Growth (%)", pd.Series(0, index=df.index)).fillna(0).clip(lower=0) * 0.15
)
df["Recommended action"], df["Risk / unknown"] = zip(*df.apply(next_step, axis=1))
ranked = df.sort_values("Priority score", ascending=False).copy()

# ---------- BRAND HEADER ----------
st.markdown("<div class='bk-eyebrow'>BEAUTY RETAIL · COMMERCIAL INTELLIGENCE</div>", unsafe_allow_html=True)
header_left, header_right = st.columns([4,1])
with header_left:
    st.title("BeautyKey")
    st.markdown("A considered view of account performance, growth opportunities and your next commercial move.")
with header_right:
    st.markdown("<div style='text-align:right;padding-top:18px'><span class='bk-pill'>ACADEMIC DEMO</span></div>", unsafe_allow_html=True)

st.markdown(f"""<div class='bk-hero'><div class='bk-eyebrow'>YOUR PORTFOLIO AT A GLANCE</div><div class='bk-hero-title'>Clarity for your next commercial move.</div><div class='bk-hero-copy'>Review performance against target, identify accounts that may need attention, and turn the data into practical next steps. <b>Reporting period:</b> {reporting_period} &nbsp; · &nbsp; <b>Source:</b> {source}</div></div>""", unsafe_allow_html=True)

sales_total = df["Current Month Sales (€)"].sum()
previous_total = df["Previous Month Sales (€)"].sum()
target_total = df["Monthly Target (€)"].sum()
attainment = sales_total / target_total if target_total else 0
growth_total = sales_total / previous_total - 1 if previous_total else 0
positive_gap = df["Gap to Target (€)"].clip(lower=0).sum()
above = int((df["Gap to Target (€)"] <= 0).sum())
alerts = int(((df["Stock Cover (weeks)"] < 3) | ((df["Sales Growth (%)"] < 0) & (df["Gap to Target (€)"] > 0))).sum())

kpis = st.columns(4)
metric_data = [
    ("NET SALES", money(sales_total), f"{growth_total:+.1%} vs previous period", "positive" if growth_total >= 0 else "negative"),
    ("TARGET ATTAINMENT", pct_plain(attainment), f"{(attainment-1)*100:+.1f} pp vs target", "positive" if attainment >= 1 else "neutral"),
    ("REMAINING TARGET GAP", money(positive_gap), "Sum of positive account-level gaps", "neutral"),
    ("ACCOUNTS ABOVE TARGET", f"{above} / {len(df)}", f"{alerts} accounts flagged for review", "neutral")
]
for col, (label, value, note, state) in zip(kpis, metric_data):
    with col:
        st.markdown(f"<div class='bk-card'><div class='bk-kpi-label'>{label}</div><div class='bk-kpi-value'>{value}</div><div class='bk-kpi-note'>{note}</div></div>", unsafe_allow_html=True)

# ---------- MAIN NAVIGATION ----------
t_overview, t_accounts, t_opportunities, t_assistant, t_data = st.tabs(["✦ Overview", "Account review", "Growth opportunities", "Action studio", "Data & guide"])

with t_overview:
    st.markdown("<div class='bk-section'><div class='bk-section-title'>Portfolio performance</div><div class='bk-section-sub'>A high-level view of target delivery and sales momentum.</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.15, 1])
    with col1:
        chart_df = df.sort_values("Target Attainment (%)")
        fig = px.bar(chart_df, x="Retail Account", y="Target Attainment (%)", color="Target Attainment (%)", hover_data=["Current Month Sales (€)", "Gap to Target (€)", "Sales Growth (%)"], color_continuous_scale=["#E8D4D1", "#C99EAA", "#80515B", "#493640"], labels={"Target Attainment (%)":"Target attainment", "Retail Account":"Retail account"})
        fig.add_hline(y=1, line_dash="dash", line_color="#B89A68", annotation_text="100% target")
        fig.update_layout(height=360, margin=dict(l=8,r=8,t=15,b=8), xaxis_tickangle=-25, coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans",color="#3F303A"), yaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        scatter = px.scatter(df, x="Sales Growth (%)", y="Gap to Target (€)", size="Current Month Sales (€)", color="Stock Cover (weeks)", hover_name="Retail Account", hover_data=["Target Attainment (%)"], color_continuous_scale=["#D9E8DF", "#77B9A4", "#397966", "#634653"], labels={"Sales Growth (%)":"Sales growth vs previous period", "Gap to Target (€)":"Gap to target (€)", "Stock Cover (weeks)":"Stock cover (weeks)"})
        scatter.add_hline(y=0, line_dash="dash", line_color="#B89A68")
        scatter.add_vline(x=0, line_dash="dash", line_color="#B89A68")
        scatter.update_layout(height=360, margin=dict(l=8,r=8,t=15,b=8), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans",color="#3F303A"))
        st.plotly_chart(scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='bk-section-title'>Recommended management focus</div><div class='bk-section-sub'>Priority signals based on sales gap, momentum and available stock-cover data.</div>", unsafe_allow_html=True)
    focus = ranked.iloc[0]
    st.markdown(f"<div class='bk-callout'><b>{focus['Retail Account']}</b> is the highest-ranked account for review under the current demo scoring. Sales are {money(focus['Current Month Sales (€)'])}, target attainment is {pct_plain(focus['Target Attainment (%)'])}, and stock cover is {focus['Stock Cover (weeks)']:g} weeks.<br><br><b>Suggested next step:</b> {focus['Recommended action']}. This is a prioritization signal, not a forecast or proof of incremental revenue.</div>", unsafe_allow_html=True)

with t_accounts:
    st.markdown("<div class='bk-section-title'>Your account, at a glance</div><div class='bk-section-sub'>Choose a retailer to review its performance, context and recommended next step.</div>", unsafe_allow_html=True)
    account_options = sorted(df["Retail Account"].dropna().unique().tolist())
    selected_account = st.selectbox("Select an account", account_options)
    account = df[df["Retail Account"] == selected_account].iloc[0]
    a1,a2,a3,a4 = st.columns(4)
    a1.metric("Current sales", money(account["Current Month Sales (€)"]))
    a2.metric("Target attainment", pct_plain(account["Target Attainment (%)"]))
    a3.metric("Sales growth", percent(account["Sales Growth (%)"]))
    a4.metric("Stock cover", f"{account['Stock Cover (weeks)']:g} weeks")
    st.markdown("### Account review")
    st.write(f"**Account type:** {account.get('Account Type','Not provided')}  ·  **Hero SKU:** {account.get('Hero SKU','Not provided')}")
    st.write(f"**Target:** {money(account['Monthly Target (€)'])}  ·  **Gap to target:** {money(account['Gap to Target (€)'])}")
    st.write(f"**Account context:** {account.get('Account Notes','No account notes supplied.')}")
    st.markdown(f"<div class='bk-callout'><b>Recommended next action</b><br>{account['Recommended action']}<br><br><b>Risk / unknown</b><br>{account['Risk / unknown']}</div>", unsafe_allow_html=True)

with t_opportunities:
    st.markdown("<div class='bk-section-title'>Growth opportunities</div><div class='bk-section-sub'>A transparent prioritization heuristic for deciding which accounts to review first.</div>", unsafe_allow_html=True)
    st.caption("Priority score combines positive target gap relative to target, negative sales growth, and positive hero-SKU growth. It is illustrative, not statistically validated.")
    opportunity_table = ranked[["Retail Account", "Current Month Sales (€)", "Monthly Target (€)", "Target Attainment (%)", "Gap to Target (€)", "Sales Growth (%)", "Stock Cover (weeks)", "Recommended action"]].copy()
    opportunity_table = opportunity_table.rename(columns={"Retail Account":"Account", "Current Month Sales (€)":"Sales (€)", "Monthly Target (€)":"Target (€)", "Target Attainment (%)":"Attainment", "Gap to Target (€)":"Gap (€)", "Sales Growth (%)":"Growth", "Stock Cover (weeks)":"Stock (weeks)", "Recommended action":"Recommended next step"})
    st.dataframe(opportunity_table, use_container_width=True, hide_index=True, column_config={"Sales (€)":st.column_config.NumberColumn(format="€%.0f"), "Target (€)":st.column_config.NumberColumn(format="€%.0f"), "Gap (€)":st.column_config.NumberColumn(format="€%.0f"), "Attainment":st.column_config.NumberColumn(format="%.1f%%"), "Growth":st.column_config.NumberColumn(format="%.1f%%"), "Stock (weeks)":st.column_config.NumberColumn(format="%.1f")})
    st.download_button("Export opportunity review (CSV)", opportunity_table.to_csv(index=False).encode("utf-8"), file_name="beautykey_opportunity_review.csv", mime="text/csv")

with t_assistant:
    st.markdown("<div class='bk-section-title'>Action studio</div><div class='bk-section-sub'>Create a practical action plan, retailer email or conditional promotion-investment assessment from the uploaded data. Nothing is sent or approved automatically.</div>", unsafe_allow_html=True)
    task = st.selectbox("What would you like to prepare?", ["Summarize the top three opportunities", "Build a 30-day action plan", "Draft a retailer business-review email", "Assess whether to run a promotion"])
    chosen = st.selectbox("Account context", ["Highest-priority account"] + account_options)
    if chosen == "Highest-priority account":
        target_row = ranked.iloc[0]
    else:
        target_row = df[df["Retail Account"] == chosen].iloc[0]
    if st.button("Generate account brief", key="assistant_generate"):
        if task == "Summarize the top three opportunities":
            for _, r in ranked.head(3).iterrows():
                st.markdown(f"**{r['Retail Account']}** · {money(r['Current Month Sales (€)'])} sales · {pct_plain(r['Target Attainment (%)'])} target attainment · {money(r['Gap to Target (€)'])} gap")
                st.write(f"Next step: {r['Recommended action']}. Unknown to validate: {r['Risk / unknown']}")
        elif task == "Build a 30-day action plan":
            st.markdown(f"### 30-day action plan · {target_row['Retail Account']}")
            st.write(f"**Evidence:** sales {money(target_row['Current Month Sales (€)'])}; target {money(target_row['Monthly Target (€)'])}; attainment {pct_plain(target_row['Target Attainment (%)'])}; stock cover {target_row['Stock Cover (weeks)']:g} weeks.")
            st.markdown("**Days 1–5 · Validate**\n- Confirm the latest sales and target data.\n- Check stock on hand, sell-through and any retailer context missing from the workbook.")
            st.markdown(f"**Days 6–15 · Align**\n- {target_row['Recommended action']}.\n- Agree the account owner, retailer contact and measurable next step.")
            st.markdown("**Days 16–23 · Execute**\n- Coordinate agreed assortment, replenishment, merchandising or communication actions.\n- Do not commit promotional spend until margin and incremental impact are assessed.")
            st.markdown("**Days 24–30 · Review**\n- Compare sales, target attainment, stock cover and hero-SKU performance with the baseline.\n- Document outcome, learnings and follow-up owner.")
            st.info("This plan is a suggested workflow. Dates, owners and commercial commitments require human confirmation.")
        elif task == "Draft a retailer business-review email":
            email = f"""Subject: Business review and growth opportunities — {target_row['Retail Account']}\n\nHi [Contact Name],\n\nI hope you are well. I would like to arrange a short business review to discuss recent performance and identify practical opportunities for the coming month.\n\nOur current reporting shows sales of {money(target_row['Current Month Sales (€)'])} against a target of {money(target_row['Monthly Target (€)'])}. I would welcome the opportunity to review the drivers together.\n\nSuggested agenda:\n• Review sales performance and target progress\n• Discuss hero SKU trends, availability and replenishment\n• Review planned commercial activity and the data needed to assess its effectiveness\n• Agree next steps, owners and KPIs\n\nWould [proposed date/time] work for you?\n\nBest regards,\n[Your Name]\n[Title]"""
            st.text_area("Email draft — review before sending", email, height=310)
            st.download_button("Download email draft", email, file_name="beautykey_retailer_email.txt", mime="text/plain")
            st.caption("Draft only. The app does not send emails.")
        else:
            st.markdown("### Promotion investment assessment")
            st.caption("Rule-based decision support. Forecasts are hypotheses, not guaranteed incremental results or proof of profitability.")
            if promotions_df.empty or "Retail Account" not in promotions_df.columns:
                st.warning("No usable Promotions sheet was found. Upload the complete workbook to assess planned commercial activity.")
            else:
                account_promos = promotions_df[promotions_df["Retail Account"].astype(str).str.strip() == str(target_row["Retail Account"]).strip()].copy()
                if "Status" in account_promos.columns:
                    open_promos = account_promos[account_promos["Status"].astype(str).str.lower().isin(["planned", "under review", "on hold", "pending"])]
                    if not open_promos.empty:
                        account_promos = open_promos
                if account_promos.empty:
                    st.info(f"No planned promotion was found for {target_row['Retail Account']} in the Promotions sheet. The app will not invent a promotion recommendation.")
                else:
                    if "Reporting Month" in account_promos.columns:
                        account_promos["_month"] = pd.to_datetime(account_promos["Reporting Month"].astype(str), errors="coerce")
                        account_promos = account_promos.sort_values("_month", na_position="last")
                    promo = account_promos.iloc[0]
                    product = str(promo.get("Product", "the selected product"))
                    discount = promo.get("Discount Rate", float("nan"))
                    incr_units = promo.get("Expected Incremental Units", float("nan"))
                    baseline_units = promo.get("Baseline Units", float("nan"))
                    brand_funding = promo.get("Brand Funding (€)", float("nan"))
                    retailer_funding = promo.get("Retailer Funding (€)", float("nan"))
                    expected_gp = promo.get("Expected Brand Gross Profit (€)", float("nan"))
                    status = str(promo.get("Status", "Status not provided"))
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Proposed discount", f"{discount:.0%}" if pd.notna(discount) else "Not provided")
                    col_b.metric("Brand funding", money(brand_funding))
                    col_c.metric("Expected incremental units", f"{incr_units:,.0f}" if pd.notna(incr_units) else "Not provided")
                    st.write(f"**Promotion:** {product} · {promo.get('Mechanic', 'Mechanic not provided')} · **Status:** {status}")
                    sku_id = str(promo.get("SKU ID", "")).strip()
                    if not inventory_df.empty and {"Retail Account", "SKU ID"}.issubset(inventory_df.columns) and sku_id and sku_id.lower() != "nan":
                        sku_stock = inventory_df[(inventory_df["Retail Account"].astype(str).str.strip() == str(target_row["Retail Account"]).strip()) & (inventory_df["SKU ID"].astype(str).str.strip() == sku_id)]
                        if not sku_stock.empty:
                            stock = sku_stock.iloc[-1]
                            stock_cols = st.columns(3)
                            stock_cols[0].metric("SKU units on hand", f"{stock.get('On-hand Units', float('nan')):,.0f}" if pd.notna(stock.get("On-hand Units", float("nan"))) else "Not provided")
                            stock_cols[1].metric("SKU stock status", str(stock.get("Availability Status", "Unknown")))
                            stock_cols[2].metric("Weekly unit sales", f"{stock.get('Avg Weekly Units Sold', float('nan')):,.0f}" if pd.notna(stock.get("Avg Weekly Units Sold", float("nan"))) else "Not provided")
                            if str(stock.get("Availability Status", "")).strip().lower() in ["watch", "low", "critical"]:
                                st.warning(f"SKU-level inventory is flagged as '{stock.get('Availability Status')}'. Resolve availability before approving demand-driving activity.")
                    if not product_master_df.empty and "Product" in product_master_df.columns:
                        product_ref = product_master_df[product_master_df["Product"].astype(str).str.strip() == product]
                        if not product_ref.empty:
                            ref = product_ref.iloc[0]
                            if pd.notna(ref.get("Gross Margin Rate", float("nan"))):
                                st.write(f"Product Master gross-margin reference: {ref['Gross Margin Rate']:.0%}. This is a reference input, not a promotion-level profit calculation; confirm how the discount and funding affect net contribution.")
                    if pd.notna(baseline_units) and pd.notna(incr_units) and baseline_units > 0:
                        st.write(f"The plan assumes {incr_units:,.0f} incremental units against a baseline of {baseline_units:,.0f} units ({incr_units / baseline_units:.1%} of baseline). This is a planning assumption, not verified uplift.")
                    sales_growth = target_row.get("Sales Growth (%)", float("nan"))
                    st.markdown("#### Decision logic")
                    if pd.notna(sales_growth) and sales_growth < 0:
                        st.write(f"The account is declining month-on-month ({sales_growth:.1%}) and is {pct_plain(target_row['Target Attainment (%)'])} of target. That makes the promotion worth assessing—but does not prove a discount is the right solution.")
                    missing_economics = []
                    if pd.isna(expected_gp): missing_economics.append("expected brand gross profit after promotional costs")
                    if pd.isna(discount): missing_economics.append("discount rate")
                    if pd.isna(brand_funding): missing_economics.append("brand funding")
                    if pd.isna(incr_units): missing_economics.append("expected incremental units")
                    if missing_economics:
                        st.error("RECOMMENDATION: HOLD FOR VALIDATION. The financial case is incomplete: " + ", ".join(missing_economics) + ".")
                    else:
                        st.warning("RECOMMENDATION: DO NOT AUTO-APPROVE. Validate the expected gross profit and incremental-sales assumptions against the funding and discount before committing spend.")
                    if pd.notna(expected_gp):
                        net_after_funding = expected_gp - (brand_funding if pd.notna(brand_funding) else 0)
                        st.write(f"Workbook-reported expected brand gross profit: {money(expected_gp)}. After brand funding alone: {money(net_after_funding)}. Confirm whether the workbook's gross-profit estimate already accounts for discounts and other costs to avoid double counting.")
                    st.markdown("**Required checks before approval**")
                    st.markdown("1. Confirm stock availability for the promoted SKU and the promotion dates.\n2. Validate net price, gross margin, discount funding and expected brand contribution.\n3. Agree how incremental units will be measured against a baseline.\n4. Set a minimum contribution hurdle and post-promotion review date.")
                    st.info("Decision owner: account manager / commercial finance. BeautyKey prepares the evidence and conditional recommendation; it does not approve spend.")
                    st.markdown("#### Suggested next action")
                    st.write(f"Request a margin-and-incrementality check for {product}; keep the promotion under review until the financial hurdle is documented. If the hurdle passes and stock is sufficient, approve a controlled test and compare actual incremental contribution with the agreed baseline.")
                    if target_row["Stock Cover (weeks)"] < 3:
                        st.warning("Account-level stock cover is below 3 weeks. Confirm SKU-level stock before any demand-driving activity; account-level stock cover may not represent this specific product.")

with t_data:
    st.markdown("<div class='bk-section-title'>Data management & methodology</div><div class='bk-section-sub'>Understand the monthly refresh process, source fields and limitations.</div>", unsafe_allow_html=True)
    st.markdown("#### Monthly refresh workflow")
    st.markdown("1. Export the latest approved account sales and target data.\n2. Update the Excel workbook and check retailer names, periods, currency and missing values.\n3. Upload the workbook using the sidebar.\n4. Review the data and recommendations before sharing or acting on them.")
    st.markdown("#### Current prototype boundaries")
    st.markdown("- Data is read from a user-uploaded workbook or the embedded fictional demo dataset.\n- The assistant uses rule-based logic; it is not connected to a live large language model.\n- No automatic retrieval from retailer systems, CRM updates, email sending or external actions occur.\n- Priority scores are illustrative heuristics, not a validated forecast.\n- Recommendations require human review and additional context such as margin, sell-through, inventory and promotional costs.")
    st.markdown("#### Account data")
    st.dataframe(df, use_container_width=True, hide_index=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download current account dataset (CSV)", csv, file_name="beautykey_account_data.csv", mime="text/csv")

st.markdown("<div class='bk-disclaimer'><b>Academic prototype disclaimer.</b> BeautyKey AI is an educational prototype developed for an academic project. All retailer, sales, product and performance data are fictional and created for demonstration purposes. The prototype is not affiliated with or endorsed by any real company.<br><br>BeautyKey AI · Retail Intelligence · Human review required · No external system actions are executed.</div>", unsafe_allow_html=True)
