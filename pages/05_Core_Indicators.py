import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ---------------------------
# 1) THEME / CSS (inject once)
# ---------------------------
COLOR_DISRUPTION = "#cf5442"   # New Lines red
COLOR_PROGRESSION = "#62af44"  # New Lines green
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
DATA_PATH = "data/Monitor - Gender Equality - Core Indicator Outputs 2025 (2).csv"

df = pd.read_csv(DATA_PATH, skiprows=1)


DATE_COL = "Date"
INDICATOR_COL = "Core Indicator"
HEADLINE_COL = "Development"
SOURCE_COL = "Link"
DIRECTION_COL = "Column 2"

# Direction mapping (using color scheme for consistency)
DIRECTION_MAP_VALUES = {
    1: "Worsening conditions",      # COLOR_DISRUPTION
    0: "Neutral / mixed",            # COLOR_NEUTRAL
    -1: "Improving conditions"       # COLOR_PROGRESSION
}

df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
df = df.dropna(subset=[DATE_COL, INDICATOR_COL]).copy()

# Add direction label column
df["Trend"] = df[DIRECTION_COL].map(DIRECTION_MAP_VALUES)

# ---------------------------
# SIDEBAR FILTER
# ---------------------------
st.sidebar.header("Filter")

# Reset filters callback
def reset_filters():
    st.session_state["indicator_filter"] = 0

st.sidebar.button("Reset Filters", on_click=reset_filters)

indicator_options = ["All"] + sorted(df[INDICATOR_COL].unique().tolist())
selected_indicator = st.sidebar.selectbox(
    "Core Indicator",
    indicator_options,
    key="indicator_filter"
)

if selected_indicator == "All":
    df_filtered = df.copy()
else:
    df_filtered = df[df[INDICATOR_COL] == selected_indicator].copy()

st.sidebar.caption(f"{len(df_filtered)} signals")

# ---------------------------
# HEADER
# ---------------------------
st.title("Core Indicator Contextualization")
st.caption(
    "Core indicators provide structural context for the policy environment. "
    "They inform analyst judgment but are not coded as discrete events."
)

# ---------------------------
# CLIMATE SUMMARY
# ---------------------------
st.subheader("Core Indicator Overview")

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
    "Attitudinal Climate": "Institutional protections, representation, and governance stability.",
    "Narrative Environment": "Media, rhetoric, and normalization patterns.",
    "Democratic Climate": "Representation, rights protection, and institutional resilience.",
    "Gendered Economic Conditions": "Economic access, labor equity, and service availability affecting gender equality.",
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
# HELPER FUNCTIONS
# ---------------------------
# Source name mapping
SOURCE_MAP = {
    "nytimes.com": "NYT",
    "apnews.com": "AP",
    "pewresearch.org": "Pew",
    "nbcnews.com": "NBC",
    "pbs.org": "PBS",
    "aauw.org": "AAUW",
    "politico.com": "POLITICO",
    "gallup.com": "Gallup",
    "glaad.org": "GLAAD",
    "unwomen.org": "UN Women",
    "independent.co.uk": "The Independent",
    "newsweek.com": "Newsweek",
    "axios.com": "Axios",
    "catholicnewsagency.com": "CNA",
    "usnews.com": "U.S. News",
    "theatlantic.com": "The Atlantic",
    "theguardian.com": "The Guardian",
    "politico.com": "POLITICO",
    "apresnouvellesquebec.com": "APR",
    "congress.gov": "Congress.gov",
}

def get_short_source(url):
    """Extract short source name from URL."""
    if not url or not isinstance(url, str):
        return "Source"
    
    url_lower = url.lower()
    for domain, short_name in SOURCE_MAP.items():
        if domain in url_lower:
            return short_name
    
    # Fallback: extract domain name
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.replace("www.", "")
        return domain.split(".")[0].upper()
    except:
        return "Source"

def trim_text(text, max_length=120):
    """Trim text to max_length characters, preferring sentence breaks."""
    if not text or len(text) <= max_length:
        return text
    
    # Try to find a sentence break before max_length
    trimmed = text[:max_length]
    
    # Look for periods, exclamation marks, or question marks
    for sentence_end in [". ", "! ", "? "]:
        last_sentence_break = trimmed.rfind(sentence_end)
        if last_sentence_break > 0 and last_sentence_break > max_length - 40:
            return trimmed[:last_sentence_break + 1]
    
    # If no sentence break found, cut at last word boundary
    last_space = trimmed.rfind(" ")
    if last_space > 0:
        return trimmed[:last_space] + "…"
    
    return trimmed + "…"

# ---------------------------
# OVERALL INDICATOR DIRECTION
# ---------------------------
st.subheader("Overall Indicator Direction")
st.markdown("##### Signals Informing Each Indicator")

direction_counts = df_filtered[DIRECTION_COL].value_counts().sort_index(ascending=False)
direction_labels = {
    1: "Worsening conditions",
    0: "Neutral / mixed",
    -1: "Improving conditions"
}

total_signals = len(df_filtered)
summary_cols = st.columns(3)

for idx, direction_val in enumerate([1, 0, -1]):
    count = direction_counts.get(direction_val, 0)
    pct = (count / total_signals * 100) if total_signals > 0 else 0
    
    with summary_cols[idx]:
        st.metric(
            label=direction_labels[direction_val],
            value=int(count),
            delta=f"{pct:.1f}%" if total_signals > 0 else "0%"
        )

st.divider()

# ---------------------------
# EVIDENCE FEED 
# ---------------------------
st.subheader("Evidence Feed")
st.caption(
    "Signals from the past 6 months. "
    "Full dataset is retained internally."
)

# Calculate 6 months ago
six_months_ago = pd.Timestamp.now() - timedelta(days=180)

# Filter for last 6 months and get the 10 most recent
feed = (
    df_filtered[df_filtered[DATE_COL] >= six_months_ago]
    .sort_values(DATE_COL, ascending=False)
    .head(10)
)

if len(feed) > 0:
    for idx, row in feed.iterrows():
        date_str = row[DATE_COL].strftime("%b %d, %Y")
        headline = trim_text(row[HEADLINE_COL], 120)
        source_short = get_short_source(row[SOURCE_COL])
        source_url = row[SOURCE_COL]
        indicator = row[INDICATOR_COL]
        trend = row["Trend"]
        
        st.markdown(f"""
**{date_str}** | {indicator} | {trend}

{headline}

[{source_short} →]({source_url})

---
""")
else:
    st.info("No signals in past 6 months for selected filters.")