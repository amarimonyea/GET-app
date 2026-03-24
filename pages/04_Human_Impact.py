import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Human Impact")

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

# Impact Chart Controls in sidebar
st.sidebar.subheader("Population Chart Controls")

# Reset controls callback
def reset_impact_controls():
    st.session_state["display_groups"] = "Top 5"
    st.session_state["rank_by_impact"] = "Number of Developments"

st.sidebar.button("Reset Controls", on_click=reset_impact_controls)

display_groups = st.sidebar.selectbox(
    "Population groups shown",
    options=["Top 3", "Top 5", "Top 10", "All"],
    index=1,
    key="display_groups"
)

rank_by_impact = st.sidebar.selectbox(
    "Rank groups by",
    options=["Number of Developments", "Disruption Intensity", "Overall Policy Activity"],
    index=0,
    key="rank_by_impact"
)

# Sidebar slider for visualization
top_n_viz = st.sidebar.slider(
    "Show top N in chart",
    min_value=5,
    max_value=30,
    value=5,
    step=1,
)

# Forecast Direction
st.sidebar.subheader("Forecast Direction")
st.sidebar.markdown("""
<div style="display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.9rem;">
  <div style="display: flex; align-items: center; gap: 0.5rem;">
    <div style="width: 20px; height: 20px; background-color: #cf5442; border-radius: 3px;"></div>
    <span style="color: #ffffff;"><strong>Disruption</strong> — Challenges to gender equity</span>
  </div>
  <div style="display: flex; align-items: center; gap: 0.5rem;">
    <div style="width: 20px; height: 20px; background-color: #62af44; border-radius: 3px;"></div>
    <span style="color: #ffffff;"><strong>Progression</strong> — Advances in gender equity</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Logo at bottom of sidebar
st.sidebar.divider()
st.sidebar.image("assets/footer_logo.svg", use_container_width=True)

st.title("Human Impact Analysis")

# Load and prepare data
df = pd.read_csv("data/Monitor - Gender Equality - GET 2025 (1).csv", skiprows=1)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
df = df.dropna(subset=["Date", "Slider Score"])

st.write(
    "Explore which population groups are most affected by gender policy developments in the U.S."
)

st.divider()

IMPACT_COL = "Who is impacted?"

def get_top_developments_for_group(data_df, group_name, top_n=2, score_filter=None):
    """Extract top N contributing developments for a given population group.
    
    score_filter: None (all), 'disruption' (positive scores), or 'progression' (negative scores)
    """
    if data_df.empty:
        return []
    
    filtered = data_df[
        (data_df[IMPACT_COL].str.contains(group_name, na=False, case=False)) & 
        (data_df["Development"].notna())
    ]
    
    # Apply score filter if specified
    if score_filter == "disruption":
        filtered = filtered[filtered["Slider Score"] > 0]
    elif score_filter == "progression":
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

# Compute initial metrics for Key Insights
df_initial = df.copy()
df_initial["Weighted Disruption"] = np.where(df_initial["Slider Score"] > 0, df_initial["Slider Score"], 0)
df_initial["Weighted Progression"] = np.where(df_initial["Slider Score"] < 0, -df_initial["Slider Score"], 0)
df_initial["Absolute Intensity"] = df_initial["Slider Score"].abs()

# Extract and count impact groups
impact_groups = []
for idx, row in df_initial.iterrows():
    if pd.notna(row[IMPACT_COL]):
        groups = [g.strip() for g in str(row[IMPACT_COL]).split(",")]
        impact_groups.extend(groups)

impact_counts = {}
for group in impact_groups:
    impact_counts[group] = impact_counts.get(group, 0) + 1

impact_counts_df = pd.DataFrame(
    list(impact_counts.items()),
    columns=[IMPACT_COL, "Event_Count"]
)

# Calculate metrics per impact group
impact_metrics_initial = []
for group in impact_counts_df[IMPACT_COL]:
    group_df = df_initial[[group in str(row) for row in df_initial[IMPACT_COL]]]
    
    if len(group_df) > 0:
        impact_metrics_initial.append({
            IMPACT_COL: group,
            "Weighted Disruption": group_df["Weighted Disruption"].sum(),
            "Weighted Progression": group_df["Weighted Progression"].sum(),
            "Absolute Intensity": group_df["Absolute Intensity"].sum(),
            "Event_Count": len(group_df)
        })

impact_metrics_initial = pd.DataFrame(impact_metrics_initial) if impact_metrics_initial else pd.DataFrame(columns=[IMPACT_COL, "Weighted Disruption", "Weighted Progression", "Absolute Intensity", "Event_Count"])

# Generate Key Insights with development examples
insights = []
insights_devs = {}

if not impact_metrics_initial.empty:
    # Insight 1: Highest Absolute Intensity
    most_impacted = impact_metrics_initial.loc[impact_metrics_initial["Absolute Intensity"].idxmax()]
    insights.append(f"<strong>{most_impacted[IMPACT_COL]}</strong> experiences the highest total intensity of impact ({most_impacted['Absolute Intensity']:.1f})")
    insights_devs["impact"] = {
        "group": most_impacted[IMPACT_COL],
        "devs": get_top_developments_for_group(df_initial, most_impacted[IMPACT_COL], top_n=2)
    }
    
    # Insight 2: Most Disrupted (different group if possible)
    most_disrupted = impact_metrics_initial.loc[impact_metrics_initial["Weighted Disruption"].idxmax()]
    if most_disrupted["Weighted Disruption"] > 0:
        # If same as most_impacted, try to get the 2nd most disrupted
        if most_disrupted[IMPACT_COL] == most_impacted[IMPACT_COL] and len(impact_metrics_initial) > 1:
            most_disrupted = impact_metrics_initial.nlargest(2, "Weighted Disruption").iloc[1]
        
        insights.append(f"<strong>{most_disrupted[IMPACT_COL]}</strong> is most affected by disruption (weighted disruption score: {most_disrupted['Weighted Disruption']:.1f})")
        insights_devs["disruption"] = {
            "group": most_disrupted[IMPACT_COL],
            "devs": get_top_developments_for_group(df_initial, most_disrupted[IMPACT_COL], top_n=2, score_filter="disruption")
        }
    
    # Insight 3: Most Progressed (different group from impact and disruption if possible)
    most_progressed = impact_metrics_initial.loc[impact_metrics_initial["Weighted Progression"].idxmax()]
    if most_progressed["Weighted Progression"] > 0:
        # Try to get a different group
        used_groups = {most_impacted[IMPACT_COL]}
        if "disruption" in insights_devs:
            used_groups.add(insights_devs["disruption"]["group"])
        
        # Find first progression entry not in used_groups
        progression_sorted = impact_metrics_initial.nlargest(len(impact_metrics_initial), "Weighted Progression")
        for idx, row in progression_sorted.iterrows():
            if row[IMPACT_COL] not in used_groups:
                most_progressed = row
                break
        
        insights.append(f"<strong>{most_progressed[IMPACT_COL]}</strong> shows the most progression (weighted progression score: {most_progressed['Weighted Progression']:.1f})")
        insights_devs["progression"] = {
            "group": most_progressed[IMPACT_COL],
            "devs": get_top_developments_for_group(df_initial, most_progressed[IMPACT_COL], top_n=2, score_filter="progression")
        }

# Determine number of unique groups
num_groups = impact_metrics_initial.shape[0] if not impact_metrics_initial.empty else 0

# Use sidebar controls to determine display settings
if display_groups == "Top 3":
    top_n_rank = 3
elif display_groups == "Top 5":
    top_n_rank = 5
elif display_groups == "Top 10":
    top_n_rank = 10
else:  # "All"
    top_n_rank = num_groups

# Map rank_by selection to column name
if rank_by_impact == "Number of Developments":
    sort_col = "Event_Count"
elif rank_by_impact == "Disruption Intensity":
    sort_col = "Weighted Disruption"
else:
    sort_col = "Absolute Intensity"

# Use pre-computed metrics
impact_metrics = impact_metrics_initial.copy()
if not impact_metrics.empty:
    impact_metrics = impact_metrics.sort_values(sort_col, ascending=False).head(top_n_viz)

st.subheader("Population Group Impact Rankings")

# Dynamic chart height based on number of groups
# Ensure minimum spacing between bars for readability
min_height_per_group = 80  # pixels per group minimum (increased for wrapped labels)
base_height = 100  # base padding
chart_height = max(400, len(impact_metrics) * min_height_per_group + base_height) if not impact_metrics.empty else 250

# Map sort_col to display titles
if sort_col == "Event_Count":
    x_field = "Event_Count:Q"
    x_title = "Number of Developments"
elif sort_col == "Weighted Disruption":
    x_field = "Weighted Disruption:Q"
    x_title = "Disruption Intensity"
else:  # "Absolute Intensity"
    x_field = "Absolute Intensity:Q"
    x_title = "Overall Policy Activity"

# Enhanced chart
if not impact_metrics.empty:
    impact_chart = (
        alt.Chart(impact_metrics)
        .mark_bar(opacity=1)
        .encode(
            x=alt.X(x_field, title=x_title, axis=alt.Axis(tickCount=10)),
            y=alt.Y(IMPACT_COL + ":N", title="Population Group", sort="-x", axis=alt.Axis(labelLimit=120, labelPadding=10, labelOffset=30)),
            color=alt.value(COLOR_DISRUPTION),
            tooltip=[alt.Tooltip(IMPACT_COL, title="Population Group"), 
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

**Disruption Intensity:** The cumulative impact of constraints, restrictions, and disruptive policy changes on each group. Higher values indicate groups facing greater institutional pressure.

**Overall Policy Activity:** The combined magnitude of policy change affecting each group regardless of direction. This metric highlights which groups are experiencing the greatest volume of policy activity.

**Interpretation:** Taken together, these metrics help distinguish between groups under sustained pressure (high frequency + high disruption) versus those in transition (high activity but mixed directional impact).
""")

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
        with st.expander("Disruption Examples"):
            st.caption(f"From: {insights_devs['disruption']['group']}")
            for short_text, full_text, url, score in insights_devs["disruption"]["devs"]:
                st.write(f"**{short_text}**")
                if full_text and full_text != short_text:
                    st.caption(full_text)
                if url:
                    st.caption(f"[View Source]({url})")

