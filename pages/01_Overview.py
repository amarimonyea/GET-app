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
  max-width: 280px;
  margin-top: auto;
}
</style>
""",
    unsafe_allow_html=True
)

# ---------------------------
# 3) DATA STRUCTURES (moved to Scenario_Outlook.py)
# ---------------------------

# ---------------------------
# 4) LOAD + CLEAN DATA
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

# Data cleaning: standardize forecast naming and filter corrupted values
# Standardize spacing: normalize "Forecast-" variations to "Forecast - "
df["Forecast"] = df["Forecast"].str.replace(r'Forecast\s*-\s*', 'Forecast - ', regex=True)
# Remove corrupted forecast values (e.g., "Forecast- 13")
df = df[~df["Forecast"].str.contains(r'Forecast\s*-\s*\d+$', regex=True, na=False)].copy()
# Strip trailing/leading whitespace from forecast
df["Forecast"] = df["Forecast"].str.strip()
# Remove "Forecast - " prefix to display cleaner names
df["Forecast"] = df["Forecast"].str.replace(r'^Forecast\s*-\s*', '', regex=True).str.strip()

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
    """Generate key insights from forecast_points dataframe including Status Quo."""
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
    
    # Insight 3: Status Quo forecasts count
    status_quo_count = len(forecast_points_df[forecast_points_df["Color Category"] == "Status Quo"])
    status_quo_pct = (status_quo_count / len(forecast_points_df) * 100) if len(forecast_points_df) > 0 else 0
    insights.append(f"<strong>Status Quo forecasts:</strong> {status_quo_count} forecast(s) ({status_quo_pct:.0f}% of total)")
    
    # Insight 4: Most concentrated forecast intensity
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
st.title("🌎 Gender Equality Tracker")
st.markdown("<p style='font-size: 1.3rem; color: rgba(27, 23, 37, 0.85); margin-top: -20px;'>Tracking directional shifts in the U.S. gender policy landscape</p>", unsafe_allow_html=True)

# ---------------------------
# 6) TOP METRICS
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Developments", len(df))
with col2:
    st.metric("Slider Score Range", f"{df['Slider Score'].min()} to {df['Slider Score'].max()}")

# ---------------------------
# 7) SIDEBAR FILTERS (clean + reset works)
# ---------------------------
st.sidebar.header("Filters")

def options_with_all(series: pd.Series) -> list[str]:
    vals = sorted(series.dropna().astype(str).unique().tolist())
    return vals

# Reset filters callback
def reset_filters():
    st.session_state["forecast_filter"] = []
    st.session_state["domain_filter"] = []
    st.session_state["sector_filter"] = []

st.sidebar.button("Reset Filters", on_click=reset_filters)

forecast_options = options_with_all(df[FORECAST_COL])
domain_options = options_with_all(df[DOMAIN_COL])
sector_options = options_with_all(df[SECTOR_COL])

selected_forecast = st.sidebar.multiselect("Forecast", forecast_options, key="forecast_filter")
selected_domain = st.sidebar.multiselect("Domain of Assessment", domain_options, key="domain_filter")
selected_sector = st.sidebar.multiselect("Sector Impacted", sector_options, key="sector_filter")

df_filtered = df.copy()
if selected_forecast:
    df_filtered = df_filtered[df_filtered[FORECAST_COL].astype(str).isin(selected_forecast)]
if selected_domain:
    df_filtered = df_filtered[df_filtered[DOMAIN_COL].astype(str).isin(selected_domain)]
if selected_sector:
    df_filtered = df_filtered[df_filtered[SECTOR_COL].astype(str).isin(selected_sector)]

st.sidebar.caption(f"Showing {len(df_filtered)} of {len(df)} developments")

# Forecast Direction
st.sidebar.subheader("Forecast Direction")
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
    latest_by_forecast = latest_by_forecast[[FORECAST_COL, "Date", "Development Short", "Slider Score", DOMAIN_COL, SECTOR_COL, "Link"]].rename(
        columns={"Date": "Latest Date", "Development Short": "Latest Development", "Slider Score": "Latest Slider Score", DOMAIN_COL: "Latest Domain", SECTOR_COL: "Latest Sector", "Link": "Latest Link"}
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
    forecast_points["Latest Link"] = None

if forecast_points.empty:
    st.info("No data available for the current filters.")
else:
    # Extract key statistics for the explanation (needed first)
    max_disr_idx = forecast_points["Disr"].idxmax()
    max_disr_name = forecast_points.loc[max_disr_idx, FORECAST_COL]
    max_disr_score = forecast_points.loc[max_disr_idx, "Disr"]
    
    max_prog_idx = forecast_points["Prog"].idxmax()
    max_prog_name = forecast_points.loc[max_prog_idx, FORECAST_COL]
    max_prog_score = forecast_points.loc[max_prog_idx, "Prog"]
    
    latest_date = df_filtered["Date"].max()
    date_str = latest_date.strftime("%B %d, %Y") if pd.notna(latest_date) else "No data"
    
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

    # Add color category based on forecast type and direction
    def get_color_category(row):
        if "Status Quo" in str(row[FORECAST_COL]):
            return "Status Quo"
        elif row["Net Direction"] > 0:
            return "Disruption"
        else:
            return "Progression"
    
    forecast_points["Color Category"] = forecast_points.apply(get_color_category, axis=1)

    # Points with color mapped to category
    points = alt.Chart(forecast_points).mark_circle(
    size=260,
    stroke="white",
    strokeWidth=1.5
).encode(
    x=alt.X("Cumulative Intensity:Q", title="Cumulative Intensity"),
    y=alt.Y("Net Direction:Q", title="Net Direction", scale=alt.Scale(padding=20)),
    color=alt.Color(
        "Color Category:N",
        scale=alt.Scale(
            domain=["Status Quo", "Disruption", "Progression"],
            range=["#62af44", "#cf5442", "#3b668c"]
        ),
        legend=None
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
      <div style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 16px; height: 16px; background-color: #62af44; border-radius: 2px;"></div>
        <span>Status Quo</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)
    
    # How to Interpret This Chart section (directly after chart)
    with st.expander("How to Interpret This Chart", expanded=False):
        st.markdown("""
