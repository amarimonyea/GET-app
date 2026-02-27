import streamlit as st
import pandas as pd

st.set_page_config(page_title="Methodology", layout="wide")
st.title("📋 Methodology")

st.write(
    """
Monitor: Gender Equality (GET) is a forecast model and early-warning system that tracks policy 
developments, political discourse, and institutional actions related to gender equality and LGBTQ+ rights.
"""
)

st.divider()

st.subheader("Project Overview")
st.write(
    """
GET functions as a **strategic foresight tool** to:
- **Interpret** developments in gender, reproductive, and LGBTQ+ policy landscapes
- **Identify** risk trajectories and emerging disruptions
- **Support** decision-making across public, private, and civil society sectors
"""
)

st.divider()

st.subheader("Key Metrics & Scoring")

st.markdown("""
### Slider Score

Each policy development is assigned a **Slider Score** ranging from **-4 to +4**:

- **Negative scores (-4 to -1)**: Represent **progressions**
  - Policy actions that establish, reinstate, or expand gender, reproductive, or LGBTQ+ protections
  - Examples: State legislation protecting reproductive rights, hate crime law expansions

- **Positive scores (+1 to +4)**: Represent **disruptions**
  - Legislative or executive actions restricting gender, reproductive, or workplace rights
  - Defunding of protections, institutional rollbacks, or service denials
  
- **Score of 0**: Status quo
  - Developments with no clear direction or impact

### Weighted Analysis

- **Weighted Disruption** = Sum of all positive slider scores
- **Weighted Progression** = Sum of absolute values of negative slider scores
- **Net Trend** = Disruption - Progression direction

""")

st.divider()

st.subheader("Development Classifications")

st.markdown("""
Each entry is categorized by:

- **Forecast Type**: Describes the nature of the development
  - Political Disruption, Diplomatic Progression, Social Disruption, etc.

- **Signpost**: Specific characteristic of the development
  - U.S. withdrawal from organizations, legislative restrictions, service denial, etc.

- **Sector Impacted**: Institutional domain affected
  - Federal Executive, Healthcare Systems, Education, International/Multilateral, etc.

- **Who is Impacted**: Target population groups
  - Transgender individuals, women and girls, LGBTQ+ communities, marginalized groups

- **Domain of Assessment**: Categorization framework
  - Procedural/Institutional, Material Impact, Discursive/Symbolic, Societal Behavior and Norms

""")

st.divider()

st.subheader("Data Source & Period")

st.markdown("""
This dashboard presents a curated dataset tracking **gender equality-related policy developments** 
from **January 2025 onwards**.

Data includes:
- Federal and state legislative and executive actions (US)
- International policy shifts and diplomatic developments
- Institutional policy changes in healthcare, education, and corporate sectors
- Civil society legal challenges and advocacy responses

""")

st.divider()

# ---------------------------
# Dataset preview (privacy-friendly sample)
# ---------------------------
st.subheader("Dataset Preview (sample only)")
st.caption("Showing a limited preview for transparency without exposing the full dataset.")
DATA_PATH = "data/Monitor_Gender_Equality_sample_data.csv"
try:
  df = pd.read_csv(DATA_PATH, skiprows=1)
  df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
  df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
  df = df.dropna(subset=["Date", "Slider Score"]).copy()
  st.dataframe(df.head(25), use_container_width=True)
except Exception:
  st.info("Dataset preview not available. Ensure the sample CSV exists in the `data/` folder.")

st.subheader("How to Use This Dashboard")

st.markdown("""
1. **Overview Page**: See monthly trend analysis and high-level metrics
2. **Sector Impacts Page**: Explore which sectors are most affected and by what metrics
3. **Human Impact Page**: Understand which population groups are experiencing policy impacts
4. **This Page**: Learn about the methodology and measurement framework

Use the sidebar filters on the Overview page to focus on specific Forecast types, Domains, or Sectors.
""")

st.divider()

st.info(
    "**Questions or feedback?** This tool is designed to support decision-makers and advocates. "
    "Consider your specific use case and interpretation needs when using these metrics."
)
