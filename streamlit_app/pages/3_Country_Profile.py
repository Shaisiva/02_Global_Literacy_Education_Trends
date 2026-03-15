"""
Country Profile – Select a country and view all indicators over time.
"""
import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_cleaning import get_cleaned_dataframes

st.set_page_config(page_title="Country Profile | Literacy Trends", page_icon="🗺️", layout="wide")

st.title("🗺️ Country Profile")

try:
    df_literacy, df_illiteracy, df_gdp_schooling = get_cleaned_dataframes(ROOT / "data")
except Exception as e:
    st.warning("Load data first: place OWID CSVs in `data/`.")
    st.stop()

# Country list from all three sources
countries = set()
for df in (df_literacy, df_illiteracy, df_gdp_schooling):
    if not df.empty and "country" in df.columns:
        countries.update(df["country"].dropna().astype(str).unique())
countries = sorted([c for c in countries if c and c not in ("nan", "")])

if not countries:
    st.info("No country data. Add CSVs to data/ and run cleaning.")
    st.stop()

country = st.selectbox("Select country", countries)

# Filter by country
lit = df_literacy[df_literacy["country"] == country] if not df_literacy.empty else pd.DataFrame()
ill = df_illiteracy[df_illiteracy["country"] == country] if not df_illiteracy.empty else pd.DataFrame()
gdp = df_gdp_schooling[df_gdp_schooling["country"] == country] if not df_gdp_schooling.empty else pd.DataFrame()

st.subheader(f"Indicators over time: {country}")

cols = st.columns(3)
with cols[0]:
    if not lit.empty and "year" in lit.columns and "adult_literacy_rate" in lit.columns:
        lit_sorted = lit.sort_values("year")
        st.line_chart(lit_sorted.set_index("year")[["adult_literacy_rate"]])
    else:
        st.write("No literacy trend data.")
with cols[1]:
    if not gdp.empty and "year" in gdp.columns and "gdp_per_capita" in gdp.columns:
        gdp_sorted = gdp.sort_values("year")
        st.line_chart(gdp_sorted.set_index("year")[["gdp_per_capita"]])
    else:
        st.write("No GDP trend data.")
with cols[2]:
    if not gdp.empty and "year" in gdp.columns and "avg_years_schooling" in gdp.columns:
        gdp_sorted = gdp.sort_values("year")
        st.line_chart(gdp_sorted.set_index("year")[["avg_years_schooling"]])
    else:
        st.write("No schooling trend data.")

# Summary table
st.subheader("Data table")
all_years = set()
if not lit.empty and "year" in lit.columns:
    all_years.update(lit["year"].dropna().astype(int))
if not gdp.empty and "year" in gdp.columns:
    all_years.update(gdp["year"].dropna().astype(int))
if not ill.empty and "year" in ill.columns:
    all_years.update(ill["year"].dropna().astype(int))

rows = []
for yr in sorted(all_years):
    row = {"year": yr}
    if not lit.empty:
        r = lit[lit["year"] == yr]
        if not r.empty:
            for c in ["adult_literacy_rate", "youth_literacy_male", "youth_literacy_female"]:
                if c in r.columns:
                    row[c] = r[c].iloc[0]
    if not gdp.empty:
        r = gdp[gdp["year"] == yr]
        if not r.empty:
            for c in ["gdp_per_capita", "avg_years_schooling"]:
                if c in r.columns:
                    row[c] = r[c].iloc[0]
    if not ill.empty:
        r = ill[ill["year"] == yr]
        if not r.empty and "illiteracy_pct" in r.columns:
            row["illiteracy_pct"] = r["illiteracy_pct"].iloc[0]
    rows.append(row)

summary_df = pd.DataFrame(rows)
if not summary_df.empty:
    st.dataframe(summary_df, use_container_width=True)
else:
    st.write("No combined data for this country.")