The Disruption and Progression Momentum graph plots cumulative forecast intensity against net directional movement. Cumulative intensity reflects the volume and concentration of forecasted developments within a domain (emerging → accelerating), while vertical positioning distinguishes between disruptive and progressive trajectories. The quadrant framework highlights which issue areas are early-stage signals versus accelerating structural shifts.
""")
    
    # Statistics below chart
    st.markdown(f"""
**Highest cumulative disruption observed to date:** {max_disr_name} (cumulative disruption score: {max_disr_score:.1f})

**Highest cumulative progression observed to date:** {max_prog_name} (cumulative progression score: {max_prog_score:.1f})

**Data current as of:** {date_str}
""")
    
    # Key Insights Strip
    insights_list = get_key_insights(forecast_points, FORECAST_COL)
    insights_html = "\n".join([f"<li style='margin-bottom: 0.5rem; color: #1b1725; font-size: 1rem;'>{insight}</li>" for insight in insights_list])
    
    st.markdown(f"""
    <div style="background-color: #f1f0ec; border-left: 4px solid #bfa359; padding: 1rem; margin: 1.5rem 0; border-radius: 2px; box-shadow: 0 1px 3px rgba(27, 23, 37, 0.08);">
      <div style="font-size: 1.1rem; font-weight: 700; color: #1b1725; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em;">Key Insights</div>
      <ul style="margin: 0; padding-left: 1.5rem; list-style: disc;">
        {insights_html}
      </ul>
    </div>
    """, unsafe_allow_html=True)

    # Latest Development by Forecast panel
    with st.expander("Latest Developments by Forecast", expanded=False):
        if not df_filtered.empty:
            latest_events_display = forecast_points[[FORECAST_COL, "Latest Date Str", "Latest Development", "Latest Domain", "Latest Sector", "Latest Slider Score", "Latest Link"]].copy()
            latest_events_display = latest_events_display[latest_events_display["Latest Date Str"] != "No data"]
            # Remove rows with NaN values in critical columns
            latest_events_display = latest_events_display.dropna(subset=["Latest Development", "Latest Date Str"])
            
            if not latest_events_display.empty:
                latest_events_display = latest_events_display.rename(columns={
                    FORECAST_COL: "Forecast",
                    "Latest Date Str": "Date",
                    "Latest Development": "Development Title",
                    "Latest Domain": "Domain",
                    "Latest Sector": "Sector",
                    "Latest Slider Score": "Score",
                    "Latest Link": "Source"
                })
                # Sort by date descending (most recent first)
                latest_events_display["Date"] = pd.to_datetime(latest_events_display["Date"], format="%b %d, %Y", errors="coerce")
                latest_events_display = latest_events_display.sort_values("Date", ascending=False).head(5)
                latest_events_display["Date"] = latest_events_display["Date"].dt.strftime("%b %d, %Y")
                latest_events_display = latest_events_display[[c for c in ["Forecast", "Date", "Development Title", "Score", "Source"] if c in latest_events_display.columns]]
                
                # Cap Development Title at 100 characters without breaking words
                def truncate_at_word_boundary(text, max_length=100):
                    if pd.isna(text) or not isinstance(text, str):
                        return ""
                    if len(text) <= max_length:
                        return text
                    truncated = text[:max_length]
                    last_space = truncated.rfind(' ')
                    if last_space > 0:
                        return truncated[:last_space] + "..."
                    return truncated + "..."
                
                # Extract domain from URL and format as readable source name
                def extract_source_name(url):
                    if pd.isna(url) or not url:
                        return "Unknown"
                    
                    # Mapping of domain names to proper publication names
                    source_mapping = {
                        "usatoday": "USA Today",
                        "nytimes": "New York Times",
                        "wsj": "Wall Street Journal",
                        "politico": "Politico",
                        "thehill": "The Hill",
                        "reuters": "Reuters",
                        "bbc": "BBC",
                        "cnn": "CNN",
                        "foxnews": "Fox News",
                        "sltrib": "Salt Lake Tribune",
                        "congress": "Congress.gov",
                        "scotus": "SCOTUS",
                        "whitehouse": "White House",
                        "npr": "NPR",
                        "theguardian": "The Guardian",
                        "bloomberg": "Bloomberg",
                        "bgov": "Bloomberg Government",
                        "cnbc": "CNBC",
                        "axios": "Axios",
                        "vox": "Vox",
                        "cpr": "Colorado Public Radio",
                    }
                    
                    try:
                        from urllib.parse import urlparse
                        parsed = urlparse(str(url))
                        domain = parsed.netloc.replace("www.", "").lower()
                        
                        # Split by dots to get domain parts
                        domain_parts = domain.split(".")
                        
                        # Try to find the main domain (second-to-last part before TLD)
                        # For news.bgov.com, we want "bgov"
                        # For usatoday.com, we want "usatoday"
                        if len(domain_parts) >= 2:
                            # Try the second-to-last part first (handles news.bgov.com, etc.)
                            main_domain = domain_parts[-2]
                        else:
                            main_domain = domain_parts[0]
                        
                        # Check if we have a mapping for this domain
                        if main_domain in source_mapping:
                            return source_mapping[main_domain]
                        
                        # If not found, try the first part (for simple domains)
                        if len(domain_parts) > 1 and domain_parts[0] in source_mapping:
                            return source_mapping[domain_parts[0]]
                        
                        # Otherwise, format the main domain name
                        main_domain = main_domain.replace("-", " ").replace("_", " ")
                        return main_domain.title()
                    except:
                        return "Unknown"
                
                latest_events_display["Development Title"] = latest_events_display["Development Title"].apply(truncate_at_word_boundary)
                latest_events_display["Source"] = latest_events_display["Source"].apply(extract_source_name)
                
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
# 9) NET DIRECTION BY DOMAIN OF ASSESSMENT
# ---------------------------
st.subheader("Net Direction by Domain of Assessment")

st.caption(
    "Net direction reflects the balance between disruptive and progressive developments across domains of assessment based on the currently selected filters. Values represent cumulative disruption minus cumulative progression."
)

# guardrails
if DOMAIN_COL not in df_filtered.columns:
    st.warning(f"Missing expected column: {DOMAIN_COL}")
else:
    # Fixed top N domains to display
    top_n = 10

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
            x=alt.X("Net Direction:Q", title="Net Direction Score (Progression ← 0 → Disruption)"),
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

    with st.expander("How to Interpret This Chart", expanded=False):
        st.markdown("""
