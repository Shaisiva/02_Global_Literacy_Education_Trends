"""
SQL Query Executor – Select a question or enter custom query, display table and optional chart.
"""
import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.db_utils import get_sqlite_engine, run_query, init_db_from_cleaned_data

st.set_page_config(page_title="SQL Executor | Literacy Trends", page_icon="🧮", layout="wide")

st.title("🧮 SQL Query Executor")

# All 13 project questions with their SQL (in order)
QUESTIONS = [
    # literacy_rates
    (
        "1. Get top 5 countries with highest adult literacy in 2020.",
        """SELECT country, year, adult_literacy_rate
FROM literacy_rates
WHERE year = 2020 AND adult_literacy_rate IS NOT NULL
ORDER BY adult_literacy_rate DESC
LIMIT 5""",
    ),
    (
        "2. Find countries where female youth literacy < 80%.",
        """SELECT DISTINCT country, youth_literacy_female, year
FROM literacy_rates
WHERE year = (SELECT MAX(year) FROM literacy_rates)
  AND youth_literacy_female IS NOT NULL AND youth_literacy_female < 80
ORDER BY youth_literacy_female""",
    ),
    (
        "3. Average adult literacy per continent (owid region).",
        """SELECT country AS region, AVG(adult_literacy_rate) AS avg_adult_literacy
FROM literacy_rates
WHERE adult_literacy_rate IS NOT NULL AND country NOT IN ('World', '')
GROUP BY country
ORDER BY avg_adult_literacy DESC""",
    ),
    # illiteracy_population
    (
        "4. Countries with illiteracy % > 20% in 2000.",
        """SELECT country, year, illiteracy_pct
FROM illiteracy_population
WHERE year = 2000 AND illiteracy_pct > 20
ORDER BY illiteracy_pct DESC""",
    ),
    (
        "5. Trend of illiteracy % for India (2000–2020).",
        """SELECT year, illiteracy_pct
FROM illiteracy_population
WHERE country = 'India' AND year BETWEEN 2000 AND 2020
ORDER BY year""",
    ),
    (
        "6. Top 10 countries with largest illiterate population in the last year.",
        """SELECT country, year, illiterate_population_total
FROM illiteracy_population
WHERE year = (SELECT MAX(year) FROM illiteracy_population)
  AND illiterate_population_total IS NOT NULL
ORDER BY illiterate_population_total DESC
LIMIT 10""",
    ),
    # gdp_schooling
    (
        "7. Find countries with avg_years_schooling > 7 and gdp_per_capita < 5000.",
        """SELECT country, year, avg_years_schooling, gdp_per_capita
FROM gdp_schooling
WHERE avg_years_schooling > 7 AND gdp_per_capita < 5000
ORDER BY gdp_per_capita""",
    ),
    (
        "8. Rank countries by GDP per schooling for the year 2020.",
        """SELECT country, year, gdp_per_schooling_year,
       RANK() OVER (ORDER BY gdp_per_schooling_year DESC) AS rk
FROM gdp_schooling
WHERE year = 2020 AND gdp_per_schooling_year IS NOT NULL
ORDER BY rk""",
    ),
    (
        "9. Find global average schooling years per year.",
        """SELECT year, AVG(avg_years_schooling) AS global_avg_schooling
FROM gdp_schooling
WHERE avg_years_schooling IS NOT NULL
GROUP BY year
ORDER BY year""",
    ),
    # Join Queries
    (
        "10. List top 10 countries in 2020 with highest GDP per capita but lowest average years of schooling (less than 6).",
        """SELECT g.country, g.gdp_per_capita, g.avg_years_schooling
FROM gdp_schooling g
WHERE g.year = 2020
  AND g.avg_years_schooling < 6
  AND g.avg_years_schooling IS NOT NULL AND g.gdp_per_capita IS NOT NULL
ORDER BY g.gdp_per_capita DESC
LIMIT 10""",
    ),
    (
        "11. Show countries where the illiterate population is high despite having more than 10 average years of schooling.",
        """SELECT i.country, i.year, i.illiterate_population_total, g.avg_years_schooling
FROM illiteracy_population i
JOIN gdp_schooling g ON i.country = g.country AND i.year = g.year
WHERE g.avg_years_schooling > 10 AND i.illiterate_population_total IS NOT NULL
ORDER BY i.illiterate_population_total DESC""",
    ),
    (
        "12. Compare literacy rates and GDP per capita growth for a selected country over the last 20 years. (country of your choice)",
        """SELECT l.year, l.adult_literacy_rate, g.gdp_per_capita
FROM literacy_rates l
LEFT JOIN gdp_schooling g ON l.country = g.country AND l.year = g.year
WHERE l.country = 'India'
  AND l.year >= (SELECT MAX(year) - 20 FROM literacy_rates WHERE country = 'India')
ORDER BY l.year""",
    ),
    (
        "13. Show the difference between youth literacy male and female rates for countries with GDP per capita above $30,000 in 2020.",
        """SELECT l.country,
       l.youth_literacy_male,
       l.youth_literacy_female,
       (l.youth_literacy_male - l.youth_literacy_female) AS literacy_gap,
       g.gdp_per_capita
FROM literacy_rates l
JOIN gdp_schooling g ON l.country = g.country AND l.year = g.year
WHERE l.year = 2020 AND g.gdp_per_capita > 30000
  AND l.youth_literacy_male IS NOT NULL AND l.youth_literacy_female IS NOT NULL
ORDER BY literacy_gap DESC""",
    ),
]

