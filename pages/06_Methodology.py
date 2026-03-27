import streamlit as st
import pandas as pd

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

st.title("Methodology")
st.caption("Understanding the framework and approach behind the Gender Equality Tracker")

st.write(
    """
The Gender Equality Tracker (GET) is a forecast model and early-warning system that tracks policy 
developments, political discourse, and institutional actions related to gender equality and LGBTQ+ rights.
"""
)

st.divider()

st.subheader("Project Overview")
st.write(
    """
GET functions as a **strategic foresight tool** to:
- **Interpret** developments in gender, reproductive, and LGBTQ+ policy landscapes
- **Identify** risk trajectories and emerging repressions
- **Support** decision-making across public, private, and civil society sectors
"""
)

st.divider()

with st.expander("**Key Metrics & Scoring**", expanded=False):
    st.markdown("""
### Slider Score

Each policy development is assigned a **Slider Score** ranging from **-4 to +4**:

- **Negative scores (-4 to -1)**: Represent **progressions**
  - Policy actions that establish, reinstate, or expand gender, reproductive, or LGBTQ+ protections
  - Examples: State legislation protecting reproductive rights, hate crime law expansions

- **Positive scores (+1 to +4)**: Represent **repressions**
  - Legislative or executive actions restricting gender, reproductive, or workplace rights
  - Defunding of protections, institutional rollbacks, or service denials
  
- **Score of 0**: Status quo
  - Developments with no clear direction or impact

### Analytic Dimensions

Each development is evaluated across **four analytic dimensions**. Scores range from **-1 (progression)** to **+1 (repression)**, with **0 indicating neutrality**. These dimensions combine to form the final slider score.

| Dimension | +1 (Repression) | 0 (Neutral) | -1 (Progression) |
|-----------|---|---|---|
| **Monitoring Indicator Alignment** | Reinforces an existing monitoring indicator | No relation | Contradicts an existing monitoring indicator |
| **Driver Alignment** | Advances or accelerates an existing scenario driver | Neutral | Opposes or slows a scenario driver |
| **Core Indicator Influence** | Reinforces attitudinal, democratic, legislative, narrative, or gendered economic deterioration | No effect | Reinforces stabilizing or protective indicator trends |
| **Impact on Scenario Probability** | Increases the likelihood of a repression scenario | No measurable probability change | Decreases the likelihood of a repression scenario |

*Note: Status quo developments can have low positive or negative scores depending on their alignment with these dimensions.*

### Weighted Analysis

- **Weighted Repression** = Sum of all positive slider scores
- **Weighted Progression** = Sum of absolute values of negative slider scores
- **Net Trend** = Repression - Progression direction

""")

st.divider()

with st.expander("**Score Aggregation: Computing Key Indicators**", expanded=False):
    st.markdown("""
The dashboard aggregates individual slider scores across forecasts to compute four key indicators:

#### **Cumulative Repression**
Sum of all **positive slider scores** for a given forecast:
- Represents the total magnitude of restrictive or disruptive policy developments
- Higher values indicate more severe or numerous repressions targeting gender equality or LGBTQ+ rights

#### **Cumulative Progression**
Sum of the absolute values of all **negative slider scores** for a given forecast:
- Represents the total magnitude of protective or progressive policy developments  
- Higher values indicate more substantial expansions of gender equality or LGBTQ+ protections

#### **Cumulative Intensity**
Sum of the absolute values of **all slider scores** (disruptive + progressive):
- Measures the overall volume and concentration of policy developments
- Indicates how active or dynamic a particular forecast trend is—regardless of direction
- Higher values show more intense or frequent policy activity

#### **Net Direction**
Calculated as **Cumulative Repression − Cumulative Progression**:
- Ranges from negative (more progression) to positive (more repression)
- Provides a directional indicator of whether developments lean toward expanding or restricting gender equality
- Shown on the y-axis of the Repression and Progression Momentum chart

These aggregations are computed at multiple levels:
- By individual **Forecast** (showing trajectory within a specific policy scenario)
- By **Domain of Assessment** (showing directional trends across institutional types)
- By **Sector** (showing which industries or institutions are experiencing the most activity)

""")

st.divider()

