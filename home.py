import streamlit as st
import pandas as pd

# ---------------------------
# 0) PAGE CONFIG MUST BE FIRST
# ---------------------------
st.set_page_config(page_title="U.S. Gender Equality Tracker", layout="wide")

# ---------------------------
# POPULATION GROUP HIERARCHY (CANONICAL - Same as Human_Impact.py)
# ---------------------------
POPULATION_STRUCTURE = {
    "Women and Girls": {
        "Women and Girls": ["women", "women and girls"],
        "Pregnant Women": ["pregnant women"],
        "Women Servicemembers": ["women servicemembers", "female servicemembers", "women veterans", "female veterans"],
        "Women in Workforce": ["women in workforce"],
    },
    "LGBTQ+ and Gender-Diverse Populations": {
        "LGBTQ+ Individuals": ["LGBTQ+ individuals", "LGBTQ+ youth"],
        "Transgender and Gender-Diverse Individuals": ["transgender and gender-diverse individuals", "trans and gender-diverse community", "transgender individuals", "nonbinary people"],
        "Gender Dysphoria": ["gender dysphoria"],
        "Transgender and Gender-Diverse Youth": ["trans youth", "transgender youth", "transgender and gender-diverse youth", "trans and non-binary youth", "non-binary youth", "trans youth and their families"],
        "Trans and Non-Binary Athletes": ["trans athletes", "transgender athletes", "trans and non binary athletes", "trans and non-binary athletes", "collegiate and professional trans athletes"],
    },
    "Patients & Beneficiaries": {
        "Reproductive Health": ["reproductive healthcare patients", "reproductive healthcare patients and providers", "abortion patients", "planned parenthood"],
        "Federal Benefits": ["SNAP recipients", "WIC recipients", "medicaid recipients", "beneficiaries of federal programs"],
        "International Aid": ["international aid recipients", "international gender rights organizations"],
    },
    "Practitioners & Researchers": {
        "Healthcare": ["healthcare providers", "healthcare practitioners", "pediatric healthcare providers", "healthcare agencies"],
        "Legal": ["legal practitioners"],
        "Education": ["educators", "public school districts", "education practitioners"],
        "Research": ["academic researchers", "public health researchers"],
    },
    "Workforce & Institutional Personnel": {
        "Federal Workforce": ["federal workforce", "trans federal workforce"],
        "Military & Service": ["trans military personnel", "trans service members", "experienced U.S. Navy personnel"],
        "Government": ["elected officials", "state governments"],
    },
    "Justice & Detention Populations": {
        "Incarcerated Populations": ["trans inmates", "incarcerated trans community"],
        "Gender-Based Violence": ["survivors of sexual violence", "victims of GBV", "gender-based violence survivors"],
    },
    "Community & Place-Based Populations": {
        "Local Residents": ["local residents", "residents", "students"],
        "Geographic": ["chicago residents", "FL residents", "indiana residents"],
    },
    "Marginalized Communities": {
        "Marginalized Communities": ["marginalized ethnicity groups", "low-income minority communities"],
    },
    "Advocacy & Civil Society / Cultural": {
        "Advocacy & Civil Society": ["foreign nationals", "international travelers", "arts institutions", "human rights advocates", "activists"],
    },
}

# Build canonical alias-to-group mapping
ALIAS_TO_GROUP = {}
for main_group, subgroups in POPULATION_STRUCTURE.items():
    for subgroup, aliases in subgroups.items():
        for alias in aliases:
            alias_lower = alias.lower().strip()
            ALIAS_TO_GROUP[alias_lower] = main_group

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
st.sidebar.divider()
st.sidebar.image("assets/footer_logo.svg", use_container_width=True)

