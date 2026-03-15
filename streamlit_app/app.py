"""
Global Literacy & Education Trends – Streamlit Dashboard
Run: streamlit run app.py (from streamlit_app folder or project root)
"""
import sys
from pathlib import Path

# Add project root so we can import src
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

st.set_page_config(
    page_title="Global Literacy & Education Trends",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Global Literacy & Education Trends")
st.markdown("Education Analytics & Socio-Economic Data Analysis")
st.sidebar.success("Select a page above: **SQL Executor**, **EDA Visualizations**, **Country Profile**.")
st.info("Use the sidebar to open **SQL Query Executor**, **EDA Visualizations**, or **Country Profile**.")
st.markdown("---")
st.markdown("""
- **SQL Executor** – Run custom SQL and view results as tables or charts.
- **EDA Visualizations** – Pre-built charts (literacy vs GDP, trends, heatmaps).
- **Country Profile** – Pick a country and see all indicators over time.
""")