with st.expander("**Core Indicators: Contextual Layer**", expanded=False):
    st.markdown("""
Beyond individual policy developments with slider scores, GET also monitors **Core Indicators** that provide 
structural context for the policy environment. These indicators inform analyst judgment but are **scored differently**—they are not coded as 
discrete events and instead use a direction-based system.

### Purpose of Core Indicators

Core indicators function as a **contextual layer** that captures:
- Shifts in public sentiment and institutional behavior
- Changes in discourse patterns and media narratives
- Governance stability and institutional resilience
- Economic conditions affecting gender equality
- Momentum in legislative and regulatory activity

### Direction System

Each core indicator is assigned a **direction value** that reflects trends:

| Direction | Meaning | Interpretation |
|-----------|---------|-----------------|
| **+1** | Worsening conditions | Deteriorating status or restrictive trends |
| **0** | Neutral / mixed | No clear direction or mixed signals |
| **-1** | Improving conditions | Progressive developments or protective trends |

### Core Indicators Tracked

The dashboard monitors five core indicators:

1. **Attitudinal Climate**
   - Institutional protections, representation, and governance stability
   - Tracks shifts in institutional capacity and governance structures

2. **Narrative Environment**
   - Media, rhetoric, and normalization patterns
   - Captures discourse trends that shape policy receptivity

3. **Democratic Climate**
   - Representation, rights protection, and institutional resilience
   - Monitors institutional protections and democratic safeguards

4. **Gendered Economic Conditions**
   - Economic access, labor equity, and service availability affecting gender equality
   - Tracks material conditions and economic disparities

5. **Legislative Momentum**
   - Rate and direction of legal and regulatory change
   - Measures the pace and nature of policy activity

### Using Core Indicators

Visit the **Core Indicators** page to:
- See the current climate across all five indicators
- View a direction summary showing the distribution of signals
- Review recent signals (past 6 months) with source citations
- Filter by specific indicator to focus on particular aspects of the policy landscape

    """)

st.divider()

with st.expander("**Development Classifications**", expanded=False):
    st.markdown("""
Each entry is categorized by:

- **Forecast Type**: Describes the nature of the development
  - Political Repression, Diplomatic Progression, Social Repression, etc.

- **Monitoring Indicator**: Observable signals that characterize the nature of developments and help identify broader policy trends
  - Example indicators include:
    - Politicization or repurposing of protective institutions for political objectives
    - U.S. withdrawal from or defunding of international organizations advancing gender, LGBTQ+, or reproductive rights
    - Medical and ethical crises emerging from restrictive abortion policies

- **Sector Impacted**: Institutional domain affected
  - Federal Executive, Healthcare Systems, Education, International/Multilateral, etc.

- **Who is Impacted**: Target population groups
  - Transgender individuals, women and girls, LGBTQ+ communities, marginalized groups

- **Domain of Assessment**: Categorization framework
  - Procedural/Institutional, Material Impact, Discursive/Symbolic, Societal Behavior and Norms

    """)

st.divider()

with st.expander("**Data Source & Period**", expanded=False):
    st.markdown("""
### Coverage

This dashboard presents a curated dataset tracking **gender equality-related policy developments** 
from **January 2025 onwards**.

Data includes:
- Federal and state legislative and executive actions (US)
- International policy shifts and diplomatic developments
- Institutional policy changes in healthcare, education, and corporate sectors
- Civil society legal challenges and advocacy responses

### Source Materials

**Developments** are sourced from:
- National news outlets (AP, Reuters, The New York Times, Washington Post, NBC News, PBS, NPR, etc.)
- Policy and advocacy organizations (Pew Research Center, GLAAD, Guttmacher Institute, Movement Advancement Project, etc.)
- Government and international sources (Congress.gov, UN Women, Stateline, etc.)
- Specialized reporting on gender, reproductive, and LGBTQ+ policy developments
- Academic and research institutions

**Core Indicators signals** are compiled from:
- Public opinion surveys and polling data (Gallup, Pew Research, AP-NORC, etc.)
- Media content analysis and discourse tracking
- Legislative and regulatory activity monitoring
- Institutional policy announcements and changes
- Economic and labor data on gender equity

Sources are credited in the Evidence Feed with hyperlinked citations, allowing users to access original reporting.

    """)

