import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import altair as alt
import html
import textwrap
import base64
import os
from urllib.parse import urlparse

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
DATA_PATH = "data/Monitor - Gender Equality - GET 2025 (1).csv"
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

# ---------------------------
# SIGNPOST MAPPING (Full to Short Labels)
# ---------------------------
SIGNPOST_MAPPING = {
    "Signpost - Legislative or executive actions restricting reproductive, gender, or workplace rights": "legislative restrictions",
    "Signpost - US withdrawal from or defunding of international organizations advancing gender, LGBTQ+, or reproductive rights": "international withdrawal",
    "Signpost - Public information and data erasure in government systems": "information erasure",
    "Signpost - Politicization or repurposing of protective institutions for political objectives": "institutional politicization",
    "Signpost - Changes to legal recognition of gender and family structure": "legal recognition changes",
    "Signpost - Increased use of executive orders to circumvent legislative and judicial constraints": "executive overreach",
    "Signpost - Removal of qualified civil servants and service members in national security sectors due to sexual orientation or gender identity": "personnel removal",
    "Signpost - Reduction of protections against gender-based violence": "violence protection rollback",
    "Signpost - Service withdrawal or denial driven by anticipated legal, financial, or political retaliation": "service withdrawal",
    "Signpost - Institutional adoption of gender-restrictive participation policies in education and sports": "participation restrictions",
    "Signpost - Judicial challenges seeking to weaken, reinterpret, or overturn gender-related civil rights precedents": "legal challenges",
    "Signpost - State or federal policy actions that establish, reinstate, or expand gender, reproductive, or LGBTQ+ protections": "rights expansions",
    "Signpost - State-level legal challenges seeking to block or overturn federal gender restrictive actions": "state legal defense",
    "Signpost - Cuts or divestments in federal scientific, evidence-based research, or mass media related to equity, gender, or social policy": "research defunding",
    "Signpost - Judicial challenges seeking to weaken…": "legal challenges",
}

def get_signpost_label(signpost_text):
    """Convert full signpost text to short label."""
    if pd.isna(signpost_text):
        return "other"
    signpost_text = str(signpost_text).strip()
    return SIGNPOST_MAPPING.get(signpost_text, signpost_text[:40] + "…")

def get_top_signposts_for_forecast(data_df, forecast_name, top_n=2):
    """
    Extract top N most frequent signposts for a given forecast category.
    Excludes Status Quo developments.
    Returns list of short label strings.
    """
    if data_df.empty:
        return []
    
    # Filter to the specific forecast and exclude empty signposts
    filtered = data_df[
        (data_df["Forecast"].str.strip() == forecast_name.strip()) & 
        (data_df["Signpost"].notna())
    ]
    
    if filtered.empty:
        return []
    
    # Group by signpost and count
    signpost_counts = filtered["Signpost"].value_counts()
    
    # Get top N and convert to short labels
    top_signposts = []
    for signpost in signpost_counts.head(top_n).index:
        label = get_signpost_label(signpost)
        top_signposts.append(label)
    
    return top_signposts

def get_top_developments_for_forecast(data_df, forecast_name, top_n=2):
    """
    Extract top N contributing developments for a given forecast category.
    Selects by highest score magnitude first, recency as tiebreaker.
    
    Args:
        data_df: Filtered data containing all developments
        forecast_name: Forecast category to filter by
        top_n: Number of developments to return (default: 2)
    
    Returns:
        List of tuples: (shortened_text, full_development_text, source_url, score)
    """
    if data_df.empty:
        return []
    
    # Filter to the specific forecast
    filtered = data_df[
        (data_df["Forecast"].str.strip() == forecast_name.strip()) & 
        (data_df["Development Short"].notna())
    ]
    
    if filtered.empty:
        return []
    
    # Sort by absolute score magnitude (descending), then by date (descending for recency)
    filtered = filtered.copy()
    filtered["Abs Score"] = filtered["Slider Score"].abs()
    filtered = filtered.sort_values(
        by=["Abs Score", "Date"],
        ascending=[False, False]
    )
    
    # Get top N developments with full details
    top_developments = []
    for idx, row in filtered.head(top_n).iterrows():
        short_text = row["Development Short"]
        full_text = row["Development"]
        source_url = row.get("Link", "")
        score = row["Slider Score"]
        top_developments.append((short_text, full_text, source_url, score))
    
    return top_developments

def get_top_developments_for_domain(data_df, domain_name, top_n=2):
    """
    Extract top N contributing developments for a given domain of assessment.
    Selects by highest score magnitude first, recency as tiebreaker.
    
    Args:
        data_df: Filtered data containing all developments
        domain_name: Domain of assessment to filter by
        top_n: Number of developments to return (default: 2)
    
    Returns:
        List of tuples: (shortened_text, full_development_text, source_url, score)
    """
    if data_df.empty:
        return []
    
    # Filter to the specific domain
    filtered = data_df[
        (data_df["Domains of Assessment"].str.strip() == domain_name.strip()) & 
        (data_df["Development Short"].notna())
    ]
    
    if filtered.empty:
        return []
    
    # Sort by absolute score magnitude (descending), then by date (descending for recency)
    filtered = filtered.copy()
    filtered["Abs Score"] = filtered["Slider Score"].abs()
    filtered = filtered.sort_values(
        by=["Abs Score", "Date"],
        ascending=[False, False]
    )
    
    # Get top N developments with full details
    top_developments = []
    for idx, row in filtered.head(top_n).iterrows():
        short_text = row["Development Short"]
        full_text = row["Development"]
        source_url = row.get("Link", "")
        score = row["Slider Score"]
        top_developments.append((short_text, full_text, source_url, score))
    
    return top_developments