with col3:
    if "progression" in insights_devs and insights_devs["progression"]["devs"]:
        with st.expander("Progression Examples"):
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
        display_columns = [IMPACT_COL, "Weighted Disruption", "Weighted Progression", "Absolute Intensity", "Event_Count"]
        st.dataframe(
            impact_metrics_initial[display_columns].sort_values(sort_col, ascending=False),
            column_config={
                IMPACT_COL: st.column_config.TextColumn(label="Population Group"),
                "Weighted Disruption": st.column_config.NumberColumn(label="Disruption Intensity", format="%d"),
                "Weighted Progression": st.column_config.NumberColumn(label="Progression Intensity", format="%d"),
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

available_groups = sorted([g.strip() for g in impact_counts.keys()]) if impact_counts else []
selected_group = st.selectbox(
    "Select Population Group:",
    available_groups,
    index=0 if available_groups else None,
    key="group_selector"
)

if selected_group:
    # Get all developments affecting the selected group
    all_group_data = df[[selected_group in str(row) for row in df[IMPACT_COL]]].sort_values("Date", ascending=False)
    
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
**{selected_group}**  
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
            direction_label = "Disruption" if score > 0 else "Progression" if score < 0 else "Neutral"
            
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
        st.info(f"No developments recorded for {selected_group}")

st.divider()

# Policy Activity Trends Over Time
st.subheader("Policy Activity Trends Over Time")

# Prepare monthly trend data for top 3 most impacted groups
df_trends = df.copy()
df_trends["Month"] = df_trends["Date"].dt.to_period("M").astype(str)
df_trends["Absolute Intensity"] = df_trends["Slider Score"].abs()

top_3_groups = (
    impact_metrics_initial.nlargest(3, "Absolute Intensity")[IMPACT_COL].tolist()
    if not impact_metrics_initial.empty else []
)

# Build trend data for top 3 groups
trend_data_list = []
for group in top_3_groups:
    group_df_monthly = df_trends[[group in str(row) for row in df_trends[IMPACT_COL]]].groupby("Month", as_index=False).agg({
        "Absolute Intensity": "sum",
        "Slider Score": "count"
    }).rename(columns={"Slider Score": "Event_Count"})
    
    group_df_monthly[IMPACT_COL] = group
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
                color=alt.Color(IMPACT_COL + ":N", 
                               scale=alt.Scale(range=group_colors),
                               title="Population Group",
                               legend=alt.Legend(orient="bottom", symbolType="square", titleAnchor="start", labelLimit=300, labelPadding=15))
            )
            .add_selection(selection)
            .encode(
                tooltip=[
                    alt.Tooltip("Month_Display:N", title="Month"),
                    alt.Tooltip(IMPACT_COL + ":N", title="Population Group"),
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