st.divider()

# Source name mapping for shortened citations
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
    "outrightinternational.org": "Outright International",
    "lgbtqnation.com": "LGBTQ Nation",
    "whitehouse.gov": "White House",
}

def short_source_name(url: str) -> str:
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
    except Exception:
        return "Source"

with st.expander("**Dataset Preview (sample only)**", expanded=False):
    st.caption("Showing a limited preview for transparency without exposing the full dataset.")
    DATA_PATH = "data/Monitor - Gender Equality - For Sharing.csv"
    try:
        df = pd.read_csv(DATA_PATH)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
        df = df.dropna(subset=["Date", "Slider Score"]).copy()
        
        # Rename Signpost to Monitoring Indicators and remove "Signpost - " prefix
        if "Signpost" in df.columns:
            df = df.rename(columns={"Signpost": "Monitoring Indicators"})
            df["Monitoring Indicators"] = df["Monitoring Indicators"].str.replace("Signpost - ", "", regex=False)
        
        # Remove "Forecast - " prefix from Forecast column
        if "Forecast" in df.columns:
            df["Forecast"] = df["Forecast"].str.replace("Forecast - ", "", regex=False)
        
        # Format date to show only date without time
        df["Date"] = df["Date"].dt.strftime("%m/%d/%Y")
        
        # Create Source column with shortened names and URLs as HTML links
        if "Link" in df.columns:
            df["Source"] = df["Link"].apply(
                lambda url: f'<a href="{url}" target="_blank" style="color: #0066cc; text-decoration: none;">{short_source_name(url)}</a>' if pd.notna(url) else ""
            )
        
        # Drop unnecessary columns
        columns_to_drop = ["Additional Link and/or note", "Link", "National Security Considerations"]
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
        
        # Render CSS styling with expandable content
        st.markdown("""
        <style>
        .table-container {
            overflow-x: auto;
            border-radius: 4px;
            border: 1px solid #e0e0e0;
        }
        .methodology-table {
            border-collapse: collapse;
            width: 100%;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
            font-size: 10px;
            color: #262730;
        }
        .methodology-table thead {
            background: linear-gradient(135deg, #f0f2f6 0%, #e8eaef 100%);
            position: sticky;
            top: 0;
            z-index: 10;
        }
        .methodology-table th {
            padding: 5px 8px;
            text-align: left;
            font-weight: 600;
            color: #262730;
            border-right: 1px solid #d4d4d8;
            white-space: nowrap;
        }
        .methodology-table th:last-child {
            border-right: none;
        }
        .methodology-table td {
            padding: 5px 8px;
            border-right: 1px solid #e8e8e8;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        .methodology-table td:nth-child(2) {
            min-width: 300px;
            word-wrap: break-word;
            overflow-wrap: break-word;
            cursor: pointer;
            position: relative;
        }
        .methodology-table td:nth-child(2):hover {
            background-color: #e3f2fd !important;
            text-decoration: underline;
        }
        .methodology-table td:last-child {
            border-right: none;
        }
        .methodology-table tbody tr {
            border-bottom: 1px solid #e8e8e8;
        }
        .methodology-table tbody tr:nth-child(odd) {
            background-color: #fafafa;
        }
        .methodology-table tbody tr:nth-child(even) {
            background-color: #ffffff;
        }
        .methodology-table tbody tr:hover {
            background-color: #f0f4f8;
        }
        .methodology-table a {
            color: #0066cc;
            text-decoration: none;
            font-weight: 500;
        }
        .methodology-table a:hover {
            color: #0052a3;
            text-decoration: underline;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Generate and render HTML table with container
        table_html = df.head(25).to_html(index=False, escape=False, classes="methodology-table")
        container_html = f'<div class="table-container">{table_html}</div>'
        st.markdown(container_html, unsafe_allow_html=True)
        
        st.caption("Showing sample of 25 rows • Development entries are fully visible")
        
    except Exception as e:
        st.info("Dataset preview not available. Ensure the sample CSV exists in the `data/` folder.")

st.divider()

st.info(
    "**Questions or feedback?** This tool is designed to support decision-makers and advocates. "
    "Consider your specific use case and interpretation needs when using these metrics."
)