def get_top_developments_for_direction(data_df, direction, top_n=2):
    """
    Extract top N contributing developments for a given direction (Deteriorating, Improving, Status Quo).
    Selects by highest score magnitude first, recency as tiebreaker.
    
    Args:
        data_df: Filtered data containing all developments
        direction: Direction to filter by ("Deteriorating", "Improving", "Status Quo")
        top_n: Number of developments to return (default: 2)
    
    Returns:
        List of tuples: (shortened_text, full_development_text, source_url, score)
    """
    if data_df.empty:
        return []
    
    # Filter based on direction using Slider Score
    if direction == "Deteriorating":
        filtered = data_df[(data_df["Slider Score"] > 0) & (data_df["Development Short"].notna())]
    elif direction == "Improving":
        filtered = data_df[(data_df["Slider Score"] < 0) & (data_df["Development Short"].notna())]
    else:  # Status Quo
        filtered = data_df[(data_df["Slider Score"] == 0) & (data_df["Development Short"].notna())]
    
    if filtered.empty:
        return []
    
    # Sort by absolute score magnitude (descending), then by date (descending for recency)
    filtered = filtered.copy()
    filtered["Abs Score"] = filtered["Slider Score"].abs()
    filtered = filtered.sort_values(
        by=["Abs Score", "Date"],
        ascending=[False, False]
    )
    
    # Get top N developments with full details
    top_developments = []
    for idx, row in filtered.head(top_n).iterrows():
        short_text = row["Development Short"]
        full_text = row["Development"]
        source_url = row.get("Link", "")
        score = row["Slider Score"]
        top_developments.append((short_text, full_text, source_url, score))
    
    return top_developments

def get_best_development_for_forecast(data_df, forecast_name, used_indices=None):
    """
    Get the best representative development for a forecast using deterministic ranking.
    
    Ranking criteria:
    - Highest absolute score magnitude (impact)
    - Most recent (by date) as tiebreaker
    
    Args:
        data_df: Filtered development data
        forecast_name: Name of the forecast to filter
        used_indices: Set of already-used index values to avoid repetition
    
    Returns:
        Tuple of (full_sentence, score, idx) or None if no qualifying development found
    """
    if data_df is None or data_df.empty:
        return None
    
    used_indices = used_indices or set()
    
    # Filter to matching forecast
    forecast_data = data_df[data_df["Forecast"].astype(str) == forecast_name].copy()
    
    if forecast_data.empty:
        return None
    
    # Remove already-used developments
    forecast_data = forecast_data[~forecast_data.index.isin(used_indices)]
    
    if forecast_data.empty:
        return None
    
    # Rank by absolute score (magnitude), then by date (recency)
    forecast_data["Abs Score"] = forecast_data["Slider Score"].abs()
    forecast_data = forecast_data.sort_values(
        by=["Abs Score", "Date"],
        ascending=[False, False]
    )
    
    # Get the top development
    best_row = forecast_data.iloc[0]
    full_text = best_row["Development"]
    score = best_row["Slider Score"]
    idx = best_row.name
    
    # Extract only the first sentence from the full development text
    import re
    full_text = str(full_text).strip() if pd.notna(full_text) else ""
    # Split on sentence-ending punctuation
    first_sentence = re.split(r'[.!?]\s+', full_text)[0].strip()
    if first_sentence:
        # Only add period if it doesn't already end with punctuation
        if not first_sentence.endswith(('.', '!', '?')):
            first_sentence += "."
    else:
        first_sentence = full_text[:100] + "." if len(full_text) > 100 else full_text
    
    return (first_sentence, score, idx)

def get_key_insights(forecast_points_df, forecast_col, data_df=None, used_indices=None):
    """
    Generate clean, dynamic key insights with three distinct analytical takeaways.
    
    Three insights per section:
    - Insight 1: Highest cumulative deterioration
    - Insight 2: Highest cumulative improvement
    - Insight 3: Overall pattern (deterioration vs improvement skew)
    
    Requirements:
    - Each insight is one concise sentence with natural language phrasing
    - One plain-text example per insight (not styled or expandable)
    - Examples are deterministically selected (not random)
    - No examples are repeated across insights
    - Fully responsive to sidebar filters
    
    Args:
        forecast_points_df: Aggregated forecast data
        forecast_col: Forecast column name
        data_df: Original detailed data (used for development extraction)
        used_indices: Set of already-used development indices to avoid repetition (updated in place)
    
    Returns:
        Tuple of (insights_list, updated_used_indices_set)
    """
    if forecast_points_df.empty:
        return (["No insights available for the selected filters."], used_indices or set())
    
    if used_indices is None:
        used_indices = set()
    
    def transform_forecast_name(name):
        """Transform forecast names from old terminology to new terminology"""
        return str(name).replace("Disruption", "Deteriorating").replace("Progression", "Improving")
    
    insights = []
    
    # Insight 1: Highest cumulative deterioration
    if "Disr" in forecast_points_df.columns and forecast_points_df["Disr"].max() > 0:
        max_disr_idx = forecast_points_df["Disr"].idxmax()
        max_disr_name = forecast_points_df.loc[max_disr_idx, forecast_col]
        max_disr_name_display = transform_forecast_name(max_disr_name)
        max_disr_score = forecast_points_df.loc[max_disr_idx, "Disr"]
        
        # Use natural language: "{forecast} developments show..." instead of "{forecast} Deteriorating shows..."
        insight_text = f"{max_disr_name_display} developments show the highest cumulative deterioration (+{max_disr_score:.1f})."
        
        # Get representative example for this forecast
        if data_df is not None and not data_df.empty:
            dev_info = get_best_development_for_forecast(data_df, max_disr_name, used_indices)
            if dev_info:
                short_text, score, dev_idx = dev_info
                used_indices.add(dev_idx)
                insight_text += f"\nExample: {short_text}"
        
        insights.append(insight_text)
    
    # Insight 2: Highest cumulative improvement
    if "Prog" in forecast_points_df.columns and forecast_points_df["Prog"].max() > 0:
        max_prog_idx = forecast_points_df["Prog"].idxmax()
        max_prog_name = forecast_points_df.loc[max_prog_idx, forecast_col]
        max_prog_name_display = transform_forecast_name(max_prog_name)
        max_prog_score = forecast_points_df.loc[max_prog_idx, "Prog"]
        
        # Use natural language "also account for" to show this is the counterpoint to deterioration
        insight_text = f"{max_prog_name_display} developments also account for the largest cumulative improvement (–{max_prog_score:.1f})."
        
        # Get representative example for this forecast
        if data_df is not None and not data_df.empty:
            dev_info = get_best_development_for_forecast(data_df, max_prog_name, used_indices)
            if dev_info:
                short_text, score, dev_idx = dev_info
                used_indices.add(dev_idx)
                insight_text += f"\nExample: {short_text}"
        
        insights.append(insight_text)
    
    # Insight 3: Overall pattern (deterioration vs improvement skew)
    total_disr = forecast_points_df["Disr"].sum() if "Disr" in forecast_points_df.columns else 0
    total_prog = forecast_points_df["Prog"].sum() if "Prog" in forecast_points_df.columns else 0
    
    if total_disr > 0 or total_prog > 0:
        # Describe the overall skew/imbalance pattern
        if total_disr > total_prog:
            skew_insight = f"Overall, activity is heavily skewed toward deterioration (+{total_disr:.1f}) rather than improvement (–{total_prog:.1f})."
        else:
            skew_insight = f"Overall, activity shows meaningful improvement (–{total_prog:.1f}), outweighing deterioration (+{total_disr:.1f})."
        
        # Get a representative example that illustrates the overall pattern
        if data_df is not None and not data_df.empty:
            # Try to find an example from the highest deterioration forecast if deterioration dominates
            if total_disr > total_prog and "Disr" in forecast_points_df.columns:
                max_disr_idx = forecast_points_df["Disr"].idxmax()
                max_disr_name = forecast_points_df.loc[max_disr_idx, forecast_col]
                dev_info = get_best_development_for_forecast(data_df, max_disr_name, used_indices)
            else:
                max_prog_idx = forecast_points_df["Prog"].idxmax()
                max_prog_name = forecast_points_df.loc[max_prog_idx, forecast_col]
                dev_info = get_best_development_for_forecast(data_df, max_prog_name, used_indices)
            
            if dev_info:
                short_text, score, dev_idx = dev_info
                used_indices.add(dev_idx)
                skew_insight += f"\nExample: {short_text}"
        
        insights.append(skew_insight)
    
    return (insights if insights else ["No significant patterns detected in the selected data."], used_indices)

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
st.title("🌎 U.S. Gender Equality Tracker")
st.markdown("<p style='font-size: 1.3rem; color: rgba(27, 23, 37, 0.85); margin-top: -20px;'>Tracking directional shifts in the U.S. gender policy landscape</p>", unsafe_allow_html=True)

