import streamlit as st

st.set_page_config(page_title="🌎 U.S. Gender Equality Tracker", layout="wide")

pg = st.navigation(
    [
        st.Page("home.py", title="Overview", default=True),
        st.Page("pages/01_Overview.py", title="Forecast Dashboard"),
        st.Page("pages/02_Scenario_Outlook.py", title="Scenario Outlook"),
        st.Page("pages/03_Sector_Impacts.py", title="Institutional Impact"),
        st.Page("pages/04_Human_Impact.py", title="Population Impact"),
        st.Page("pages/05_Core_Indicators.py", title="Core Indicators"),
        st.Page("pages/06_Methodology.py", title="Methodology"),
    ]
)

pg.run()


