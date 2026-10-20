import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="BeautyKey | Retail Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DESIGN SYSTEM ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
 --ink:#3F303A; --plum:#634653; --rose:#A87885;
 --ivory:#F8F5F1; --paper:#FFFFFF; --muted:#8C7D83;
 --line:#E9E0DB; --green:#397966;
}
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:var(--ivory); color:var(--ink);}
.block-container {max-width:1500px;padding-top:1.7rem;padding-bottom:3rem;}
[data-testid="stSidebar"] {background:#F0E8E3;border-right:1px solid #E4D8D2;}
h1,h2,h3 {color:var(--ink)!important;letter-spacing:-.4px;}
h1 {font-family:'Playfair Display',serif!important;font-weight:600!important;font-size:2.45rem!important;}
h2 {font-size:1.35rem!important;font-weight:700!important;}
h3 {font-size:1.05rem!important;font-weight:700!important;}
.bk-brand {display:flex;align-items:center;gap:12px;margin-bottom:8px;}
.bk-mark {width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;color:#F8F0E9;background:var(--plum);font-size:23px;}
.bk-wordmark {font-family:'Playfair Display',serif;font-size:24px;font-weight:600;color:var(--ink);line-height:1.05;}
.bk-subbrand {color:var(--muted);font-size:9px;letter-spacing:1.7px;font-weight:700;margin-top:5px;}
.bk-eyebrow {font-size:10px;letter-spacing:2px;color:var(--rose);font-weight:700;text-transform:uppercase;}
.bk-hero {background:linear-gradient(115deg,#F0E6E1 0%,#F8F5F1 70%);border:1px solid var(--line);border-radius:20px;padding:25px 28px;margin:12px 0 20px 0;}
.bk-hero-title {font-family:'Playfair Display',serif;font-size:30px;line-height:1.2;color:var(--ink);margin:6px 0 8px 0;}
.bk-hero-copy {color:#786970;font-size:13px;max-width:680px;line-height:1.65;}
.bk-pill {display:inline-block;background:#E5D5D5;color:#694955;border-radius:20px;padding:6px 10px;font-size:10px;font-weight:700;letter-spacing:.6px;}
.bk-card {background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:18px 20px;min-height:125px;box-shadow:0 3px 14px rgba(63,48,58,.025);}
.bk-kpi-label {font-size:10px;letter-spacing:1.2px;font-weight:700;color:var(--muted);text-transform:uppercase;}
.bk-kpi-value {font-size:29px;font-weight:700;letter-spacing:-1px;color:var(--ink);margin:8px 0 5px 0;}
.bk-kpi-note {font-size:11px;color:var(--muted);}
.bk-section-title {font-weight:700;font-size:15px;color:var(--ink);margin-bottom:3px;}
.bk-section-sub {color:var(--muted);font-size:11px;margin-bottom:14px;}
.bk-callout {background:#F3E9E8;border-left:3px solid var(--rose);border-radius:8px;padding:14px 16px;color:#59434D;font-size:12px;line-height:1.65;}
.bk-disclaimer {color:#94858A;font-size:10px;line-height:1.6;border-top:1px solid var(--line);padding-top:15px;margin-top:25px;}
[data-testid="stMetric"] {background:#fff;border:1px solid var(--line);padding:16px 18px;border-radius:15px;}
[data-testid="stMetricLabel"] {color:var(--muted)!important;font-size:11px!important;}
[data-testid="stMetricValue"] {color:var(--ink)!important;font-weight:700;}
.stButton>button {border-radius:9px;border:1px solid var(--plum);background:var(--plum);color:white;font-weight:600;padding:.55rem 1rem;}
.stButton>button:hover {background:#4D3642;color:white;border-color:#4D3642;}
[data-testid="stTabs"] [role="tab"] {color:var(--muted);font-weight:600;padding:10px 14px;}
[data-testid="stTabs"] [aria-selected="true"] {color:var(--plum)!important;border-bottom-color:var(--rose)!important;}
hr {border-color:var(--line)!important;}
[data-testid="stDataFrame"] {border:1px solid var(--line);border-radius:12px;overflow:hidden;}
@media(max-width:800px) {.bk-hero-title{font-size:24px;}.bk-kpi-value{font-size:23px;}}
</style>
""", unsafe_allow_html=True)

# ---------- FICTIONAL DEMO DATA ----------
DEMO_DATA = [
    {"Retail Account":"Sephora Spain","Account Type":"Prestige beauty","Monthly Target (€)":52000,"Current Month Sales (€)":46800,"Previous Month Sales (€)":44200,"Stock Cover (weeks)":3.5,"Hero SKU":"Vitamin C Serum","Hero SKU Sales Growth (%)":0.042,"Promotion Planned?":"No","Account Notes":"Strong growth, but below target; serum is a key driver."},
    {"Retail Account":"Douglas Spain","Account Type":"Prestige beauty","Monthly Target (€)":40000,"Current Month Sales (€)":43200,"Previous Month Sales (€)":40500,"Stock Cover (weeks)":4,"Hero SKU":"Barrier Repair Cream","Hero SKU Sales Growth (%)":0.07,"Promotion Planned?":"Yes","Account Notes":"Above target; opportunity to protect momentum and expand hero SKU."},
    {"Retail Account":"Lookfantastic Spain","Account Type":"Online beauty retailer","Monthly Target (€)":30000,"Current Month Sales (€)":24600,"Previous Month Sales (€)":27000,"Stock Cover (weeks)":2.5,"Hero SKU":"Retinol Night Serum","Hero SKU Sales Growth (%)":0.038,"Promotion Planned?":"No","Account Notes":"Sales declined versus previous month; investigate traffic, conversion, and assortment."},
    {"Retail Account":"El Corte Inglés Beauty","Account Type":"Department store","Monthly Target (€)":36000,"Current Month Sales (€)":32400,"Previous Month Sales (€)":31800,"Stock Cover (weeks)":5,"Hero SKU":"Hydrating Cleanser","Hero SKU Sales Growth (%)":0.065,"Promotion Planned?":"Yes","Account Notes":"Near target with positive growth; planned promotion needs ROI review."},
    {"Retail Account":"Primor","Account Type":"Beauty specialist","Monthly Target (€)":45000,"Current Month Sales (€)":40500,"Previous Month Sales (€)":38200,"Stock Cover (weeks)":2,"Hero SKU":"SPF 50 Fluid","Hero SKU Sales Growth (%)":0.025,"Promotion Planned?":"No","Account Notes":"Large target gap among specialist accounts; stock cover is tight."},
    {"Retail Account":"Druni","Account Type":"Beauty specialist","Monthly Target (€)":28000,"Current Month Sales (€)":29400,"Previous Month Sales (€)":27600,"Stock Cover (weeks)":6,"Hero SKU":"Vitamin C Serum","Hero SKU Sales Growth (%)":0.085,"Promotion Planned?":"No","Account Notes":"Above target with strong growth; potential for cross-sell and replenishment."},
    {"Retail Account":"Perfume's Club","Account Type":"Online beauty retailer","Monthly Target (€)":22000,"Current Month Sales (€)":17600,"Previous Month Sales (€)":19000,"Stock Cover (weeks)":3,"Hero SKU":"Retinol Night Serum","Hero SKU Sales Growth (%)":0.05,"Promotion Planned?":"Yes","Account Notes":"Below target and declining; assess whether planned promotion can recover sales."},
    {"Retail Account":"Marionnaud Spain","Account Type":"Prestige beauty","Monthly Target (€)":25000,"Current Month Sales (€)":23750,"Previous Month Sales (€)":23000,"Stock Cover (weeks)":4,"Hero SKU":"Barrier Repair Cream","Hero SKU Sales Growth (%)":0.045,"Promotion Planned?":"No","Account Notes":"Close to target; opportunity to improve merchandising and staff education."},
]

REQUIRED = [
    "Retail Account", "Monthly Target (€)", "Current Month Sales (€)",
    "Previous Month Sales (€)", "Stock Cover (weeks)"
]

def prepare_data(frame):
    frame = frame.copy()
    frame = frame.rename(columns={
        "Current Net Sales (€)": "Current Month Sales (€)",
        "Net Sales (€)": "Current Month Sales (€)",
        "Hero SKU Growth (%)": "Hero SKU Sales Growth (%)",
        "Priority Notes": "Account Notes"
    })

    for col in [
        "Monthly Target (€)", "Current Month Sales (€)",
        "Previous Month Sales (€)", "Stock Cover (weeks)",
        "Hero SKU Sales Growth (%)"
    ]:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")

    missing = [col for col in REQUIRED if col not in frame.columns]
    if missing:
        return None, missing

    frame["Sales Growth (%)"] = (
        frame["Current Month Sales (€)"] /
        frame["Previous Month Sales (€)"].replace(0, float("nan")) - 1
    )
    frame["Target Attainment (%)"] = (
        frame["Current Month Sales (€)"] /
        frame["Monthly Target (€)"].replace(0, float("nan"))
    )
    frame["Gap to Target (€)"] = (
        frame["Monthly Target (€)"] - frame["Current Month Sales (€)"]
    )
    return frame, []

def money(x):
    return f"€{x:,.0f}" if pd.notna(x) else "—"

def percent(x):
    return f"{x:+.1%}" if pd.notna(x) else "—"

def pct_plain(x):
    return f"{x:.1%}" if pd.notna(x) else "—"

def next_step(row):
    gap = row["Gap to Target (€)"]
    growth = row["Sales Growth (%)"]
    stock = row["Stock Cover (weeks)"]

    if stock < 3:
        return "Validate replenishment", "Low stock cover may constrain sales recovery."
    if growth < 0 and gap > 0:
        return "Review sales drivers", "The workbook does not identify the cause of the decline."
    if gap > 0:
        return "Build a targeted recovery plan", "Validate margin and incremental sales before any promotion."
    return "Protect momentum and cross-sell", "Validate sell-through and margin before expanding assortment."

# ---------- SIDEBAR / DATA MANAGEMENT ----------
with st.sidebar:
    st.markdown("""
    <div class='bk-brand'>
      <div class='bk-mark'>✦</div>
      <div>
        <div class='bk-wordmark'>BeautyKey</div>
        <div class='bk-subbrand'>RETAIL INTELLIGENCE</div>
      </div>
    </div>
    <hr>
    <div class='bk-eyebrow'>WORKSPACE</div>
    """, unsafe_allow_html=True)

    reporting_period = st.text_input("Reporting period", "September 2026")
    uploaded_file = st.file_uploader("Refresh account data (.xlsx)", type=["xlsx"])
    st.caption("Monthly workflow: upload the refreshed workbook to start a new analysis.")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("**Data status**")

    if uploaded_file:
        st.success("Workbook selected")
    else:
        st.info("Using fictional demonstration data")

    st.caption("No automatic data retrieval, CRM updates or emails are enabled.")

# ---------- LOAD DATA ----------
source = "Fictional demonstration dataset"
df = pd.DataFrame(DEMO_DATA)

if uploaded_file:
    try:
        workbook = pd.ExcelFile(uploaded_file)
        preferred = (
            "Account Targets" if "Account Targets" in workbook.sheet_names
            else "Current Sales" if "Current Sales" in workbook.sheet_names
            else workbook.sheet_names[0]
        )
        sheet_name = st.sidebar.selectbox(
            "Workbook sheet",
            workbook.sheet_names,
            index=workbook.sheet_names.index(preferred)
        )
        header = 2 if sheet_name in ["Account Targets", "Current Sales"] else 0
        uploaded_df = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=header)

        if sheet_name == "Account Targets" and "Current Sales" in workbook.sheet_names:
            try:
                sales_sheet = pd.read_excel(uploaded_file, sheet_name="Current Sales", header=2)
                sales_sheet = sales_sheet.rename(columns={"Net Sales (€)": "Current Month Sales (€)"})
                if {"Retail Account", "Current Month Sales (€)"}.issubset(sales_sheet.columns):
                    sums = sales_sheet.groupby("Retail Account", as_index=False)["Current Month Sales (€)"].sum()
                    uploaded_df = uploaded_df.drop(
                        columns=["Current Net Sales (€)", "Current Month Sales (€)"],
                        errors="ignore"
                    ).merge(sums, on="Retail Account", how="left")
            except Exception:
                pass

        df, missing = prepare_data(uploaded_df)
        if missing:
            st.sidebar.error("Missing required columns: " + ", ".join(missing))
            st.stop()

        source = f"Uploaded workbook · {sheet_name}"

    except Exception as exc:
        st.error(f"Unable to read workbook: {exc}")
        st.stop()

if df is None:
    st.stop()

df, missing = prepare_data(df)
if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.stop()

df = df.dropna(subset=[
    "Monthly Target (€)", "Current Month Sales (€)", "Previous Month Sales (€)"
])
df = df[df["Monthly Target (€)"] > 0]

if df.empty:
    st.error("No valid account rows found. Check the uploaded workbook.")
    st.stop()

# ---------- TRANSPARENT OPPORTUNITY SCORING ----------
hero_growth = df.get("Hero SKU Sales Growth (%)", pd.Series(0, index=df.index)).fillna(0)
df["Priority score"] = (
    (df["Gap to Target (€)"].clip(lower=0) / df["Monthly Target (€)"]) * 0.55
    + (-df["Sales Growth (%)"]).clip(lower=0) * 0.30
    + hero_growth.clip(lower=0) * 0.15
)

actions = df.apply(next_step, axis=1)
df["Recommended action"] = [a[0] for a in actions]
df["Risk / unknown"] = [a[1] for a in actions]
ranked = df.sort_values("Priority score", ascending=False).copy()

# ---------- BRAND HEADER ----------
st.markdown(
    "<div class='bk-eyebrow'>COMMERCIAL PERFORMANCE · ACCOUNT GROWTH</div>",
    unsafe_allow_html=True
)

header_left, header_right = st.columns([4, 1])
with header_left:
    st.title("BeautyKey Intelligence")
    st.markdown(
        "Portfolio performance, account opportunities and recommended next actions — in one workspace."
    )
with header_right:
    st.markdown(
        "<div style='text-align:right;padding-top:18px'><span class='bk-pill'>ACADEMIC DEMO</span></div>",
        unsafe_allow_html=True
    )

st.markdown(f"""
<div class='bk-hero'>
  <div class='bk-eyebrow'>YOUR PORTFOLIO AT A GLANCE</div>
  <div class='bk-hero-title'>Clarity for your next commercial move.</div>
  <div class='bk-hero-copy'>
    Review performance against target, identify accounts that may need attention,
    and turn the data into practical next steps.
    <b>Reporting period:</b> {reporting_period} &nbsp; · &nbsp;
    <b>Source:</b> {source}
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- EXECUTIVE KPIs ----------
sales_total = df["Current Month Sales (€)"].sum()
previous_total = df["Previous Month Sales (€)"].sum()
target_total = df["Monthly Target (€)"].sum()
attainment = sales_total / target_total if target_total else 0
growth_total = sales_total / previous_total - 1 if previous_total else 0
positive_gap = df["Gap to Target (€)"].clip(lower=0).sum()
above = int((df["Gap to Target (€)"] <= 0).sum())
alerts = int((
    (df["Stock Cover (weeks)"] < 3) |
    ((df["Sales Growth (%)"] < 0) & (df["Gap to Target (€)"] > 0))
).sum())

kpis = st.columns(4)
metric_data = [
    ("NET SALES", money(sales_total), f"{growth_total:+.1%} vs previous period"),
    ("TARGET ATTAINMENT", pct_plain(attainment), f"{(attainment-1)*100:+.1f} pp vs target"),
    ("REMAINING TARGET GAP", money(positive_gap), "Sum of positive account-level gaps"),
    ("ACCOUNTS ABOVE TARGET", f"{above} / {len(df)}", f"{alerts} accounts flagged for review")
]

for col, (label, value, note) in zip(kpis, metric_data):
    with col:
        st.markdown(f"""
        <div class='bk-card'>
          <div class='bk-kpi-label'>{label}</div>
          <div class='bk-kpi-value'>{value}</div>
          <div class='bk-kpi-note'>{note}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------- PRODUCT NAVIGATION ----------
t_overview, t_accounts, t_opportunities, t_assistant, t_data = st.tabs([
    "Overview", "Account intelligence", "Growth opportunities",
    "AI workspace", "Data & methodology"
])

with t_overview:
    st.markdown(
        "<div class='bk-section-title'>Portfolio performance</div>"
        "<div class='bk-section-sub'>A high-level view of target delivery and sales momentum.</div>",
        unsafe_allow_html=True
    )
    col1, col2 = st.columns([1.15, 1])

    with col1:
        chart_df = df.sort_values("Target Attainment (%)")
        fig = px.bar(
            chart_df, x="Retail Account", y="Target Attainment (%)",
            color="Target Attainment (%)",
            hover_data=["Current Month Sales (€)", "Gap to Target (€)", "Sales Growth (%)"],
            color_continuous_scale=["#E8D4D1", "#C99EAA", "#80515B", "#493640"],
            labels={"Target Attainment (%)": "Target attainment", "Retail Account": "Retail account"}
        )
        fig.add_hline(
            y=1, line_dash="dash", line_color="#B89A68",
            annotation_text="100% target"
        )
        fig.update_layout(
            height=360, margin=dict(l=8, r=8, t=15, b=8),
            xaxis_tickangle=-25, coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#3F303A"),
            yaxis_tickformat=".0%"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        scatter = px.scatter(
            df, x="Sales Growth (%)", y="Gap to Target (€)",
            size="Current Month Sales (€)", color="Stock Cover (weeks)",
            hover_name="Retail Account", hover_data=["Target Attainment (%)"],
            color_continuous_scale=["#D9E8DF", "#77B9A4", "#397966", "#634653"],
            labels={
                "Sales Growth (%)": "Sales growth vs previous period",
                "Gap to Target (€)": "Gap to target (€)",
                "Stock Cover (weeks)": "Stock cover (weeks)"
            }
        )
        scatter.add_hline(y=0, line_dash="dash", line_color="#B89A68")
        scatter.add_vline(x=0, line_dash="dash", line_color="#B89A68")
        scatter.update_layout(
            height=360, margin=dict(l=8, r=8, t=15, b=8),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#3F303A")
        )
        st.plotly_chart(scatter, use_container_width=True)

    st.markdown(
        "<div class='bk-section-title'>Recommended management focus</div>"
        "<div class='bk-section-sub'>Priority signals based on sales gap, momentum and stock-cover data.</div>",
        unsafe_allow_html=True
    )
    focus = ranked.iloc[0]
    st.markdown(f"""
    <div class='bk-callout'>
      <b>{focus['Retail Account']}</b> is the highest-ranked account for review under
      the current demo scoring. Sales are {money(focus['Current Month Sales (€)'])},
      target attainment is {pct_plain(focus['Target Attainment (%)'])}, and stock
      cover is {focus['Stock Cover (weeks)']:g} weeks.<br><br>
      <b>Suggested next step:</b> {focus['Recommended action']}.
      This is a prioritization signal, not a forecast or proof of incremental revenue.
    </div>
    """, unsafe_allow_html=True)

with t_accounts:
    st.markdown(
        "<div class='bk-section-title'>Account intelligence</div>"
        "<div class='bk-section-sub'>Compare performance and review the context behind each recommendation.</div>",
        unsafe_allow_html=True
    )
    account_options = sorted(df["Retail Account"].dropna().unique().tolist())
    selected_account = st.selectbox("Select an account", account_options)
    account = df[df["Retail Account"] == selected_account].iloc[0]

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Current sales", money(account["Current Month Sales (€)"]))
    a2.metric("Target attainment", pct_plain(account["Target Attainment (%)"]))
    a3.metric("Sales growth", percent(account["Sales Growth (%)"]))
    a4.metric("Stock cover", f"{account['Stock Cover (weeks)']:g} weeks")

    st.markdown("### Account review")
    st.write(
        f"**Account type:** {account.get('Account Type', 'Not provided')} · "
        f"**Hero SKU:** {account.get('Hero SKU', 'Not provided')}"
    )
    st.write(
        f"**Target:** {money(account['Monthly Target (€)'])} · "
        f"**Gap to target:** {money(account['Gap to Target (€)'])}"
    )
    st.write(f"**Account context:** {account.get('Account Notes', 'No notes supplied.')}")
    st.markdown(f"""
    <div class='bk-callout'>
      <b>Recommended next action</b><br>{account['Recommended action']}<br><br>
      <b>Risk / unknown</b><br>{account['Risk / unknown']}
    </div>
    """, unsafe_allow_html=True)

with t_opportunities:
    st.markdown(
        "<div class='bk-section-title'>Growth opportunities</div>"
        "<div class='bk-section-sub'>A transparent prioritization heuristic for deciding which accounts to review first.</div>",
        unsafe_allow_html=True
    )
    st.caption(
        "Priority score combines positive target gap relative to target, negative sales growth, "
        "and positive hero-SKU growth. It is illustrative, not statistically validated."
    )

    opportunity_table = ranked[[
        "Retail Account", "Current Month Sales (€)", "Monthly Target (€)",
        "Target Attainment (%)", "Gap to Target (€)", "Sales Growth (%)",
        "Stock Cover (weeks)", "Recommended action"
    ]].copy()

    opportunity_table = opportunity_table.rename(columns={
        "Retail Account": "Account",
        "Current Month Sales (€)": "Sales (€)",
        "Monthly Target (€)": "Target (€)",
        "Target Attainment (%)": "Attainment",
        "Gap to Target (€)": "Gap (€)",
        "Sales Growth (%)": "Growth",
        "Stock Cover (weeks)": "Stock (weeks)",
        "Recommended action": "Recommended next step"
    })

    st.dataframe(opportunity_table, use_container_width=True, hide_index=True)
    st.download_button(
        "Export opportunity review (CSV)",
        opportunity_table.to_csv(index=False).encode("utf-8"),
        file_name="beautykey_opportunity_review.csv",
        mime="text/csv"
    )

with t_assistant:
    st.markdown(
        "<div class='bk-section-title'>BeautyKey assistant</div>"
        "<div class='bk-section-sub'>Turn account data into structured next steps using transparent rules.</div>",
        unsafe_allow_html=True
    )

    task = st.selectbox("What would you like to prepare?", [
        "Summarize the top three opportunities",
        "Build a 30-day action plan",
        "Draft a retailer business-review email",
        "Assess whether to run a promotion"
    ])
    chosen = st.selectbox(
        "Account context",
        ["Highest-priority account"] + sorted(df["Retail Account"].unique().tolist())
    )
    target_row = ranked.iloc[0] if chosen == "Highest-priority account" else df[df["Retail Account"] == chosen].iloc[0]

    if st.button("Generate account brief", key="assistant_generate"):
        if task == "Summarize the top three opportunities":
            for _, row in ranked.head(3).iterrows():
                st.markdown(
                    f"**{row['Retail Account']}** · {money(row['Current Month Sales (€)'])} sales · "
                    f"{pct_plain(row['Target Attainment (%)'])} target attainment · "
                    f"{money(row['Gap to Target (€)'])} gap"
                )
                st.write(
                    f"Next step: {row['Recommended action']}. "
                    f"Unknown to validate: {row['Risk / unknown']}"
                )

        elif task == "Build a 30-day action plan":
            st.markdown(f"### 30-day action plan · {target_row['Retail Account']}")
            st.write(
                f"**Evidence:** sales {money(target_row['Current Month Sales (€)'])}; "
                f"target {money(target_row['Monthly Target (€)'])}; "
                f"attainment {pct_plain(target_row['Target Attainment (%)'])}; "
                f"stock cover {target_row['Stock Cover (weeks)']:g} weeks."
            )
            st.markdown("""
            **Days 1–5 · Validate**
            - Confirm the latest sales and target data.
            - Check stock on hand, sell-through and missing retailer context.
            
            **Days 6–15 · Align**
            """)
            st.write(f"- {target_row['Recommended action']}.")
            st.markdown("""
            - Agree the account owner, retailer contact and measurable next step.

            **Days 16–23 · Execute**
            - Coordinate agreed assortment, replenishment, merchandising or communication actions.
            - Do not commit promotional spend until margin and incremental impact are assessed.

            **Days 24–30 · Review**
            - Compare sales, target attainment, stock cover and hero-SKU performance with baseline.
            - Document outcomes, learnings and follow-up owner.
            """)
            st.info("Suggested workflow only. Dates, owners and commercial commitments require human confirmation.")

        elif task == "Draft a retailer business-review email":
            email = f"""Subject: Business review and growth opportunities — {target_row['Retail Account']}

Hi [Contact Name],

I hope you are well. I would like to arrange a short business review to discuss recent performance and identify practical opportunities for the coming month.

Our current reporting shows sales of {money(target_row['Current Month Sales (€)'])} against a target of {money(target_row['Monthly Target (€)'])}. I would welcome the opportunity to review the drivers together.

Suggested agenda:
• Review sales performance and target progress
• Discuss hero SKU trends, availability and replenishment
• Review planned commercial activity and the data needed to assess its effectiveness
• Agree next steps, owners and KPIs

Would [proposed date/time] work for you?

Best regards,
[Your Name]
[Title]"""
            st.text_area("Email draft — review before sending", email, height=310)
            st.download_button(
                "Download email draft", email,
                file_name="beautykey_retailer_email.txt",
                mime="text/plain"
            )
            st.caption("Draft only. The app does not send emails.")

        else:
            st.markdown("### Promotion assessment · evidence required")
            st.write(
                "Sales gaps alone do not establish whether a promotion will be profitable. "
                "Before recommending spend, gather gross margin, promotional costs and funding, "
                "expected incremental sell-through, baseline sales, stock on hand, and a way to estimate incrementality."
            )
            if target_row["Stock Cover (weeks)"] < 3:
                st.warning("Stock cover is below 3 weeks. Validate replenishment before demand-driving activity.")
            else:
                st.info("No low-stock warning from the supplied stock-cover figure; inventory and profitability still need validation.")

with t_data:
    st.markdown(
        "<div class='bk-section-title'>Data management & methodology</div>"
        "<div class='bk-section-sub'>Understand the monthly refresh process, source fields and limitations.</div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    #### Monthly refresh workflow
    1. Export the latest approved account sales and target data.
    2. Update the Excel workbook and check retailer names, periods, currency and missing values.
    3. Upload the workbook using the sidebar.
    4. Review the data and recommendations before acting on them.

    #### Current prototype boundaries
    - Data is read from a user-uploaded workbook or the embedded fictional demo dataset.
    - The assistant uses rule-based logic; it is not connected to a live large language model.
    - No automatic retrieval from retailer systems, CRM updates, email sending or external actions occur.
    - Priority scores are illustrative heuristics, not a validated forecast.
    - Recommendations require human review and additional context such as margin, sell-through, inventory and promotional costs.
    """)

    st.markdown("#### Account data")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download current account dataset (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        file_name="beautykey_account_data.csv",
        mime="text/csv"
    )

# ---------- DISCLAIMER ----------
st.markdown("""
<div class='bk-disclaimer'>
<b>Academic prototype disclaimer.</b>
BeautyKey AI is an educational prototype developed for an academic project.
All retailer, sales, product and performance data are fictional and created for
demonstration purposes. The prototype is not affiliated with or endorsed by any real company.
<br><br>
BeautyKey AI · Retail Intelligence · Human review required · No external system actions are executed.
</div>
""", unsafe_allow_html=True)