Net direction indicates whether developments within each domain are trending towards disruption or progression. The value reflects the difference between cumulative disruption and progression based on the currently selected forecast type, sector, and group filters. Higher values indicate domains where disruptive developments trend higher, while values closer to zero indicate a more balanced mix of disruption and progression.
""")

    # Key Insights for Domain Assessment (only if data exists)
    if not dom_top.empty:
        dom_sorted = dom_top.sort_values("Net Direction", ascending=False)
        max_disruption_domain = dom_sorted.iloc[0][DOMAIN_COL]
        max_disruption_value = dom_sorted.iloc[0]["Net Direction"]
        
        min_disruption_domain = dom_sorted.iloc[-1][DOMAIN_COL]
        min_disruption_value = dom_sorted.iloc[-1]["Net Direction"]
        
        # Find most balanced (closest to zero)
        dom_balance = dom_top.copy()
        dom_balance["Balance"] = abs(dom_balance["Net Direction"])
        most_balanced_domain = dom_balance.loc[dom_balance["Balance"].idxmin(), DOMAIN_COL]
        most_balanced_value = dom_balance.loc[dom_balance["Balance"].idxmin(), "Net Direction"]
        
        domain_insights_list = [
            f"<strong>Most disruption-oriented domain:</strong> {max_disruption_domain} (net direction: {max_disruption_value:.1f})",
            f"<strong>Most progression-oriented domain:</strong> {min_disruption_domain} (net direction: {min_disruption_value:.1f})",
            f"<strong>Most balanced domain:</strong> {most_balanced_domain} (net direction: {most_balanced_value:.1f})"
        ]
        domain_insights_html = "\n".join([f"<li style='margin-bottom: 0.5rem; color: #1b1725; font-size: 1rem;'>{insight}</li>" for insight in domain_insights_list])
        
        st.markdown(f"""
        <div style="background-color: #f1f0ec; border-left: 4px solid #bfa359; padding: 1rem; margin: 1.5rem 0; border-radius: 2px; box-shadow: 0 1px 3px rgba(27, 23, 37, 0.08);">
          <div style="font-size: 1.1rem; font-weight: 700; color: #1b1725; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em;">Key Insights</div>
          <ul style="margin: 0; padding-left: 1.5rem; list-style: disc;">
            {domain_insights_html}
          </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Domain totals table (interactive)
        with st.expander("Domain Totals Table", expanded=False):
            st.dataframe(
                dom_top[[DOMAIN_COL, "Disr", "Prog", "Net Direction"]]
                    .sort_values("Net Direction", ascending=False),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("No domain data available for the current filters.")

# ---------------------------
# 9) FORECAST COMPOSITION (monthly, two-level hierarchy)
# ---------------------------
st.subheader("Forecast Composition Over Time")

# Add a Direction column based on forecast name
def get_direction(forecast_name):
    if pd.isna(forecast_name):
        return "Unknown"
    forecast_name = str(forecast_name).lower()
    if "status quo" in forecast_name:
        return "Status Quo"
    elif any(word in forecast_name for word in ["disruption", "disruption"]):
        return "Disruption"
    else:  # Contains "progression" or other
        return "Progression"

df_filtered["Direction"] = df_filtered[FORECAST_COL].apply(get_direction)

# Aggregate daily data into monthly totals
df_filtered["Month"] = df_filtered["Date"].dt.to_period("M").dt.to_timestamp(how="start")

# Create month-year label for display (e.g., "Jan 2025")
df_filtered["MonthLabel"] = df_filtered["Date"].dt.strftime("%b %Y")

# Prepare data for top-level (direction) chart
monthly_direction_counts = (
    df_filtered.groupby(["Month", "MonthLabel", "Direction"]).size().reset_index(name="Count")
).sort_values("Month")

# Prepare data for breakdown chart (by forecast type)
monthly_forecast_counts = (
    df_filtered.groupby(["Month", "MonthLabel", "Direction", FORECAST_COL]).size().reset_index(name="Count")
).sort_values("Month")

# Interactive selection on direction
direction_click = alt.selection_point(fields=["Direction"], bind="legend")

# Top level chart: Direction (Progression, Status Quo, Disruption)
direction_colors = alt.Scale(
    domain=["Progression", "Status Quo", "Disruption"],
    range=[COLOR_PROGRESSION, "#62af44", COLOR_DISRUPTION]
)

# Calculate monthly totals for display
monthly_totals = monthly_direction_counts.groupby("MonthLabel")["Count"].sum().reset_index()
month_label_sort = list(monthly_direction_counts["MonthLabel"].unique())

direction_chart = alt.Chart(monthly_direction_counts).mark_bar().encode(
    x=alt.X("MonthLabel:N", title="Month", sort=month_label_sort, axis=alt.Axis(labelAngle=0), scale=alt.Scale(paddingInner=0.3)),
    y=alt.Y("Count:Q", title="Number of Developments", stack="zero"),
    color=alt.Color(
        "Direction:N",
        scale=direction_colors,
        legend=alt.Legend(title="Forecast Direction", orient="top", direction="horizontal")
    ),
    opacity=alt.condition(direction_click, alt.value(1.0), alt.value(0.2)),
    tooltip=[
        alt.Tooltip("MonthLabel:N", title="Month"),
        alt.Tooltip("Direction:N", title="Direction"),
        alt.Tooltip("Count:Q", title="Developments"),
    ],
).add_params(direction_click).properties(
    title=alt.TitleParams(
        text="Monthly Forecast Composition",
        anchor="middle",
        fontSize=14,
        fontWeight="bold"
    )
)

# Add text labels with monthly totals on top of bars
total_text = alt.Chart(monthly_totals).mark_text(dy=-5, fontSize=11, fontWeight="bold").encode(
    x=alt.X("MonthLabel:N", sort=month_label_sort),
    y=alt.Y("Count:Q"),
    text=alt.Text("Count:Q")
)

direction_chart_with_totals = (direction_chart + total_text).properties(height=300, width=1000)

# Second chart: Breakdown by forecast type (filtered by clicked direction)
if not monthly_forecast_counts.empty:
    st.markdown("**Breakdown by Forecast Type** — Click a direction in the Forecast Direction legend above to highlight only that direction's forecast types")
    
    # Extended color palette for forecast categories
    SECONDARY_COLORS = ["#1b1725", "#bfa359", "#f1f0ec", "#3b668c", "#cf5442", "#773344", "#e1bb4b", "#fade82", "#93b5c3", "#dca465", "#62af44"]
    
    # Get unique forecast values from data to map colors consistently
    forecast_categories = sorted(monthly_forecast_counts[FORECAST_COL].unique().tolist())
    
    # Custom color mapping for all forecast types - each with distinct color
    custom_colors = {
        "Diplomatic Disruption": "#d97e7a",           # Light red
        "Diplomatic Progression": "#5081a3",          # Deep blue
        "Economic Disruption": "#c94b3a",             # Dark red
        "Economic Progression": "#7fa3c0",            # Light blue
        "Hybrid Political/Security Disruption": "#8b4453",   # Burgundy
        "Hybrid Political/Social Disruption": "#6b9d7d",     # Sage green
        "Political Disruption": "#e85c52",            # Bright red-orange
        "Political Progression": "#2d5375",           # Navy blue
        "Social Disruption": "#f4896f",               # Coral
        "Social Progression": "#4a95d8",              # Sky blue
        "Status Quo": "#62af44"                       # Green
    }
    
    # Build color range: use custom colors for specified types, fill rest with SECONDARY_COLORS
    color_range = []
    used_secondary_colors = []
    for cat in forecast_categories:
        if cat in custom_colors:
            color_range.append(custom_colors[cat])
        else:
            # Use remaining colors from SECONDARY_COLORS
            available_secondary = [c for c in SECONDARY_COLORS if c not in used_secondary_colors and c not in color_range]
            if available_secondary:
                color_range.append(available_secondary[0])
                used_secondary_colors.append(available_secondary[0])
            else:
                color_range.append(SECONDARY_COLORS[0])
    
    forecast_color_scale = alt.Scale(domain=forecast_categories, range=color_range)
    
    # Calculate monthly totals for breakdown chart
    monthly_breakdown_totals = monthly_forecast_counts.groupby("MonthLabel")["Count"].sum().reset_index()
    breakdown_month_sort = list(monthly_forecast_counts["MonthLabel"].unique())
    
    breakdown_chart = alt.Chart(monthly_forecast_counts).mark_bar().encode(
        x=alt.X("MonthLabel:N", title="Month", sort=breakdown_month_sort, axis=alt.Axis(labelAngle=0), scale=alt.Scale(paddingInner=0.3)),
        y=alt.Y("Count:Q", title="Number of Developments", stack="zero"),
        color=alt.Color(f"{FORECAST_COL}:N", scale=forecast_color_scale, legend=alt.Legend(title="Forecast Type", orient="bottom", direction="horizontal", titleFontSize=12, labelFontSize=10, columns=4)),
        opacity=alt.condition(
            direction_click,
            alt.value(1.0),
            alt.value(0.15)
        ),
        tooltip=[
            alt.Tooltip("MonthLabel:N", title="Month"),
            alt.Tooltip("Direction:N", title="Direction"),
            alt.Tooltip(f"{FORECAST_COL}:N", title="Forecast Type"),
            alt.Tooltip("Count:Q", title="Developments"),
        ],
    ).properties(
        height=300,
        width=1000,
        title=alt.TitleParams(
            text="Breakdown by Forecast Type — Select a direction above to see which specific forecast types are associated with each direction",
            anchor="middle",
            fontSize=14,
            fontWeight="bold"
        )
    )
    
    # Combine both charts vertically so interaction works across both
    # Using alt.vconcat() for vertical stacking with shared interaction
    combined_chart = alt.vconcat(direction_chart_with_totals, breakdown_chart).properties(
        spacing=20
    ).resolve_scale(color='independent')
    
    st.altair_chart(combined_chart, use_container_width=True)
    
    with st.expander("How to Interpret This Chart", expanded=False):
        st.markdown("""
These charts show how forecast developments are distributed over time. The top chart displays the total number of developments grouped by direction (disruption, status quo, and progression). The lower chart breaks those developments down by forecast type. Selecting a direction in the top chart filters the lower chart to highlight the associated forecasts.
""")
    
    # Key Insights for Forecast Composition
    if not monthly_direction_counts.empty:
        # Calculate totals by direction
        direction_totals = monthly_direction_counts.groupby("Direction")["Count"].sum().sort_values(ascending=False)
        most_represented_direction = direction_totals.idxmax()
        most_represented_count = direction_totals.max()
        
        # Calculate totals by forecast type
        forecast_totals = monthly_forecast_counts.groupby(FORECAST_COL)["Count"].sum().sort_values(ascending=False)
        most_represented_forecast = forecast_totals.idxmax()
        most_represented_forecast_count = forecast_totals.max()
        
        # Calculate total developments
        total_developments = monthly_forecast_counts["Count"].sum()
        
        composition_insights_list = [
            f"<strong>Most represented direction:</strong> {most_represented_direction} ({most_represented_count} developments)",
            f"<strong>Most represented forecast type:</strong> {most_represented_forecast} ({most_represented_forecast_count} developments)",
            f"<strong>Total developments tracked:</strong> {total_developments} developments"
        ]
        composition_insights_html = "\n".join([f"<li style='margin-bottom: 0.5rem; color: #1b1725; font-size: 1rem;'>{insight}</li>" for insight in composition_insights_list])
        
        st.markdown(f"""
        <div style="background-color: #f1f0ec; border-left: 4px solid #bfa359; padding: 1rem; margin: 1.5rem 0; border-radius: 2px; box-shadow: 0 1px 3px rgba(27, 23, 37, 0.08);">
          <div style="font-size: 1.1rem; font-weight: 700; color: #1b1725; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em;">Key Insights</div>
          <ul style="margin: 0; padding-left: 1.5rem; list-style: disc;">
            {composition_insights_html}
          </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Expandable data table
    with st.expander("View Monthly Forecast Data"):
        # Create pivot table by direction using MonthLabel for display, sorted by Month
        monthly_direction_pivot = (
            monthly_direction_counts[["Month", "MonthLabel", "Direction", "Count"]]
            .pivot_table(index="MonthLabel", columns="Direction", values="Count", aggfunc="sum")
            .fillna(0)
            .astype(int)
        )
        monthly_direction_pivot.index.name = "Month"
        # Sort by converting back to datetime for proper month ordering
        month_order = sorted(monthly_direction_counts[["Month", "MonthLabel"]].drop_duplicates()["MonthLabel"].tolist())
        monthly_direction_pivot = monthly_direction_pivot.reindex(month_order)
        
        # Create pivot table by forecast type using MonthLabel for display
        monthly_forecast_pivot = (
            monthly_forecast_counts[["Month", "MonthLabel", FORECAST_COL, "Count"]]
            .pivot_table(index="MonthLabel", columns=FORECAST_COL, values="Count", aggfunc="sum")
            .fillna(0)
            .astype(int)
        )
        monthly_forecast_pivot.index.name = "Month"
        # Sort by month ordering
        monthly_forecast_pivot = monthly_forecast_pivot.reindex(month_order)
        
        # Use tabs for the two views
        tab1, tab2 = st.tabs(["By Direction", "By Forecast Type"])
        
        with tab1:
            st.dataframe(
                monthly_direction_pivot.iloc[::-1],
                use_container_width=True,
                hide_index=False
            )
        
        with tab2:
            st.dataframe(
                monthly_forecast_pivot.iloc[::-1],
                use_container_width=True,
                hide_index=False
            )

st.divider()

# ---------------------------
# 10) PRIVACY-FRIENDLY DATA PREVIEW (moved to Methodology page)
# ---------------------------