st.title("🌎 U.S. Gender Equality Tracker")
st.write("**How to use the tracker:** Use the sidebar to explore institutional impacts, population group impacts, and the indicators shaping the forecast.")
st.write("Since January 2025, the gender landscape in the United States has experienced significant rollbacks, prompting the development of the U.S. Gender Equality Tracker (GET) to better anticipate major shifts.")

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
st.markdown("""
<div style="
    background: linear-gradient(135deg, #bfa359 0%, #a08a42 100%);
    padding: 30px;
    border-radius: 12px;
    border-left: 6px solid #8b7835;
    box-shadow: 0 4px 12px rgba(191, 163, 89, 0.3);
    margin-bottom: 20px;
">
    <div>
        <p style="color: #ffffff; font-size: 18px; font-weight: 700; margin: 0 0 12px 0; line-height: 1.4;">
            At a Glance
        </p>
        <p style="color: #f8f8f8; font-size: 16px; margin: 0; line-height: 1.6; font-weight: 400;">
            The Gender Equality Tracker analyzes gender-related developments in federal, executive, and state level policy actions to develop forecasts of trajectories of ongoing political, security, economic, and social shifts.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
st.subheader("Current Outlook")
st.write("Directional trajectory and severity by domain")
st.caption("Updated: March 2026")

# Load data first
@st.cache_data
def load_data():
    df = pd.read_csv("data/Monitor - Gender Equality - GET 2025 (1).csv", skiprows=1)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()

# Function to extract net direction scores
@st.cache_data
def calculate_domain_scores(data_df):
    """
    Calculate net direction scores for each core domain.
    net score = cumulative disruption score - cumulative progression score
    Only pure forecasts (no hybrids, status quo, or diplomatic).
    """
    domain_scores = {
        "Political": {"disruption": 0, "progression": 0, "count": 0},
        "Social": {"disruption": 0, "progression": 0, "count": 0},
        "Economic": {"disruption": 0, "progression": 0, "count": 0},
        "Security": {"disruption": 0, "progression": 0, "count": 0},
    }
    
    for idx, row in data_df.iterrows():
        forecast = str(row["Forecast"]).strip()
        slider_score = pd.to_numeric(row["Slider Score"], errors="coerce")
        
        # Skip if slider_score is invalid
        if pd.isna(slider_score):
            continue
        
        # Skip invalid forecast types (hybrid, status quo, diplomatic)
        if any(x in forecast for x in ["Hybrid", "Status Quo", "Diplomatic"]):
            continue
        
        # Check if this is a pure core forecast
        for domain in ["Political", "Social", "Economic", "Security"]:
            if domain in forecast:
                if "Disruption" in forecast:
                    domain_scores[domain]["disruption"] += slider_score
                    domain_scores[domain]["count"] += 1
                elif "Progression" in forecast:
                    domain_scores[domain]["progression"] += slider_score
                    domain_scores[domain]["count"] += 1
                break
    
    # Calculate net score, average intensity, and direction for each domain
    for domain in domain_scores:
        disruption = domain_scores[domain]["disruption"]
        progression = domain_scores[domain]["progression"]
        net = disruption - progression
        count = domain_scores[domain]["count"]
        
        domain_scores[domain]["net"] = net
        
        # Calculate average intensity per development (0-10 scale)
        if count > 0:
            average_per_dev = net / count
            # Map to 0-10 scale: normalize based on typical range
            # Assuming average typically ranges from -4 to +4, map to 0-10
            intensity_10_scale = ((average_per_dev + 4) / 8) * 10
            # Clamp to 0-10
            intensity_10_scale = max(0, min(10, intensity_10_scale))
        else:
            average_per_dev = 0
            intensity_10_scale = 5  # neutral
        
        domain_scores[domain]["average_per_dev"] = average_per_dev
        domain_scores[domain]["intensity_10"] = intensity_10_scale
        
        # Determine direction label based on net score
        if net > 10:
            domain_scores[domain]["direction"] = "Deteriorating"
        elif net < -10:
            domain_scores[domain]["direction"] = "Improving"
        else:
            domain_scores[domain]["direction"] = "Mixed"
    
    return domain_scores

def score_to_grade(intensity_10_scale):
    """
    Convert intensity (0-10 scale) to A-F grade:
    A = strong progression (0-1.5)
    B = moderate progression (1.5-3.5)
    C = mixed (3.5-6.5)
    D = moderate disruption (6.5-8.5)
    F = strong disruption (8.5-10)
    """
    if intensity_10_scale < 1.5:
        return "A"
    elif intensity_10_scale < 3.5:
        return "B"
    elif intensity_10_scale < 6.5:
        return "C"
    elif intensity_10_scale < 8.5:
        return "D"
    else:
        return "F"

def get_card_color(grade):
    """Get card background color based on grade"""
    colors = {
        "F": "#cf5442",  # Red - strong disruption
        "D": "#e67e5a",  # Orange-red - moderate disruption
        "C": "#bfa359",  # Gold - mixed
        "B": "#88b379",  # Light green - moderate progression
        "A": "#62af44",  # Green - strong progression
    }
    return colors.get(grade, "#bfa359")

def get_text_color(grade):
    """Get text color based on grade for readability"""
    if grade in ["F", "D"]:
        return "#ffffff"
    elif grade == "C":
        return "#1b1725"
    else:
        return "#ffffff"

# Calculate scores
domain_scores = calculate_domain_scores(df)

# Create columns for forecast cards (2x2 grid)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
columns = [
    (col1, "Political"),
    (col2, "Social"),
    (col3, "Economic"),
    (col4, "Security"),
]

for col, domain in columns:
    with col:
        score_data = domain_scores[domain]
        net_score = score_data["net"]
        intensity_10 = score_data["intensity_10"]
        grade = score_to_grade(intensity_10)
        direction = score_data["direction"]
        dev_count = score_data["count"]
        bg_color = get_card_color(grade)
        text_color = get_text_color(grade)
        
        sign = "+" if net_score > 0 else ""
        
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 24px; border-radius: 8px; text-align: center; height: 100%; border: 2px solid {text_color};">
            <p style="color: {text_color}; font-size: 14px; margin: 0 0 12px 0; font-weight: 400; opacity: 0.95; text-transform: uppercase; letter-spacing: 0.5px;">{domain} Outlook</p>
            <p style="color: {text_color}; font-size: 36px; margin: 0 0 12px 0; font-weight: 700;">{grade}</p>
            <p style="color: {text_color}; font-size: 13px; margin: 0 0 12px 0; font-weight: 500; opacity: 0.9;">{intensity_10:.1f} / 10</p>
            <p style="color: {text_color}; font-size: 14px; margin: 0; font-weight: 500;">{direction}</p>
        </div>
        """, unsafe_allow_html=True)

