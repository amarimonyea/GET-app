import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import html
import textwrap 

# ---------------------------
# 0) PAGE CONFIG MUST BE FIRST
# ---------------------------
st.set_page_config(page_title="Monitor: Gender Equality Tracker", layout="wide")

# ---------------------------
# 1) THEME / CSS (inject once)
# ---------------------------
COLOR_DISRUPTION = "#cf5442"   # New Lines red
COLOR_PROGRESSION = "#3b668c"  # New Lines blue
COLOR_NEUTRAL = "#1b1725"      # dark

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');

/* Global font */
html, body, [class*="css"] {
  font-family: 'Roboto', sans-serif;
}

/* App background (cream) */
.stApp {
  background-color: #f1f0ec;
}

/* Sidebar (NL navy) */
section[data-testid="stSidebar"] {
  background-color: #1b1725;
  color: white;
}
section[data-testid="stSidebar"] * {
  color: white;
}
</style>
""",
    unsafe_allow_html=True,
)
# ---------------------------
# 2) HEADER
# ---------------------------
st.title("🌍 Monitor: Gender Equality Tracker")
st.write(
    "Tracking the U.S. gender policy landscape"
)

# ---------------------------
# 3) FORECAST CARDS (static copy) - defined here, displayed after quadrant
# ---------------------------
FORECAST_CARDS = [
    {"name": "Political",  "probability": "Medium–High", "direction": "Disruption",
     "summary": "Executive consolidation and judicial pressure are accelerating institutional rollback."},
    {"name": "Social",     "probability": "Medium–High", "direction": "Disruption",
     "summary": "Service withdrawal and policy compliance pressures are reshaping access and social norms."},
    {"name": "Economic",   "probability": "Low–Medium",  "direction": "Disruption",
     "summary": "Funding cuts and privatization pressures are weakening gender-responsive infrastructure."},
    {"name": "Diplomatic", "probability": "Low–Medium",  "direction": "Disruption",
     "summary": "U.S. credibility erosion is contributing to global rollback and norm diffusion."},
    {"name": "Hybrid",     "probability": "Medium",      "direction": "Disruption",
     "summary": "Cross-domain reinforcement is amplifying political, social, and security impacts."},
]

# Sort cards by probability
PROB_RANK = {"Low": 1, "Low–Medium": 2, "Medium": 3, "Medium–High": 4, "High": 5}

# ---------------------------
# 4) LOAD + CLEAN DATA
# ---------------------------
DATA_PATH = "data/Monitor_Gender_Equality_sample_data.csv"
df = pd.read_csv(DATA_PATH, skiprows=1)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Slider Score"] = pd.to_numeric(df["Slider Score"], errors="coerce")
df = df.dropna(subset=["Date", "Slider Score"]).copy()

FORECAST_COL = "Forecast"
DOMAIN_COL = "Domains of Assessment"
SECTOR_COL = "Sector Impacted"

# ---------------------------
# 5) TOP METRICS
# ---------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Events", len(df))
with col2:
    st.metric("Slider Score Range", f"{df['Slider Score'].min()} to {df['Slider Score'].max()}")
with col3:
    st.metric("Columns Tracked", len(df.columns))

# ---------------------------
# 6) SIDEBAR FILTERS (clean + reset works)
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

st.divider()

# ---------------------------
# 7) TRAJECTORY QUADRANT (cleaner)
# ---------------------------
st.subheader("Trajectory Quadrant")
st.caption("Cumulative intensity (emerging → accelerating) vs net direction (progression ↓ | disruption ↑).")

quad = df_filtered.copy()
quad["Prog"] = np.where(quad["Slider Score"] < 0, -quad["Slider Score"], 0)
quad["Disr"] = np.where(quad["Slider Score"] > 0,  quad["Slider Score"], 0)

forecast_points = quad.groupby(FORECAST_COL, as_index=False)[["Prog", "Disr"]].sum()
forecast_points["Cumulative Intensity"] = forecast_points["Prog"] + forecast_points["Disr"]
forecast_points["Net Direction"] = forecast_points["Disr"] - forecast_points["Prog"]

if forecast_points.empty:
    st.info("No data available for the current filters.")
else:
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
    y=alt.Y("Net Direction:Q", title="Net Direction"),
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
            color="#d4af37"   # ← NL gold
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
        .configure_view(fill="white")  # chart background
        .configure_axis(labelFont="Roboto", titleFont="Roboto")
        .configure_title(font="Roboto")
    )

    st.altair_chart(chart, use_container_width=True)

st.divider()

import textwrap
import re

# ---------------------------
# 8) FORECAST SCENARIOS CARDS (STACKED DECK + PROBABILITY)
# ---------------------------
st.subheader("📊 Forecast Scenarios")

NL_BLUE = "#3b668c"
NL_RED  = "#cf5442"
NL_NAVY = "#1b1725"
NL_GOLD = "#bfa359"

st.markdown(
    f"""
