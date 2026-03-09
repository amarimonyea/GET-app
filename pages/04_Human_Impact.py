import streamlit as st
import pandas as pd
import altair as alt

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

st.title("👥 Human Impact Analysis")

# Load and prepare data
df = pd.read_csv("data/Monitor_Gender_Equality_sample_data.csv", skiprows=1)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
df = df.dropna(subset=["Date", "Slider Score"])

st.write(
    "Understand who is being impacted by these gender equality policy developments."
)

st.divider()

IMPACT_COL = "Who is impacted?"

# Count occurrences of different impact populations
impact_groups = []
for idx, row in df.iterrows():
    if pd.notna(row[IMPACT_COL]):
        # Split by comma and clean up whitespace
        groups = [g.strip() for g in str(row[IMPACT_COL]).split(",")]
        impact_groups.extend(groups)

impact_counts = {}
for group in impact_groups:
    impact_counts[group] = impact_counts.get(group, 0) + 1

impact_df = pd.DataFrame(
    list(impact_counts.items()),
    columns=[IMPACT_COL, "Frequency"]
).sort_values("Frequency", ascending=False)

# Sidebar slider for top N groups
top_n = st.sidebar.slider(
    "Show top N population groups",
    min_value=5,
    max_value=min(30, len(impact_df)),
    value=15,
    step=1,
)

st.subheader("Population Groups Most Impacted")

# Display table
st.dataframe(impact_df, use_container_width=True)

st.divider()

# Chart: Population impacts
chart = (
    alt.Chart(impact_df.head(top_n))
    .mark_bar(orient='horizontal')
    .encode(
        x=alt.X("Frequency:Q", title="Number of Events"),
        y=alt.Y(IMPACT_COL + ":N", sort="-x"),
        color=alt.value("#3b668c"),
        tooltip=[IMPACT_COL, "Frequency"],
    )
    .properties(height=min(500, top_n * 20))
)

st.altair_chart(chart, use_container_width=True)

st.caption("Population groups appearing most frequently in the dataset's impact descriptions.")
