# Entry point for Streamlit app
# This file serves as the main entry point for the Streamlit application
import streamlit as st

# Page config
st.set_page_config(page_title="Monitor: Gender Equality Tracker", layout="wide")

# Display welcome/home page
st.title("Monitor: Gender Equality Tracker")
st.markdown("""
Welcome to the Gender Equality Tracker. Use the navigation menu on the left to explore different analyses.
""")
