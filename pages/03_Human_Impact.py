import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Human Impact", layout="wide")
st.title("👥 Human Impact Analysis")

# Load and prepare data
df = pd.read_csv("data/Monitor_Gender_Equality_sample_data.csv", skiprows=1)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
df = df.dropna(subset=["Date", "Slider Score"])

st.write(
    "Understand who is being impacted by these gender equality policy developments."
)

st.divider()

IMPACT_COL = "Who is impacted?"

# Count occurrences of different impact populations
impact_groups = []
for idx, row in df.iterrows():
    if pd.notna(row[IMPACT_COL]):
        # Split by comma and clean up whitespace
        groups = [g.strip() for g in str(row[IMPACT_COL]).split(",")]
        impact_groups.extend(groups)

impact_counts = {}
for group in impact_groups:
    impact_counts[group] = impact_counts.get(group, 0) + 1

impact_df = pd.DataFrame(
    list(impact_counts.items()),
    columns=[IMPACT_COL, "Frequency"]
).sort_values("Frequency", ascending=False)

# Sidebar slider for top N groups
top_n = st.sidebar.slider(
    "Show top N population groups",
    min_value=5,
    max_value=min(30, len(impact_df)),
    value=15,
    step=1,
)

st.subheader("Population Groups Most Impacted")

# Display table
st.dataframe(impact_df, use_container_width=True)

st.divider()

# Chart: Population impacts
chart = (
    alt.Chart(impact_df.head(top_n))
    .mark_bar(orient='horizontal')
    .encode(
        x=alt.X("Frequency:Q", title="Number of Events"),
        y=alt.Y(IMPACT_COL + ":N", sort="-x"),
        color=alt.value("#3b668c"),
        tooltip=[IMPACT_COL, "Frequency"],
    )
    .properties(height=min(500, top_n * 20))
)

st.altair_chart(chart, use_container_width=True)

st.caption("Population groups appearing most frequently in the dataset's impact descriptions.")
