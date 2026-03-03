import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import altair as alt
import html
import textwrap 

# ---------------------------
# 0) PAGE CONFIG MUST BE FIRST
# ---------------------------
st.set_page_config(page_title="Gender Equality Monitor", layout="wide")

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

# Sort cards by probability
PROB_RANK = {"Low": 1, "Low–Medium": 2, "Medium": 3, "Medium–High": 4, "High": 5}

# ---------------------------
# 3) FORECAST SCENARIOS (initialize empty)
# ---------------------------
FORECAST_CARDS = [
    {
        "name": "Political",
        "direction": "Progression",
        "probability": "Low/Medium",
        "summary": "Come back and write real scenarios later"
    },
    {
        "name": "Political", 
        "direction": "Disruption",
        "probability": "Medium/High",
        "summary": "Come back and write real scenarios later"
    },
    {
        "name": "Diplomatic", 
        "direction": "Disruption",
        "probability": "Low/Medium",
        "summary": "Come back and write real scenarios later"
    },
    {
        "name": "Diplomatic", 
        "direction": "Progression",
        "probability": "Low",
        "summary": "Come back and write real scenarios later"
    },
     {
        "name": "Economic", 
        "direction": "Progression",
        "probability": "Low",
        "summary": "Come back and write real scenarios later"
    },
     {
        "name": "Economic", 
        "direction": "Disruption",
        "probability": "Low/Medium",
        "summary": "Come back and write real scenarios later"
    },
     {
        "name": "Social", 
        "direction": "Disruption",
        "probability": "Medium/High",
        "summary": "Come back and write real scenarios later"
    },
      {
        "name": "Social", 
        "direction": "Progression",
        "probability": "Low",
        "summary": "Come back and write real scenarios later"
    },
          {
        "name": "Security", 
        "direction": "Progression",
        "probability": "Low",
        "summary": "Come back and write real scenarios later"
    },
        {
        "name": "Security", 
        "direction": "Disruption",
        "probability": "Medium",
        "summary": "Come back and write real scenarios later"
    },
     {
        "name": "Hybrid Political/Security", 
        "direction": "Disruption",
        "probability": "Medium",
        "summary": "Come back and write real scenarios later"
    },
      {
        "name": "Hybrid Political/Social", 
        "direction": "Disruption",
        "probability": "Medium",
        "summary": "Come back and write real scenarios later"
    },
      {
        "name": "Status Quo", 
        "direction": "Status Quo",
        "probability": "",
        "summary": "Come back and write real scenarios later"
    },
]

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
# 5) PAGE TITLE
# ---------------------------
st.title("🌍 Gender Equality Tracker")
st.caption("Tracking directional shifts in the U.S. gender policy landscape")

# ---------------------------
# 6) TOP METRICS
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Events", len(df))
with col2:
    st.metric("Slider Score Range", f"{df['Slider Score'].min()} to {df['Slider Score'].max()}")

# ---------------------------
# 7) SIDEBAR FILTERS (clean + reset works)
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

# Logo at bottom of sidebar
st.sidebar.divider()
st.sidebar.image("assets/footer_logo.svg", use_container_width=True)

st.divider()

# ---------------------------
# 8) DISRUPTION AND PROGRESSION MOMENTUM (cleaner)
# ---------------------------
st.markdown("""
<style>
.momentum-container {
    border: 2px solid #1b1725;   /* NL Navy */
    border-radius: 12px;
    padding: 1.25rem 1.5rem 1.5rem 1.5rem;
    background-color: #ffffff;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="momentum-container">', unsafe_allow_html=True)
    
    st.subheader("Disruption and Progression Momentum")
    st.caption("Cumulative intensity (emerging → accelerating) vs net direction (progression ↓ | disruption ↑).")

quad = df.copy()
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
        .configure_view(fill="white", stroke="#fade82", strokeWidth=2)  # chart background with outline
        .configure_axis(labelFont="Roboto", titleFont="Roboto")
        .configure_title(font="Roboto")
    )

    st.altair_chart(chart, use_container_width=True)
    
    # Extract key statistics for the explanation
    max_disr_idx = forecast_points["Disr"].idxmax()
    max_disr_name = forecast_points.loc[max_disr_idx, FORECAST_COL]
    max_disr_score = forecast_points.loc[max_disr_idx, "Disr"]
    
    max_prog_idx = forecast_points["Prog"].idxmax()
    max_prog_name = forecast_points.loc[max_prog_idx, FORECAST_COL]
    max_prog_score = forecast_points.loc[max_prog_idx, "Prog"]
    
    latest_date = df_filtered["Date"].max()
    date_str = latest_date.strftime("%B %d, %Y")
    
    st.markdown(f"""
**Momentum Graph Explanation**

The Disruption and Progression Momentum graph plots cumulative forecast intensity against net directional movement. Cumulative intensity reflects the volume and concentration of forecasted developments within a domain (emerging → accelerating), while vertical positioning distinguishes between disruptive and progressive trajectories. The quadrant framework highlights which issue areas are early-stage signals versus accelerating structural shifts.

**Highest cumulative disruption observed to date:** {max_disr_name} (cumulative disruption score: {max_disr_score:.1f})

**Highest cumulative progression observed to date:** {max_prog_name} (cumulative progression score: {max_prog_score:.1f})

**Data current as of:** {date_str}
""")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

import textwrap
import re

# ---------------------------
# 9) FORECAST SCENARIOS CARDS (STACKED DECK + PROBABILITY)
# ---------------------------
st.subheader("Forecast Scenarios")

NL_BLUE = "#3b668c"
NL_RED  = "#cf5442"
NL_GOLD = "#bfa359"
CARD_CSS = f"""
<style>
/* =========================
   GRID (3 columns)
   ========================= */
.deck {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.5rem;
  margin-top: .5rem;
  align-items: start;
}}

