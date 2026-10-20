import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="BeautyKey AI", page_icon="✨", layout="wide")

DEMO_DATA = [
    {"Retail Account":"Sephora Spain","Account Type":"Prestige beauty","Monthly Target (€)":52000,"Current Month Sales (€)":46800,"Previous Month Sales (€)":44200,"Stock Cover (weeks)":3.5,"Hero SKU":"Vitamin C Serum","Hero SKU Sales Growth (%)":0.042,"Promotion Planned?":"No","Account Notes":"Strong growth, but below target; serum is a key driver."},
    {"Retail Account":"Douglas Spain","Account Type":"Prestige beauty","Monthly Target (€)":40000,"Current Month Sales (€)":43200,"Previous Month Sales (€)":40500,"Stock Cover (weeks)":4,"Hero SKU":"Barrier Repair Cream","Hero SKU Sales Growth (%)":0.07,"Promotion Planned?":"Yes","Account Notes":"Above target; opportunity to protect momentum and expand hero SKU."},
    {"Retail Account":"Lookfantastic Spain","Account Type":"Online beauty retailer","Monthly Target (€)":30000,"Current Month Sales (€)":24600,"Previous Month Sales (€)":27000,"Stock Cover (weeks)":2.5,"Hero SKU":"Retinol Night Serum","Hero SKU Sales Growth (%)":0.038,"Promotion Planned?":"No","Account Notes":"Sales declined versus previous month; investigate traffic, conversion, and assortment."},
    {"Retail Account":"El Corte Inglés Beauty","Account Type":"Department store","Monthly Target (€)":36000,"Current Month Sales (€)":32400,"Previous Month Sales (€)":31800,"Stock Cover (weeks)":5,"Hero SKU":"Hydrating Cleanser","Hero SKU Sales Growth (%)":0.065,"Promotion Planned?":"Yes","Account Notes":"Near target with positive growth; planned promotion needs ROI review."},
    {"Retail Account":"Primor","Account Type":"Beauty specialist","Monthly Target (€)":45000,"Current Month Sales (€)":40500,"Previous Month Sales (€)":38200,"Stock Cover (weeks)":2,"Hero SKU":"SPF 50 Fluid","Hero SKU Sales Growth (%)":0.025,"Promotion Planned?":"No","Account Notes":"Largest absolute target gap among specialist accounts; stock cover is tight."},
    {"Retail Account":"Druni","Account Type":"Beauty specialist","Monthly Target (€)":28000,"Current Month Sales (€)":29400,"Previous Month Sales (€)":27600,"Stock Cover (weeks)":6,"Hero SKU":"Vitamin C Serum","Hero SKU Sales Growth (%)":0.085,"Promotion Planned?":"No","Account Notes":"Above target with strong growth; potential for cross-sell and replenishment."},
    {"Retail Account":"Perfume's Club","Account Type":"Online beauty retailer","Monthly Target (€)":22000,"Current Month Sales (€)":17600,"Previous Month Sales (€)":19000,"Stock Cover (weeks)":3,"Hero SKU":"Retinol Night Serum","Hero SKU Sales Growth (%)":0.05,"Promotion Planned?":"Yes","Account Notes":"Below target and declining; assess whether planned promotion can recover sales."},
    {"Retail Account":"Marionnaud Spain","Account Type":"Prestige beauty","Monthly Target (€)":25000,"Current Month Sales (€)":23750,"Previous Month Sales (€)":23000,"Stock Cover (weeks)":4,"Hero SKU":"Barrier Repair Cream","Hero SKU Sales Growth (%)":0.045,"Promotion Planned?":"No","Account Notes":"Close to target; low-risk opportunity to improve merchandising and staff education."},
]

REQUIRED = ["Retail Account", "Monthly Target (€)", "Current Month Sales (€)", "Previous Month Sales (€)", "Stock Cover (weeks)"]

