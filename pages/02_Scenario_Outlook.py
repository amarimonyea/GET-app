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
COLOR_PROGRESSION = "#62af44"  # New Lines green
COLOR_NEUTRAL = "#1b1725"      # dark
NL_GOLD = "#bfa359"
NL_CREAM = "#f1f0ec"
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');

/* ---------- GLOBAL FONT ---------- */
body, [class*="css"] {{
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
        "summary": "This forecast envisions a reversal in which policy actions at state and federal levels establish, reinstate, or expand protections for gender, reproductive, and LGBTQ+ rights. Through institutional checks and pragmatic governance, rights fragmentation reverses and equity outcomes strengthen.",
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
        "summary": "This forecast illustrates how withdrawal from international gender frameworks and defunding of multilateral organizations undermines the US's ability to shape global gender policy. The resulting loss of soft power diminishes US credibility and accelerates global adoption of restrictive gender policies.",
        "monitoring_indicators": ["Adoption of US aligned conservative gender policies by foreign governments", "US withdrawal from or defunding of international organizations advancing gender, LGBTQ+, or reproductive rights"],
        "implications": ["Reduction of US credibility in multilateral institutions", "Decreased global access to reproductive, gender-based, and LGBTQ+ health and protection programs"]
    },
    {
        "name": "Diplomatic", 
        "direction": "Progression",
        "probability": "Low (5-25%)",
        "summary": "This forecast envisions renewed US commitment to international gender equality frameworks and restored funding for organizations advancing reproductive, LGBTQ+, and gender rights. Strengthened multilateral engagement rebuilds US credibility and increases global access to gender-affirming support systems.",
        "monitoring_indicators": ["Reaffirming support of international organizations supporting gender, LGBTQ+, and reproductive rights"],
        "implications": ["Implications coming soon"]
    },
     {
        "name": "Economic", 
        "direction": "Progression",
        "probability": "Low (5-25%)",
        "summary": "This forecast reflects increased investment in evidence-based research, public universities, and workforce development programs that advance gender equity and economic inclusion. Strengthened institutional commitment to equitable economic participation expands opportunities for marginalized communities and drives broader economic resilience.",
        "implications": ["Implications coming soon"]
    },
     {
        "name": "Economic", 
        "direction": "Disruption",
        "probability": "Low/Medium (25-40%)",
        "summary": "This forecast illustrates how cuts to federal research funding and defunding of equity-focused institutions disrupts workforce diversity initiatives and limits economic opportunities for marginalized communities. Reduced evidence-based policymaking weakens institutional capacity to address gender-driven economic inequities.",
        "monitoring_indicators": ["Cuts or divestments in federal scientific, evidence-based research, or mass media related to equity, gender, or social policy", "Decreased funding for public universities focused on social science research"],
        "implications": ["Reduced economic opportunities for marginalized communities", "Disruption of workforce diversity and inclusion initiatives"]
    },
     {
        "name": "Social", 
        "direction": "Disruption",
        "probability": "Medium/High (60-75%)",
        "summary": "This forecast illustrates how restrictive abortion policies create medical and ethical crises while anticipatory fear drives healthcare providers to withdraw services from vulnerable populations. The compounding effects of institutional pauses, discrimination escalation, and global human rights impacts reshape social landscapes.",
        "monitoring_indicators": ["Medical and ethical crises emerging from restrictive abortion policies", "Service withdrawal or denial driven by anticipated legal, financial, or political retaliation"],
        "implications": ["Increasing discrimination towards trans and gender-diverse individuals", "Global impact on diplomacy and human rights"]
    },
      {
        "name": "Social", 
        "direction": "Progression",
        "probability": "Low (5-25%)",
        "summary": "This forecast envisions the establishment or reinstatement of gender-conscious protection programs and the restoration of reproductive and gender-affirming services following periods of institutional pause. Strengthened social commitment to equity outcomes reverses discrimination trends and rebuilds community trust.",
        "monitoring_indicators": ["Establishment or reinstatement of gender-conscious or equity-oriented protection programs", "Restoration of reproductive and gender-affirming services following institutional pause"],
        "implications": ["Implications coming soon"]
    },
          {
        "name": "Security", 
        "direction": "Progression",
        "probability": "Low (5-25%)",
        "summary": "This forecast reflects rollback of national security laws targeting gender identity and increased inclusion of diverse voices in security policymaking. Institutional recognition of intersectional security vulnerabilities strengthens national resilience and protects marginalized communities.",
        "monitoring_indicators": ["Rollback of national laws targeting gender identity and based on sex", "Inclusion of diverse voices in national security policymaking spaces"],
        "implications": ["Implications coming soon"]
    },
        {
        "name": "Security", 
        "direction": "Disruption",
        "probability": "Medium (40-60%)",
        "summary": "This forecast illustrates how national security laws that target gender identity and that expand surveillance on women's and LGBTQ+ rights organizations criminalize vulnerable populations and limit civic participation.",
        "monitoring_indicators": ["National security laws targeting gender identity", "Expansion of state surveillance on women's and LGBTQ+ rights organizations"],
        "implications": ["Implications coming soon"]
    },
     {
        "name": "Hybrid Political/Security", 
        "direction": "Disruption",
        "probability": "Medium (40-60%)",
        "summary": "This forecast illustrates how political decisions drive removal of qualified personnel from defense and security sectors based on sexual orientation or gender identity while expanding surveillance of healthcare providers and advocacy organizations. The intersection of political purges and security-based criminalization creates cascading vulnerabilities for LGBTQ+ populations.",
        "monitoring_indicators": ["Removal of qualified civil servants and service members in national security sectors due to sexual orientation or gender identity", "Increased state surveillance and criminalization of healthcare providers offering gender-affirming services"],
        "implications": ["Implications coming soon"]
    },
      {
        "name": "Hybrid Political/Social", 
        "direction": "Disruption",
        "probability": "Medium (40-60%)",
        "summary": "This forecast illustrates how political decisions reduce legal protections against gender-based violence while simultaneously erasing gender-affirming care and related institutional support systems. The policy convergence around erasure and vulnerability creates compounding harms for women, trans, and gender-diverse populations.",
        "monitoring_indicators": ["Reduction of protections against gender-based violence", "Political and policy decisions resulting in the erasure of gender-affirming care and related protections"],
        "implications": ["Implications coming soon"]
    },
      {
        "name": "Status Quo", 
        "direction": "Status Quo",
        "probability": "",
        "summary": "The U.S. gender policy landscape remains highly contested due to geopolitical shifts, withdrawal from global gender frameworks, and state-level policy restrictions rolling back reproductive and transgender rights.",
        "full_assessment": "<p>The US has instigated several international conflicts since the beginning of the year, including invading Venezuela and starting a war with Israel against Iran. The United States' standing as global gender rights champion is no longer true as the U.S. has pulled out of <a href=\"https://apnews.com/article/united-nations-trump-international-organizations-withdrawal-d704fb9b444dc9cf569865d391b544a6\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">66 international organizations</a>, including UN Women, UNFPA, and other global cooperation initiatives.</p><p>Several states are rolling back protections for transgender individuals. For example, Kansas passed a law <a href=\"https://apnews.com/article/transgender-rights-drivers-licenses-birth-certificates-bathrooms-3048b856b81d24553efd9da4aaa94bc7\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">banning the changes of sex markers</a> on birth certificates and driver licenses, immediately making over 1,800 residents' IDs invalid.</p><p>Additionally, the SAVE Act represents another policy shift with significant implications for gender equity and immigration-related protections.</p>",
        "implications": []
    },
]

