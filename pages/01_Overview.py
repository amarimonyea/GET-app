import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import altair as alt
import html
import textwrap
import base64
import os 

# ---------------------------
# 0) PAGE CONFIG MUST BE FIRST
# ---------------------------
st.set_page_config(page_title="Gender Equality Monitor", layout="wide")

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

# Sort cards by probability
PROB_RANK = {"Low": 1, "Low–Medium": 2, "Medium": 3, "Medium–High": 4, "High": 5}

# ---------------------------
# 3) FORECAST SCENARIOS (initialize empty)
# ---------------------------
FORECAST_CARDS = [
    {
        "name": "Political",
        "direction": "Progression",
        "probability": "Low/Medium (25-40%)",
        "summary": "Come back and write real scenarios later",
        "monitoring_indicators": ["State or federal policy actions that establish, reinstate, or expand gender, reproductive, or LGBTQ+ protections", "Judicial rulings or injunctions that reinforce, expand, or affirm gender, reproductive, or LGBTQ+ rights"],
        "implications": ["Strengthened social equity and inclusion outcomes for marginalized groups", "Partial restoration of US credibility on gender and human rights issues"]
    },
    {
        "name": "Political", 
        "direction": "Disruption",
        "probability": "Medium/High (60-75%)",
        "summary": "This forecast illustrates how concentrated executive authority and heightened political polarization can drive accelerated disruption within the gender policy landscape. As institutional checks erode, policy volatility and rights fragmentation become more likely.",
        "monitoring_indicators": ["Legislative or executive actions restricting reproductive, gender, or workplace rights", "Politicization or repurposing of protective institutions for political objectives"],
        "implications": ["Normalization of executive unilateralism in policymaking", "Federal-state fragmentation in rights protection"]
    },
    {
        "name": "Diplomatic", 
        "direction": "Disruption",
        "probability": "Low/Medium (25-40%)",
        "summary": "Come back and write real scenarios later",
        "monitoring_indicators": ["Adoption of US aligned conservative gender policies by foreign governments", "US withdrawal from or defunding of international organizations advancing gender, LGBTQ+, or reproductive rights"],
        "implications": ["Reduction of US credibility in multilateral institutions", "Decreased global access to reproductive, gender-based, and LGBTQ+ health and protection programs"]
    },
    {
        "name": "Diplomatic", 
        "direction": "Progression",
        "probability": "Low (5-25%)",
        "summary": "Come back and write real scenarios later",
        "implications": ["Implications coming soon"]
    },
     {
        "name": "Economic", 
        "direction": "Progression",
        "probability": "Low (5-25%)",
        "summary": "Come back and write real scenarios later",
        "implications": ["Implications coming soon"]
    },
     {
        "name": "Economic", 
        "direction": "Disruption",
        "probability": "Low/Medium (25-40%)",
        "summary": "Come back and write real scenarios later",
        "monitoring_indicators": ["Cuts or divestments in federal scientific, evidence-based research, or mass media related to equity, gender, or social policy", "Decreased funding for public universities focused on social science research"],
        "implications": ["Reduced economic opportunities for marginalized communities", "Disruption of workforce diversity and inclusion initiatives"]
    },
     {
        "name": "Social", 
        "direction": "Disruption",
        "probability": "Medium/High (60-75%)",
        "summary": "Come back and write real scenarios later",
        "monitoring_indicators": ["Medical and ethical crises emerging from restrictive abortion policies", "Service withdrawal or denial driven by anticipated legal, financial, or political retaliation"],
        "implications": ["Increasing discrimination towards trans and gender-diverse individuals", "Global impact on diplomacy and human rights"]
    },
      {
        "name": "Social", 
        "direction": "Progression",
        "probability": "Low (5-25%)",
        "summary": "Come back and write real scenarios later",
        "implications": ["Implications coming soon"]
    },
          {
        "name": "Security", 
        "direction": "Progression",
        "probability": "Low (5-25%)",
        "summary": "Come back and write real scenarios later",
        "implications": ["Implications coming soon"]
    },
        {
        "name": "Security", 
        "direction": "Disruption",
        "probability": "Medium (40-60%)",
        "summary": "Come back and write real scenarios later",
        "monitoring_indicators": ["Removal of gender diverse and trans individuals from law enforcement, military, and intelligence roles", "Targeting of healthcare officials and personnel providing gender affirming services and care"],
        "implications": ["Implications coming soon"]
    },
     {
        "name": "Hybrid Political/Security", 
        "direction": "Disruption",
        "probability": "Medium (40-60%)",
        "summary": "Come back and write real scenarios later",
        "implications": ["Implications coming soon"]
    },
      {
        "name": "Hybrid Political/Social", 
        "direction": "Disruption",
        "probability": "Medium (40-60%)",
        "summary": "Come back and write real scenarios later",
        "implications": ["Implications coming soon"]
    },
      {
        "name": "Status Quo", 
        "direction": "Status Quo",
        "probability": "",
        "summary": "Current policy and institutional landscape continues without major directional shifts. Existing protections and disruptions remain relatively stable.",
        "implications": []
    },
]

