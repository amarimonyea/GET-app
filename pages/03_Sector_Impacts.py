import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ---------------------------
# 0) PAGE CONFIG MUST BE FIRST
# ---------------------------
st.set_page_config(page_title="Sector Impacts", layout="wide")

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
  bottom: 80px;
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

st.title("📊 Sector Impacts Analysis")

# Load and prepare data
df = pd.read_csv("data/Monitor_Gender_Equality_sample_data.csv", skiprows=1)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
df = df.dropna(subset=["Date", "Slider Score"])

st.write(
    "Explore which sectors are most impacted by gender-related policy developments and disruptions."
)

st.divider()

SECTOR_COL = "Sector Impacted"

top_n = st.slider("Show top N sectors", min_value=5, max_value=25, value=10, step=1)

metric_choice = st.radio(
    "Rank sectors by:",
    [
        "Event Count",
        "Weighted Disruption (sum of positive Slider Score)",
        "Total Intensity (sum of |Slider Score|)"
    ],
    horizontal=True,
)

# Compute metrics for each sector
df["Weighted Disruption"] = np.where(df["Slider Score"] > 0, df["Slider Score"], 0)
df["Weighted Progression"] = np.where(df["Slider Score"] < 0, -df["Slider Score"], 0)
df["Absolute Intensity"] = df["Slider Score"].abs()

# Get actual event counts by sector
sector_counts = df[SECTOR_COL].value_counts().reset_index()
sector_counts.columns = [SECTOR_COL, "Event_Count"]

# Compute aggregated metrics per sector
sector_metrics = (
    df.groupby(SECTOR_COL, as_index=False)
    .agg({
        "Weighted Disruption": "sum",
        "Weighted Progression": "sum",
        "Absolute Intensity": "sum",
    })
)

# Merge with event counts
sector_metrics = sector_metrics.merge(sector_counts, on=SECTOR_COL, how="left")

# Sort by chosen metric
if metric_choice == "Event Count":
    sort_col = "Event_Count"
elif metric_choice == "Weighted Disruption (sum of positive Slider Score)":
    sort_col = "Weighted Disruption"
else:
    sort_col = "Absolute Intensity"

sector_metrics = sector_metrics.sort_values(sort_col, ascending=False).head(top_n)

st.subheader(f"Top {top_n} Sectors by {metric_choice}")

# Display as table
st.dataframe(
    sector_metrics.sort_values(sort_col, ascending=False),
    column_config={
        "Weighted Disruption": st.column_config.NumberColumn(format="%.1f"),
        "Weighted Progression": st.column_config.NumberColumn(format="%.1f"),
        "Absolute Intensity": st.column_config.NumberColumn(format="%.1f"),
    },
    use_container_width=True,
)

st.divider()

# Chart: Event count by sector
chart_data = sector_counts.sort_values("Event_Count", ascending=False).head(top_n)

sector_chart = (
    alt.Chart(chart_data)
    .mark_bar()
    .encode(
        x=alt.X("Event_Count:Q", title="Number of Events"),
        y=alt.Y(SECTOR_COL + ":N", title="Sector", sort="-x"),
        color=alt.value("#cf5442"),
        tooltip=[SECTOR_COL, "Event_Count"],
    )
    .properties(height=400)
)

st.altair_chart(sector_chart, use_container_width=True)

st.caption(
    "✨ Sectors closest to the bottom are most frequently impacted by gender-related policy developments."
)
