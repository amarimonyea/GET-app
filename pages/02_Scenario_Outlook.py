import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import altair as alt
import html
import textwrap
import base64
import os 
import re

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

# Logo at bottom of sidebar
st.sidebar.image("assets/footer_logo.svg", use_container_width=True)

# Sort cards by probability
PROB_RANK = {"Low": 1, "Low–Medium": 2, "Medium": 3, "Medium–High": 4, "High": 5}

# ---------------------------
# 2) FORECAST SCENARIOS (initialize)
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
        "summary": "The U.S. gender policy landscape remains highly contested due to geopolitical shifts, withdrawal from global gender frameworks, and state-level policy restrictions rolling back reproductive and transgender rights.",
        "full_assessment": "The US has been in several international conflicts since the beginning of the year including Mexico, Venezuela, and Iran. The United States's standing as global gender rights champion is no longer true as they have pulled out of <a href=\"https://apnews.com/article/united-nations-trump-international-organizations-withdrawal-d704fb9b444dc9cf569865d391b544a6\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">66 international organizations</a>, including UN Women, UNFPA, and other global cooperation initiatives.\n\nSeveral states are rolling back protections for trans individuals as Kansas passed a law <a href=\"https://apnews.com/article/united-nations-trump-international-organizations-withdrawal-d704fb9b444dc9cf569865d391b544a6\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">banning the changes of sex markers</a> on birth certificates and driver licenses, immediately making over 1000 residents IDs invalid.\n\nAdditionally, the SAVE Act represents another policy shift with significant implications for gender equity and immigration-related protections.",
        "implications": []
    },
]

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

st.title("Scenario Outlook")
st.markdown("<p style='font-size: 1.1rem; color: rgba(27, 23, 37, 0.85); margin-top: -20px;'>Explore different scenarios for the evolution of the U.S. gender policy landscape</p>", unsafe_allow_html=True)

st.divider()

# ---------------------------
# 3) CURRENT ENVIRONMENT 
# ---------------------------
st.subheader("Current Environment")

