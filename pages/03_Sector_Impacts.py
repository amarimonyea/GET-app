import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Sector Impacts", layout="wide")
st.title("📊 Sector Impacts Analysis")

# Load and prepare data
df = pd.read_csv("data/Monitor_Gender_Equality_sample_data.csv", skiprows=1)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
df = df.dropna(subset=["Date", "Slider Score"])

st.write(
    "Explore which sectors are most impacted by gender-related policy developments and disruptions."
)

st.divider()

SECTOR_COL = "Sector Impacted"

top_n = st.slider("Show top N sectors", min_value=5, max_value=25, value=10, step=1)

metric_choice = st.radio(
    "Rank sectors by:",
    [
        "Event Count",
        "Weighted Disruption (sum of positive Slider Score)",
        "Total Intensity (sum of |Slider Score|)"
    ],
    horizontal=True,
)

# Compute metrics for each sector
df["Weighted Disruption"] = np.where(df["Slider Score"] > 0, df["Slider Score"], 0)
df["Weighted Progression"] = np.where(df["Slider Score"] < 0, -df["Slider Score"], 0)
df["Absolute Intensity"] = df["Slider Score"].abs()

# Get actual event counts by sector
sector_counts = df[SECTOR_COL].value_counts().reset_index()
sector_counts.columns = [SECTOR_COL, "Event_Count"]

# Compute aggregated metrics per sector
sector_metrics = (
    df.groupby(SECTOR_COL, as_index=False)
    .agg({
        "Weighted Disruption": "sum",
        "Weighted Progression": "sum",
        "Absolute Intensity": "sum",
    })
)

# Merge with event counts
sector_metrics = sector_metrics.merge(sector_counts, on=SECTOR_COL, how="left")

# Sort by chosen metric
if metric_choice == "Event Count":
    sort_col = "Event_Count"
elif metric_choice == "Weighted Disruption (sum of positive Slider Score)":
    sort_col = "Weighted Disruption"
else:
    sort_col = "Absolute Intensity"

sector_metrics = sector_metrics.sort_values(sort_col, ascending=False).head(top_n)

st.subheader(f"Top {top_n} Sectors by {metric_choice}")

# Display as table
st.dataframe(
    sector_metrics.sort_values(sort_col, ascending=False),
    column_config={
        "Weighted Disruption": st.column_config.NumberColumn(format="%.1f"),
        "Weighted Progression": st.column_config.NumberColumn(format="%.1f"),
        "Absolute Intensity": st.column_config.NumberColumn(format="%.1f"),
    },
    use_container_width=True,
)

st.divider()

# Chart: Event count by sector
chart_data = sector_counts.sort_values("Event_Count", ascending=False).head(top_n)

sector_chart = (
    alt.Chart(chart_data)
    .mark_bar()
    .encode(
        x=alt.X("Event_Count:Q", title="Number of Events"),
        y=alt.Y(SECTOR_COL + ":N", title="Sector", sort="-x"),
        color=alt.value("#cf5442"),
        tooltip=[SECTOR_COL, "Event_Count"],
    )
    .properties(height=400)
)

st.altair_chart(sector_chart, use_container_width=True)

st.caption(
    "✨ Sectors closest to the bottom are most frequently impacted by gender-related policy developments."
)
