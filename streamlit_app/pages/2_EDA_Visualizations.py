"""
EDA Visualizations – Pre-built charts from cleaned data.
"""
import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_cleaning import get_cleaned_dataframes, DATA_DIR

st.set_page_config(page_title="EDA | Literacy Trends", page_icon="📈", layout="wide")

st.title("📈 EDA Visualizations")

# Resolve data path: try next to app, then project root
data_dir = ROOT / "data"
if not data_dir.exists():
    data_dir = DATA_DIR

try:
    df_literacy, df_illiteracy, df_gdp_schooling = get_cleaned_dataframes(data_dir)
except Exception as e:
    st.warning("Load data first: place OWID CSVs in `data/` and run data cleaning, or initialize DB.")
    st.code(str(e))
    st.stop()

if df_literacy.empty and df_gdp_schooling.empty:
    st.info("No data in data/ folder. Run Colab notebook to download CSVs and place them in data/.")
    st.stop()

# Detect adult literacy column (canonical or any matching name)
def _adult_lit_col(df):
    if df is None or df.empty:
        return None
    if "adult_literacy_rate" in df.columns:
        return "adult_literacy_rate"
    for c in df.columns:
        if isinstance(c, str) and "adult" in c.lower() and "literacy" in c.lower():
            return c
    return None

adult_lit_col = _adult_lit_col(df_literacy)

viz = st.selectbox(
    "Choose visualization",
    [
        "Adult literacy distribution",
        "GDP vs Adult literacy (scatter)",
        "Literacy trend over time (global average)",
        "Correlation heatmap (merged)",
        "Top 15 countries by adult literacy (latest year)",
    ],
)

merged = pd.DataFrame()
if not df_literacy.empty and not df_gdp_schooling.empty:
    merged = df_literacy.merge(df_gdp_schooling, on=["country", "year"], how="inner")

fig, ax = plt.subplots(figsize=(10, 5))

if viz == "Adult literacy distribution":
    if adult_lit_col and df_literacy[adult_lit_col].notna().any():
        df_literacy[adult_lit_col].dropna().hist(ax=ax, bins=30, edgecolor="black", alpha=0.7)
        ax.set_title("Distribution of Adult Literacy Rate")
        ax.set_xlabel("Adult Literacy (%)")
    else:
        ax.set_title("No adult literacy data available")
        st.info("No adult literacy rate column or all values are missing. Ensure CSVs are in `data/` and re-run.")

elif viz == "GDP vs Adult literacy (scatter)":
    lit_col = _adult_lit_col(merged)
    if not merged.empty and "gdp_per_capita" in merged.columns and lit_col:
        recent = merged[merged["year"] >= 2015].dropna(subset=[lit_col, "gdp_per_capita"])
        if not recent.empty:
            sns.scatterplot(data=recent, x="gdp_per_capita", y=lit_col, alpha=0.6, ax=ax)
            ax.set_xscale("log")
            ax.set_title("Adult Literacy vs GDP per Capita (2015+)")
            ax.set_xlabel("GDP per capita")
            ax.set_ylabel("Adult Literacy (%)")
        else:
            ax.set_title("No data for 2015+ after dropping missing values")
    else:
        ax.set_title("Merge literacy + GDP data first (need both data/ CSVs)")
        st.info("Requires both literacy and GDP CSVs in `data/`.")

elif viz == "Literacy trend over time (global average)":
    if adult_lit_col and "year" in df_literacy.columns:
        global_avg = df_literacy.groupby("year")[adult_lit_col].mean().reset_index()
        valid = global_avg[adult_lit_col].notna()
        if valid.any():
            g = global_avg[valid]
            ax.plot(g["year"], g[adult_lit_col], marker="o", markersize=4)
            ax.set_title("Global Average Adult Literacy Over Time")
            ax.set_xlabel("Year")
            ax.set_ylabel("Adult Literacy (%)")
            ax.grid(True, alpha=0.3)
        else:
            ax.set_title("No adult literacy values by year")
    else:
        ax.set_title("No year or adult literacy column in data")
        st.info("Ensure literacy CSV is in `data/` with year and adult literacy columns.")

elif viz == "Correlation heatmap (merged)":
    if not merged.empty:
        num_cols = ["adult_literacy_rate", "gdp_per_capita", "avg_years_schooling", "illiteracy_pct", "youth_literacy_avg"]
        cols = [c for c in num_cols if c in merged.columns]
        if cols:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(merged[cols].corr(), annot=True, fmt=".2f", cmap="RdYlGn", center=0, ax=ax)
            ax.set_title("Correlation Heatmap (Literacy, GDP, Schooling)")
        else:
            ax.set_title("No numeric columns available for heatmap")
    else:
        ax.set_title("No merged data for heatmap")

elif viz == "Top 15 countries by adult literacy (latest year)":
    if adult_lit_col and "year" in df_literacy.columns:
        latest = df_literacy["year"].max()
        sub = df_literacy[df_literacy["year"] == latest].dropna(subset=[adult_lit_col])
        top = sub.nlargest(15, adult_lit_col)
        if not top.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(top["country"], top[adult_lit_col])
            ax.set_xlabel("Adult Literacy (%)")
            ax.set_title(f"Top 15 Countries by Adult Literacy ({int(latest)})")
            ax.invert_yaxis()
        else:
            ax.set_title("No data for latest year")
    else:
        ax.set_title("No adult literacy or year column")
        if not adult_lit_col:
            st.info("Adult literacy column not found. Ensure literacy CSVs are in `data/`.")

else:
    ax.set_title("Select a visualization")

plt.tight_layout()
st.pyplot(fig)
plt.close()