NL_BLUE = "#3b668c"
NL_RED  = "#cf5442"
NL_GOLD = "#bfa359"
CARD_CSS = f"""
<style>
/* =========================
   GRID (4 columns)
   ========================= */
.scenario-cards-container {{
  max-height: 1000px;
  overflow-y: auto;
  padding-right: 8px;
}}

.scenario-cards-container::-webkit-scrollbar {{
  width: 10px;
}}

.scenario-cards-container::-webkit-scrollbar-track {{
  background: rgba(27, 23, 37, 0.05);
  border-radius: 5px;
}}

.scenario-cards-container::-webkit-scrollbar-thumb {{
  background: rgba(27, 23, 37, 0.25);
  border-radius: 5px;
}}

.scenario-cards-container::-webkit-scrollbar-thumb:hover {{
  background: rgba(27, 23, 37, 0.4);
}}

.deck {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.5rem;
  min-height: 0;
  align-items: start;
}}

@media (max-width: 1100px) {{
  .deck {{
    grid-template-columns: 1fr;
    gap: 1rem;
  }}
}}

.status-quo-section {{
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid rgba(27, 23, 37, 0.15);
}}

.status-quo-label {{
  font-size: 0.9rem;
  font-weight: 600;
  color: rgba(27, 23, 37, 0.6);
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

/* ========================= 
   EXPANDABLE ASSESSMENT
   ========================= */
.assessment-summary {{
  color: #1b1725;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  font-weight: 500;
}}

.assessment-toggle {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  padding: 0.75rem 0;
  color: #3b668c;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.15s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.assessment-toggle:hover {{
  color: #1b1725;
}}

.assessment-toggle-icon {{
  display: inline-block;
  transition: transform 0.2s ease;
}}

.assessment-toggle.expanded .assessment-toggle-icon {{
  transform: rotate(180deg);
}}

.assessment-full {{
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, opacity 0.3s ease, padding 0.3s ease;
  opacity: 0;
  padding: 0;
  color: rgba(27, 23, 37, 0.85);
}}

.assessment-full.expanded {{
  max-height: 1000px;
  opacity: 1;
  padding: 1rem 0;
}}

.assessment-full {{
  font-size: 0.93rem;
  line-height: 1.7;
  color: rgba(27, 23, 37, 0.85);
  white-space: pre-wrap;
  word-wrap: break-word;
}}


.status-quo-container {{
  display: flex;
  justify-content: center;
  width: 100%;
}}

.status-quo-container .deck-item {{
  max-width: 400px;
  width: 100%;
}}

.status-quo-container .deck-card {{
  padding: 1rem;
}}

.deck-pile {{
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 0;
}}

/* Hide column headers entirely (if present) */
.deck-pile-header {{
  display: block !important;
  font-size: 1.3rem;
  font-weight: 700;
  color: #1b1725;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid #bfa359;
  text-transform: uppercase;
  letter-spacing: 0.08em;
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
  height: auto;
  overflow: visible;
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
  margin-top: .5rem;
  font-size: 0.95rem;
  line-height: 1.5;
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
  border-top-color: #773344 !important;
}}
.deck-card.hybrid .deck-title::before {{
  background: #773344 !important;
}}
.deck-card.hybrid .prob-fill {{
  background: #773344 !important;
}}

/* =========================
   NET ASSESSMENT SPOTLIGHT
   ========================= */
/* PARENT WRAPPER */
.spotlight-section {{
  background-color: #f1f0ec;
  margin: 2rem 0;
  padding: 2rem;
  border-radius: 4px;
  border-top: 1px solid rgba(27, 23, 37, 0.1);
  overflow: visible;
}}

.spotlight-title {{
  font-size: 1.3rem;
  font-weight: 700;
  color: #1b1725;
  margin-bottom: 1.5rem;
  letter-spacing: 0.02em;
}}

/* TWO-COLUMN LAYOUT */
.spotlight-container {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: stretch;
}}

/* LEFT COLUMN */
.spotlight-main {{
  background: white;
  border-radius: 4px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;  /* pushes source link down nicely */
  overflow: visible;
  min-height: 100%;
  box-sizing: border-box;
  box-shadow: 0 1px 2px rgba(27, 23, 37, 0.06);
  border-top: 4px solid #3b668c;
}}

.spotlight-main.disruption {{
  border-top-color: #cf5442;
}}

.spotlight-main.progression {{
  border-top-color: #3b668c;
}}

.spotlight-main.hybrid {{
  border-top-color: #bfa359;
}}

.spotlight-headline {{
  font-size: 1.1rem;
  font-weight: 700;
  color: #1b1725;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}}

.spotlight-meta {{
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: rgba(27, 23, 37, 0.6);
}}

.spotlight-meta-item {{
  display: flex;
  align-items: center;
  gap: 0.25rem;
}}

.spotlight-badge {{
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.spotlight-badge.disruption {{
  background-color: rgba(207, 84, 66, 0.1);
  color: #cf5442;
}}

.spotlight-badge.progression {{
  background-color: rgba(59, 102, 140, 0.1);
  color: #3b668c;
}}

.spotlight-analysis {{
  font-size: 0.95rem;
  color: #1b1725;
  line-height: 1.5;
  margin-bottom: 1rem;
}}

.spotlight-source {{
  font-size: 0.85rem;
  color: #bfa359;
  text-decoration: none;
  font-weight: 600;
}}

.spotlight-source:hover {{
  text-decoration: underline;
}}

/* RIGHT COLUMN: two stacked equal tiles */
.spotlight-articles {{
  display: grid;
  grid-template-rows: 1fr 1fr;
  gap: 1.5rem;
  height: 100%;
  width: 100%;
}}

/* article links are grid items */
.spotlight-articles > a {{
  display: flex;
  flex-direction: column;
  min-height: 0;
}}

/* article tile fills the link and row */
.article-tile {{
  background: white;
  border-radius: 4px;
  overflow: visible;
  box-shadow: 0 1px 2px rgba(27, 23, 37, 0.06);
  transition: box-shadow 0.2s ease;
  width: 100%;
  display: flex;
  flex-direction: column;
  flex: 1;
  box-sizing: border-box;
}}

.article-tile:hover {{
  box-shadow: 0 2px 4px rgba(27, 23, 37, 0.12);
}}

.article-image {{
  width: 100%;
  height: 140px;
  object-fit: cover;
  display: block;
  flex-shrink: 0;
}}

.article-content {{
  padding: 1rem;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}}

.article-title {{
  font-size: 0.9rem;
  font-weight: 700;
  color: #1b1725;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}}

.article-source {{
  font-size: 0.8rem;
  color: rgba(27, 23, 37, 0.6);
  margin-bottom: 0.75rem;
}}

.article-link {{
  display: inline-block;
  color: #bfa359;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
}}

.article-link:hover {{
  text-decoration: underline;
}}

/* MOBILE */
@media (max-width: 768px) {{
  .spotlight-container {{
    grid-template-columns: 1fr;
  }}

  .spotlight-articles {{
    grid-template-rows: auto;
  }}

  .spotlight-articles > a {{
    height: auto;
  }}

  .article-tile {{
    height: auto;
  }}
}}
</style>
"""