@media (max-width: 1100px) {{
  .deck {{
    grid-template-columns: 1fr;
    gap: 1rem;
  }}
}}

.deck-pile {{
  display: flex;
  flex-direction: column;
  gap: 1rem;
}}

/* Hide column headers entirely (if present) */
.deck-pile-header {{
  display: none !important;
}}

/* Kill any leftover stacked layers from older versions */
.deck-item::before,
.deck-item::after {{
  content: none !important;
  display: none !important;
}}

/* =========================
   CARD BASE (Structured Briefing)
   ========================= */
:root {{
  --nl-navy: #1b1725;
  --nl-cream: #f1f0ec;
  --nl-red:   #cf5442;
  --nl-blue:  #3b668c;
  --nl-gold:  #bfa359;
  --nl-slate: #93b5c3;  /* muted */
}}

.deck-card {{
  position: relative;
  border-radius: 14px;
  padding: 1.0rem 1.1rem;
  background: var(--nl-cream) !important;     /* cream card */
  color: var(--nl-navy) !important;          /* navy text */
  border: 1px solid rgba(27, 23, 37, 0.10);   /* subtle outline */
  border-top: 4px solid rgba(27, 23, 37, 0.25); /* default top rule */
  box-shadow: 0 10px 24px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: transform .15s ease, box-shadow .15s ease;
}}

.deck-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 14px 30px rgba(0,0,0,0.08);
}}

/* Collapse behavior */
.deck-card.collapsed .deck-body,
.deck-card.collapsed .prob-wrap {{
  display: none;
}}

.deck-title {{
  font-size: 1.05rem;
  font-weight: 900;
  margin: 0 0 .55rem 0;
  color: var(--nl-navy) !important;
}}

/* small accent dot (optional but nice) */
.deck-title::before {{
  content: "";
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  margin-right: .55rem;
  background: rgba(27, 23, 37, 0.35);
  transform: translateY(-1px);
}}

.deck-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: .45rem;
  margin: 0 0 .35rem 0;
}}

.deck-chip {{
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  padding: .20rem .55rem;
  border-radius: 999px;
  font-size: .78rem;
  font-weight: 800;
  border: 1px solid rgba(27, 23, 37, 0.14);
  background: rgba(27, 23, 37, 0.03);
  color: var(--nl-navy) !important;
}}

/* Body text */
.deck-body {{
  margin-top: .65rem;
  font-size: .95rem;
  line-height: 1.35;
  color: rgba(27, 23, 37, 0.92) !important;
  max-width: 72ch;
}}

/* Probability bar */
.prob-wrap {{ margin-top: .55rem; }}
.prob-label {{
  font-size: .72rem;
  letter-spacing: .2px;
  color: rgba(27, 23, 37, 0.75) !important;
  margin-bottom: .25rem;
}}

.prob-bar {{
  height: 10px;
  border-radius: 999px;
  background: rgba(27, 23, 37, 0.10);
  overflow: hidden;
  border: 1px solid rgba(27, 23, 37, 0.12);
}}

.prob-fill {{
  height: 100%;
  border-radius: 999px;
  background: var(--nl-gold); /* default fill */
}}

/* =========================
   ACCENTS (minimal use)
   ========================= */

/* Disruption = red accent */
.deck-card.disruption {{
  border-top-color: var(--nl-red) !important;
}}
.deck-card.disruption .deck-title::before {{
  background: var(--nl-red) !important;
}}
.deck-card.disruption .prob-fill {{
  background: var(--nl-red) !important;
}}

/* Progression = blue accent */
.deck-card.progression {{
  border-top-color: var(--nl-blue) !important;
}}
.deck-card.progression .deck-title::before {{
  background: var(--nl-blue) !important;
}}
.deck-card.progression .prob-fill {{
  background: var(--nl-blue) !important;
}}

/* Status quo = muted slate */
.deck-card.statusquo {{
  border-top-color: var(--nl-slate) !important;
}}
.deck-card.statusquo .deck-title::before {{
  background: var(--nl-slate) !important;
}}
.deck-card.statusquo .prob-fill {{
  background: var(--nl-slate) !important;
}}

