import streamlit as st
import pandas as pd

# ---------------------------
# 1) THEME / CSS (inject once)
# ---------------------------
COLOR_DISRUPTION = "#cf5442"   # New Lines red
COLOR_PROGRESSION = "#3b668c"  # New Lines blue
COLOR_NEUTRAL = "#1b1725"      # dark
NL_GOLD = "#bfa359"
NL_CREAM = "#f1f0ec"
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');

/* ---------- GLOBAL FONT ---------- */
html, body, [class*="css"] {{
  font-family: 'Roboto', sans-serif;
}}

/* ---------- MAIN APP BACKGROUND ---------- */
.stApp {{
  background-color: #f1f0ec;
}}
</style>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<style>
/* Sidebar background */
section[data-testid="stSidebar"]{
  background-color:#1b1725;
}

/* --- Keep sidebar NAV / page titles readable (white) --- */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] .stPageLink,
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] *{
  color:#ffffff !important;
  opacity:1 !important;
}

/* --- Filters header + labels (white) --- */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stCaption{
  color:#ffffff !important;
  opacity:1 !important;
}

/* --- Selectbox input: WHITE BOX + BLACK TEXT --- */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div{
  background:#ffffff !important;
  border-radius:8px !important;
}

/* Selected value + placeholder */
section[data-testid="stSidebar"] div[data-baseweb="select"] *{
  color:#000000 !important;
}

/* Dropdown menu background */
div[data-baseweb="popover"] div[role="listbox"]{
  background:#ffffff !important;
}

/* Dropdown option text */
div[data-baseweb="popover"] div[role="option"] *{
  color:#000000 !important;
}

/* Hover */
div[data-baseweb="popover"] div[role="option"]:hover{
  background:rgba(0,0,0,0.08) !important;
}

/* Reset button (optional) */
section[data-testid="stSidebar"] button{
  background:#ffffff !important;
  color:#000000 !important;
  border-radius:8px !important;
}

/* Header bar background */
header[data-testid="stHeader"]{
  background-color: rgba(191, 163, 89, 0.55) !important;
}

/* Fixed logo position at bottom of sidebar */
section[data-testid="stSidebar"] {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

section[data-testid="stSidebar"] > div:nth-child(n+2) {
  flex: 1;
  overflow-y: auto;
}

section[data-testid="stSidebar"] img {
  position: fixed;
  bottom: 60px;
  left: 10px;
  right: 10px;
  width: calc(100% - 20px);
  max-width: 280px;
  z-index: 999;
}
</style>
""",
    unsafe_allow_html=True
)

# Logo at bottom of sidebar
st.sidebar.divider()
st.sidebar.image("assets/footer_logo.svg", use_container_width=True)

# ---------------------------
# DATA
# ---------------------------
DATA_PATH = "data/Monitor - Gender Equality - Core Indicator Outputs 2025.csv"

df = pd.read_csv(DATA_PATH)


DATE_COL = "Date"
INDICATOR_COL = "Core Indicator"
HEADLINE_COL = "Development"
SOURCE_COL = "Link"

df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
df = df.dropna(subset=[DATE_COL, INDICATOR_COL]).copy()

# ---------------------------
# HEADER
# ---------------------------
st.title("🧭 Core Indicator Climate")
st.caption(
    "Core indicators function as a background climate layer. "
    "They contextualize policy developments and inform analyst judgment, "
    "but are not scored as discrete events."
)

# ---------------------------
# SIDEBAR FILTER
# ---------------------------
st.sidebar.header("Filter")

indicator_options = ["All"] + sorted(df[INDICATOR_COL].unique().tolist())
selected_indicator = st.sidebar.selectbox("Core Indicator", indicator_options)

if selected_indicator == "All":
    df_filtered = df.copy()
else:
    df_filtered = df[df[INDICATOR_COL] == selected_indicator].copy()

st.sidebar.caption(f"{len(df_filtered)} signals")

# ---------------------------
# CLIMATE SUMMARY
# ---------------------------
st.subheader("Indicator Climate Overview")

summary = (
    df_filtered
    .groupby(INDICATOR_COL)
    .agg(
        Signal_Count=(DATE_COL, "count"),
        Last_Update=(DATE_COL, "max")
    )
    .reset_index()
    .sort_values("Signal_Count", ascending=False)
)

DIRECTION_MAP = {
    "Attitudinal Climate": "Shifting public sentiment",
    "Narrative Environment": "Escalating discourse pressure",
    "Democratic Climate": "Institutional stress",
    "Gendered Economic Conditions": "Material access strain",
    "Legislative Momentum": "Accelerating policy activity",
}

NOTE_MAP = {
    "Attitudinal Climate": "Changes in public opinion that shape political receptivity.",
    "Narrative Environment": "Media, rhetoric, and normalization patterns.",
    "Democratic Climate": "Representation, rights protection, and institutional resilience.",
    "Gendered Economic Conditions": "Economic access, labor equity, and service stability.",
    "Legislative Momentum": "Rate and direction of legal and regulatory change.",
}

cols = st.columns(3)
for i, row in summary.iterrows():
    with cols[i % 3]:
        st.markdown(
            f"""
**{row[INDICATOR_COL]}**

*{DIRECTION_MAP.get(row[INDICATOR_COL], "Mixed signals")}*

**Signals tracked:** {row.Signal_Count}  
**Last update:** {row.Last_Update:%b %d, %Y}

{NOTE_MAP.get(row[INDICATOR_COL], "")}
"""
        )

st.divider()

# ---------------------------
# EVIDENCE FEED 
# ---------------------------
st.subheader("Evidence Feed)")
st.caption(
    "Illustrative sample of underlying indicator signals. "
    "Full dataset is retained internally."
)

feed = (
    df_filtered
    .sort_values(DATE_COL, ascending=False)
    [[DATE_COL, INDICATOR_COL, HEADLINE_COL, SOURCE_COL]]
    .head(10)
)

st.dataframe(feed, use_container_width=True)