def normalize_prob(p: str) -> str:
    p = (p or "").strip()
    # Remove percentage ranges like (5-25%) or (25-40%)
    p = re.sub(r"\s*\([^)]*%[^)]*\)\s*", "", p)
    p = p.replace("–", "-").replace("/", "-").replace(" to ", "-")
    p = re.sub(r"\s+", "", p).lower()
    return p

def direction_class(direction: str, name: str = "") -> str:
    n = (name or "").strip().lower()
    d = (direction or "").strip().lower()
    if "hybrid" in n or "hybrid" in d:
        return "hybrid"
    if "disruption" in d:
        return "disruption"
    if "progression" in d:
        return "progression"
    if "status" in d:
        return "statusquo"
    return "statusquo"

PROB_WIDTH = {"low": "20%", "low-medium": "40%", "medium": "60%", "medium-high": "80%", "high": "100%"}

cards_sorted = sorted(
    FORECAST_CARDS,
    key=lambda c: PROB_RANK.get(normalize_prob(str(c.get("probability", ""))), 0),
    reverse=True,
)

# Group cards by direction (excluding Status Quo)
cards_by_direction = {"Disruption": [], "Hybrid Disruption": [], "Progression": []}
status_quo_card = None

for c in cards_sorted:
    direction = c.get("direction", "Status Quo")
    # Separate Status Quo for its own section
    if direction == "Status Quo":
        status_quo_card = c
    # Separate hybrid disruption cards into their own column
    elif direction == "Disruption" and "Hybrid" in c.get("name", ""):
        cards_by_direction["Hybrid Disruption"].append(c)
    elif direction not in cards_by_direction:
        cards_by_direction[direction] = []
        cards_by_direction[direction].append(c)
    else:
        cards_by_direction[direction].append(c)

# Sort cards within each direction by probability (highest to lowest)
for direction in cards_by_direction:
    cards_by_direction[direction] = sorted(
        cards_by_direction[direction],
        key=lambda c: PROB_RANK.get(normalize_prob(str(c.get("probability", ""))), 0),
        reverse=True,
    )

cards_html = CARD_CSS

card_counter = 0

# Add Status Quo section at the top (with expandable full assessment)
status_quo_card_html = ""
if status_quo_card:
    summary = str(status_quo_card.get("summary", ""))
    full_assessment = str(status_quo_card.get("full_assessment", ""))
    
    status_quo_card_html += '<div class="status-quo-section">'
    status_quo_card_html += '<div class="status-quo-label">Baseline Scenario</div>'
    status_quo_card_html += '<div style="color: #1b1725; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em;">Status Quo</div>'
    
    # Summary text (always visible)
    status_quo_card_html += f'<div class="assessment-summary">{html.escape(summary)}</div>'
    
    # Expandable section with toggle button
    if full_assessment:
        status_quo_card_html += '<button class="assessment-toggle" onclick="this.classList.toggle(\'expanded\'); this.nextElementSibling.classList.toggle(\'expanded\');">'
        status_quo_card_html += '<span class="assessment-toggle-icon">▾</span>'
        status_quo_card_html += '<span>Read Full Q1 Net Assessment</span>'
        status_quo_card_html += '</button>'
        # Use full_assessment directly (allows HTML links) instead of escaping
        status_quo_card_html += f'<div class="assessment-full">{full_assessment}</div>'
    
    status_quo_card_html += '</div>'

cards_html += status_quo_card_html