# ---------------------------
# 3B) FEATURED DEEP DIVES (quarterly highlights)
# ---------------------------
FEATURED_DEEP_DIVES = [
    {
        "headline": "Senate Advances Comprehensive Paid Leave Legislation",
        "date": "March 15, 2025",
        "forecast": "Political Progression",
        "direction": "progression",
        "analysis": "The FAMILY Act reintroduction signals sustained momentum on economic security for caregivers. Key sponsors include Finance Committee members, indicating broader coalition support. The bill targets six weeks of paid leave, a significant compromise from earlier proposals. Success depends on reconciliation mechanics and mid-year legislative window.",
        "source_url": "https://www.congress.gov",
        "articles": [
            {
                "title": "Paid Leave Bill Gains Bipartisan Momentum in Senate",
                "source": "The Hill",
                "image_url": "assets/senate-placeholder.jpg",
                "link_url": "https://thehill.com"
            },
            {
                "title": "Economic Inequality: New Framework for Caregiving Support",
                "source": "Politico",
                "image_url": "assets/un-women-placeholder.jpg",
                "link_url": "https://politico.com"
            }
        ]
    },
    {
        "headline": "Corporate Diversity Programs Under Increased Legal Scrutiny",
        "date": "March 10, 2025",
        "forecast": "Political Disruption",
        "direction": "disruption",
        "analysis": "Multiple lawsuits targeting DEI initiatives and affirmative action programs suggest sustained legal challenges to gender equity mechanisms. The Supreme Court's recent standing decisions lower barriers for plaintiffs. Legal uncertainty may prompt corporations to pause or restructure programs, creating short-term disruption in institutional commitments to gender parity.",
        "source_url": "https://www.scotus.gov",
        "articles": [
            {
                "title": "Corporate DEI Programs Face Wave of Legal Challenges",
                "source": "Wall Street Journal",
                "image_url": "assets/senate-placeholder.jpg",
                "link_url": "https://wsj.com"
            },
            {
                "title": "Affirmative Action Ban Forces Corporate Strategy Reassessment",
                "source": "Reuters",
                "image_url": "assets/un-women-placeholder.jpg",
                "link_url": "https://reuters.com"
            }
        ]
    }
]

# ---------------------------
# 4) LOAD + CLEAN DATA
# ---------------------------
DATA_PATH = "data/Monitor_Gender_Equality_sample_data.csv"
df = pd.read_csv(DATA_PATH, skiprows=1)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
df = df.dropna(subset=["Date", "Slider Score"]).copy()

# Create short display version of development text
def shorten_text(text, max_chars=120):
    if pd.isna(text):
        return ""
    text = str(text).strip().replace("\n", " ")
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "…"

df["Development Short"] = df["Development"].apply(shorten_text)

def get_key_insights(forecast_points_df, forecast_col):
    """Generate 3 key insights from forecast_points dataframe."""
    if forecast_points_df.empty:
        return ["No insights available for the selected filters."]
    
    insights = []
    
    # Insight 1: Highest cumulative disruption
    max_disr_idx = forecast_points_df["Disr"].idxmax()
    max_disr_name = forecast_points_df.loc[max_disr_idx, forecast_col]
    max_disr_score = forecast_points_df.loc[max_disr_idx, "Disr"]
    insights.append(f"<strong>Highest cumulative disruption:</strong> {max_disr_name} ({max_disr_score:.1f})")
    
    # Insight 2: Highest cumulative progression
    max_prog_idx = forecast_points_df["Prog"].idxmax()
    max_prog_name = forecast_points_df.loc[max_prog_idx, forecast_col]
    max_prog_score = forecast_points_df.loc[max_prog_idx, "Prog"]
    insights.append(f"<strong>Highest cumulative progression:</strong> {max_prog_name} ({max_prog_score:.1f})")
    
    # Insight 3: Most concentrated forecast intensity
    max_intensity_idx = forecast_points_df["Cumulative Intensity"].idxmax()
    max_intensity_name = forecast_points_df.loc[max_intensity_idx, forecast_col]
    max_intensity_score = forecast_points_df.loc[max_intensity_idx, "Cumulative Intensity"]
    insights.append(f"<strong>Most concentrated forecast intensity:</strong> {max_intensity_name} ({max_intensity_score:.1f})")
    
    return insights