# Explanation
with st.expander("How are these grades calculated?", expanded=False):
    st.markdown("""
    **Grades reflect severity per development, while direction reflects overall trajectory.**
    
    ---
    
    **What the grades mean:**
    - **A** = Strong improvement (0–1.5)
    - **B** = Moderate improvement (1.5–3.5)
    - **C** = Mixed or contested (3.5–6.5)
    - **D** = Moderate deterioration (6.5–8.5)
    - **F** = Strong deterioration (8.5–10)
    
    **How it is calculated:**
    - Net score = deterioration − improvement
    - Average per development = net score ÷ number of developments
    - Severity (0–10) = normalized average
    
    **Direction labels:**
    - **Deteriorating** = overall negative trajectory
    - **Improving** = overall positive trajectory
    - **Mixed** = contested or unclear direction
    
    **Pattern tags** describe the type of change driving the forecast (e.g., erosion, regression, suppression) and are used for interpretation only. They do not affect scores or grades.
    
    **How to interpret:**
    - Grades show how concentrated deterioration or improvement is
    - Direction shows overall directional momentum
    - Severity (0–10) indicates the intensity of change
    
    **Example:**
    - Political: D (5.8) = broad, sustained deterioration
    - Security: F (8.6) = concentrated, high-severity deterioration
    
    **Scope**: Only core forecasts (Political, Social, Economic, Security deteriorations & improvements) are included. Hybrid forecasts, status quo, and diplomatic actions are excluded.
    """)

# Most Targeted Institutions and Population Groups
st.markdown("---")
st.subheader("Most Targeted Institutions & Groups")

# Get date range
date_min = df["Date"].min()
date_max = df["Date"].max()
date_range_str = f"{date_min.strftime('%B %d, %Y')} to {date_max.strftime('%B %d, %Y')}"

st.caption(f"Based on developments tracked from {date_range_str}")

# Function to map specific group values to broader labels
def map_to_broader_group(impacted_text):
    """Map specific population groups to their broader parent category.
    
    Handles:
    - Case insensitivity
    - Multiple groups in one entry (comma-separated) - returns ALL applicable groups
    
    Returns: List of broader groups that apply
    """
    if not isinstance(impacted_text, str) or pd.isna(impacted_text):
        return []
    
    results = []
    items = [item.strip().lower() for item in impacted_text.split(',')]
    
    for item in items:
        if item in ALIAS_TO_GROUP:
            results.append(ALIAS_TO_GROUP[item])
    
    return results