# Render Net Assessment Spotlight section
if FEATURED_DEEP_DIVES:
    spotlight_dive = FEATURED_DEEP_DIVES[0]  # Use first deep dive for now
    direction_class_spotlight = spotlight_dive["direction"].lower()
    headline_escaped = html.escape(spotlight_dive["headline"])
    forecast_escaped = html.escape(spotlight_dive["forecast"])
    date_escaped = html.escape(spotlight_dive["date"])
    analysis_escaped = html.escape(spotlight_dive["analysis"])
    source_url = html.escape(spotlight_dive["source_url"])
    
    spotlight_html = '<div class="spotlight-section">'
    spotlight_html += '<div class="spotlight-title">Developments Shaping the Current Assessment</div>'
    spotlight_html += '<div class="spotlight-container">'
    
    # Main content (60%)
    spotlight_html += f'<div class="spotlight-main {direction_class_spotlight}">'
    spotlight_html += f'<div class="spotlight-headline">{headline_escaped}</div>'
    spotlight_html += '<div class="spotlight-meta">'
    spotlight_html += f'<div class="spotlight-meta-item">📅 {date_escaped}</div>'
    spotlight_html += f'<span class="spotlight-badge {direction_class_spotlight}">{forecast_escaped}</span>'
    spotlight_html += '</div>'
    spotlight_html += f'<div class="spotlight-analysis">{analysis_escaped}</div>'
    spotlight_html += f'<a href="{source_url}" target="_blank" class="spotlight-source">Read more →</a>'
    spotlight_html += '</div>'
    
    # Articles section (40%)
    spotlight_html += '<div class="spotlight-articles">'
    for article in spotlight_dive.get("articles", []):
        article_title = html.escape(article["title"])
        article_source = html.escape(article["source"])
        article_image_path = article["image_url"]
        article_link = html.escape(article["link_url"])
        
        # Convert image to base64 data URI
        article_image_data = image_to_base64(article_image_path)
        if article_image_data is None:
            # Fallback if image can't be loaded
            article_image_data = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='140'%3E%3Crect fill='%23ddd' width='300' height='140'/%3E%3C/svg%3E"
        
        spotlight_html += '<a href="' + article_link + '" target="_blank" style="text-decoration: none;">'
        spotlight_html += '<div class="article-tile">'
        spotlight_html += f'<img src="{article_image_data}" alt="Article" class="article-image">'
        spotlight_html += '<div class="article-content">'
        spotlight_html += f'<div class="article-title">{article_title}</div>'
        spotlight_html += f'<div class="article-source">{article_source}</div>'
        spotlight_html += '<div class="article-link">Read article →</div>'
        spotlight_html += '</div></div></a>'
    spotlight_html += '</div>'
    
    spotlight_html += '</div></div>'
    cards_html += spotlight_html

cards_html += '<div class="scenario-cards-container"><div class="deck">'

# Create three piles
for pile_direction in ["Disruption", "Hybrid Disruption", "Progression"]:
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
        summary = str(c.get("summary", ""))  # Don't escape to allow HTML links

        # Build monitoring indicators HTML
        monitoring_indicators = c.get("monitoring_indicators", [])
        if monitoring_indicators:
            indicators_html = '<ul style="margin: 0; padding-left: 20px; font-size: 0.90rem; color: rgba(27, 23, 37, 0.75);">'
            for indicator in monitoring_indicators:
                indicators_html += f'<li>{html.escape(str(indicator))}</li>'
            indicators_html += '</ul>'
        else:
            indicators_html = '<div style="font-size: 0.90rem; color: rgba(27, 23, 37, 0.75);">Coming soon</div>'

        bar_width = PROB_WIDTH.get(prob_key, "0%")
        card_class = direction_class(c.get("direction", ""), c.get("name", ""))

        # Build indicators section only for non-Status Quo cards
        indicators_section = ""
        implications_section = ""
        
        if c.get("direction") != "Status Quo":
            indicators_section = f"""
      <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(27, 23, 37, 0.15);">
        <div style="font-size: 0.85rem; font-weight: 700; color: var(--nl-navy); margin-bottom: 0.5rem;">Selected Monitoring Indicators</div>
        {indicators_html}
      </div>
"""
            
            # Build implications HTML
            implications = c.get("implications", [])
            if implications:
                implications_html = '<ul style="margin: 0; padding-left: 20px; font-size: 0.90rem; color: rgba(27, 23, 37, 0.75);">'
                for implication in implications:
                    implications_html += f'<li>{html.escape(str(implication))}</li>'
                implications_html += '</ul>'
            else:
                implications_html = '<div style="font-size: 0.90rem; color: rgba(27, 23, 37, 0.75);">Implications coming soon</div>'
            
            implications_section = f"""
      <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(27, 23, 37, 0.15);">
        <div style="font-size: 0.85rem; font-weight: 700; color: var(--nl-navy); margin-bottom: 0.5rem;">Potential Implications</div>
        {implications_html}
      </div>
"""

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

      <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(27, 23, 37, 0.15);">
        <div style="font-size: 0.85rem; font-weight: 700; color: var(--nl-navy); margin-bottom: 0.5rem;">Scenario Overview</div>
        <div class="deck-body">{summary}</div>
      </div>
{indicators_section}{implications_section}    </div>
  </div>
"""
    
    cards_html += '</div>'

cards_html += '</div>'  # Close scenario-cards-container
cards_html += '</div>'  # Close deck (no longer needed but keep for consistency)

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

# Split rendering: Gender Currently section (Status Quo + Developments)
cards_html_current = cards_html.split('<div class="scenario-cards-container">')[0]
cards_html_current_final = cards_html_current + DECK_JS
components.html(cards_html_current_final, height=825)

# Forecast Scenarios section
st.subheader("Forecast Scenarios")
cards_html_forecast = CARD_CSS + '<div class="scenario-cards-container">' + cards_html.split('<div class="scenario-cards-container">')[1] + DECK_JS
components.html(cards_html_forecast, height=1100)