# Initialize DB if needed
db_path = ROOT / "data" / "literacy.db"
if not db_path.exists():
    if st.button("Initialize database from cleaned data (data/ folder)"):
        try:
            init_db_from_cleaned_data(ROOT / "data")
            st.success("Database initialized. Run your query below.")
        except Exception as e:
            st.error(str(e))
else:
    engine = get_sqlite_engine(str(db_path))
    if engine is None:
        st.error("SQLAlchemy not installed. pip install sqlalchemy")
        st.stop()

    st.markdown("### 📋 Project questions (select one below to run)")
    with st.expander("View all questions", expanded=True):
        st.markdown("**literacy_rates**")
        st.markdown("1. Get top 5 countries with highest adult literacy in 2020.")
        st.markdown("2. Find countries where female youth literacy < 80%.")
        st.markdown("3. Average adult literacy per continent (owid region).")
        st.markdown("**illiteracy_population**")
        st.markdown("4. Countries with illiteracy % > 20% in 2000.")
        st.markdown("5. Trend of illiteracy % for India (2000–2020).")
        st.markdown("6. Top 10 countries with largest illiterate population in the last year.")
        st.markdown("**gdp_schooling**")
        st.markdown("7. Find countries with avg_years_schooling > 7 and gdp_per_capita < 5000.")
        st.markdown("8. Rank countries by GDP per schooling for the year 2020.")
        st.markdown("9. Find global average schooling years per year.")
        st.markdown("**Join Queries**")
        st.markdown("10. List top 10 countries in 2020 with highest GDP per capita but lowest average years of schooling (less than 6).")
        st.markdown("11. Show countries where the illiterate population is high despite having more than 10 average years of schooling.")
        st.markdown("12. Compare literacy rates and GDP per capita growth for a selected country over the last 20 years. (country of your choice)")
        st.markdown("13. Show the difference between youth literacy male and female rates for countries with GDP per capita above $30,000 in 2020.")

    options = ["Custom query"] + [q[0] for q in QUESTIONS]
    choice = st.selectbox("Select question", options, label_visibility="collapsed")

    if choice == "Custom query":
        sql = st.text_area("SQL query", height=120, placeholder="SELECT ... FROM literacy_rates ...")
    else:
        idx = options.index(choice) - 1
        question_text, sql = QUESTIONS[idx]
        st.info(f"**Question:** {question_text}")
        sql = st.text_area("SQL (editable)", value=sql, height=140, label_visibility="collapsed")

    if st.button("Run query") and sql.strip():
        try:
            df = run_query(engine, sql)
            st.dataframe(df, use_container_width=True)
            if not df.empty and df.shape[1] >= 2:
                num_cols = df.select_dtypes(include=["number"]).columns.tolist()
                if num_cols:
                    x_col = df.columns[0] if df.columns[0] not in num_cols else num_cols[0]
                    y_col = num_cols[0] if x_col != num_cols[0] else (num_cols[1] if len(num_cols) > 1 else None)
                    if y_col and st.checkbox("Show chart"):
                        st.bar_chart(df.set_index(x_col)[[y_col]].head(20))
        except Exception as e:
            st.error(str(e))