<style>
/* ONE COLUMN "DECK" */
.deck {{
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.15rem;
  margin-top: .5rem;
  max-width: 980px;   /* keeps it feeling like a deck */
}}

/* Card wrapper creates the stack effect */
.deck-item {{
  position: relative;
  padding-left: 18px;  /* room for the back layers */
  padding-top: 10px;
}}

/* Back layers (the "stack") */
.deck-item::before,
.deck-item::after {{
  content:"";
  position:absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  border-radius: 16px;
  z-index: 0;
}}

.deck-item::before {{
  transform: translate(10px, 10px);
  background: rgba(59,102,140,0.90); /* NL blue shadow sheet */
  filter: blur(.2px);
}}

.deck-item::after {{
  transform: translate(18px, 18px);
  background: rgba(207,84,66,0.85);  /* NL red deeper sheet */
  filter: blur(.2px);
}}

/* Front card */
.deck-card {{
  position: relative;
  z-index: 1;
  border-radius: 16px;
  padding: 1.25rem 1.35rem 1.1rem 1.35rem;
  background: {NL_BLUE};
  color: #fff;
  border: 3px solid rgba(255,255,255,.10);
  box-shadow: 0 18px 46px rgba(0,0,0,.22);
}}

.deck-title {{
  font-size: 1.35rem;
  font-weight: 900;
  margin: 0 0 .55rem 0;
}}

.deck-badge {{
  position:absolute;
  top: 14px;
  right: 16px;
  font-weight: 900;
  font-size: 2.2rem;
  opacity: .22;
}}

.deck-meta {{
  margin: .25rem 0 .55rem 0;
  opacity: .95;
}}

.deck-chip {{
  display:inline-block;
  padding:.22rem .60rem;
  border-radius:999px;
  font-size:.78rem;
  font-weight:800;
  margin-right:.45rem;
  border:1px solid rgba(255,255,255,.18);
  background: rgba(255,255,255,.10);
}}

.deck-body {{
  margin-top:.65rem;
  font-size:.98rem;
  opacity:.93;
  line-height:1.35;
  max-width: 70ch;
}}

/* Probability bar */
.prob-wrap {{ margin-top:.55rem; }}
.prob-label {{
  font-size:.72rem;
  letter-spacing:.2px;
  opacity:.88;
  margin-bottom:.25rem;
}}
.prob-bar {{
  height:10px;
  border-radius:999px;
  background: rgba(255,255,255,.18);
  overflow:hidden;
  border: 1px solid rgba(255,255,255,.18);
}}
.prob-fill {{
  height:100%;
  border-radius:999px;
  background: {NL_GOLD};
}}
</style>
""",
    unsafe_allow_html=True,
)

# --- probability helpers ---
def normalize_prob(p: str) -> str:
    p = (p or "").strip()
    p = p.replace("–", "-").replace("/", "-").replace(" to ", "-")
    p = p.replace(" ", "").lower()
    return p

PROB_RANK = {"low": 1, "low-medium": 2, "medium": 3, "medium-high": 4, "high": 5}
PROB_WIDTH = {"low": "20%", "low-medium": "40%", "medium": "60%", "medium-high": "80%", "high": "100%"}

# Sort by probability (high first)
cards_sorted = sorted(
    FORECAST_CARDS,
    key=lambda c: PROB_RANK.get(normalize_prob(str(c.get("probability", ""))), 0),
    reverse=True,
)

cards_html = '<div class="deck">'
for i, c in enumerate(cards_sorted, start=1):
    name = html.escape(str(c.get("name", "")))
    direction = html.escape(str(c.get("direction", "")))
    prob_raw = str(c.get("probability", ""))
    prob_key = normalize_prob(prob_raw)
    prob_display = html.escape(prob_raw)
    summary = html.escape(str(c.get("summary", "")))

    bar_width = PROB_WIDTH.get(prob_key, "0%")

    cards_html += f"""
      <div class="deck-item">
        <div class="deck-card">
          <div class="deck-badge">{i:02d}</div>
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

          <div class="deck-body">{summary}</div>
        </div>
      </div>
    """

cards_html += "</div>"
st.markdown(cards_html, unsafe_allow_html=True)

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
            y=alt.Y(f"{DOMAIN_COL}:N", sort=None, title="Domain of Assessment"),
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

    st.altair_chart((domain_chart + zero_line), use_container_width=True)

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
st.subheader("📋 Forecast Composition Over Time (Monthly)")

df_filtered["Month"] = df_filtered["Date"].dt.to_period("M").dt.to_timestamp(how="start")
monthly_forecast_counts = (
    df_filtered.groupby(["Month", FORECAST_COL]).size().reset_index(name="Count")
)

forecast_click = alt.selection_point(fields=[FORECAST_COL], bind="legend")

composition_chart = alt.Chart(monthly_forecast_counts).mark_bar().encode(
    x=alt.X("Month:T", title="Month"),
    y=alt.Y("Count:Q", title="Number of events"),
    color=alt.Color(f"{FORECAST_COL}:N", legend=alt.Legend(title="Forecast")),
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