# ---------------------------
# 6) TOP METRICS
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Developments", len(df))
with col2:
    st.metric("Slider Score Range", f"{df['Slider Score'].min()} to {df['Slider Score'].max()}")
    st.markdown(f"<p style='font-size: 0.85rem; margin-top: -10px;'><a href='./Methodology' target='_self' style='color: #3b668c; text-decoration: none;'>Learn more about scoring →</a></p>", unsafe_allow_html=True)

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

# Transform forecast labels: Disruption -> Deteriorating, Progression -> Improving
def transform_forecast_label(label):
    """Transform forecast labels for display"""
    label = str(label).replace("Disruption", "Deteriorating").replace("Progression", "Improving")
    return label

forecast_options_display = [transform_forecast_label(f) for f in forecast_options]

# Reverse mapping for filtering
forecast_mapping = {transform_forecast_label(f): f for f in forecast_options}

selected_forecast_display = st.sidebar.multiselect("Forecast", forecast_options_display, key="forecast_filter")

# Convert back to original names for filtering
selected_forecast = [forecast_mapping[f] for f in selected_forecast_display]

# Forecast Conditions Legend
st.sidebar.caption("Forecast Conditions:")
st.sidebar.markdown("""
<div style="display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.85rem; margin-bottom: 1rem;">
  <div style="display: flex; align-items: center; gap: 0.5rem;">
    <div style="width: 16px; height: 16px; background-color: #cf5442; border-radius: 2px; flex-shrink: 0;"></div>
    <span style="color: #ffffff;"><strong>Deteriorating</strong> — Challenges to gender equity</span>
  </div>
  <div style="display: flex; align-items: center; gap: 0.5rem;">
    <div style="width: 16px; height: 16px; background-color: #62af44; border-radius: 2px; flex-shrink: 0;"></div>
    <span style="color: #ffffff;"><strong>Improving</strong> — Advances in gender equity</span>
  </div>
</div>
""", unsafe_allow_html=True)

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

# Logo at bottom of sidebar
st.sidebar.divider()
st.sidebar.image("assets/footer_logo.svg", use_container_width=True)

st.divider()

# ---------------------------
# 8) DETERIORATING AND IMPROVING MOMENTUM (cleaner)
# ---------------------------
st.subheader("Deteriorating and Improving Momentum")

