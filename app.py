
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BeautyKey AI", page_icon="✨", layout="wide")

# ---------- PREMIUM BEAUTY-TECH DESIGN ----------
st.markdown("""
<style>
:root {
    --ivory: #FAF7F3;
    --rose: #80515B;
    --plum: #493640;
    --muted: #806D76;
    --border: #EADFD9;
}
.stApp { background: var(--ivory); color: var(--plum); }
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1500px; }
h1, h2, h3 { color: var(--plum) !important; letter-spacing: -0.45px; }
h1 { font-weight: 760 !important; }
[data-testid="stMetric"] {
    background: white; border: 1px solid var(--border);
    padding: 20px 18px; border-radius: 16px;
    box-shadow: 0 3px 12px rgba(73,54,64,.045);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; }
[data-testid="stMetricValue"] { color: var(--plum) !important; font-weight: 700; }
[data-testid="stSidebar"] { background: #F0E7E2; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--plum) !important; }
.stButton > button {
    background: var(--rose); color: white; border: 1px solid var(--rose);
    border-radius: 10px; padding: .55rem 1.15rem; font-weight: 600;
}
.stButton > button:hover { background: #65404A; color: white; border-color: #65404A; }
hr { border-color: var(--border) !important; }
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"] { border-radius: 12px; }
.bk-eyebrow { color: #92766F; font-size: 12px; letter-spacing: 2.2px; font-weight: 700; }
.bk-disclaimer {
    background: #F0E7E2; border: 1px solid #E4D3CC;
    border-left: 4px solid #80515B; padding: 14px 17px;
    border-radius: 10px; color: #59454E; font-size: 13px;
    line-height: 1.55; margin: 12px 0 22px 0;
}
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

REQUIRED = [
    "Retail Account", "Monthly Target (€)", "Current Month Sales (€)",
    "Previous Month Sales (€)", "Stock Cover (weeks)"
]

def prepare(df):
    df = df.copy()
    numeric = [
        "Monthly Target (€)", "Current Month Sales (€)",
        "Previous Month Sales (€)", "Stock Cover (weeks)",
        "Hero SKU Sales Growth (%)"
    ]
    for col in numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Sales Growth (%)"] = (
        df["Current Month Sales (€)"] /
        df["Previous Month Sales (€)"].replace(0, float("nan")) - 1
    )
    df["Target Attainment (%)"] = (
        df["Current Month Sales (€)"] /
        df["Monthly Target (€)"].replace(0, float("nan"))
    )
    df["Gap to Target (€)"] = (
        df["Monthly Target (€)"] - df["Current Month Sales (€)"]
    )
    return df

def money(value):
    return f"€{value:,.0f}" if pd.notna(value) else "—"

def pct(value):
    return f"{value:.1%}" if pd.notna(value) else "—"

def recommend(row):
    gap = row["Gap to Target (€)"]
    growth = row["Sales Growth (%)"]
    stock = row["Stock Cover (weeks)"]

    if stock < 3:
        action = "Check inventory and agree replenishment before adding a demand-driving promotion."
        risk = "Low stock cover may constrain sales recovery."
    elif growth < 0 and gap > 0:
        action = "Review traffic, conversion, assortment and promotional mechanics with the retailer."
        risk = "The reason for the sales decline is not established by this workbook."
    elif gap > 0 and growth >= 0:
        action = "Build a targeted recovery plan around the hero SKU; review merchandising and cross-sell."
        risk = "Margin and incremental-sales data are unavailable to validate promotion ROI."
    else:
        action = "Protect momentum and assess selective assortment expansion or cross-sell."
        risk = "Expansion should be validated against sell-through and margin."
    return action, risk

# ---------- HEADER AND DISCLAIMER ----------
st.markdown(
    "<div class='bk-eyebrow'>COMMERCIAL INTELLIGENCE</div>",
    unsafe_allow_html=True
)
st.title("✨ BeautyKey AI")
st.caption("AI Key Account Manager for multi-brand beauty retail")

st.markdown("""
<div class="bk-disclaimer">
<strong>Academic prototype disclaimer</strong><br>
BeautyKey AI is an educational prototype developed for an academic project.
All retailer, sales, product and performance data are fictional and created
for demonstration purposes. The prototype is not affiliated with or
endorsed by any real company.
</div>
""", unsafe_allow_html=True)

# ---------- REPORTING WORKSPACE ----------
with st.sidebar:
    st.header("Reporting workspace")
    uploaded = st.file_uploader(
        "Upload the updated Excel workbook",
        type=["xlsx"]
    )
    period = st.text_input(
        "Reporting period",
        value="Demo period — replace with actual month"
    )
    st.info(
        "Monthly workflow: a human uploads the refreshed workbook and starts "
        "the analysis. This prototype does not automatically retrieve data or send reports."
    )
    st.markdown("**Data source**")
    st.caption("Uploaded workbook, or the embedded fictional demo dataset.")

source = "Embedded fictional demo data"

if uploaded:
    try:
        xl = pd.ExcelFile(uploaded)
        preferred = (
            "Account Targets" if "Account Targets" in xl.sheet_names
            else ("Sales Data" if "Sales Data" in xl.sheet_names else xl.sheet_names[0])
        )
        default_index = xl.sheet_names.index(preferred)
        sheet = st.selectbox(
            "Select sales sheet",
            xl.sheet_names,
            index=default_index
        )

        header_row = 2 if sheet in ["Account Targets", "Current Sales"] else 0
        raw = pd.read_excel(uploaded, sheet_name=sheet, header=header_row)

        if (
            sheet == "Account Targets"
            and {"Retail Account", "Monthly Target (€)",
                 "Previous Month Sales (€)", "Stock Cover (weeks)"}.issubset(raw.columns)
            and "Current Sales" in xl.sheet_names
        ):
            current = pd.read_excel(uploaded, sheet_name="Current Sales", header=2)
            if {"Retail Account", "Net Sales (€)"}.issubset(current.columns):
                aggregations = {"Net Sales (€)": "sum"}
                if "Previous Month Sales (€)" in current.columns:
                    aggregations["Previous Month Sales (€)"] = "sum"
                totals = current.groupby("Retail Account", as_index=False).agg(aggregations)

                raw = raw.drop(
                    columns=[
                        "Current Net Sales (€)", "Sales Growth (%)",
                        "Target Attainment (%)", "Gap to Target (€)"
                    ],
                    errors="ignore"
                )
                raw = raw.merge(
                    totals,
                    on="Retail Account",
                    how="left",
                    suffixes=("", "_from_sales")
                )
                if "Net Sales (€)" in raw.columns:
                    raw = raw.rename(columns={"Net Sales (€)": "Current Month Sales (€)"})
                if "Previous Month Sales (€)_from_sales" in raw.columns:
                    raw["Previous Month Sales (€)"] = (
                        raw["Previous Month Sales (€)_from_sales"]
                        .fillna(raw["Previous Month Sales (€)"])
                    )
                    raw = raw.drop(columns=["Previous Month Sales (€)_from_sales"])
                raw = raw.rename(columns={
                    "Hero SKU Growth (%)": "Hero SKU Sales Growth (%)",
                    "Priority Notes": "Account Notes"
                })
        else:
            raw = raw.rename(columns={
                "Current Net Sales (€)": "Current Month Sales (€)",
                "Net Sales (€)": "Current Month Sales (€)",
                "Hero SKU Growth (%)": "Hero SKU Sales Growth (%)",
                "Priority Notes": "Account Notes"
            })

        missing = [col for col in REQUIRED if col not in raw.columns]
        if missing:
            st.error(
                "The selected sheet is missing required columns: "
                + ", ".join(missing)
                + ". For the complete BeautyKey database, select 'Account Targets'."
            )
            st.stop()

        df = raw
        source = f"Uploaded workbook · {sheet}"

    except Exception as error:
        st.error(f"Could not read workbook: {error}")
        st.stop()
else:
    df = pd.DataFrame(DEMO_DATA)

df = prepare(df)

if df["Retail Account"].duplicated().any():
    st.warning("Duplicate retailer names detected. Check whether these are separate records.")

if df[REQUIRED].isna().any().any():
    st.warning("Some required values are missing or non-numeric. Check the workbook.")

if (df["Monthly Target (€)"] <= 0).any():
    st.warning("Targets must be greater than zero for reliable target-attainment calculations.")

valid = df.dropna(subset=[
    "Monthly Target (€)", "Current Month Sales (€)",
    "Previous Month Sales (€)"
])
valid = valid[valid["Monthly Target (€)"] > 0]

if valid.empty:
    st.error("No valid account records are available. Please check the uploaded workbook.")
    st.stop()

target = valid["Monthly Target (€)"].sum()
sales = valid["Current Month Sales (€)"].sum()
prev = valid["Previous Month Sales (€)"].sum()
gap = valid["Gap to Target (€)"].clip(lower=0).sum()
attainment = sales / target if target else 0
growth = sales / prev - 1 if prev else 0

st.markdown(
    f"**Period:** {period} &nbsp; · &nbsp; "
    f"**Source:** {source} &nbsp; · &nbsp; **Accounts:** {len(valid)}"
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Current sales", money(sales), f"{growth:+.1%} vs previous month")
c2.metric("Target attainment", pct(attainment))
c3.metric("Positive target gaps", money(gap))
c4.metric(
    "Accounts above target",
    f"{(valid['Gap to Target (€)'] <= 0).sum()} / {len(valid)}"
)

# ---------- DASHBOARD CHARTS ----------
st.divider()
left, right = st.columns([1.15, 1])

with left:
    st.subheader("Account performance")
    fig = px.bar(
        valid.sort_values("Target Attainment (%)"),
        x="Retail Account",
        y="Target Attainment (%)",
        color="Target Attainment (%)",
        hover_data=[
            "Current Month Sales (€)", "Gap to Target (€)", "Sales Growth (%)"
        ],
        labels={
            "Target Attainment (%)": "Target attainment",
            "Retail Account": "Retail account"
        },
        color_continuous_scale=["#E8D4D1", "#C99EAA", "#80515B", "#493640"]
    )
    fig.add_hline(
        y=1, line_dash="dash", line_color="#B89A68",
        annotation_text="100% target"
    )
    fig.update_layout(
        height=360, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_tickangle=-25, coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#493640"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Sales growth vs. target gap")
    fig2 = px.scatter(
        valid,
        x="Sales Growth (%)",
        y="Gap to Target (€)",
        size="Current Month Sales (€)",
        color="Stock Cover (weeks)",
        hover_name="Retail Account",
        hover_data=["Target Attainment (%)"],
        labels={
            "Sales Growth (%)": "Sales growth vs previous month",
            "Gap to Target (€)": "Gap to target (€)",
            "Stock Cover (weeks)": "Stock cover (weeks)"
        },
        color_continuous_scale=["#B7DCCB", "#65BFA4", "#2E8D83", "#493640"]
    )
    fig2.add_hline(y=0, line_dash="dash", line_color="#B89A68")
    fig2.add_vline(x=0, line_dash="dash", line_color="#B89A68")
    fig2.update_layout(
        height=360, margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#493640"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------- RANKED OPPORTUNITIES ----------
st.divider()
st.subheader("Ranked commercial opportunities")

ranked = valid.copy()
ranked["Priority signal"] = ranked.apply(
    lambda r: (
        (max(r["Gap to Target (€)"], 0) / max(r["Monthly Target (€)"], 1)) * 0.45
        + max(-r["Sales Growth (%)"], 0) * 0.35
        + max(r.get("Hero SKU Sales Growth (%)", 0) or 0, 0) * 0.20
    ),
    axis=1
)
ranked = ranked.sort_values("Priority signal", ascending=False)

rows = []
for i, (_, row) in enumerate(ranked.iterrows(), 1):
    action, risk = recommend(row)
    rows.append({
        "Rank": i,
        "Retail account": row["Retail Account"],
        "Sales": money(row["Current Month Sales (€)"]),
        "Target attainment": pct(row["Target Attainment (%)"]),
        "Gap": money(row["Gap to Target (€)"]),
        "Growth": pct(row["Sales Growth (%)"]),
        "Stock cover": f"{row['Stock Cover (weeks)']:g} weeks",
        "Recommended next step": action,
        "Main risk": risk
    })

st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
st.caption(
    "The ranking is a transparent demo heuristic, not a validated forecasting model. "
    "Review account context and data quality before taking action."
)

# ---------- COMMERCIAL ASSISTANT ----------
st.divider()
st.subheader("✨ BeautyKey AI · Commercial assistant")
st.caption(
    "Prototype mode: responses use the uploaded table and transparent rules. "
    "A production LLM connection would be required for free-form AI reasoning."
)

question = st.selectbox(
    "Choose a demo task",
    [
        "Explain the top three account opportunities",
        "Create a 30-day action plan for the highest-priority account",
        "Draft a business review email",
        "Should we run a promotion next month?"
    ]
)

if st.button("Generate recommendation", type="primary"):
    top = ranked.head(3)

    if question == "Explain the top three account opportunities":
        st.markdown("### Top opportunity signals")
        for _, row in top.iterrows():
            action, risk = recommend(row)
            st.markdown(
                f"**{row['Retail Account']}** — sales "
                f"{money(row['Current Month Sales (€)'])}, target attainment "
                f"{pct(row['Target Attainment (%)'])}, target gap "
                f"{money(row['Gap to Target (€)'])}, month-on-month growth "
                f"{pct(row['Sales Growth (%)'])}, stock cover "
                f"{row['Stock Cover (weeks)']:g} weeks."
            )
            st.write(f"Suggested next step: {action} **Risk / unknown:** {risk}")

    elif question == "Create a 30-day action plan for the highest-priority account":
        row = top.iloc[0]
        action, risk = recommend(row)
        st.markdown(f"### 30-day plan · {row['Retail Account']}")
        st.write(
            f"**Evidence:** target gap {money(row['Gap to Target (€)'])}; "
            f"sales growth {pct(row['Sales Growth (%)'])}; "
            f"stock cover {row['Stock Cover (weeks)']:g} weeks; "
            f"hero SKU: {row.get('Hero SKU', 'not supplied')}."
        )
        st.write(
            f"**Days 1–5 · Account manager:** validate sales, stock and retailer context. "
            f"**Days 6–15 · KAM + supply team:** {action} "
            f"**Days 16–23 · Account manager + retailer:** agree the feasible action and owner. "
            f"**Days 24–30 · KAM:** review sales, stock and target attainment versus baseline."
        )
        st.write(
            "**Objective:** close part of the evidenced target gap without making "
            "unsupported profitability claims. **KPIs:** sales, target attainment, "
            "stock cover and hero SKU sales. **Additional data needed:** sell-through, "
            "stock on hand, margin, promotional cost and retailer traffic/conversion."
        )
        st.write(f"**Main risk:** {risk}")

    elif question == "Draft a business review email":
        row = top.iloc[0]
        email = f"""Subject: Business review and growth opportunities — {row['Retail Account']}

Hi [Contact Name],

I hope you are well. I would like to arrange a short business review to discuss recent performance and identify practical opportunities for the coming month.

Our current reporting shows sales of {money(row['Current Month Sales (€)'])} against a target of {money(row['Monthly Target (€)'])}. I would welcome the opportunity to review the drivers together.

Suggested agenda:
• Review sales performance and target progress
• Discuss hero SKU trends, availability and replenishment
• Review planned commercial activity and the information needed to assess its effectiveness
• Agree next steps, owners and KPIs

Would [proposed date/time] work for you?

Best regards,
[Your Name]
[Title]"""
        st.markdown(f"### Draft email · {row['Retail Account']}")
        st.code(email, language="text")
        st.caption("Draft only. Review the figures, contact details and tone before sending.")

    else:
        st.markdown("### Promotion decision: more evidence needed")
        st.write(
            "The workbook can identify sales gaps and stock constraints, but it cannot "
            "establish whether a promotion will be profitable."
        )
        st.write(
            "Before approving spend, obtain gross margin, promotional funding and costs, "
            "expected incremental sell-through, baseline sales, stock on hand, retailer "
            "media/placement details, and a method to estimate incrementality."
        )
        low_stock = valid[valid["Stock Cover (weeks)"] < 3]
        if not low_stock.empty:
            st.warning(
                "Inventory caution: "
                + ", ".join(low_stock["Retail Account"].astype(str))
                + " have less than 3 weeks of stock cover in this demo. "
                "Validate replenishment before demand-driving activity."
            )

with st.expander("View the underlying account data"):
    display = df.copy()
    for col in [
        "Sales Growth (%)", "Target Attainment (%)", "Hero SKU Sales Growth (%)"
    ]:
        if col in display.columns:
            display[col] = display[col].map(pct)
    st.dataframe(display, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption(
    "BeautyKey AI prototype · fictional data only · human review required · "
    "no retailer communications or external system updates are executed."
)
