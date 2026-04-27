import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Human Impact")

# ---------------------------
# POPULATION GROUP HIERARCHY (CANONICAL)
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
    "Transgender and Gender-Diverse Youth": {
        "Transgender and Gender-Diverse Youth": ["trans youth", "transgender youth", "transgender and gender-diverse youth"],
        "Trans and Non Binary Athletes": ["trans athletes", "transgender athletes", "trans and non binary athletes"],
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
            ALIAS_TO_GROUP[alias_lower] = (main_group, subgroup)

def parse_population_groups(impacted_text):
    """
    Parse comma-separated population groups from raw text.
    Returns a list of (Main Group, Subgroup) tuples.
    
    Example:
        parse_population_groups("women and girls, LGBTQ+ individuals")
        → [("Women and Girls", "Women and Girls"), ("LGBTQ+ and Gender-Diverse Populations", "LGBTQ+ Individuals")]
    """
    if not isinstance(impacted_text, str) or pd.isna(impacted_text):
        return []
    
    results = []
    items = [item.strip().lower() for item in impacted_text.split(',')]
    
    for item in items:
        if item in ALIAS_TO_GROUP:
            results.append(ALIAS_TO_GROUP[item])
    
    return results

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

# Chart border styling
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
        overflow-x: auto !important;
        overflow-y: hidden !important;
        max-width: 100% !important;
      }
      
      div[data-testid="stVegaLiteChart"] > div {
        overflow-x: auto !important;
        overflow-y: hidden !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Population Group Filters (Cascading)
st.sidebar.divider()

# Load data
df = pd.read_csv("data/Monitor - Gender Equality - GET 2025 (1).csv", skiprows=1)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
df = df.dropna(subset=["Date", "Slider Score"])

# Parse and explode population groups
# Each development can impact multiple groups - create a row for each
df["Parsed_Groups"] = df["Who is impacted?"].apply(parse_population_groups)

# Filter to rows that have at least one parsed group
df = df[df["Parsed_Groups"].apply(len) > 0].copy()

# Now explode the list into separate rows
df = df.explode("Parsed_Groups", ignore_index=True)

# Extract the tuple into separate columns
df[["Main_Population_Group", "Specific_Subgroup"]] = pd.DataFrame(
    df["Parsed_Groups"].apply(list).tolist(), 
    index=df.index
)

# Drop the intermediate column
df = df.drop(columns=["Parsed_Groups"])

st.sidebar.subheader("Filter by Population Group")

# Reset button
if st.sidebar.button("Reset Filters", use_container_width=True):
    st.session_state.main_population_group = 0
    st.session_state.sub_population_group = 0
    st.rerun()

# Main group selector with "All" option
main_group_options = ["All Population Groups"] + list(POPULATION_STRUCTURE.keys())
main_group = st.sidebar.selectbox(
    "Main Population Group",
    options=main_group_options,
    index=0,
    key="main_population_group"
)

# Subgroup selector (cascades based on main_group)
if main_group == "All Population Groups":
    subgroups = ["All Subgroups"]
else:
    subgroups = ["All Subgroups"] + list(POPULATION_STRUCTURE[main_group].keys())

sub_group = st.sidebar.selectbox(
    "Specific Subgroup",
    options=subgroups,
    key="sub_population_group"
)

# Get the terms for the selected subgroup
if main_group == "All Population Groups":
    # Collect all terms from all groups and subgroups
    selected_terms = []
    for group_dict in POPULATION_STRUCTURE.values():
        for term_list in group_dict.values():
            selected_terms.extend(term_list)
elif sub_group == "All Subgroups":
    # Collect all terms from all subgroups in the selected main group
    selected_terms = []
    for term_list in POPULATION_STRUCTURE[main_group].values():
        selected_terms.extend(term_list)
else:
    selected_terms = POPULATION_STRUCTURE[main_group][sub_group]

# Display selected focus
st.sidebar.info(
    f"Showing data for **{main_group}** → **{sub_group}**"
)

# Forecast Direction
st.sidebar.subheader("Forecast Direction")
st.sidebar.markdown("""
<div style="display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.9rem;">
  <div style="display: flex; align-items: center; gap: 0.5rem;">
    <div style="width: 20px; height: 20px; background-color: #cf5442; border-radius: 3px;"></div>
    <span style="color: #ffffff;"><strong>Deteriorating</strong> — Challenges to gender equity</span>
  </div>
  <div style="display: flex; align-items: center; gap: 0.5rem;">
    <div style="width: 20px; height: 20px; background-color: #62af44; border-radius: 3px;"></div>
    <span style="color: #ffffff;"><strong>Improving</strong> — Advances in gender equity</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Logo at bottom of sidebar
st.sidebar.divider()
st.sidebar.image("assets/footer_logo.svg", use_container_width=True)

st.title("Population Group Impact Analysis")

st.write(
    "Explore which population groups are most targeted by gender policy developments in the U.S."
)

# Display all available groups and subgroups
with st.expander("View all Population Groups & Subgroups", expanded=False):
    for main_group_name, subgroups_dict in POPULATION_STRUCTURE.items():
        st.subheader(main_group_name)
        for subgroup_name, keywords in subgroups_dict.items():
            st.markdown(f"**{subgroup_name}**")
            # Display keywords as a comma-separated list
            keywords_str = ", ".join([f"_{kw}_" for kw in keywords])
            st.markdown(f"{keywords_str}", unsafe_allow_html=True)

st.divider()

IMPACT_COL = "Specific_Subgroup"  # Use the mapped subgroup column instead of raw text
MAIN_GROUP_COL = "Main_Population_Group"  # Use the mapped main group column

# Filter data by selected main population group
# Since data is now pre-parsed, filtering is direct column matching
if main_group == "All Population Groups":
    # Show all groups
    if sub_group == "All Subgroups":
        df_filtered = df.copy()
    else:
        # This shouldn't happen with cascade logic, but handle it
        df_filtered = df.copy()
else:
    # Filter to selected main group
    df_filtered = df[df[MAIN_GROUP_COL] == main_group].copy()
    
    # Further filter by subgroup if specified
    if sub_group != "All Subgroups":
        df_filtered = df_filtered[df_filtered[IMPACT_COL] == sub_group].copy()

st.markdown(f"**Filtering by:** {main_group} → {sub_group}")

if df_filtered.empty:
    st.warning(f"No data available for: {main_group} → {sub_group}")
    st.stop()

df = df_filtered  # Use filtered data for all subsequent analysis

def get_top_developments_for_group(data_df, main_group_name, subgroup_name, top_n=1, score_filter=None):
    """Extract top N contributing developments for a given population group.
    
    score_filter: None (all), 'deterioration' (positive scores), or 'improvement' (negative scores)
    """
    if data_df.empty:
        return []
    
    # Filter by main group and subgroup 
    filtered = data_df[
        (data_df[MAIN_GROUP_COL] == main_group_name) & 
        (data_df[IMPACT_COL] == subgroup_name) &
        (data_df["Development"].notna())
    ]
    
    # Apply score filter if specified
    if score_filter == "deterioration":
        filtered = filtered[filtered["Slider Score"] > 0]
    elif score_filter == "improvement":
        filtered = filtered[filtered["Slider Score"] < 0]
    
    if filtered.empty:
        return []
    
    filtered = filtered.copy()
    filtered["Abs Score"] = filtered["Slider Score"].abs()
    filtered = filtered.sort_values(
        by=["Abs Score", "Date"],
        ascending=[False, False]
    )
    
    top_developments = []
    for idx, row in filtered.head(top_n).iterrows():
        full_text = row["Development"]
        # Create short text by finding first sentence (period + space) or truncating to 100 chars
        if isinstance(full_text, str):
            # Look for sentence end (period followed by space or end of string)
            sentences = full_text.split('. ')
            short_text = sentences[0]
            # If first part is less than 20 chars and there's a second sentence, include both
            if len(short_text) < 20 and len(sentences) > 1:
                short_text = sentences[0] + '. ' + sentences[1]
            short_text = short_text.strip()
            if not short_text.endswith('.'):
                short_text += '.'
        else:
            short_text = full_text
        # Truncate if too long
        if len(short_text) > 100:
            short_text = short_text[:97] + "..."
        source_url = row.get("Link", "")
        score = row["Slider Score"]
        top_developments.append((short_text, full_text, source_url, score))
    
    return top_developments

# Compute metrics based on current filter selection
df_initial = df.copy()  # Use filtered data for metrics
df_initial["Weighted Deterioration"] = np.where(df_initial["Slider Score"] > 0, df_initial["Slider Score"], 0)
df_initial["Weighted Improvement"] = np.where(df_initial["Slider Score"] < 0, -df_initial["Slider Score"], 0)
df_initial["Absolute Intensity"] = df_initial["Slider Score"].abs()

# Determine what level to display metrics at
# CRITICAL RULE: The Population Group Impact chart ONLY shows Main Population Groups
# Subgroups are for filtering and detail tables, never for the main chart

# === CHART METRICS: Always aggregate by Main Population Group ===
impact_metrics_chart = []
for group_name in df_initial[MAIN_GROUP_COL].unique():
    if pd.notna(group_name):
        group_df = df_initial[df_initial[MAIN_GROUP_COL] == group_name]
        if len(group_df) > 0:
            impact_metrics_chart.append({
                "Group": group_name,
                "Weighted Deterioration": group_df["Weighted Deterioration"].sum(),
                "Weighted Improvement": group_df["Weighted Improvement"].sum(),
                "Absolute Intensity": group_df["Absolute Intensity"].sum(),
                "Event_Count": len(group_df)
            })

impact_metrics_initial = pd.DataFrame(impact_metrics_chart) if impact_metrics_chart else pd.DataFrame(columns=["Group", "Weighted Deterioration", "Weighted Improvement", "Absolute Intensity", "Event_Count"])

# === DETAIL METRICS: For drill-down views, show subgroups only (not for chart) ===
detail_metrics = []

if main_group != "All Population Groups" and sub_group == "All Subgroups":
    # Drill-down: Show per-subgroup breakdown in a detail table
    for subgroup_name in df_initial[IMPACT_COL].unique():
        if pd.notna(subgroup_name):
            subgroup_df = df_initial[df_initial[IMPACT_COL] == subgroup_name]
            if len(subgroup_df) > 0:
                detail_metrics.append({
                    "Subgroup": subgroup_name,
                    "Weighted Deterioration": subgroup_df["Weighted Deterioration"].sum(),
                    "Weighted Improvement": subgroup_df["Weighted Improvement"].sum(),
                    "Absolute Intensity": subgroup_df["Absolute Intensity"].sum(),
                    "Event_Count": len(subgroup_df)
                })

detail_metrics_df = pd.DataFrame(detail_metrics) if detail_metrics else pd.DataFrame()

# Generate Key Insights with development examples
insights = []
insights_devs = {}

# Only generate detailed insights when showing all Population Groups
if not impact_metrics_initial.empty and main_group == "All Population Groups":
    # Insight 1: Highest Absolute Intensity
    most_impacted = impact_metrics_initial.loc[impact_metrics_initial["Absolute Intensity"].idxmax()]
    group_name = most_impacted["Group"]
    insights.append(f"<strong>{group_name}</strong> experiences the highest total intensity of impact ({most_impacted['Absolute Intensity']:.1f})")
    # For all population groups view, get top dev from that main group
    group_devs = df_initial[df_initial[MAIN_GROUP_COL] == group_name]
    example_devs = group_devs.nlargest(1, "Absolute Intensity") if len(group_devs) > 0 else pd.DataFrame()
    if len(example_devs) > 0:
        row = example_devs.iloc[0]
        short_text = row["Development"][:100] if isinstance(row["Development"], str) else ""
        insights_devs["impact"] = {"group": group_name, "example": short_text}
    
    # Insight 2: Most Disrupted
    most_disrupted = impact_metrics_initial.loc[impact_metrics_initial["Weighted Deterioration"].idxmax()]
    if most_disrupted["Weighted Deterioration"] > 0:
        if most_disrupted["Group"] == most_impacted["Group"] and len(impact_metrics_initial) > 1:
            most_disrupted = impact_metrics_initial.nlargest(2, "Weighted Deterioration").iloc[1]
        
        group_name = most_disrupted["Group"]
        insights.append(f"<strong>{group_name}</strong> is most affected by deterioration (weighted deterioration score: {most_disrupted['Weighted Deterioration']:.1f})")
        insights_devs["disruption"] = {"group": group_name}
    
    # Insight 3: Most Progressed
    most_progressed = impact_metrics_initial.loc[impact_metrics_initial["Weighted Improvement"].idxmax()]
    if most_progressed["Weighted Improvement"] > 0:
        used_groups = {most_impacted["Group"]}
        if "disruption" in insights_devs:
            used_groups.add(insights_devs["disruption"]["group"])
        
        improvement_sorted = impact_metrics_initial.nlargest(len(impact_metrics_initial), "Weighted Improvement")
        for idx, row in improvement_sorted.iterrows():
            if row["Group"] not in used_groups:
                most_progressed = row
                break
        
        group_name = most_progressed["Group"]
        insights.append(f"<strong>{group_name}</strong> shows the most improvement (weighted improvement score: {most_progressed['Weighted Improvement']:.1f})")
        insights_devs["progression"] = {"group": group_name}

# Determine number of unique groups
num_groups = impact_metrics_initial.shape[0] if not impact_metrics_initial.empty else 0

# Display selector for top N groups
st.divider()

col1, col2 = st.columns([3, 1])
with col2:
    display_option = st.selectbox(
        "Show",
        options=["Top 5", "Top 10", "All"],
        index=0,
        label_visibility="collapsed",
        key="top_groups_display_option"
    )

# Determine how many groups to display based on selection
if display_option == "Top 5":
    top_n_viz = min(5, num_groups)
elif display_option == "Top 10":
    top_n_viz = min(10, num_groups)
else:  # All
    top_n_viz = num_groups

# Set sort column for ranking
sort_col = "Event_Count"  # Sort by number of developments

# Use pre-computed metrics and filter to top N
impact_metrics = impact_metrics_initial.copy()
if not impact_metrics.empty:
    impact_metrics = impact_metrics.sort_values(sort_col, ascending=False).head(top_n_viz)

st.subheader("Population Group Impact Rankings")

# Add subtitle explaining which level is being displayed
if main_group == "All Population Groups":
    st.caption("**View Level:** All Main Population Groups (10 categories)")
elif sub_group != "All Subgroups":
    st.caption(f"**View Level:** Detailed - {sub_group} only")
else:
    st.caption(f"**View Level:** Subgroups of {main_group}")

# Dynamic chart height based on number of groups
# Ensure minimum spacing between bars for readability
min_height_per_group = 80  # pixels per group minimum (increased for wrapped labels)
base_height = 100  # base padding
chart_height = max(400, len(impact_metrics) * min_height_per_group + base_height) if not impact_metrics.empty else 250

# Chart shows main groups ranked by development count
x_field = "Event_Count:Q"
x_title = "Number of Developments"

# Enhanced chart
if not impact_metrics.empty:
    impact_chart = (
        alt.Chart(impact_metrics)
        .mark_bar(opacity=1)
        .encode(
            x=alt.X(x_field, title=x_title, axis=alt.Axis(tickCount=10)),
            y=alt.Y("Group:N", title="Population Group", sort="-x", axis=alt.Axis(labelLimit=120, labelPadding=10, labelOffset=30)),
            color=alt.value(COLOR_DISRUPTION),
            tooltip=[alt.Tooltip("Group", title="Population Group"), 
                    alt.Tooltip(x_field, title=x_title)],
        )
        .properties(height=chart_height, width=1500, title="Gender Policy Activity by Population Group")
        .configure_mark(opacity=1)
        .configure_title(anchor="middle")
    )

    st.altair_chart(impact_chart, use_container_width=True)
else:
    st.info("No population groups data available for visualization.")

# How to Interpret This Chart section
with st.expander("How to Interpret This Chart", expanded=False):
    st.markdown("""
**Number of Developments:** The total number of gender policy developments affecting each population group. Higher counts indicate groups experiencing more frequent policy impact.

**Chart Always Shows:** Main Population Groups only (10 categories) to ensure clean, non-overlapping categories aligned with the hierarchical structure.

**Drill-Down:** Select a specific population group from the sidebar to view detailed breakdown by subgroups.
""")

# Show subgroup detail table if drilling down into a specific main group
if main_group != "All Population Groups" and sub_group == "All Subgroups" and not detail_metrics_df.empty:
    st.subheader(f"Breakdown: {main_group} → All Subgroups")
    st.caption("Detailed metrics for each subgroup within this population group")
    st.dataframe(
        detail_metrics_df.sort_values("Event_Count", ascending=False),
        column_config={
            "Subgroup": st.column_config.TextColumn(label="Subgroup"),
            "Weighted Deterioration": st.column_config.NumberColumn(label="Deterioration", format="%d"),
            "Weighted Improvement": st.column_config.NumberColumn(label="Improvement", format="%d"),
            "Absolute Intensity": st.column_config.NumberColumn(label="Total Intensity", format="%d"),
            "Event_Count": st.column_config.NumberColumn(label="# Developments", format="%d"),
        },
        use_container_width=True,
        hide_index=True,
    )
    st.divider()

# Key Insights section
insights_html = "\n".join([f"<li style='margin-bottom: 0.5rem; color: #1b1725; font-size: 1rem;'>{insight}</li>" for insight in insights])

st.markdown(f"""
<div style="background-color: #f1f0ec; border-left: 4px solid #bfa359; padding: 1rem; margin: 1.5rem 0; border-radius: 2px; box-shadow: 0 1px 3px rgba(27, 23, 37, 0.08);">
  <div style="font-size: 1.1rem; font-weight: 700; color: #1b1725; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em;">Key Insights</div>
  <ul style="margin: 0; padding-left: 1.5rem; list-style: disc;">
    {insights_html}
  </ul>
</div>
""", unsafe_allow_html=True)

# Display development examples for each insight
st.subheader("Example Developments")

col1, col2, col3 = st.columns(3)

with col1:
    if "impact" in insights_devs and insights_devs["impact"]["devs"]:
        with st.expander("Highest Impact Developments"):
            st.caption(f"From: {insights_devs['impact']['group']}")
            for short_text, full_text, url, score in insights_devs["impact"]["devs"]:
                st.write(f"**{short_text}**")
                if full_text and full_text != short_text:
                    st.caption(full_text)
                if url:
                    st.caption(f"[View Source]({url})")

with col2:
    if "disruption" in insights_devs and insights_devs["disruption"]["devs"]:
        with st.expander("Deterioration Examples"):
            st.caption(f"From: {insights_devs['disruption']['group']}")
            for short_text, full_text, url, score in insights_devs["disruption"]["devs"]:
                st.write(f"**{short_text}**")
                if full_text and full_text != short_text:
                    st.caption(full_text)
                if url:
                    st.caption(f"[View Source]({url})")

with col3:
    if "progression" in insights_devs and insights_devs["progression"]["devs"]:
        with st.expander("Improvement Examples"):
            st.caption(f"From: {insights_devs['progression']['group']}")
            for short_text, full_text, url, score in insights_devs["progression"]["devs"]:
                st.write(f"**{short_text}**")
                if full_text and full_text != short_text:
                    st.caption(full_text)
                if url:
                    st.caption(f"[View Source]({url})")

st.divider()

# Display as collapsible table
with st.expander("View Detailed Population Group Metrics", expanded=False):
    if not impact_metrics_initial.empty:
        # Reorder columns for display
        display_columns = ["Group", "Weighted Deterioration", "Weighted Improvement", "Absolute Intensity", "Event_Count"]
        st.dataframe(
            impact_metrics_initial[display_columns].sort_values(sort_col, ascending=False),
            column_config={
                "Group": st.column_config.TextColumn(label="Population Group"),
                "Weighted Deterioration": st.column_config.NumberColumn(label="Deterioration Intensity", format="%d"),
                "Weighted Improvement": st.column_config.NumberColumn(label="Improvement Intensity", format="%d"),
                "Absolute Intensity": st.column_config.NumberColumn(label="Overall Policy Activity", format="%d"),
                "Event_Count": st.column_config.NumberColumn(label="Number of Developments", format="%d"),
            },
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No population groups data available.")

st.divider()

# Recent Developments Panel
st.subheader("Recent Developments by Population Group")

# Use the selected main_group and sub_group
if sub_group:
    # Get all developments affecting the selected group using the filtered data
    all_group_data = df.sort_values("Date", ascending=False)
    
    if not all_group_data.empty:
        # Calculate context metrics
        total_devs = len(all_group_data)
        disruption_count = len(all_group_data[all_group_data["Slider Score"] > 0])
        progression_count = len(all_group_data[all_group_data["Slider Score"] < 0])
        neutral_count = len(all_group_data[all_group_data["Slider Score"] == 0])
        
        # Get date range
        earliest_date = all_group_data["Date"].min()
        latest_date = all_group_data["Date"].max()
        if pd.notna(earliest_date):
            date_range_str = f"since {earliest_date.strftime('%b %Y')}"
        else:
            date_range_str = "on record"
        
        # Display context summary
        st.markdown(f"""
**{main_group} → {sub_group}**  
{total_devs} developments {date_range_str}  
{disruption_count} Disruption | {neutral_count} Neutral | {progression_count} Progression
        """)
        
        # Display recent developments (top 5)
        group_data = all_group_data.head(5)
        
        st.markdown("**Latest developments:**")
        
        for idx, row in group_data.iterrows():
            # Format date
            date_str = row["Date"].strftime("%b %d, %Y") if pd.notna(row["Date"]) else "Unknown Date"
            
            # Determine direction color
            score = row["Slider Score"]
            direction_color = COLOR_DISRUPTION if score > 0 else COLOR_PROGRESSION if score < 0 else "#999"
            direction_label = "Deteriorating" if score > 0 else "Improving" if score < 0 else "Neutral"
            
            # Format development text
            dev_text = str(row["Development"])
            if len(dev_text) > 200:
                dev_text = dev_text[:197] + "..."
            
            # Build the card
            card_html = f"""
            <div style="
                background: white;
                border-left: 4px solid {direction_color};
                padding: 0.75rem 1rem;
                margin-bottom: 0.75rem;
                border-radius: 2px;
                box-shadow: 0 1px 2px rgba(27, 23, 37, 0.08);
            ">
                <div style="font-size: 0.75rem; color: rgba(27, 23, 37, 0.6); font-weight: 600; margin-bottom: 0.4rem;">
                    {date_str} • <span style="
                        display: inline-block;
                        text-transform: uppercase;
                        background: {direction_color}25;
                        color: {direction_color};
                        padding: 0.3rem 0.6rem;
                        border-radius: 2px;
                        letter-spacing: 0.05em;
                        font-size: 0.7rem;
                        font-weight: 700;
                    ">{direction_label}</span>
                </div>
                <div style="font-size: 0.9rem; color: #1b1725; line-height: 1.4; margin-bottom: 0.4rem; font-weight: 500;">
                    {dev_text}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem;">
                    <span style="color: rgba(27, 23, 37, 0.7);"><strong>{row.get("Forecast", "N/A")}</strong></span>
                    {f'<a href="{row["Link"]}" target="_blank" style="color: #bfa359; text-decoration: none; font-weight: 600;">View Source →</a>' if pd.notna(row.get("Link")) and row["Link"] else ""}
                </div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.info(f"No developments recorded for {main_group} → {sub_group}")

st.divider()

# Policy Activity Trends Over Time
st.subheader("Policy Activity Trends Over Time")

# Prepare monthly trend data for top 3 most impacted groups
df_trends = df.copy()
df_trends["Month"] = df_trends["Date"].dt.to_period("M").astype(str)
df_trends["Absolute Intensity"] = df_trends["Slider Score"].abs()

top_3_groups = (
    impact_metrics_initial.nlargest(3, "Absolute Intensity")["Group"].tolist()
    if not impact_metrics_initial.empty else []
)

# Build trend data for top 3 groups
trend_data_list = []
for group in top_3_groups:
    # Filter by the mapped group column (no regex needed - exact match)
    group_df = df_trends[df_trends["Group"] == group]
    if len(group_df) > 0:
        group_df_monthly = group_df.groupby("Month", as_index=False).agg({
            "Absolute Intensity": "sum",
            "Slider Score": "count"
        }).rename(columns={"Slider Score": "Event_Count"})
        
        group_df_monthly["Group"] = group
        trend_data_list.append(group_df_monthly)

if trend_data_list:
    trend_data = pd.concat(trend_data_list, ignore_index=True)
    
    # Convert Month back to datetime for proper sorting
    trend_data["Month_Date"] = pd.to_datetime(trend_data["Month"])
    trend_data = trend_data.sort_values("Month_Date")
    # Format month for display in tooltip
    trend_data["Month_Display"] = trend_data["Month_Date"].dt.strftime("%b %Y")
    
    if not trend_data.empty:
        # Create selection for tooltip
        selection = alt.selection_single(on="mouseover", empty="none")
        
        # Custom color palette
        group_colors = ["#bfa359", "#62af44", "#7fa3c0"]
        
        trend_chart = (
            alt.Chart(trend_data)
            .mark_line(point=True, size=2)
            .encode(
                x=alt.X(
                    "Month_Date:T",
                    title="Period",
                    axis=alt.Axis(format="%b %Y", labelAngle=0, labelPadding=15, tickCount=2),
                    scale=alt.Scale(nice=False)
                ),
                y=alt.Y("Absolute Intensity:Q", title="Cumulative Policy Activity"),
                color=alt.Color("Group:N", 
                               scale=alt.Scale(range=group_colors),
                               title="Population Group",
                               legend=alt.Legend(orient="bottom", symbolType="square", titleAnchor="start", labelLimit=300, labelPadding=15))
            )
            .add_selection(selection)
            .encode(
                tooltip=[
                    alt.Tooltip("Month_Display:N", title="Month"),
                    alt.Tooltip("Group:N", title="Population Group"),
                    alt.Tooltip("Absolute Intensity:Q", title="Policy Activity", format=".1f"),
                    alt.Tooltip("Event_Count:Q", title="Count")
                ]
            )
            .properties(height=350, width=1200)
        )
        
        st.altair_chart(trend_chart, use_container_width=False)
        
        with st.expander("How to Interpret this Chart", expanded=False):
            st.markdown("""
**Lines:** Each line represents one of the three most impacted population groups, showing how cumulative policy activity evolves over time.

**Rising lines:** Indicate accelerating institutional pressure and policy change affecting that group.

**Declining lines:** Suggest stabilization or a slowdown in policy activity.

**Month-to-month comparison:** Compare groups to identify which are experiencing intensifying vs. stabilizing policy environments. Groups with steeper upward trends are experiencing rapid policy transformation.
            """)
else:
    st.info("Insufficient data to generate trend visualization.")