# Lightweight explanatory block
st.markdown(
    """
    <div style="
        background-color: rgba(191, 163, 89, 0.08);
        border-left: 3px solid rgba(191, 163, 89, 0.4);
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 16px;
    ">
        <p style="margin: 0; font-size: 0.95rem; color: #4a4a4a; line-height: 1.5;">
            <strong style="color: #5a5a5a;">How to Read the Data</strong><br>
            Developments are real-world policy actions tracked by the Gender Equality Tracker. Each development is categorized by forecast (for example, deteriorating or improving) and assigned a score based on its scale, impact, and institutional significance. Scores reflect the magnitude and direction of change using publicly reported policy, legal, and institutional developments.
        </p>
        <p style="margin: 6px 0 0 0; font-size: 0.88rem; color: #7a7a7a; font-style: italic; line-height: 1.4;">
            Example: Political Deteriorating Conditions (+3) — Executive branch pressure on the judiciary/intimidation of judges
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("**Cumulative intensity (emerging → accelerating) vs net direction (Improving ↓ | Deteriorating ↑).**")
quad = df.copy()
quad["Prog"] = np.where(quad["Slider Score"] < 0, -quad["Slider Score"], 0)
quad["Disr"] = np.where(quad["Slider Score"] > 0,  quad["Slider Score"], 0)

forecast_points = quad.groupby(FORECAST_COL, as_index=False)[["Prog", "Disr"]].sum()
forecast_points["Cumulative Intensity"] = forecast_points["Prog"] + forecast_points["Disr"]
forecast_points["Net Direction"] = forecast_points["Disr"] - forecast_points["Prog"]

# Extract forecast domain/prefix (e.g., "Social" from "Social Deteriorating")
forecast_points["Forecast_Prefix"] = forecast_points[FORECAST_COL].str.split().str[0]

# Calculate category-level totals (all forecasts within same prefix measured against each other)
category_totals = forecast_points.groupby("Forecast_Prefix")[["Disr", "Prog"]].transform("sum")
forecast_points["Category_Total_Disr"] = category_totals["Disr"]
forecast_points["Category_Total_Prog"] = category_totals["Prog"]
forecast_points["Category_Total_Intensity"] = forecast_points["Category_Total_Disr"] + forecast_points["Category_Total_Prog"]

# Calculate percentage breakdown relative to category totals
forecast_points["Deterioration_Pct_Category"] = (
    (forecast_points["Category_Total_Disr"] / forecast_points["Category_Total_Intensity"] * 100)
    .round(0)
    .fillna(0)
    .astype(int)
)
forecast_points["Improvement_Pct_Category"] = 100 - forecast_points["Deterioration_Pct_Category"]

# Create breakdown label for tooltip (using category-level percentages)
forecast_points["Breakdown"] = forecast_points.apply(
    lambda row: f"Activity split: {row['Deterioration_Pct_Category']:.0f}% deteriorating / {row['Improvement_Pct_Category']:.0f}% improving" 
    if row["Category_Total_Intensity"] > 0 
    else "No activity",
    axis=1
)

# Add display name for forecast that replaces old terminology
def transform_forecast_name(name):
    """Transform forecast names from old terminology to new terminology"""
    return name.replace("Disruption", "Deteriorating").replace("Progression", "Improving")

forecast_points["Forecast Display"] = forecast_points[FORECAST_COL].apply(transform_forecast_name)

# Get latest event per forecast from filtered data first
if not df_filtered.empty:
    latest_by_forecast = df_filtered.sort_values("Date", ascending=False).groupby(FORECAST_COL, as_index=False).first()
    latest_by_forecast = latest_by_forecast[[FORECAST_COL, "Date", "Development Short", "Development", "Slider Score", DOMAIN_COL, SECTOR_COL, "Link"]].rename(
        columns={"Date": "Latest Date", "Development Short": "Latest Development", "Development": "Latest Development Full", "Slider Score": "Latest Slider Score", DOMAIN_COL: "Latest Domain", SECTOR_COL: "Latest Sector", "Link": "Latest Link"}
    )
    forecast_points = forecast_points.merge(latest_by_forecast, left_on=FORECAST_COL, right_on=FORECAST_COL, how="left")
else:
    forecast_points["Latest Date"] = None
    forecast_points["Latest Development"] = None
    forecast_points["Latest Development Full"] = None
    forecast_points["Latest Slider Score"] = None
    forecast_points["Latest Domain"] = None
    forecast_points["Latest Sector"] = None
    forecast_points["Latest Link"] = None

# For forecasts missing Latest Development Full (because they weren't in filtered data), get from full data
if "Latest Development Full" in forecast_points.columns:
    missing_full_dev = forecast_points[forecast_points["Latest Development Full"].isna() | (forecast_points["Latest Development Full"] == "")]
    if not missing_full_dev.empty:
        latest_all = df.sort_values("Date", ascending=False).groupby(FORECAST_COL, as_index=False).first()
        latest_all = latest_all[[FORECAST_COL, "Development"]].rename(columns={"Development": "Latest Development Full"})
        forecast_points.loc[missing_full_dev.index, "Latest Development Full"] = forecast_points.loc[missing_full_dev.index, FORECAST_COL].map(
            dict(zip(latest_all[FORECAST_COL], latest_all["Latest Development Full"]))
        )

# For forecasts missing Latest Link (because they weren't in filtered data), get from full data
if "Latest Link" in forecast_points.columns:
    missing_links = forecast_points[forecast_points["Latest Link"].isna() | (forecast_points["Latest Link"] == "")]
    if not missing_links.empty:
        latest_all = df.sort_values("Date", ascending=False).groupby(FORECAST_COL, as_index=False).first()
        latest_all = latest_all[[FORECAST_COL, "Link"]].rename(columns={"Link": "Latest Link"})
        forecast_points.loc[missing_links.index, "Latest Link"] = forecast_points.loc[missing_links.index, FORECAST_COL].map(
            dict(zip(latest_all[FORECAST_COL], latest_all["Latest Link"]))
        )

# Format Latest Date Str - handle NaN values properly
if "Latest Date" in forecast_points.columns:
    forecast_points["Latest Date Str"] = forecast_points["Latest Date"].apply(
        lambda x: pd.Timestamp(x).strftime("%b %d, %Y") if pd.notna(x) else "No data"
    )
else:
    forecast_points["Latest Date Str"] = "No data"

if "Latest Development" not in forecast_points.columns:
    forecast_points["Latest Development"] = None
if "Latest Slider Score" not in forecast_points.columns:
    forecast_points["Latest Slider Score"] = None
if "Latest Domain" not in forecast_points.columns:
    forecast_points["Latest Domain"] = None
if "Latest Sector" not in forecast_points.columns:
    forecast_points["Latest Sector"] = None
if "Latest Link" not in forecast_points.columns:
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
            return "Deteriorating"
        else:
            return "Improving"
    
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
            domain=["Status Quo", "Deteriorating", "Improving"],
            range=["#3b668c", "#cf5442", "#62af44"]
        ),
        legend=None
    ),
    tooltip=[
    alt.Tooltip("Forecast Display:N", title="Forecast"),
    alt.Tooltip("Disr:Q", title="Cumulative Deterioration", format=".1f"),
    alt.Tooltip("Prog:Q", title="Cumulative Improvement", format=".1f"),
    alt.Tooltip("Breakdown:N", title="Breakdown"),
    alt.Tooltip("Latest Date Str:N", title="Latest Event Date"),
    alt.Tooltip("Latest Development:N", title="Latest Event"),
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
        text=alt.condition(hover, alt.Text("Forecast Display:N"), alt.value("")),
    )
)

    # Quadrant names
    x_max = float(forecast_points["Cumulative Intensity"].max() or 1)
    y_max = float(forecast_points["Net Direction"].max() or 1)
    y_min = float(forecast_points["Net Direction"].min() or -1)

    # place quadrant text inside chart area
    quad_labels = pd.DataFrame([
        {"x": x0 * 0.20, "y": y_max * 0.85 if y_max > 0 else 5,  "t": "Emerging Deteriorating"},
        {"x": x0 + (x_max - x0) * 0.55, "y": y_max * 0.85 if y_max > 0 else 5, "t": "Accelerating Deteriorating"},
        {"x": x0 * 0.20, "y": y_min * 0.85 if y_min < 0 else -5, "t": "Emerging Improving"},
        {"x": x0 + (x_max - x0) * 0.55, "y": y_min * 0.85 if y_min < 0 else -5, "t": "Accelerating Improving"},
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
        <span>Deteriorating</span>
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 16px; height: 16px; background-color: #62af44; border-radius: 2px;"></div>
        <span>Improving</span>
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 16px; height: 16px; background-color: #3b668c; border-radius: 2px;"></div>
        <span>Status Quo</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)
    
    # How to Interpret This Chart section (directly after chart)
    with st.expander("How to Interpret This Chart", expanded=False):
        st.markdown("""
The Deteriorating and Improving Momentum graph plots cumulative forecast intensity against net directional movement of tracked developments. The horizontal positioning of cumulative intensity reflects the volume and concentration of forecasted developments within a domain (emerging → accelerating), while the vertical positioning of Net Direction distinguishes between deteriorating and improving trajectories. The quadrant framework highlights which issue areas are early-stage signals versus accelerating structural shifts.
""")
    
    # Statistics below chart
    st.markdown(f"""
**Highest cumulative deterioration observed to date:** {max_disr_name} (cumulative deterioration score: {max_disr_score:.1f})

**Highest cumulative improvement observed to date:** {max_prog_name} (cumulative improvement score: {max_prog_score:.1f})

**Data current as of:** {date_str}
""")
    
    # Key Insights Strip - initialize shared used_development_indices
    insights_list, global_used_indices = get_key_insights(forecast_points, FORECAST_COL, data_df=df_filtered, used_indices=set())
    
    # Format insights with examples as plain text
    insights_html = ""
    for insight in insights_list:
        # Split insight into statement and example (if present)
        parts = insight.split("\nExample: ")
        statement = parts[0]
        example = f"Example: {parts[1]}" if len(parts) > 1 else None
        
        # Build li content
        li_content = f"<strong>{statement}</strong>"
        if example:
            li_content += f"<br><span style='font-size: 0.9em; color: #555; margin-top: 0.25rem; display: block;'>{html.escape(example)}</span>"
        
        insights_html += f"<li style='margin-bottom: 0.75rem; color: #1b1725; font-size: 1rem; line-height: 1.5;'>{li_content}</li>"
    
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
            # Check required columns exist
            if "Latest Link" not in forecast_points.columns:
                forecast_points["Latest Link"] = ""
            if "Latest Development Full" not in forecast_points.columns:
                forecast_points["Latest Development Full"] = forecast_points.get("Latest Development", "")
            
            latest_events_display = forecast_points[[FORECAST_COL, "Latest Date Str", "Latest Development", "Latest Development Full", "Latest Domain", "Latest Sector", "Latest Slider Score", "Latest Link"]].copy()
            latest_events_display = latest_events_display[latest_events_display["Latest Date Str"] != "No data"]
            # Remove rows with NaN values in critical columns
            latest_events_display = latest_events_display.dropna(subset=["Latest Development", "Latest Date Str"])
            
            if not latest_events_display.empty:
                latest_events_display = latest_events_display.rename(columns={
                    FORECAST_COL: "Forecast",
                    "Latest Date Str": "Date",
                    "Latest Development": "Development Title",
                    "Latest Development Full": "Full Development",
                    "Latest Domain": "Domain",
                    "Latest Sector": "Sector",
                    "Latest Slider Score": "Score",
                    "Latest Link": "Source URL"
                })
                # Sort by date descending (most recent first)
                latest_events_display["Date"] = pd.to_datetime(latest_events_display["Date"], format="%b %d, %Y", errors="coerce")
                latest_events_display = latest_events_display.sort_values("Date", ascending=False).head(5)
                latest_events_display["Date"] = latest_events_display["Date"].dt.strftime("%b %d, %Y")
                
                # Extract readable source name from URL - improved version
                def extract_source_name(url):
                    if pd.isna(url) or not url or not str(url).strip():
                        return None  # Return None instead of "Unknown"
                    
                    source_mapping = {
                        "usatoday": "USA Today",
                        "nytimes": "NYT",
                        "wsj": "WSJ",
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
                        "bgov": "BGov",
                        "cnbc": "CNBC",
                        "axios": "Axios",
                        "vox": "Vox",
                        "cpr": "CPR",
                        "apnews": "AP",
                        "pbs": "PBS",
                        "nbcnews": "NBC",
                        "abcnews": "ABC",
                        "cbsnews": "CBS",
                    }
                    
                    try:
                        from urllib.parse import urlparse
                        parsed = urlparse(str(url))
                        domain = parsed.netloc.replace("www.", "").lower()
                        domain_parts = domain.split(".")
                        
                        # Try second-to-last part first
                        if len(domain_parts) >= 2:
                            main_domain = domain_parts[-2]
                            if main_domain in source_mapping:
                                return source_mapping[main_domain]
                        
                        # Try first part
                        if domain_parts[0] in source_mapping:
                            return source_mapping[domain_parts[0]]
                        
                        # Format domain name
                        main_domain = domain_parts[0].replace("-", " ").replace("_", " ").title()
                        return main_domain if main_domain else None
                    except:
                        return None
                
                # Create Source Display column
                latest_events_display["Source Display"] = latest_events_display["Source URL"].apply(extract_source_name)
                
                # Build custom card-style layout instead of table to avoid rendering issues
                html_output = "<div style='display: flex; flex-direction: column; gap: 1.5rem;'>"
                
                for idx, row in latest_events_display.iterrows():
                    forecast_name = html.escape(str(row["Forecast"]))
                    # Transform forecast name from old to new terminology
                    forecast_name = transform_forecast_name(forecast_name)
                    date_str = html.escape(str(row["Date"]))
                    title = html.escape(str(row["Development Title"]))
                    full_text = html.escape(str(row["Full Development"])) if pd.notna(row["Full Development"]) else ""
                    score = row["Score"]
                    source_url = str(row["Source URL"]).strip() if pd.notna(row["Source URL"]) else ""
                    source_display = row["Source Display"]
                    
                    # Build source link
                    if source_url and source_display:
                        source_html = f"<a href='{html.escape(source_url)}' target='_blank' style='color: #0066cc; text-decoration: underline; font-weight: 500;'>{html.escape(str(source_display))}</a>"
                    else:
                        source_html = "<span style='color: #999;'>No source</span>"
                    
                    # Card HTML with all information in a readable format
                    card_html = f"""
<div style='border: 1px solid #ddd; border-radius: 4px; padding: 1rem; background-color: #fafafa; box-shadow: 0 1px 2px rgba(0,0,0,0.05);'>
  <div style='display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;'>
    <div style='flex: 1;'>
      <div style='display: flex; gap: 1rem; margin-bottom: 0.75rem; font-size: 0.9em;'>
        <span style='background-color: #e8e7e0; padding: 0.25rem 0.5rem; border-radius: 3px; color: #1b1725;'><strong>{forecast_name}</strong></span>
        <span style='color: #666;'>{date_str}</span>
      </div>
      <div style='margin-bottom: 0.75rem;'>
        <details style='cursor: pointer; user-select: none;'>
          <summary style='color: #0066cc; text-decoration: underline; cursor: pointer; font-weight: 500; margin-bottom: 0.5rem;'>{title}</summary>
          <div style='margin-top: 0.75rem; padding: 0.75rem; background-color: #fff; border-left: 3px solid #bfa359; border-radius: 2px; font-size: 0.95em; line-height: 1.6; color: #333; white-space: normal; word-wrap: break-word; overflow-wrap: break-word;'>
{full_text}
          </div>
        </details>
      </div>
      <div style='display: flex; gap: 1rem; font-size: 0.85em;'>
        <span style='color: #666;'><strong>Source:</strong> {source_html}</span>
        <span style='color: #666;'><strong>Score:</strong> {score}</span>
      </div>
    </div>
  </div>
</div>
"""
                    html_output += card_html
                
                html_output += "</div>"
                st.markdown(html_output, unsafe_allow_html=True)
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
        dom_top["Net Direction"] > 0, "Deteriorating", np.where(dom_top["Net Direction"] < 0, "Improving", "Neutral")
    )

    # nicer ordering for horizontal bars
    dom_top = dom_top.sort_values("Net Direction", ascending=True)

    # chart
    domain_chart = (
        alt.Chart(dom_top)
        .mark_bar()
        .encode(
            y=alt.Y(f"{DOMAIN_COL}:N", sort=None, title="Domain of Assessment", axis=alt.Axis(labelLimit=300, labelPadding=15)),
            x=alt.X("Net Direction:Q", title="Net Direction Score (Improving ← 0 → Deteriorating)"),
            color=alt.Color(
                "Direction Label:N",
                scale=alt.Scale(
                    domain=["Improving", "Deteriorating", "Neutral"],
                    range=[COLOR_PROGRESSION, COLOR_DISRUPTION, COLOR_NEUTRAL],
                ),
                legend=alt.Legend(title=None),
            ),
            tooltip=[
                alt.Tooltip(f"{DOMAIN_COL}:N", title="Domain"),
                alt.Tooltip("Disr:Q", title="Weighted Deteriorating", format=".1f"),
                alt.Tooltip("Prog:Q", title="Weighted Improvement", format=".1f"),
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
Net direction indicates whether developments within each domain are trending towards deterioration or improvement. The value reflects the difference between cumulative deterioration and improvement based on the currently selected forecast type, sector, and group filters. Higher values indicate domains where deteriorating developments trend higher, while values closer to zero indicate a more balanced mix of deteriorating and improving developments.
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
        
        # Build insights using deterministic, clean approach with shared used indices
        domain_insights_list = []
        
        # Insight 1: Domain with highest deterioration
        insight1_text = f"{max_disruption_domain} developments show the highest cumulative deterioration (+{max_disruption_value:.1f})."
        if not df_filtered.empty:
            # Filter to developments in this domain
            domain_data = df_filtered[df_filtered[DOMAIN_COL].astype(str) == max_disruption_domain].copy()
            if not domain_data.empty:
                domain_data["Abs Score"] = domain_data["Slider Score"].abs()
                domain_data = domain_data.sort_values(by=["Abs Score", "Date"], ascending=[False, False])
                domain_data = domain_data[~domain_data.index.isin(global_used_indices)]
                if not domain_data.empty:
                    best_row = domain_data.iloc[0]
                    import re
                    full_text = str(best_row["Development"]).strip() if pd.notna(best_row["Development"]) else ""
                    first_sentence = re.split(r'[.!?]\s+', full_text)[0].strip()
                    if first_sentence:
                        if not first_sentence.endswith(('.', '!', '?')):
                            first_sentence += "."
                        short_text = first_sentence
                    else:
                        short_text = full_text[:100] + "." if len(full_text) > 100 else full_text
                    global_used_indices.add(best_row.name)
                    insight1_text += f"\nExample: {short_text}"
        domain_insights_list.append(insight1_text)
        
        # Insight 2: Domain with highest improvement
        insight2_text = f"{min_disruption_domain} developments also account for the largest cumulative improvement (–{abs(min_disruption_value):.1f})."
        if not df_filtered.empty:
            domain_data = df_filtered[df_filtered[DOMAIN_COL].astype(str) == min_disruption_domain].copy()
            if not domain_data.empty:
                domain_data["Abs Score"] = domain_data["Slider Score"].abs()
                domain_data = domain_data.sort_values(by=["Abs Score", "Date"], ascending=[False, False])
                domain_data = domain_data[~domain_data.index.isin(global_used_indices)]
                if not domain_data.empty:
                    best_row = domain_data.iloc[0]
                    import re
                    full_text = str(best_row["Development"]).strip() if pd.notna(best_row["Development"]) else ""
                    first_sentence = re.split(r'[.!?]\s+', full_text)[0].strip()
                    if first_sentence:
                        if not first_sentence.endswith(('.', '!', '?')):
                            first_sentence += "."
                        short_text = first_sentence
                    else:
                        short_text = full_text[:100] + "." if len(full_text) > 100 else full_text
                    global_used_indices.add(best_row.name)
                    insight2_text += f"\nExample: {short_text}"
        domain_insights_list.append(insight2_text)
        
        # Insight 3: Most balanced domain
        insight3_text = f"{most_balanced_domain} shows the most balanced mix of developments, with activity nearly evenly distributed between deterioration and improvement."
        if not df_filtered.empty:
            domain_data = df_filtered[df_filtered[DOMAIN_COL].astype(str) == most_balanced_domain].copy()
            if not domain_data.empty:
                domain_data["Abs Score"] = domain_data["Slider Score"].abs()
                domain_data = domain_data.sort_values(by=["Abs Score", "Date"], ascending=[False, False])
                domain_data = domain_data[~domain_data.index.isin(global_used_indices)]
                if not domain_data.empty:
                    best_row = domain_data.iloc[0]
                    import re
                    full_text = str(best_row["Development"]).strip() if pd.notna(best_row["Development"]) else ""
                    first_sentence = re.split(r'[.!?]\s+', full_text)[0].strip()
                    if first_sentence:
                        if not first_sentence.endswith(('.', '!', '?')):
                            first_sentence += "."
                        short_text = first_sentence
                    else:
                        short_text = full_text[:100] + "." if len(full_text) > 100 else full_text
                    global_used_indices.add(best_row.name)
                    insight3_text += f"\nExample: {short_text}"
        domain_insights_list.append(insight3_text)
        
        domain_insights_html = ""
        for insight in domain_insights_list:
            # Handle both old format (with HTML tags) and new format (plain text with Example:)
            # Split on newline if Example is present
            if "\nExample: " in insight:
                parts = insight.split("\nExample: ")
                statement = parts[0]
                example = f"Example: {parts[1]}"
                li_content = f"<strong>{statement}</strong><br><span style='font-size: 0.9em; color: #555; margin-top: 0.25rem; display: block;'>{html.escape(example)}</span>"
            else:
                # Old format (with HTML tags) - keep as is
                li_content = insight
            domain_insights_html += f"<li style='margin-bottom: 0.75rem; color: #1b1725; font-size: 1rem; line-height: 1.5;'>{li_content}</li>"
        
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
    elif any(word in forecast_name for word in ["disruption", "deteriorating"]):
        return "Deteriorating"
    else:  # Contains "progression", "improving" or other
        return "Improving"

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

# Top level chart: Direction (Improving, Status Quo, Deteriorating)
direction_colors = alt.Scale(
    domain=["Improving", "Status Quo", "Deteriorating"],
    range=[COLOR_PROGRESSION, "#3b668c", COLOR_DISRUPTION]
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
    
    # Transform forecast labels for display (Disruption -> Deteriorating, Progression -> Improving)
    monthly_forecast_counts["Forecast Display"] = monthly_forecast_counts[FORECAST_COL].apply(
        lambda x: str(x).replace("Disruption", "Deteriorating").replace("Progression", "Improving")
    )
    
    # ============================================================================
    # REFINED DIRECTIONAL COLOR SYSTEM
    # ============================================================================
    # Primary principle: Direction is the main visual signal (red/green/blue)
    # Forecast type is secondary (subtle variation within each directional family)
    # ============================================================================
    
    # ============================================================================
    # FIXED STACKING ORDER (Bottom to Top)
    # ============================================================================
    # Enforces consistent visual structure across all months:
    # 1. Status Quo (blue) - bottom
    # 2. Improving categories (greens) - middle
    # 3. Deteriorating categories (reds) - top
    # 
    # Within each direction, order by domain importance:
    # Political → Economic → Social → Security → Hybrid → Diplomatic
    # ============================================================================
    
    # Define the canonical stacking order (bottom to top)
    stacking_order = [
        "Status Quo",
        # Improving (greens) - middle layer
        "Political Improving",
        "Economic Improving",
        "Social Improving",
        "Security Improving",
        "Hybrid Political/Security Improving",
        "Hybrid Political/Social Improving",
        "Diplomatic Improving",
        # Deteriorating (reds) - top layer
        "Political Deteriorating",
        "Economic Deteriorating",
        "Social Deteriorating",
        "Security Deteriorating",
        "Hybrid Political/Security Deteriorating",
        "Hybrid Political/Social Deteriorating",
        "Diplomatic Deteriorating",
    ]
    
    # Filter to only include categories that exist in the data
    all_forecast_categories = monthly_forecast_counts["Forecast Display"].unique().tolist()
    ordered_forecast_categories = [cat for cat in stacking_order if cat in all_forecast_categories]
    
    # Add any unexpected categories at the end (for robustness)
    for cat in sorted(all_forecast_categories):
        if cat not in ordered_forecast_categories:
            ordered_forecast_categories.append(cat)
    
    # ----
    # RED FAMILY (Deteriorating) - Muted, cohesive reds
    # Darker reds for major policy domains, lighter reds for others
    # ----
    red_family = {
        "Political Deteriorating": "#8b3a3a",          # Dark red (major domain)
        "Economic Deteriorating": "#a84d42",           # Medium-dark red
        "Social Deteriorating": "#c4614f",             # Medium red
        "Security Deteriorating": "#d0814b",           # Medium-light red
        "Diplomatic Deteriorating": "#d97257",         # Light-medium red
        "Hybrid Political/Security Deteriorating": "#da8277",  # Light red
        "Hybrid Political/Social Deteriorating": "#e5999f",    # Very light red
    }
    
    # ----
    # GREEN FAMILY (Improving) - Muted, cohesive greens
    # Darker greens for major policy domains, lighter greens for others
    # ----
    green_family = {
        "Political Improving": "#2d5a3d",          # Dark green (major domain)
        "Economic Improving": "#4d8f56",           # Medium green
        "Social Improving": "#3d7149",             # Medium-dark green
        "Security Improving": "#5aa366",           # Medium-light green
        "Diplomatic Improving": "#6aad7f",         # Light-medium green
        "Hybrid Political/Security Improving": "#7ec194",      # Light green
        "Hybrid Political/Social Improving": "#9cd4ad",        # Very light green
    }
    
    # ----
    # BLUE FAMILY (Status Quo) - Muted, desaturated blue
    # Single neutral tone for all status quo developments
    # ----
    blue_family = {
        "Status Quo": "#5a7a90",  # Steel blue (muted, secondary signal)
    }
    
    # Build unified color mapping
    custom_colors = {}
    custom_colors.update(red_family)
    custom_colors.update(green_family)
    custom_colors.update(blue_family)
    
    # Create color range using the fixed stacking order
    color_range = [custom_colors.get(cat, "#888888") for cat in ordered_forecast_categories]
    
    # Color scale uses the fixed ordered list to ensure consistent stacking across all months
    forecast_color_scale = alt.Scale(domain=ordered_forecast_categories, range=color_range)
    
    # ============================================================================
    # ENHANCED LEGEND
    # ============================================================================
    # Legend is restructured to reinforce directional grouping while maintaining
    # clarity about forecast type breakdown
    # ============================================================================
    
    # Creates labels that hint at directional grouping in the legend
    # Altair doesn't support grouped legends natively, so we use visual ordering
    # and consistent naming to guide user interpretation
    
    legend_title = "Forecast Type Breakdown (Bottom to Top: Status Quo → Improving → Deteriorating)\n(Red = Deteriorating, Green = Improving, Blue = Stable)"
    
    # Calculate monthly totals for breakdown chart
    monthly_breakdown_totals = monthly_forecast_counts.groupby("MonthLabel")["Count"].sum().reset_index()
    breakdown_month_sort = list(monthly_forecast_counts["MonthLabel"].unique())
    
    breakdown_chart = alt.Chart(monthly_forecast_counts).mark_bar().encode(
        x=alt.X("MonthLabel:N", title="Month", sort=breakdown_month_sort, axis=alt.Axis(labelAngle=0), scale=alt.Scale(paddingInner=0.3)),
        y=alt.Y("Count:Q", title="Number of Developments", stack="zero"),
        color=alt.Color(
            "Forecast Display:N", 
            scale=forecast_color_scale,
            sort=ordered_forecast_categories,
            legend=alt.Legend(
                title=legend_title,
                orient="bottom",
                direction="horizontal",
                titleFontSize=12,
                labelFontSize=10,
                columns=6,
                titleLimit=200
            )
        ),
        opacity=alt.condition(
            direction_click,
            alt.value(1.0),
            alt.value(0.15)
        ),
        tooltip=[
            alt.Tooltip("MonthLabel:N", title="Month"),
            alt.Tooltip("Direction:N", title="Direction"),
            alt.Tooltip("Forecast Display:N", title="Forecast Type"),
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
    
    # Add text labels with monthly totals on top of breakdown bars
    breakdown_text = alt.Chart(monthly_breakdown_totals).mark_text(dy=-5, fontSize=11, fontWeight="bold").encode(
        x=alt.X("MonthLabel:N", sort=breakdown_month_sort),
        y=alt.Y("Count:Q"),
        text=alt.Text("Count:Q")
    )
    
    breakdown_chart_with_totals = (breakdown_chart + breakdown_text)
    
    # Combine both charts vertically so interaction works across both
    # Using alt.vconcat() for vertical stacking with shared interaction
    combined_chart = alt.vconcat(direction_chart_with_totals, breakdown_chart_with_totals).properties(
        spacing=20
    ).resolve_scale(color='independent')
    
    st.altair_chart(combined_chart, use_container_width=True)
    
    with st.expander("How to Interpret This Chart", expanded=False):
        st.markdown("""
These charts show how forecast developments are distributed over time. The top chart displays the total number of developments grouped by direction (deteriorating, status quo, and improving). The lower chart breaks those developments down by forecast type. Selecting a direction in the top chart filters the lower chart to highlight the associated forecasts.
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
        
        # Build insights using deterministic, clean approach with shared used indices
        composition_insights_list = []
        
        # Insight 1: Most represented direction with proportion
        pct_count = (most_represented_count / total_developments * 100) if total_developments > 0 else 0
        insight1_text = f"Developments are primarily {most_represented_direction} ({most_represented_count} of {total_developments}, or {pct_count:.0f}%)."
        if not df_filtered.empty:
            # Filter to developments with this direction
            direction_data = df_filtered[df_filtered["Direction"].astype(str) == most_represented_direction].copy()
            if not direction_data.empty:
                direction_data["Abs Score"] = direction_data["Slider Score"].abs()
                direction_data = direction_data.sort_values(by=["Abs Score", "Date"], ascending=[False, False])
                direction_data = direction_data[~direction_data.index.isin(global_used_indices)]
                if not direction_data.empty:
                    best_row = direction_data.iloc[0]
                    import re
                    full_text = str(best_row["Development"]).strip() if pd.notna(best_row["Development"]) else ""
                    first_sentence = re.split(r'[.!?]\s+', full_text)[0].strip()
                    if first_sentence:
                        if not first_sentence.endswith(('.', '!', '?')):
                            first_sentence += "."
                        short_text = first_sentence
                    else:
                        short_text = full_text[:100] + "." if len(full_text) > 100 else full_text
                    global_used_indices.add(best_row.name)
                    insight1_text += f"\nExample: {short_text}"
        composition_insights_list.append(insight1_text)
        
        # Insight 2: Most represented forecast type
        insight2_text = f"By forecast type, {most_represented_forecast} accounts for the largest share ({most_represented_forecast_count} developments)."
        if not df_filtered.empty:
            forecast_data = df_filtered[df_filtered[FORECAST_COL].astype(str) == most_represented_forecast].copy()
            if not forecast_data.empty:
                forecast_data["Abs Score"] = forecast_data["Slider Score"].abs()
                forecast_data = forecast_data.sort_values(by=["Abs Score", "Date"], ascending=[False, False])
                forecast_data = forecast_data[~forecast_data.index.isin(global_used_indices)]
                if not forecast_data.empty:
                    best_row = forecast_data.iloc[0]
                    import re
                    full_text = str(best_row["Development"]).strip() if pd.notna(best_row["Development"]) else ""
                    first_sentence = re.split(r'[.!?]\s+', full_text)[0].strip()
                    if first_sentence:
                        if not first_sentence.endswith(('.', '!', '?')):
                            first_sentence += "."
                        short_text = first_sentence
                    else:
                        short_text = full_text[:100] + "." if len(full_text) > 100 else full_text
                    global_used_indices.add(best_row.name)
                    insight2_text += f"\nExample: {short_text}"
        composition_insights_list.append(insight2_text)
        
        # Insight 3: Overall composition pattern
        # Determine if deterioration or improvement dominates
        deteriorating_count = direction_totals.get("Deteriorating", 0)
        improving_count = direction_totals.get("Improving", 0)
        status_quo_count = direction_totals.get("Status Quo", 0)
        
        if deteriorating_count > improving_count:
            insight3_text = f"Overall, deteriorating developments ({deteriorating_count}) substantially outnumber improving ones ({improving_count})."
        else:
            insight3_text = f"Overall, improving developments ({improving_count}) substantively match or exceed deteriorating ones ({deteriorating_count})."
        
        composition_insights_list.append(insight3_text)
        
        composition_insights_html = ""
        for insight in composition_insights_list:
            # Handle both old format (with HTML tags) and new format (plain text with Example:)
            if "\nExample: " in insight:
                parts = insight.split("\nExample: ")
                statement = parts[0]
                example = f"Example: {parts[1]}"
                li_content = f"<strong>{statement}</strong><br><span style='font-size: 0.9em; color: #555; margin-top: 0.25rem; display: block;'>{html.escape(example)}</span>"
            else:
                # Old format (with HTML tags or simple text) - keep as is
                li_content = insight
            composition_insights_html += f"<li style='margin-bottom: 0.75rem; color: #1b1725; font-size: 1rem; line-height: 1.5;'>{li_content}</li>"
        
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