# Get top 3 sectors and groups (grouped by broader labels)
top_sectors = df["Sector Impacted"].value_counts().head(3)

# Map specific groups to broader labels and count
# Each entry can map to multiple broader groups (when comma-separated)
df_with_broader_groups = df.copy()
df_with_broader_groups["Broader Groups"] = df_with_broader_groups["Who is impacted?"].apply(map_to_broader_group)

# Expand rows with multiple groups so each group is counted
expanded_rows = []
for idx, row in df_with_broader_groups.iterrows():
    broader_groups = row["Broader Groups"]
    if broader_groups:  # Only if there are mapped groups
        for group in broader_groups:
            expanded_rows.append({**row.to_dict(), "Broader Group": group})

df_expanded = pd.DataFrame(expanded_rows) if expanded_rows else pd.DataFrame(columns=list(df.columns) + ["Broader Group"])
top_groups = df_expanded["Broader Group"].value_counts().head(3) if len(df_expanded) > 0 else pd.Series()

targeted_col1, targeted_col2, targeted_col3 = st.columns(3)

# Display top 3 sectors
with targeted_col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #262232 0%, #1b1725 100%); padding: 25px; border-radius: 8px; height: 100%; text-align: center;">
        <p style="color: #ffffff; font-size: 16px; margin: 0 0 20px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Most Targeted Institutions</p>
    </div>
    """, unsafe_allow_html=True)
    for i, (sector, count) in enumerate(top_sectors.items(), 1):
        st.markdown(f"<p style='margin: 12px 0; font-size: 16px;'>{sector}<br><span style='font-size: 14px; color: #666; font-weight: 500;'>{count} incident{'s' if count > 1 else ''}</span></p>", unsafe_allow_html=True)

# Display top 3 groups
with targeted_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1b1725 0%, #0f0f1a 100%); padding: 25px; border-radius: 8px; height: 100%; text-align: center;">
        <p style="color: #ffffff; font-size: 16px; margin: 0 0 20px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Most Targeted Populations</p>
    </div>
    """, unsafe_allow_html=True)
    for i, (group, count) in enumerate(top_groups.items(), 1):
        st.markdown(f"<p style='margin: 12px 0; font-size: 16px;'>{group}<br><span style='font-size: 14px; color: #666; font-weight: 500;'>{count} incident{'s' if count > 1 else ''}</span></p>", unsafe_allow_html=True)
    
    # About Population Groups Info
    with st.expander("About Population Groups", expanded=False):
        st.markdown("""
        **Population groups** are organized hierarchically into main categories and sub-groups to capture the complexity of gender-related policy impacts.
        
        Example: "Women and Girls" (main group) contains sub-groups like "Pregnant Women", "Women Servicemembers", and "Women in Workforce".
        
        **Important:** A single development can impact multiple population groups across different categories. Counts shown here represent the number of developments tagged with each group, so totals may exceed the overall development count due to cross-cutting impacts.
        """)

# Display total entries
with targeted_col3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1f1b2e 0%, #1b1725 100%); padding: 25px; border-radius: 8px; text-align: center; height: 100%;">
        <p style="color: #ffffff; font-size: 13px; margin: 0 0 15px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Scope of Impact</p>
        <p style="color: #ffffff; font-size: 42px; margin: 15px 0; font-weight: 700;">{len(df)}</p>
        <p style="color: #ffffff; font-size: 12px; margin: 0; opacity: 0.95;">total developments<br>tracked</p>
    </div>
    """
    , unsafe_allow_html=True)
    
    # What are Developments? Info
    with st.expander("What are Developments?", expanded=False):
        st.markdown("""
        **Developments** are real-world policy actions, legal decisions, and institutional changes tracked by the Gender Equality Tracker.
        
        Examples include state laws, federal agency actions, court rulings, executive orders, and internal agency memos.
        
        For more details on how developments are identified and evaluated, see the [**Methodology →**](./Methodology)
        """)
