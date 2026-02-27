import streamlit as st
import pandas as pd

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="GET • Core Indicators",
    layout="wide"
)

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