/* Hybrid = gold */
.deck-card.hybrid {{
  border-top-color: var(--nl-gold) !important;
}}
.deck-card.hybrid .deck-title::before {{
  background: var(--nl-gold) !important;
}}
.deck-card.hybrid .prob-fill {{
  background: var(--nl-gold) !important;
}}
</style>
"""

def normalize_prob(p: str) -> str:
    p = (p or "").strip()
    p = p.replace("–", "-").replace("/", "-").replace(" to ", "-")
    p = re.sub(r"\s+", "", p).lower()
    return p

def direction_class(direction: str) -> str:
    d = (direction or "").strip().lower()
    if "disruption" in d:
        return "disruption"
    if "progression" in d:
        return "progression"
    if "status" in d:
        return "statusquo"
    if "hybrid" in d:
        return "hybrid"
    return "statusquo"

PROB_RANK  = {"low": 1, "low-medium": 2, "medium": 3, "medium-high": 4, "high": 5}
PROB_WIDTH = {"low": "20%", "low-medium": "40%", "medium": "60%", "medium-high": "80%", "high": "100%"}

cards_sorted = sorted(
    FORECAST_CARDS,
    key=lambda c: PROB_RANK.get(normalize_prob(str(c.get("probability", ""))), 0),
    reverse=True,
)

# Group cards by direction
cards_by_direction = {"Disruption": [], "Status Quo": [], "Progression": []}
for c in cards_sorted:
    direction = c.get("direction", "Status Quo")
    if direction not in cards_by_direction:
        cards_by_direction[direction] = []
    cards_by_direction[direction].append(c)

cards_html = CARD_CSS + '<div class="deck">'

# Create three piles
card_counter = 0
for pile_direction in ["Disruption", "Status Quo", "Progression"]:
    direction_lower = pile_direction.lower().replace(" ", "")
    cards_html += f'<div class="deck-pile deck-pile-{direction_lower}">'
    cards_html += f'<div class="deck-pile-header">{pile_direction}</div>'
    
    for c in cards_by_direction.get(pile_direction, []):
        card_counter += 1
        name = html.escape(str(c.get("name", "")))
        direction = html.escape(str(c.get("direction", "")))
        prob_raw = str(c.get("probability", ""))
        prob_key = normalize_prob(prob_raw)
        prob_display = html.escape(prob_raw)
        summary = html.escape(str(c.get("summary", "")))

        bar_width = PROB_WIDTH.get(prob_key, "0%")
        card_class = direction_class(c.get("direction", ""))

        cards_html += f"""
  <div class="deck-item">
    <div class="deck-card {card_class}" data-card-id="card-{card_counter}">
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
    
    cards_html += '</div>'

cards_html += "</div>"

# Add JavaScript for interactivity
DECK_JS = """
<script>
document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.deck-card');

  // Add click handlers
  cards.forEach((card) => {
    card.addEventListener('click', function(e) {
      e.stopPropagation();
      // Simply toggle the clicked card
      card.classList.toggle('collapsed');
    });
  });

  // Collapse all cards initially
  cards.forEach((card) => {
    card.classList.add('collapsed');
  });
});
</script>
"""

cards_html_final = cards_html + DECK_JS

# Render with Streamlit's HTML component
components.html(cards_html_final, height=850)

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
            y=alt.Y(f"{DOMAIN_COL}:N", sort=None, title="Domain of Assessment", axis=alt.Axis(labelLimit=300, labelPadding=15)),
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

    st.altair_chart((domain_chart + zero_line).properties(padding={"left": 40, "right": 40, "top": 20, "bottom": 20}), use_container_width=True)

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
st.subheader("Forecast Composition Over Time")

df_filtered["Month"] = df_filtered["Date"].dt.to_period("M").dt.to_timestamp(how="start")
monthly_forecast_counts = (
    df_filtered.groupby(["Month", FORECAST_COL]).size().reset_index(name="Count")
)

forecast_click = alt.selection_point(fields=[FORECAST_COL], bind="legend")

# Extended color palette for forecast categories
SECONDARY_COLORS = ["#1b1725", "#bfa359", "#f1f0ec", "#3b668c", "#cf5442", "#773344", "#e1bb4b", "#fade82", "#93b5c3", "#dca465", "#62af44"]

# Get unique forecast values from data to map colors consistently
forecast_categories = sorted(monthly_forecast_counts[FORECAST_COL].unique().tolist())
# Create a color mapping for each forecast category
color_range = SECONDARY_COLORS[:len(forecast_categories)]
color_scale = alt.Scale(domain=forecast_categories, range=color_range)

composition_chart = alt.Chart(monthly_forecast_counts).mark_bar().encode(
    x=alt.X("Month:T", title="Month"),
    y=alt.Y("Count:Q", title="Number of events"),
    color=alt.Color(f"{FORECAST_COL}:N", scale=color_scale, legend=alt.Legend(title="Forecast")),
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