def prepare(df):
    df = df.copy()
    for c in ["Monthly Target (€)", "Current Month Sales (€)", "Previous Month Sales (€)", "Stock Cover (weeks)", "Hero SKU Sales Growth (%)"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["Sales Growth (%)"] = df["Current Month Sales (€)"].div(df["Previous Month Sales (€)"]).sub(1)
    df["Target Attainment (%)"] = df["Current Month Sales (€)"].div(df["Monthly Target (€)"])
    df["Gap to Target (€)"] = df["Monthly Target (€)"] - df["Current Month Sales (€)"]
    return df

def money(x): return f"€{x:,.0f}"
def pct(x): return f"{x:.1%}" if pd.notna(x) else "—"

def recommend(row):
    name = row['Retail Account']; gap = row['Gap to Target (€)']; growth = row['Sales Growth (%)']; stock = row['Stock Cover (weeks)']
    if stock < 3:
        action = "Check inventory and agree replenishment before adding demand-driving promotion."
        risk = "Low stock cover may constrain sales recovery."
    elif growth < 0 and gap > 0:
        action = "Run a retailer business review on traffic, conversion, assortment and promotional mechanics."
        risk = "Sales decline cause is not established by this workbook."
    elif gap > 0 and growth >= 0:
        action = "Build a targeted recovery plan around the hero SKU and review merchandising / cross-sell."
        risk = "No margin or incremental-sales data to validate promotion ROI."
    else:
        action = "Protect momentum and assess selective assortment expansion or cross-sell."
        risk = "Expansion should be validated against sell-through and margin."
    return action, risk

st.markdown("<div style='padding:8px 0 2px 0'><span style='font-size:13px;letter-spacing:2px;color:#927c68'>COMMERCIAL INTELLIGENCE</span></div>", unsafe_allow_html=True)
st.title("✨ BeautyKey AI")
st.caption("AI Key Account Manager for multi-brand beauty retail · Fictional demo data")

with st.sidebar:
    st.header("Reporting workspace")
    uploaded = st.file_uploader("Upload the updated Excel workbook", type=["xlsx"])
    period = st.text_input("Reporting period", value="Demo period — replace with actual month")
    st.info("Monthly workflow: a human uploads the refreshed workbook and starts the analysis. This prototype does not automatically retrieve data or send reports.")
    st.markdown("**Data source**")
    st.caption("Uploaded workbook, or the embedded fictional demo dataset if no file is uploaded.")

source = "Embedded fictional demo data"
if uploaded:
    try:
        xl = pd.ExcelFile(uploaded)
        preferred = "Account Targets" if "Account Targets" in xl.sheet_names else ("Sales Data" if "Sales Data" in xl.sheet_names else 0)
        sheet = st.selectbox("Select sales sheet", xl.sheet_names, index=xl.sheet_names.index(preferred) if isinstance(preferred, str) else preferred)
        # The complete BeautyKey workbook uses a title row and notes row before the headers.
        if sheet in ["Account Targets", "Current Sales", "Sales Data"]:
            raw = pd.read_excel(uploaded, sheet_name=sheet, header=2 if sheet != "Sales Data" else 0)
        else:
            raw = pd.read_excel(uploaded, sheet_name=sheet)

        # Native support for the complete 11-tab BeautyKey retail database.
        if sheet == "Account Targets" and {"Retail Account", "Monthly Target (€)", "Previous Month Sales (€)", "Stock Cover (weeks)"}.issubset(raw.columns) and "Current Sales" in xl.sheet_names:
            current = pd.read_excel(uploaded, sheet_name="Current Sales", header=2)
            if {"Retail Account", "Net Sales (€)", "Previous Month Sales (€)"}.issubset(current.columns):
                totals = current.groupby("Retail Account", as_index=False).agg({"Net Sales (€)":"sum", "Previous Month Sales (€)":"sum"})
                raw = raw.drop(columns=["Current Net Sales (€)", "Sales Growth (%)", "Target Attainment (%)", "Gap to Target (€)"], errors="ignore")
                raw = raw.merge(totals[["Retail Account", "Net Sales (€)", "Previous Month Sales (€)" ]], on="Retail Account", how="left", suffixes=("", "_from_sales"))
                raw = raw.rename(columns={"Net Sales (€)":"Current Month Sales (€)"})
                if "Previous Month Sales (€)_from_sales" in raw.columns:
                    raw["Previous Month Sales (€)"] = raw["Previous Month Sales (€)_from_sales"].fillna(raw["Previous Month Sales (€)"])
                    raw = raw.drop(columns=["Previous Month Sales (€)_from_sales"])
                raw = raw.rename(columns={"Hero SKU Growth (%)":"Hero SKU Sales Growth (%)", "Priority Notes":"Account Notes"})
        else:
            # Friendly aliases for the original one-sheet demo workbook.
            raw = raw.rename(columns={"Current Net Sales (€)":"Current Month Sales (€)", "Net Sales (€)":"Current Month Sales (€)", "Hero SKU Growth (%)":"Hero SKU Sales Growth (%)", "Priority Notes":"Account Notes"})

        missing = [c for c in REQUIRED if c not in raw.columns]
        if missing:
            st.error("The selected sheet is missing required columns: " + ", ".join(missing) + ". For the complete BeautyKey database, select 'Account Targets'.")
            st.stop()
        df = raw
        source = f"Uploaded workbook · {sheet}"
    except Exception as e:
        st.error(f"Could not read workbook: {e}")
        st.stop()
else:
    df = pd.DataFrame(DEMO_DATA)

df = prepare(df)
if df["Retail Account"].duplicated().any():
    st.warning("Data quality warning: duplicate retailer names detected. Confirm whether these represent separate channels or duplicate records.")
if df[REQUIRED].isna().any().any():
    st.warning("Data quality warning: missing or non-numeric values found in required fields. Check the workbook before acting on the rankings.")
if (df["Monthly Target (€)"] <= 0).any():
    st.warning("Data quality warning: targets must be greater than zero to calculate target attainment reliably.")

valid = df.dropna(subset=["Monthly Target (€)", "Current Month Sales (€)", "Previous Month Sales (€)"])
target = valid["Monthly Target (€)"].sum(); sales = valid["Current Month Sales (€)"].sum(); prev = valid["Previous Month Sales (€)"].sum()
gap = (valid["Gap to Target (€)"].clip(lower=0)).sum()
attainment = sales / target if target else 0
growth = sales / prev - 1 if prev else 0

st.markdown(f"**Period:** {period} &nbsp; · &nbsp; **Source:** {source} &nbsp; · &nbsp; **Accounts:** {len(df)}")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Current sales", money(sales), f"{growth:+.1%} vs previous month")
c2.metric("Target attainment", pct(attainment))
c3.metric("Positive target gaps", money(gap))
c4.metric("Accounts above target", f"{(valid['Gap to Target (€)'] <= 0).sum()} / {len(valid)}")

st.divider()
left,right = st.columns([1.15, 1])
with left:
    st.subheader("Account performance")
    fig = px.bar(valid.sort_values("Target Attainment (%)"), x="Retail Account", y="Target Attainment (%)", color="Target Attainment (%)", hover_data=["Current Month Sales (€)", "Gap to Target (€)", "Sales Growth (%)"], labels={"Target Attainment (%)":"Target attainment", "Retail Account":"Retail account"}, color_continuous_scale="Tealgrn")
    fig.add_hline(y=1, line_dash="dash", line_color="#9a6b4f", annotation_text="100% target")
    fig.update_layout(height=360, margin=dict(l=10,r=10,t=20,b=10), xaxis_tickangle=-25, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Sales growth vs. target gap")
    fig2 = px.scatter(valid, x="Sales Growth (%)", y="Gap to Target (€)", size="Current Month Sales (€)", color="Stock Cover (weeks)", hover_name="Retail Account", hover_data=["Target Attainment (%)", "Hero SKU"], labels={"Sales Growth (%)":"Sales growth vs previous month", "Gap to Target (€)":"Gap to target (€)", "Stock Cover (weeks)":"Stock cover (weeks)"}, color_continuous_scale="Tealgrn")
    fig2.add_hline(y=0, line_dash="dash", line_color="#9a6b4f")
    fig2.add_vline(x=0, line_dash="dash", line_color="#9a6b4f")
    fig2.update_layout(height=360, margin=dict(l=10,r=10,t=20,b=10))
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("Ranked commercial opportunities")
ranked = valid.copy()
# Transparent heuristic: prioritize positive gap and declining growth, while flagging low stock as a constraint.
ranked["Priority signal"] = ranked.apply(lambda r: (max(r["Gap to Target (€)"],0) / max(r["Monthly Target (€)"],1)) * 0.45 + max(-r["Sales Growth (%)"],0)*0.35 + max(r.get("Hero SKU Sales Growth (%)",0) or 0,0)*0.20, axis=1)
ranked = ranked.sort_values("Priority signal", ascending=False)
rows=[]
for i,(_,r) in enumerate(ranked.iterrows(),1):
    action,risk=recommend(r)
    rows.append({"Rank":i,"Retail account":r["Retail Account"],"Sales":money(r["Current Month Sales (€)"]),"Target attainment":pct(r["Target Attainment (%)"]),"Gap":money(r["Gap to Target (€)"]),"Growth":pct(r["Sales Growth (%)"]),"Stock cover":f"{r['Stock Cover (weeks)']:g} wks","Recommended next step":action,"Main risk":risk})
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
st.caption("Ranking is a transparent demo heuristic, not a validated forecasting model. Review account context and data quality before taking action.")

st.divider()
st.subheader("BeautyKey AI · Ask the commercial assistant")
st.caption("Prototype mode: responses use the uploaded table and transparent rules; a production LLM connection would be needed for free-form AI reasoning.")
question = st.selectbox("Choose a demo task", ["Explain the top three account opportunities", "Create a 30-day action plan for the highest-priority account", "Draft a business review email", "Should we run a promotion next month?"])
if st.button("Generate recommendation", type="primary"):
    top = ranked.head(3)
    if question == "Explain the top three account opportunities":
        st.markdown("### Top opportunity signals")
        for _,r in top.iterrows():
            action,risk=recommend(r)
            st.markdown(f"**{r['Retail Account']}** — sales {money(r['Current Month Sales (€)'])}, target attainment {pct(r['Target Attainment (%)'])}, target gap {money(r['Gap to Target (€)'])}, month-on-month growth {pct(r['Sales Growth (%)'])}, stock cover {r['Stock Cover (weeks)']:g} weeks.")
            st.write(f"Suggested next step: {action} **Risk / unknown:** {risk}")
    elif question == "Create a 30-day action plan for the highest-priority account":
        r=top.iloc[0]; action,risk=recommend(r)
        st.markdown(f"### 30-day plan · {r['Retail Account']}")
        st.write(f"**Evidence:** target gap {money(r['Gap to Target (€)'])}; sales growth {pct(r['Sales Growth (%)'])}; stock cover {r['Stock Cover (weeks)']:g} weeks; hero SKU: {r.get('Hero SKU','not supplied')}.")
        st.write(f"**Days 1–5 · Account manager:** validate sales, stock and retailer context. **Days 6–15 · KAM + supply team:** {action} **Days 16–23 · Account manager + retailer:** agree the feasible action and owner. **Days 24–30 · KAM:** review sales, stock and target attainment versus baseline.")
        st.write("**Objective:** close part of the evidenced target gap without creating an unsupported profitability claim. **KPI:** sales, target attainment, stock cover, hero SKU sales. **Additional data:** sell-through, stock on hand, margin, promotional cost and retailer traffic/conversion.")
        st.write(f"**Main risk:** {risk}")
    elif question == "Draft a business review email":
        r=top.iloc[0]
        st.markdown(f"### Draft email · {r['Retail Account']}")
        st.code(f"Subject: Business review and growth opportunities — {r['Retail Account']}\n\nHi [Contact Name],\n\nI hope you are well. I would like to arrange a short business review to discuss recent performance and identify practical opportunities for the coming month. Our current reporting shows sales of {money(r['Current Month Sales (€)'])} against a target of {money(r['Monthly Target (€)'])}, and I would welcome the opportunity to review the drivers together.\n\nSuggested agenda:\n• Review sales performance and target progress\n• Discuss hero SKU trends, availability and replenishment\n• Review planned commercial activity and the information needed to assess its effectiveness\n• Agree next steps, owners and KPIs\n\nWould [proposed date/time] work for you?\n\nBest regards,\n[Your Name]\n[Title]", language="text")
        st.caption("Draft only — review figures, contact details and tone before sending.")
    else:
        st.markdown("### Promotion decision: not enough evidence to approve spend")
        st.write("Use the current workbook to identify accounts with a sales gap and inspect stock cover. Do not conclude a promotion will be profitable from sales growth alone.")
        st.write("Before recommending spend, obtain gross margin, promotional funding and execution costs, expected incremental sell-through, baseline sales, stock on hand, retailer media/placement details, and a method to estimate incrementality.")
        low = valid[valid["Stock Cover (weeks)"] < 3]
        if not low.empty:
            st.warning("Inventory caution: " + ", ".join(low["Retail Account"].astype(str).tolist()) + " have less than 3 weeks of stock cover in this demo. Validate replenishment before demand-driving activity.")

with st.expander("View the underlying account data"):
    display = df.copy()
    for c in ["Sales Growth (%)", "Target Attainment (%)", "Hero SKU Sales Growth (%)"]:
        if c in display: display[c] = display[c].map(pct)
    st.dataframe(display, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("BeautyKey AI prototype · fictional data only · human review required · no retailer communications or external system updates are executed.")