FEATURED_DEEP_DIVES = [
    {
        "headline": "SAVE Act Implementation: Implications for Gender Equity and Vulnerable Populations",
        "forecast": "Forecasted Political Disruption",
        "direction": "disruption",
        "analysis": "The Safeguard Voter Eligibility (SAVE) Act which passed in the House <a href=\"https://www.brennancenter.org/our-work/analysis-opinion/house-passes-save-act-brennan-center-reacts\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">last year</a>, an updated version in <a href=\"https://rules.house.gov/bill/119/s-1383#:~:text=Revises%20the%20effective%20date%20of,rather%20than%202027%20or%20later.&text=Revised%20Prohibits%20federal%20funds%20from,the%20militarization%20of%20polling%20places.\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">February</a>, and is likely to pass in the Senate within the next few months would dramatically change the way voting is conducted in the United States right before midterm elections. President Trump has uttered support for this Act and has said he would refuse to sign <a href=\"https://www.theguardian.com/us-news/2026/mar/13/explainer-save-america-act\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">any other bills until it is passed</a>.\n\nIf passed the SAVE Act would impose strict voter ID regulations requiring voters to produce proof of citizenship and introduces <a href=\"https://campaignlegal.org/document/fact-sheet-save-act-threatens-all-voters\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">criminal liability</a> for election officials who fail to register voters without proper documentation and allows them to be sued to by private citizens. Moreover, the Trump Administration has challenged the validity of <a href=\"https://thehill.com/homenews/senate/5786819-save-america-act-absentee-voting/\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">absentee ballots</a>, which could negatively impact rural and elderly Americans.\n\nPassing the SAVE Act before the midterms will cause confusion and chaos among voters and election precincts, also with provisions built in with <a href=\"https://www.pbs.org/newshour/politics/watch-live-senate-begins-consideration-of-save-america-act\" target=\"_blank\" style=\"color: #3b668c; text-decoration: underline;\">Department of Homeland Security Oversight</a> it challenges the integrity of federal elections, undermining democratic processes.\n\nThe SAVE Act impacts all voters, but it specifically harms women, marginalized communities, and trans and non-binary communities. Several of these vulnerable populations do not have their personal documentation readily available and have financial barriers or social stigmas from obtaining new ones.",
        "analysis_by": "Amari Jones, Associate Analyst",
        "source_url": "https://www.congress.gov/bill/119th-congress/house-bill/22",
        "articles": [
            {
                "title": "Transgender Rights & Gender Recognition",
                "source": "AP News",
                "image_url": "assets/senate-placeholder.jpg",
                "link_url": "https://apnews.com/article/transgender-drivers-licenses-kansas-lawsuit-b34d868d7fe93b2946f54c831307b935",
                "analysis": "A case filed on Feb 26 by two transgender men against the state of Kansas argues that a new state law, which invalidated roughly 1800 transgender people's identification documents, violates rights privacy, autonomy, and due legal process granted by the state's Constitution. This law forces trans individuals in Kansas to carry identification that matches their sex as assigned on their birth certificate.\n\nThe new legislation represents ongoing attempts at the state and national levels to dehumanize, erase, and discriminate against transgender individuals, stripping them of their civil and legal rights and increasing already disproportionate community level vulnerabilities to mental health challenges, body dysphoria, suicide, self-harm, and identity-based targeting and violence.\n\nThe case challenging the law represents mobilized resistance against the escalated dehumanization of and discrimination against trans people—while Kansas is not the first state to enact this kind of policy, it is the first state to retroactively invalidate licenses already given, demonstrating a further regression of gender equality.",
                "analysis_by": "Riley Sullivan, Student Fellow"
            },
            {
                "title": "US International Reproductive Health Funding Restrictions",
                "source": "NPR",
                "image_url": "assets/un-women-placeholder.jpg",
                "link_url": "https://www.npr.org/2026/01/23/nx-s1-5683204/abortion-trump-mexico-city-policy",
                "analysis": "The federal government announced an expansion of the Mexico City Policy, a policy that initially barred U.S. funds from being used for abortions and reproductive healthcare. The new iteration of the policy earmarks $30 billion in federal aid funding to restrict its use for programs related to \"gender ideology\" and DEI.\n\nForeign- and U.S.-based organizations will be forced to stop lifesaving international programming for women, the LGBTQ+ community, people with HIV/AIDS, and other marginalized communities or risk funding withdrawals and becoming effectively defunct.\n\nOn top of the detriments to human security and organizational functionality, this shift will affect the U.S.'s ability to exert influence over and garner information from global public health networks, making the U.S. more vulnerable to public health threats.\n\nFurther, humanitarian assistance has been a long-established bargaining chip for the U.S. to use in diplomatic engagements. The expansion of the Mexico City Policy, however, limits the U.S.'s capacity to operationalize its humanitarian involvement as leverage, leaving the U.S. at a national security disadvantage. Without this \"soft\" power influence, the U.S. will be more likely to lean on more coercive or aggressive methods of engagement to pursue its interests abroad.",
                "analysis_by": "Riley Sullivan, Student Fellow"
            },
            {
                "title": "Immigration Enforcement & Reproductive Rights",
                "source": "Center for Reproductive Rights",
                "image_url": "assets/senate-placeholder.jpg",
                "link_url": "https://reproductiverights.org/news/trump-admin-must-provide-answers-for-horrifying-treatment-of-pregnant-ice-detainees/",
                "analysis": "Emerging reports of inhumane treatment of pregnant women in ICE custody detail concerning deprivations of maternal healthcare. Federal policy establishes that CBP and ICE are mandated to provide maternal healthcare and prenatal care, are restricted from moving pregnant minors to detention centers in states that prohibit reproductive healthcare like abortions, and are barred from detaining pregnant, postpartum, or nursing mothers outside of \"extreme circumstances.\" Yet, the treatment of pregnant women by CBP and ICE officials has been demonstrated to violate federal regulations. This represents a broad disregard for existing protective policies, and, combined with impunity from the federal government for these offenses, demonstrates that ICE is operating outside the scope of the law. Failure to comply with the policy designed to protect vulnerable populations illustrates a broader trend of unchecked federal overreach that jeopardizes human security.",
                "analysis_by": "Riley Sullivan, Student Fellow"
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
st.markdown("<p style='font-size: 1.1rem; color: rgba(27, 23, 37, 0.85); margin-top: -20px;'>Explore different forecast scenarios for the future of the U.S. gender policy landscape brought to you by New Lines' Gender Policy experts.</p>", unsafe_allow_html=True)

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
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid rgba(27, 23, 37, 0.15);
  page-break-inside: avoid;
  clear: both;
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

.assessment-details {{
  margin-top: 0.5rem;
}}

.assessment-summary-toggle {{
  cursor: pointer;
  color: #3b668c;
  font-size: 0.95rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  list-style: none;
  outline: none;
  padding: 0.5rem 0;
}}

.assessment-summary-toggle:hover {{
  color: #1b1725;
}}

.assessment-summary-toggle::-webkit-details-marker {{
  display: none;
}}

.assessment-summary-toggle::before {{
  content: "▸";
  display: inline-block;
  margin-right: 0.5rem;
  transition: transform 0.2s ease;
}}

.assessment-details[open] .assessment-summary-toggle::before {{
  transform: rotate(90deg);
}}

.assessment-full-text {{
  padding: 0.75rem 0 0 0;
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

/* Collapsible sections in cards */
details {{
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(27, 23, 37, 0.15);
}}

details summary {{
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--nl-navy);
  margin-bottom: 0.5rem;
  list-style: none;
  user-select: none;
}}

details summary::-webkit-details-marker {{
  display: none;
}}

details summary::before {{
  content: "▸";
  display: inline-block;
  margin-right: 0.5rem;
  transition: transform 0.2s ease;
}}

details[open] summary::before {{
  transform: rotate(90deg);
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
.prob-wrap {{ 
  margin-top: .55rem;
  display: block !important;
  visibility: visible !important;
}}
.prob-label {{
  font-size: .72rem;
  letter-spacing: .2px;
  color: rgba(27, 23, 37, 0.75) !important;
  margin-bottom: .25rem;
  display: block;
}}

.prob-bar {{
  height: 12px;
  border-radius: 999px;
  background: rgba(27, 23, 37, 0.10);
  overflow: visible;
  border: 1px solid rgba(27, 23, 37, 0.12);
  width: 100%;
  display: block;
}}

.prob-fill {{
  height: 100%;
  border-radius: 999px;
  background: var(--nl-gold);
  display: block;
  transition: width 0.3s ease;
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
  margin: 3rem 0 2rem 0;
  padding: 2rem;
  border-radius: 4px;
  border-top: 1px solid rgba(27, 23, 37, 0.1);
  overflow: visible;
  position: relative;
  z-index: 1;
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
  align-items: start;
}}

.spotlight-left {{
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  height: 100%;
  justify-content: space-between;
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
  min-height: 0;
  box-sizing: border-box;
  box-shadow: 0 1px 2px rgba(27, 23, 37, 0.06);
  border-top: 4px solid #3b668c;
  flex: 1;
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
  overflow: hidden;
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
  width: 100% !important;
  height: 140px !important;
  object-fit: cover !important;
  display: block !important;
  flex-shrink: 0 !important;
  background-color: #f0f0f0;
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
}}

.article-content {{
  padding: 1rem;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}}

.article-title {{
  font-size: 0.95rem;
  font-weight: 700;
  color: #1b1725;
  margin-bottom: 0.6rem;
  line-height: 1.35;
}}

.article-source {{
  font-size: 0.80rem;
  color: #1b1725;
  margin-bottom: 0.5rem;
  font-weight: 500;
}}

.article-analysis-by {{
  font-size: 0.80rem;
  color: #bfa359;
  font-weight: 600;
  margin-bottom: 0.6rem;
}}

.article-analysis {{
  font-size: 0.88rem;
  color: #1b1725;
  line-height: 1.55;
  margin-bottom: 0.75rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}}

.article-link {{
  display: inline-block;
  color: #bfa359;
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 600;
  margin-top: auto;
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

def format_analysis_as_bullets(text: str) -> str:
    """Convert analysis text into bullet-formatted HTML, treating paragraphs as distinct ideas."""
    import re
    
    # First, try to detect paragraph breaks (double newlines or significant spacing)
    # Split by double newlines, or by line breaks followed by capitalization
    paragraphs = re.split(r'\n\s*\n|\n(?=[A-Z])', text.strip())
    
    # Clean up each paragraph
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    if len(paragraphs) <= 1:
        # If no paragraph breaks detected, fallback to sentence grouping
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
        if len(sentences) <= 1:
            return text
        paragraphs = sentences
    
    # Create bullet list HTML
    bullets_html = '<ul style="margin: 0; padding-left: 1.2rem; list-style-type: disc;">'
    for idea in paragraphs:
        # Clean up the text (remove extra whitespace)
        idea = ' '.join(idea.split())
        bullets_html += f'<li style="margin-bottom: 0.35rem;">{idea}</li>'
    bullets_html += '</ul>'
    
    return bullets_html

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
    
    # Expandable section with native details/summary
    if full_assessment:
        status_quo_card_html += '<details class="assessment-details">'
        status_quo_card_html += '<summary class="assessment-summary-toggle">Read Full Q1 2026 Assessment</summary>'
        status_quo_card_html += f'<div class="assessment-full-text">{full_assessment}</div>'
        status_quo_card_html += '</details>'
    
    status_quo_card_html += '</div>'

cards_html += status_quo_card_html

# Render Net Assessment Spotlight section
if FEATURED_DEEP_DIVES:
    spotlight_dive = FEATURED_DEEP_DIVES[0]  # Use first deep dive for now
    direction_class_spotlight = spotlight_dive["direction"].lower()
    headline_escaped = html.escape(spotlight_dive["headline"])
    forecast_escaped = html.escape(spotlight_dive["forecast"])
    analysis_escaped = spotlight_dive["analysis"]
    source_url = html.escape(spotlight_dive["source_url"])
    
    spotlight_html = '<div class="spotlight-section">'
    spotlight_html += '<div class="spotlight-title">Developments Shaping the Current Assessment</div>'
    spotlight_html += '<div style="font-size: 0.85rem; color: rgba(27, 23, 37, 0.6); margin-bottom: 1.5rem;">Last Updated: March 12, 2026</div>'
    spotlight_html += '<div class="spotlight-container">'
    
    # LEFT COLUMN: Main content + first article
    spotlight_html += '<div class="spotlight-left">'
    spotlight_html += f'<div class="spotlight-main {direction_class_spotlight}">'
    spotlight_html += f'<div class="spotlight-headline">{headline_escaped}</div>'
    spotlight_html += '<div class="spotlight-meta">'
    spotlight_html += f'<span class="spotlight-badge {direction_class_spotlight}">{forecast_escaped}</span>'
    spotlight_html += '</div>'
    analysis_by = html.escape(spotlight_dive.get("analysis_by", ""))
    if analysis_by:
        spotlight_html += f'<div style="font-size: 0.85rem; color: #bfa359; font-weight: 600; margin-bottom: 1rem;">— {analysis_by}</div>'
    spotlight_html += f'<div class="spotlight-analysis">{analysis_escaped}</div>'
    spotlight_html += f'<a href="{source_url}" target="_blank" class="spotlight-source">Read Bill</a>'
    spotlight_html += '</div>'
    
    # First article on the left
    articles_list = spotlight_dive.get("articles", [])
    if articles_list:
        article = articles_list[0]
        article_title = html.escape(article["title"])
        article_source = html.escape(article["source"])
        article_image_path = article["image_url"]
        article_link = html.escape(article["link_url"])
        article_analysis_raw = article.get("analysis", "")
        article_analysis = format_analysis_as_bullets(article_analysis_raw)
        article_analysis_by = html.escape(article.get("analysis_by", ""))
        
        article_image_data = image_to_base64(article_image_path)
        if article_image_data is None:
            article_image_data = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25' viewBox='0 0 300 140'%3E%3Crect fill='%23ddd' width='300' height='140'/%3E%3C/svg%3E"
        
        spotlight_html += '<a href="' + article_link + '" target="_blank" style="text-decoration: none;">'
        spotlight_html += '<div class="article-tile">'
        spotlight_html += f'<img src="{article_image_data}" alt="Article" class="article-image">'
        spotlight_html += '<div class="article-content">'
        spotlight_html += f'<div class="article-title">{article_title}</div>'
        spotlight_html += f'<div class="article-source">{article_source}</div>'
        spotlight_html += f'<div class="article-analysis-by">— {article_analysis_by}</div>'
        spotlight_html += f'<div class="article-analysis">{article_analysis}</div>'
        spotlight_html += '<div class="article-link">Source →</div>'
        spotlight_html += '</div></div></a>'
    
    spotlight_html += '</div>'  # Close spotlight-left
    
    # RIGHT COLUMN: remaining 2 articles
    spotlight_html += '<div class="spotlight-articles">'
    for article in articles_list[1:]:  # Only articles 1 and 2
        article_title = html.escape(article["title"])
        article_source = html.escape(article["source"])
        article_image_path = article["image_url"]
        article_link = html.escape(article["link_url"])
        article_analysis_raw = article.get("analysis", "")
        article_analysis = format_analysis_as_bullets(article_analysis_raw)
        article_analysis_by = html.escape(article.get("analysis_by", ""))
        
        article_image_data = image_to_base64(article_image_path)
        if article_image_data is None:
            article_image_data = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25' viewBox='0 0 300 140'%3E%3Crect fill='%23ddd' width='300' height='140'/%3E%3C/svg%3E"
        
        spotlight_html += '<a href="' + article_link + '" target="_blank" style="text-decoration: none;">'
        spotlight_html += '<div class="article-tile">'
        spotlight_html += f'<img src="{article_image_data}" alt="Article" class="article-image">'
        spotlight_html += '<div class="article-content">'
        spotlight_html += f'<div class="article-title">{article_title}</div>'
        spotlight_html += f'<div class="article-source">{article_source}</div>'
        spotlight_html += f'<div class="article-analysis-by">— {article_analysis_by}</div>'
        spotlight_html += f'<div class="article-analysis">{article_analysis}</div>'
        spotlight_html += '<div class="article-link">Source →</div>'
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
      <details style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(27, 23, 37, 0.15);">
        <summary style="cursor: pointer; font-size: 0.85rem; font-weight: 700; color: var(--nl-navy); margin-bottom: 0.5rem; list-style: none;">Selected Monitoring Indicators</summary>
        {indicators_html}
      </details>
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
      <details style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(27, 23, 37, 0.15);">
        <summary style="cursor: pointer; font-size: 0.85rem; font-weight: 700; color: var(--nl-navy); margin-bottom: 0.5rem; list-style: none;">Potential Implications</summary>
        {implications_html}
      </details>
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

  // Add click handlers for cards
  cards.forEach((card) => {
    card.addEventListener('click', function(e) {
      // Don't toggle card if clicking on details/summary elements or links
      if (e.target.tagName === 'SUMMARY' || 
          e.target.tagName === 'A' || 
          e.target.closest('details') ||
          e.target.closest('a')) {
        return;
      }
      
      e.stopPropagation();
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
st.markdown(cards_html_current_final, unsafe_allow_html=True)

# Forecast Scenarios section
st.subheader("Forecast Scenarios")
cards_html_forecast = CARD_CSS + '<div class="scenario-cards-container">' + cards_html.split('<div class="scenario-cards-container">')[1] + DECK_JS
components.html(cards_html_forecast, height=1100)
