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