def image_to_base64(image_path):
    """Convert image file to base64 data URI."""
    if not os.path.exists(image_path):
        return None
    try:
        with open(image_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            ext = os.path.splitext(image_path)[1].lower().replace(".", "")
            mime_type = f"image/{ext}"
            return f"data:{mime_type};base64,{img_data}"
    except Exception as e:
        st.warning(f"Could not load image {image_path}: {e}")
        return None

FORECAST_COL = "Forecast"
DOMAIN_COL = "Domains of Assessment"
SECTOR_COL = "Sector Impacted"

# ---------------------------
# 5) PAGE TITLE
# ---------------------------
st.title("🌍 Gender Equality Tracker")
st.markdown("<p style='font-size: 1.3rem; color: rgba(27, 23, 37, 0.85); margin-top: -20px;'>Tracking directional shifts in the U.S. gender policy landscape</p>", unsafe_allow_html=True)

# ---------------------------
# 6) TOP METRICS
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Events", len(df))
with col2:
    st.metric("Slider Score Range", f"{df['Slider Score'].min()} to {df['Slider Score'].max()}")

# ---------------------------
# 7) SIDEBAR FILTERS (clean + reset works)
# ---------------------------
st.sidebar.header("🔍 Filters")

def options_with_all(series: pd.Series) -> list[str]:
    vals = sorted(series.dropna().astype(str).unique().tolist())
    return ["All"] + vals

# reset: delete keys then rerun
if st.sidebar.button("🔄 Reset Filters"):
    for k in ["forecast_filter", "domain_filter", "sector_filter"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

forecast_options = options_with_all(df[FORECAST_COL])
domain_options = options_with_all(df[DOMAIN_COL])
sector_options = options_with_all(df[SECTOR_COL])

selected_forecast = st.sidebar.selectbox("Forecast", forecast_options, key="forecast_filter")
selected_domain = st.sidebar.selectbox("Domain of Assessment", domain_options, key="domain_filter")
selected_sector = st.sidebar.selectbox("Sector Impacted", sector_options, key="sector_filter")

df_filtered = df.copy()
if selected_forecast != "All":
    df_filtered = df_filtered[df_filtered[FORECAST_COL].astype(str) == selected_forecast]
if selected_domain != "All":
    df_filtered = df_filtered[df_filtered[DOMAIN_COL].astype(str) == selected_domain]
if selected_sector != "All":
    df_filtered = df_filtered[df_filtered[SECTOR_COL].astype(str) == selected_sector]

st.sidebar.caption(f"Showing {len(df_filtered)} of {len(df)} events")

# Forecast Direction
st.sidebar.divider()
st.sidebar.subheader("📊 Forecast Direction")
st.sidebar.markdown("""
<div style="display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.9rem;">
  <div style="display: flex; align-items: center; gap: 0.5rem;">
    <div style="width: 20px; height: 20px; background-color: #cf5442; border-radius: 3px;"></div>
    <span style="color: #ffffff;"><strong>Disruption</strong> — Challenges to gender equity</span>
  </div>
  <div style="display: flex; align-items: center; gap: 0.5rem;">
    <div style="width: 20px; height: 20px; background-color: #3b668c; border-radius: 3px;"></div>
    <span style="color: #ffffff;"><strong>Progression</strong> — Advances in gender equity</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Logo at bottom of sidebar
st.sidebar.divider()
st.sidebar.image("assets/footer_logo.svg", use_container_width=True)

st.divider()

# ---------------------------
# 8) DISRUPTION AND PROGRESSION MOMENTUM (cleaner)
# ---------------------------
st.subheader("Disruption and Progression Momentum")
st.markdown("**Cumulative intensity (emerging → accelerating) vs net direction (progression ↓ | disruption ↑).**")
quad = df.copy()
quad["Prog"] = np.where(quad["Slider Score"] < 0, -quad["Slider Score"], 0)
quad["Disr"] = np.where(quad["Slider Score"] > 0,  quad["Slider Score"], 0)

forecast_points = quad.groupby(FORECAST_COL, as_index=False)[["Prog", "Disr"]].sum()
forecast_points["Cumulative Intensity"] = forecast_points["Prog"] + forecast_points["Disr"]
forecast_points["Net Direction"] = forecast_points["Disr"] - forecast_points["Prog"]

# Get latest event per forecast from filtered data
if not df_filtered.empty:
    latest_by_forecast = df_filtered.sort_values("Date", ascending=False).groupby(FORECAST_COL, as_index=False).first()
    latest_by_forecast = latest_by_forecast[[FORECAST_COL, "Date", "Development Short", "Slider Score", DOMAIN_COL, SECTOR_COL]].rename(
        columns={"Date": "Latest Date", "Development Short": "Latest Development", "Slider Score": "Latest Slider Score", DOMAIN_COL: "Latest Domain", SECTOR_COL: "Latest Sector"}
    )
    forecast_points = forecast_points.merge(latest_by_forecast, left_on=FORECAST_COL, right_on=FORECAST_COL, how="left")
    forecast_points["Latest Date Str"] = forecast_points["Latest Date"].dt.strftime("%b %d, %Y")
else:
    forecast_points["Latest Date"] = None
    forecast_points["Latest Date Str"] = "No data"
    forecast_points["Latest Development"] = None
    forecast_points["Latest Slider Score"] = None
    forecast_points["Latest Domain"] = None
    forecast_points["Latest Sector"] = None

if forecast_points.empty:
    st.info("No data available for the current filters.")
else:
    # Key Insights Strip
    insights_list = get_key_insights(forecast_points, FORECAST_COL)
    insights_html = "\n".join([f"<li style='margin-bottom: 0.5rem; color: #1b1725;'>{insight}</li>" for insight in insights_list])
    
    st.markdown(f"""
    <div style="background-color: #f1f0ec; border-left: 4px solid #bfa359; padding: 1rem; margin: 1.5rem 0; border-radius: 2px; box-shadow: 0 1px 3px rgba(27, 23, 37, 0.08);">
      <div style="font-size: 0.75rem; font-weight: 700; color: #1b1725; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em;">Key Insights</div>
      <ul style="margin: 0; padding-left: 1.5rem; list-style: disc;">
        {insights_html}
      </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Quadrant thresholds
    x0 = float(forecast_points["Cumulative Intensity"].median())
    y0 = 0.0

    # Hover selection (so we don't need always-on labels)
    hover = alt.selection_point(fields=[FORECAST_COL], on="mouseover", nearest=True, empty=False)

    # Thicker midlines
    vline = (
        alt.Chart(pd.DataFrame({"x": [x0]}))
        .mark_rule(strokeDash=[6, 4], strokeWidth=3, opacity=0.75)
        .encode(x="x:Q")
    )
    hline = (
        alt.Chart(pd.DataFrame({"y": [y0]}))
        .mark_rule(strokeDash=[6, 4], strokeWidth=3, opacity=0.75)
        .encode(y="y:Q")
    )

    # Points (pick ONE point color)
    POINT_COLOR = "#1b1725"  # NL dark (neutral)
    points = alt.Chart(forecast_points).mark_circle(
    size=260,
    stroke="white",
    strokeWidth=1.5
).encode(
    x=alt.X("Cumulative Intensity:Q", title="Cumulative Intensity"),
    y=alt.Y("Net Direction:Q", title="Net Direction", scale=alt.Scale(padding=20)),
    color=alt.condition(
        "datum['Net Direction'] > 0",
        alt.value("#cf5442"),
        alt.value("#3b668c")
    ),
    tooltip=[
    alt.Tooltip(f"{FORECAST_COL}:N", title="Forecast"),
    alt.Tooltip("Prog:Q", title="Cumulative Progression", format=".1f"),
    alt.Tooltip("Disr:Q", title="Cumulative Disruption", format=".1f"),
    alt.Tooltip("Cumulative Intensity:Q", title="Cumulative Intensity", format=".1f"),
    alt.Tooltip("Net Direction:Q", title="Net Direction", format=".1f"),
    alt.Tooltip("Latest Date Str:N", title="Latest Event Date"),
    alt.Tooltip("Latest Development:N", title="Latest Event"),
    alt.Tooltip("Latest Slider Score:Q", title="Latest Event Score", format=".1f"),
] 
).add_params(hover)

    # Show label only on hover (prevents overlap)
    hover_labels = (
        alt.Chart(forecast_points)
        .mark_text(
            align="left",
            dx=12,
            dy=-10,
            fontSize=12,
            font="Roboto",
            fontWeight="bold",
            color="#000000"   # ← Black text
        )
    .encode(
        x="Cumulative Intensity:Q",
        y="Net Direction:Q",
        text=alt.condition(hover, alt.Text(f"{FORECAST_COL}:N"), alt.value("")),
    )
)

    # Quadrant names
    x_max = float(forecast_points["Cumulative Intensity"].max() or 1)
    y_max = float(forecast_points["Net Direction"].max() or 1)
    y_min = float(forecast_points["Net Direction"].min() or -1)

    # place quadrant text inside chart area
    quad_labels = pd.DataFrame([
        {"x": x0 * 0.20, "y": y_max * 0.85 if y_max > 0 else 5,  "t": "Emerging Disruption"},
        {"x": x0 + (x_max - x0) * 0.55, "y": y_max * 0.85 if y_max > 0 else 5, "t": "Accelerating Disruption"},
        {"x": x0 * 0.20, "y": y_min * 0.85 if y_min < 0 else -5, "t": "Emerging Progression"},
        {"x": x0 + (x_max - x0) * 0.55, "y": y_min * 0.85 if y_min < 0 else -5, "t": "Accelerating Progression"},
    ])

    quad_text = (
        alt.Chart(quad_labels)
        .mark_text(opacity=0.55, font="Roboto", fontSize=13, fontWeight="bold")
        .encode(x="x:Q", y="y:Q", text="t:N")
    )

    chart = (
        (vline + hline + points + hover_labels + quad_text)
        .properties(height=420)
        .configure_view(fill="white")
        .configure_axis(labelFont="Roboto", titleFont="Roboto")
        .configure_title(font="Roboto")
    )

    # Add legend for colors
    st.markdown("""
    <div style="display: flex; gap: 20px; margin-bottom: 15px; font-size: 0.9rem;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 16px; height: 16px; background-color: #cf5442; border-radius: 2px;"></div>
        <span>Disruption</span>
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 16px; height: 16px; background-color: #3b668c; border-radius: 2px;"></div>
        <span>Progression</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)
    
    # Extract key statistics for the explanation
    max_disr_idx = forecast_points["Disr"].idxmax()
    max_disr_name = forecast_points.loc[max_disr_idx, FORECAST_COL]
    max_disr_score = forecast_points.loc[max_disr_idx, "Disr"]
    
    max_prog_idx = forecast_points["Prog"].idxmax()
    max_prog_name = forecast_points.loc[max_prog_idx, FORECAST_COL]
    max_prog_score = forecast_points.loc[max_prog_idx, "Prog"]
    
    latest_date = df_filtered["Date"].max()
    date_str = latest_date.strftime("%B %d, %Y")
    
    st.markdown(f"""
**Momentum Graph Explanation**

The Disruption and Progression Momentum graph plots cumulative forecast intensity against net directional movement. Cumulative intensity reflects the volume and concentration of forecasted developments within a domain (emerging → accelerating), while vertical positioning distinguishes between disruptive and progressive trajectories. The quadrant framework highlights which issue areas are early-stage signals versus accelerating structural shifts.

**Highest cumulative disruption observed to date:** {max_disr_name} (cumulative disruption score: {max_disr_score:.1f})

**Highest cumulative progression observed to date:** {max_prog_name} (cumulative progression score: {max_prog_score:.1f})

**Data current as of:** {date_str}
""")

    # Latest Event by Forecast panel
    st.subheader("Latest Events by Forecast")
    
    if not df_filtered.empty:
        latest_events_display = forecast_points[[FORECAST_COL, "Latest Date Str", "Latest Development", "Latest Domain", "Latest Sector", "Latest Slider Score"]].copy()
        latest_events_display = latest_events_display[latest_events_display["Latest Date Str"] != "No data"]
        
        if not latest_events_display.empty:
            latest_events_display = latest_events_display.rename(columns={
                FORECAST_COL: "Forecast",
                "Latest Date Str": "Date",
                "Latest Development": "Event Title",
                "Latest Domain": "Domain",
                "Latest Sector": "Sector",
                "Latest Slider Score": "Score"
            })
            # Sort by date descending (most recent first)
            latest_events_display["Date"] = pd.to_datetime(latest_events_display["Date"], format="%b %d, %Y", errors="coerce")
            latest_events_display = latest_events_display.sort_values("Date", ascending=False).head(3)
            latest_events_display["Date"] = latest_events_display["Date"].dt.strftime("%b %d, %Y")
            latest_events_display = latest_events_display[[c for c in ["Forecast", "Date", "Event Title", "Score"] if c in latest_events_display.columns]]
            
            # Cap Event Title at 100 characters without breaking words
            def truncate_at_word_boundary(text, max_length=100):
                if len(text) <= max_length:
                    return text
                truncated = text[:max_length]
                last_space = truncated.rfind(' ')
                if last_space > 0:
                    return truncated[:last_space] + "..."
                return truncated + "..."
            
            latest_events_display["Event Title"] = latest_events_display["Event Title"].apply(truncate_at_word_boundary)
            
            st.markdown(
                """
                <style>
                [data-testid="stDataFrame"] [data-testid="stDataFrameContainer"] div {
                    word-wrap: break-word;
                    white-space: normal;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.dataframe(latest_events_display, use_container_width=True, hide_index=True)
        else:
            st.info("No events available for selected forecasts in current filters.")
    else:
        st.info("No events in current filters.")

    st.markdown(
        """
        <style>
          /* Wrap the chart container with gold border */
          div[data-testid="stVegaLiteChart"] {
            border: 4px solid #e1bb4b !important;
            border-radius: 14px !important;
            padding: 4px !important;
            background: #ffffff !important;
            margin-top: 10px !important;
            box-sizing: border-box !important;
            width: 100% !important;
            overflow: hidden !important;
            max-width: 100% !important;
          }
          
          div[data-testid="stVegaLiteChart"] > div {
            overflow: hidden !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.divider()

import textwrap
import re

# ---------------------------
# 9) GENDER CURRENTLY (Status Quo + Developments)
# ---------------------------
st.subheader("Current Environment")

NL_BLUE = "#3b668c"
NL_RED  = "#cf5442"
NL_GOLD = "#bfa359"
CARD_CSS = f"""
<style>
/* =========================
   GRID (4 columns)
   ========================= */
.scenario-cards-container {{
  max-height: 600px;
  overflow-y: auto;
  padding-right: 8px;
}}

.scenario-cards-container::-webkit-scrollbar {{
  width: 10px;
}}

.scenario-cards-container::-webkit-scrollbar-track {{
  background: rgba(27, 23, 37, 0.05);
  border-radius: 5px;
}}

.scenario-cards-container::-webkit-scrollbar-thumb {{
  background: rgba(27, 23, 37, 0.25);
  border-radius: 5px;
}}

.scenario-cards-container::-webkit-scrollbar-thumb:hover {{
  background: rgba(27, 23, 37, 0.4);
}}

.deck {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.5rem;
  min-height: 0;
  align-items: start;
}}

@media (max-width: 1100px) {{
  .deck {{
    grid-template-columns: 1fr;
    gap: 1rem;
  }}
}}

.status-quo-section {{
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid rgba(27, 23, 37, 0.15);
}}

.status-quo-label {{
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(27, 23, 37, 0.6);
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.status-quo-container {{
  display: flex;
  justify-content: center;
  width: 100%;
}}

.status-quo-container .deck-item {{
  max-width: 400px;
  width: 100%;
}}

.status-quo-container .deck-card {{
  padding: 1rem;
}}

.deck-pile {{
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 0;
}}

/* Hide column headers entirely (if present) */
.deck-pile-header {{
  display: none !important;
}}

/* Kill any leftover stacked layers from older versions */
.deck-item::before,
.deck-item::after {{
  content: none !important;
  display: none !important;
}}

/* =========================
   CARD BASE (Structured Briefing)
   ========================= */
:root {{
  --nl-navy: #1b1725;
  --nl-cream: #f1f0ec;
  --nl-red:   #cf5442;
  --nl-blue:  #3b668c;
  --nl-gold:  #bfa359;
  --nl-slate: #93b5c3;  /* muted */
}}

.deck-card {{
  position: relative;
  border-radius: 14px;
  padding: 1.0rem 1.1rem;
  background: var(--nl-cream) !important;     /* cream card */
  color: var(--nl-navy) !important;          /* navy text */
  border: 1px solid rgba(27, 23, 37, 0.10);   /* subtle outline */
  border-top: 4px solid rgba(27, 23, 37, 0.25); /* default top rule */
  box-shadow: 0 10px 24px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: transform .15s ease, box-shadow .15s ease;
  height: auto;
  overflow: visible;
}}

.deck-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 14px 30px rgba(0,0,0,0.08);
}}

/* Collapse behavior */
.deck-card.collapsed .deck-body,
.deck-card.collapsed .prob-wrap {{
  display: none;
}}

.deck-title {{
  font-size: 1.05rem;
  font-weight: 900;
  margin: 0 0 .55rem 0;
  color: var(--nl-navy) !important;
}}

/* small accent dot (optional but nice) */
.deck-title::before {{
  content: "";
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  margin-right: .55rem;
  background: rgba(27, 23, 37, 0.35);
  transform: translateY(-1px);
}}

.deck-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: .45rem;
  margin: 0 0 .35rem 0;
}}

.deck-chip {{
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  padding: .20rem .55rem;
  border-radius: 999px;
  font-size: .78rem;
  font-weight: 800;
  border: 1px solid rgba(27, 23, 37, 0.14);
  background: rgba(27, 23, 37, 0.03);
  color: var(--nl-navy) !important;
}}

/* Body text */
.deck-body {{
  margin-top: .5rem;
  font-size: 0.95rem;
  line-height: 1.5;
  color: rgba(27, 23, 37, 0.92) !important;
  max-width: 72ch;
}}

/* Probability bar */
.prob-wrap {{ margin-top: .55rem; }}
.prob-label {{
  font-size: .72rem;
  letter-spacing: .2px;
  color: rgba(27, 23, 37, 0.75) !important;
  margin-bottom: .25rem;
}}

.prob-bar {{
  height: 10px;
  border-radius: 999px;
  background: rgba(27, 23, 37, 0.10);
  overflow: hidden;
  border: 1px solid rgba(27, 23, 37, 0.12);
}}

.prob-fill {{
  height: 100%;
  border-radius: 999px;
  background: var(--nl-gold); /* default fill */
}}

/* =========================
   ACCENTS (minimal use)
   ========================= */

/* Disruption = red accent */
.deck-card.disruption {{
  border-top-color: var(--nl-red) !important;
}}
.deck-card.disruption .deck-title::before {{
  background: var(--nl-red) !important;
}}
.deck-card.disruption .prob-fill {{
  background: var(--nl-red) !important;
}}

/* Progression = blue accent */
.deck-card.progression {{
  border-top-color: var(--nl-blue) !important;
}}
.deck-card.progression .deck-title::before {{
  background: var(--nl-blue) !important;
}}
.deck-card.progression .prob-fill {{
  background: var(--nl-blue) !important;
}}

/* Status quo = muted slate */
.deck-card.statusquo {{
  border-top-color: var(--nl-slate) !important;
}}
.deck-card.statusquo .deck-title::before {{
  background: var(--nl-slate) !important;
}}
.deck-card.statusquo .prob-fill {{
  background: var(--nl-slate) !important;
}}

/* Hybrid = gold */
.deck-card.hybrid {{
  border-top-color: var(--nl-gold) !important;
}}
.deck-card.hybrid .deck-title::before {{
  background: var(--nl-gold) !important;
}}
.deck-card.hybrid .prob-fill {{
  background: var(--nl-gold) !important;
}}

/* =========================
   NET ASSESSMENT SPOTLIGHT
   ========================= */
.spotlight-section {{
  background-color: #f1f0ec;
  margin: 2rem 0;
  padding: 2rem;
  border-radius: 4px;
  border-top: 1px solid rgba(27, 23, 37, 0.1);
}}

.spotlight-title {{
  font-size: 1.3rem;
  font-weight: 700;
  color: #1b1725;
  margin-bottom: 1.5rem;
  letter-spacing: 0.02em;
}}

.spotlight-container {{
  display: flex;
  gap: 2rem;
}}

.spotlight-main {{
  flex: 0 0 50%;
  background: white;
  padding: 1.5rem;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(27, 23, 37, 0.06);
  border-top: 4px solid #3b668c;
}}

.spotlight-main.disruption {{
  border-top-color: #cf5442;
}}

.spotlight-main.progression {{
  border-top-color: #3b668c;
}}

.spotlight-main.hybrid {{
  border-top-color: #bfa359;
}}

.spotlight-headline {{
  font-size: 1.1rem;
  font-weight: 700;
  color: #1b1725;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}}

.spotlight-meta {{
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: rgba(27, 23, 37, 0.6);
}}

.spotlight-meta-item {{
  display: flex;
  align-items: center;
  gap: 0.25rem;
}}

.spotlight-badge {{
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.spotlight-badge.disruption {{
  background-color: rgba(207, 84, 66, 0.1);
  color: #cf5442;
}}

.spotlight-badge.progression {{
  background-color: rgba(59, 102, 140, 0.1);
  color: #3b668c;
}}

.spotlight-analysis {{
  font-size: 0.95rem;
  color: #1b1725;
  line-height: 1.5;
  margin-bottom: 1rem;
}}

.spotlight-source {{
  font-size: 0.85rem;
  color: #bfa359;
  text-decoration: none;
  font-weight: 600;
}}

.spotlight-source:hover {{
  text-decoration: underline;
}}

.spotlight-articles {{
  flex: 0 0 50%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}}

.article-tile {{
  background: white;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(27, 23, 37, 0.06);
  transition: box-shadow 0.2s ease;
}}

.article-tile:hover {{
  box-shadow: 0 2px 4px rgba(27, 23, 37, 0.12);
}}

.article-image {{
  width: 100%;
  height: 140px;
  object-fit: cover;
  display: block;
}}

.article-content {{
  padding: 1rem;
}}

.article-title {{
  font-size: 0.9rem;
  font-weight: 700;
  color: #1b1725;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}}

.article-source {{
  font-size: 0.8rem;
  color: rgba(27, 23, 37, 0.6);
  margin-bottom: 0.75rem;
}}

.article-link {{
  display: inline-block;
  color: #bfa359;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
}}

.article-link:hover {{
  text-decoration: underline;
}}

@media(max-width: 768px) {{
  .spotlight-container {{
    flex-direction: column;
  }}
  
  .spotlight-main {{
    flex: 0 0 100%;
  }}
  
  .spotlight-articles {{
    flex: 0 0 100%;
  }}
}}
</style>
"""

def normalize_prob(p: str) -> str:
    p = (p or "").strip()
    # Remove percentage ranges like (5-25%) or (25-40%)
    p = re.sub(r"\s*\([^)]*%[^)]*\)\s*", "", p)
    p = p.replace("–", "-").replace("/", "-").replace(" to ", "-")
    p = re.sub(r"\s+", "", p).lower()
    return p

def direction_class(direction: str) -> str:
    d = (direction or "").strip().lower()
    if "disruption" in d:
        return "disruption"
    if "progression" in d:
        return "progression"
    if "status" in d:
        return "statusquo"
    if "hybrid" in d:
        return "hybrid"
    return "statusquo"

PROB_RANK  = {"low": 1, "low-medium": 2, "medium": 3, "medium-high": 4, "high": 5}
PROB_WIDTH = {"low": "20%", "low-medium": "40%", "medium": "60%", "medium-high": "80%", "high": "100%"}

cards_sorted = sorted(
    FORECAST_CARDS,
    key=lambda c: PROB_RANK.get(normalize_prob(str(c.get("probability", ""))), 0),
    reverse=True,
)

# Group cards by direction (excluding Status Quo)
cards_by_direction = {"Disruption": [], "Hybrid Disruption": [], "Progression": []}
status_quo_card = None

for c in cards_sorted:
    direction = c.get("direction", "Status Quo")
    # Separate Status Quo for its own section
    if direction == "Status Quo":
        status_quo_card = c
    # Separate hybrid disruption cards into their own column
    elif direction == "Disruption" and "Hybrid" in c.get("name", ""):
        cards_by_direction["Hybrid Disruption"].append(c)
    elif direction not in cards_by_direction:
        cards_by_direction[direction] = []
        cards_by_direction[direction].append(c)
    else:
        cards_by_direction[direction].append(c)

# Sort cards within each direction by probability (highest to lowest)
for direction in cards_by_direction:
    cards_by_direction[direction] = sorted(
        cards_by_direction[direction],
        key=lambda c: PROB_RANK.get(normalize_prob(str(c.get("probability", ""))), 0),
        reverse=True,
    )

cards_html = CARD_CSS

card_counter = 0

# Add Status Quo section at the top (simplified, no card formatting)
status_quo_card_html = ""
if status_quo_card:
    summary = str(status_quo_card.get("summary", ""))
    
    status_quo_card_html += '<div class="status-quo-section">'
    status_quo_card_html += '<div class="status-quo-label">Baseline Scenario</div>'
    status_quo_card_html += f'<div style="color: #1b1725; font-size: 0.95rem; line-height: 1.5;">{html.escape(summary)}</div>'
    status_quo_card_html += '</div>'

cards_html += status_quo_card_html

# Render Net Assessment Spotlight section
if FEATURED_DEEP_DIVES:
    spotlight_dive = FEATURED_DEEP_DIVES[0]  # Use first deep dive for now
    direction_class_spotlight = spotlight_dive["direction"].lower()
    headline_escaped = html.escape(spotlight_dive["headline"])
    forecast_escaped = html.escape(spotlight_dive["forecast"])
    date_escaped = html.escape(spotlight_dive["date"])
    analysis_escaped = html.escape(spotlight_dive["analysis"])
    source_url = html.escape(spotlight_dive["source_url"])
    
    spotlight_html = '<div class="spotlight-section">'
    spotlight_html += '<div class="spotlight-title">Developments Shaping the Current Assessment</div>'
    spotlight_html += '<div class="spotlight-container">'
    
    # Main content (60%)
    spotlight_html += f'<div class="spotlight-main {direction_class_spotlight}">'
    spotlight_html += f'<div class="spotlight-headline">{headline_escaped}</div>'
    spotlight_html += '<div class="spotlight-meta">'
    spotlight_html += f'<div class="spotlight-meta-item">📅 {date_escaped}</div>'
    spotlight_html += f'<span class="spotlight-badge {direction_class_spotlight}">{forecast_escaped}</span>'
    spotlight_html += '</div>'
    spotlight_html += f'<div class="spotlight-analysis">{analysis_escaped}</div>'
    spotlight_html += f'<a href="{source_url}" target="_blank" class="spotlight-source">Read more →</a>'
    spotlight_html += '</div>'
    
    # Articles section (40%)
    spotlight_html += '<div class="spotlight-articles">'
    for article in spotlight_dive.get("articles", []):
        article_title = html.escape(article["title"])
        article_source = html.escape(article["source"])
        article_image_path = article["image_url"]
        article_link = html.escape(article["link_url"])
        
        # Convert image to base64 data URI
        article_image_data = image_to_base64(article_image_path)
        if article_image_data is None:
            # Fallback if image can't be loaded
            article_image_data = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='140'%3E%3Crect fill='%23ddd' width='300' height='140'/%3E%3C/svg%3E"
        
        spotlight_html += '<a href="' + article_link + '" target="_blank" style="text-decoration: none;">'
        spotlight_html += '<div class="article-tile">'
        spotlight_html += f'<img src="{article_image_data}" alt="Article" class="article-image">'
        spotlight_html += '<div class="article-content">'
        spotlight_html += f'<div class="article-title">{article_title}</div>'
        spotlight_html += f'<div class="article-source">{article_source}</div>'
        spotlight_html += '<div class="article-link">Read article →</div>'
        spotlight_html += '</div></div></a>'
    spotlight_html += '</div>'
    
    spotlight_html += '</div></div>'
    cards_html += spotlight_html

cards_html += '<div class="scenario-cards-container"><div class="deck">'

# Create three piles
for pile_direction in ["Disruption", "Hybrid Disruption", "Progression"]:
    direction_lower = pile_direction.lower().replace(" ", "")
    cards_html += f'<div class="deck-pile deck-pile-{direction_lower}">'
    cards_html += f'<div class="deck-pile-header">{pile_direction}</div>'
    
    for c in cards_by_direction.get(pile_direction, []):
        card_counter += 1
        name = html.escape(str(c.get("name", "")))
        direction = html.escape(str(c.get("direction", "")))
        prob_raw = str(c.get("probability", ""))
        prob_key = normalize_prob(prob_raw)
        prob_display = html.escape(prob_raw)
        summary = str(c.get("summary", ""))  # Don't escape to allow HTML links

        # Build monitoring indicators HTML
        monitoring_indicators = c.get("monitoring_indicators", [])
        if monitoring_indicators:
            indicators_html = '<ul style="margin: 0; padding-left: 20px; font-size: 0.90rem; color: rgba(27, 23, 37, 0.75);">'
            for indicator in monitoring_indicators:
                indicators_html += f'<li>{html.escape(str(indicator))}</li>'
            indicators_html += '</ul>'
        else:
            indicators_html = '<div style="font-size: 0.90rem; color: rgba(27, 23, 37, 0.75);">Coming soon</div>'

        bar_width = PROB_WIDTH.get(prob_key, "0%")
        card_class = direction_class(c.get("direction", ""))

        # Build indicators section only for non-Status Quo cards
        indicators_section = ""
        implications_section = ""
        
        if c.get("direction") != "Status Quo":
            indicators_section = f"""
      <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(27, 23, 37, 0.15);">
        <div style="font-size: 0.85rem; font-weight: 700; color: var(--nl-navy); margin-bottom: 0.5rem;">Selected Monitoring Indicators</div>
        {indicators_html}
      </div>
"""
            
            # Build implications HTML
            implications = c.get("implications", [])
            if implications:
                implications_html = '<ul style="margin: 0; padding-left: 20px; font-size: 0.90rem; color: rgba(27, 23, 37, 0.75);">'
                for implication in implications:
                    implications_html += f'<li>{html.escape(str(implication))}</li>'
                implications_html += '</ul>'
            else:
                implications_html = '<div style="font-size: 0.90rem; color: rgba(27, 23, 37, 0.75);">Implications coming soon</div>'
            
            implications_section = f"""
      <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(27, 23, 37, 0.15);">
        <div style="font-size: 0.85rem; font-weight: 700; color: var(--nl-navy); margin-bottom: 0.5rem;">Potential Implications</div>
        {implications_html}
      </div>
"""

        cards_html += f"""
  <div class="deck-item">
    <div class="deck-card {card_class}" data-card-id="card-{card_counter}">
      <div class="deck-title">{name}</div>

      <div class="deck-meta">
        <span class="deck-chip">Direction: {direction}</span>
        <span class="deck-chip">Probability: {prob_display}</span>
      </div>

      <div class="prob-wrap">
        <div class="prob-label">Scenario Materialization Probability</div>
        <div class="prob-bar">
          <div class="prob-fill" style="width:{bar_width};"></div>
        </div>
      </div>

      <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(27, 23, 37, 0.15);">
        <div style="font-size: 0.85rem; font-weight: 700; color: var(--nl-navy); margin-bottom: 0.5rem;">Scenario Overview</div>
        <div class="deck-body">{summary}</div>
      </div>
{indicators_section}{implications_section}    </div>
  </div>
"""
    
    cards_html += '</div>'

cards_html += '</div>'  # Close scenario-cards-container
cards_html += '</div>'  # Close deck (no longer needed but keep for consistency)

# Add JavaScript for interactivity
DECK_JS = """
<script>
document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.deck-card');

  // Add click handlers
  cards.forEach((card) => {
    card.addEventListener('click', function(e) {
      e.stopPropagation();
      // Simply toggle the clicked card
      card.classList.toggle('collapsed');
    });
  });

  // Collapse all cards initially
  cards.forEach((card) => {
    card.classList.add('collapsed');
  });
});
</script>
"""

# Split rendering: Gender Currently section (Status Quo + Developments)
cards_html_current = cards_html.split('<div class="scenario-cards-container">')[0]
cards_html_current_final = cards_html_current + DECK_JS
components.html(cards_html_current_final, height=750)

# Forecast Scenarios section
st.subheader("Forecast Scenarios")
cards_html_forecast = CARD_CSS + '<div class="scenario-cards-container">' + cards_html.split('<div class="scenario-cards-container">')[1] + DECK_JS
components.html(cards_html_forecast, height=1100)

st.divider()
# ---------------------------
# NET DIRECTION BY DOMAIN OF ASSESSMENT
# ---------------------------
st.subheader("Net Direction by Domain of Assessment")

st.caption(
    "Net Direction is computed as cumulative disruption minus cumulative progression "
    "(equivalent to the sum of Slider Scores in the current filtered view)."
)

# guardrails
if DOMAIN_COL not in df_filtered.columns:
    st.warning(f"Missing expected column: {DOMAIN_COL}")
else:
    top_n = st.slider("Show top N domains", min_value=3, max_value=20, value=10, step=1)

    # compute components + net
    dom = df_filtered.copy()
    dom["Prog"] = np.where(dom["Slider Score"] < 0, -dom["Slider Score"], 0)
    dom["Disr"] = np.where(dom["Slider Score"] > 0,  dom["Slider Score"], 0)

    dom_summary = (
        dom.groupby(DOMAIN_COL, as_index=False)[["Prog", "Disr", "Slider Score"]]
           .sum()
           .rename(columns={"Slider Score": "Net Direction"})
    )
    dom_summary["Abs Net"] = dom_summary["Net Direction"].abs()

    # pick top N by absolute net (largest movement, either direction)
    dom_top = dom_summary.sort_values("Abs Net", ascending=False).head(top_n)

    # color by direction (NL colors)
    dom_top["Direction Label"] = np.where(
        dom_top["Net Direction"] > 0, "Disruption", np.where(dom_top["Net Direction"] < 0, "Progression", "Neutral")
    )

    # nicer ordering for horizontal bars
    dom_top = dom_top.sort_values("Net Direction", ascending=True)

    # chart
    domain_chart = (
        alt.Chart(dom_top)
        .mark_bar()
        .encode(
            y=alt.Y(f"{DOMAIN_COL}:N", sort=None, title="Domain of Assessment", axis=alt.Axis(labelLimit=300, labelPadding=15)),
            x=alt.X("Net Direction:Q", title="Net Direction (Progression ⟵ 0 ⟶ Disruption)"),
            color=alt.Color(
                "Direction Label:N",
                scale=alt.Scale(
                    domain=["Progression", "Disruption", "Neutral"],
                    range=[COLOR_PROGRESSION, COLOR_DISRUPTION, COLOR_NEUTRAL],
                ),
                legend=alt.Legend(title=None),
            ),
            tooltip=[
                alt.Tooltip(f"{DOMAIN_COL}:N", title="Domain"),
                alt.Tooltip("Disr:Q", title="Weighted Disruption", format=".1f"),
                alt.Tooltip("Prog:Q", title="Weighted Progression", format=".1f"),
                alt.Tooltip("Net Direction:Q", title="Net Direction", format=".1f"),
            ],
        )
        .properties(height=320)
    )

    # zero line
    zero_line = alt.Chart(pd.DataFrame({"x": [0]})).mark_rule(strokeDash=[6, 4]).encode(x="x:Q")

    st.altair_chart((domain_chart + zero_line).properties(padding={"left": 40, "right": 40, "top": 20, "bottom": 20}), use_container_width=True)

    st.markdown("""
**Explanation**

Net direction reflects the balance between disruptive and progressive developments across each domain of assessment. Values are calculated by subtracting cumulative progression scores from cumulative disruption scores (equivalent to the sum of slider scores in the filtered view). Higher values indicate domains where disruptive developments are more concentrated, while values closer to zero reflect a more balanced mix of progression and disruption.
""")

    # optional: quick table for export/readability
    with st.expander("See domain totals"):
        st.dataframe(
            dom_top[[DOMAIN_COL, "Disr", "Prog", "Net Direction"]]
                .sort_values("Net Direction", ascending=False),
            use_container_width=True
        )

# ---------------------------
# 9) FORECAST COMPOSITION (monthly, interactive legend)
# ---------------------------
st.subheader("Forecast Composition Over Time")

df_filtered["Month"] = df_filtered["Date"].dt.to_period("M").dt.to_timestamp(how="start")
monthly_forecast_counts = (
    df_filtered.groupby(["Month", FORECAST_COL]).size().reset_index(name="Count")
)

forecast_click = alt.selection_point(fields=[FORECAST_COL], bind="legend")

# Extended color palette for forecast categories
SECONDARY_COLORS = ["#1b1725", "#bfa359", "#f1f0ec", "#3b668c", "#cf5442", "#773344", "#e1bb4b", "#fade82", "#93b5c3", "#dca465", "#62af44"]

# Get unique forecast values from data to map colors consistently
forecast_categories = sorted(monthly_forecast_counts[FORECAST_COL].unique().tolist())
# Create a color mapping for each forecast category
color_range = SECONDARY_COLORS[:len(forecast_categories)]
color_scale = alt.Scale(domain=forecast_categories, range=color_range)

composition_chart = alt.Chart(monthly_forecast_counts).mark_bar().encode(
    x=alt.X("Month:T", title="Month"),
    y=alt.Y("Count:Q", title="Number of events"),
    color=alt.Color(f"{FORECAST_COL}:N", scale=color_scale, legend=alt.Legend(title="Forecast")),
    opacity=alt.condition(forecast_click, alt.value(1.0), alt.value(0.2)),
    tooltip=[
        alt.Tooltip("yearmonth(Month):T", title="Month"),
        alt.Tooltip(f"{FORECAST_COL}:N", title="Forecast"),
        alt.Tooltip("Count:Q", title="Events"),
    ],
).add_params(forecast_click).properties(height=350)

st.altair_chart(composition_chart, use_container_width=True)

st.divider()

# ---------------------------
# 10) PRIVACY-FRIENDLY DATA PREVIEW (moved to Methodology page)
# ---------------------------