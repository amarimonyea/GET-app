import streamlit as st
import pandas as pd

# ---------------------------
# 0) PAGE CONFIG MUST BE FIRST
# ---------------------------
st.set_page_config(page_title="U.S. Gender Equality Tracker", layout="wide")

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
st.sidebar.image("assets/footer_logo.svg", use_container_width=True)

st.title("🌎 U.S. Gender Equality Tracker")
st.write("**How to use the tracker:** Use the sidebar to explore sector impacts, human impacts, and the indicators shaping the forecast.")
st.write("The U.S. Gender Equality Tracker (GET) is an early-warning system that tracks gender-related policies and forecasts their broader political, social, and security impacts.")

# Video placeholder
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: center; align-items: center; height: 400px; background-color: #e8e8e8; border-radius: 8px; border: 2px solid #ccc;">
    <div style="text-align: center;">
        <div style="font-size: 48px; margin-bottom: 10px;">🎬</div>
        <p style="font-size: 18px; color: #666;">Video coming soon...</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Forecasts Section
st.markdown("---")
st.subheader("Current Risk Outlook")
st.write("Overview of principal forecasts and risk trajectories:")
st.caption("Updated: March 2026")

# Create columns for forecast cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background-color: #cf5442; padding: 20px; border-radius: 8px; text-align: center; height: 100%;">
        <p style="color: #ffffff; font-size: 16px; margin: 0 0 10px 0; font-weight: 400;">Political Disruption Risk</p>
        <p style="color: #ffffff; font-size: 32px; margin: 10px 0; font-weight: 700;">Elevated</p>
        <p style="color: #ffffff; font-size: 16px; margin: 10px 0 0 0; opacity: 0.9;">Based on policy and discourse trends</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #bfa359; padding: 20px; border-radius: 8px; text-align: center; height: 100%;">
        <p style="color: #1b1725; font-size: 16px; margin: 0 0 10px 0; font-weight: 400;">Economic Impact Forecast</p>
        <p style="color: #1b1725; font-size: 32px; margin: 10px 0; font-weight: 700;">Moderate</p>
        <p style="color: #1b1725; font-size: 16px; margin: 10px 0 0 0; opacity: 0.85;">Gender-related economic trajectories</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color: #3b668c; padding: 20px; border-radius: 8px; text-align: center; height: 100%;">
        <p style="color: #ffffff; font-size: 16px; margin: 0 0 10px 0; font-weight: 400;">Security Considerations</p>
        <p style="color: #ffffff; font-size: 32px; margin: 10px 0; font-weight: 700;">Emerging</p>
        <p style="color: #ffffff; font-size: 16px; margin: 10px 0 0 0; opacity: 0.9;">Emerging security implications</p>
    </div>
    """, unsafe_allow_html=True)

# Most Affected Groups and Systems
st.markdown("---")
st.subheader("Most Affected Sectors & Groups")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/Monitor - Gender Equality - GET 2025 (1).csv", skiprows=1)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()

# Get date range
date_min = df["Date"].min()
date_max = df["Date"].max()
date_range_str = f"{date_min.strftime('%B %d, %Y')} to {date_max.strftime('%B %d, %Y')}"

st.caption(f"Based on developments tracked from {date_range_str}")

# Get top 3 sectors and groups
top_sectors = df["Sector Impacted"].value_counts().head(3)
top_groups = df["Who is impacted?"].value_counts().head(3)

affected_col1, affected_col2, affected_col3 = st.columns(3)

# Display top 3 sectors
with affected_col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #cf5442 0%, #a83c2f 100%); padding: 25px; border-radius: 8px; height: 100%; text-align: center;">
        <p style="color: #ffffff; font-size: 16px; margin: 0 0 20px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Most Affected Sectors</p>
    </div>
    """, unsafe_allow_html=True)
    for i, (sector, count) in enumerate(top_sectors.items(), 1):
        st.markdown(f"<p style='margin: 12px 0; font-size: 16px;'>{sector}<br><span style='font-size: 14px; color: #666; font-weight: 500;'>{count} incident{'s' if count > 1 else ''}</span></p>", unsafe_allow_html=True)

# Display top 3 groups
with affected_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #bfa359 0%, #9d8247 100%); padding: 25px; border-radius: 8px; height: 100%; text-align: center;">
        <p style="color: #ffffff; font-size: 16px; margin: 0 0 20px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Most Affected Groups</p>
    </div>
    """, unsafe_allow_html=True)
    for i, (group, count) in enumerate(top_groups.items(), 1):
        st.markdown(f"<p style='margin: 12px 0; font-size: 16px;'>{group}<br><span style='font-size: 14px; color: #666; font-weight: 500;'>{count} incident{'s' if count > 1 else ''}</span></p>", unsafe_allow_html=True)

# Display total entries
with affected_col3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #3b668c 0%, #2d4a66 100%); padding: 25px; border-radius: 8px; text-align: center; height: 100%;">
        <p style="color: #ffffff; font-size: 13px; margin: 0 0 15px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Scope of Impact</p>
        <p style="color: #ffffff; font-size: 42px; margin: 15px 0; font-weight: 700;">{len(df)}</p>
        <p style="color: #ffffff; font-size: 12px; margin: 0; opacity: 0.95;">total developments<br>tracked</p>
    </div>
    """
    , unsafe_allow_html=True)
