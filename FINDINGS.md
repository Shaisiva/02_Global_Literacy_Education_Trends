# Summary of Findings – Global Literacy & Education Trends

*(Fill in after completing EDA and running SQL queries.)*

## Data Overview
- **Sources:** Our World in Data (adult/youth literacy, illiterate population, GDP per capita, average years of schooling).
- **Scope:** Countries and years (filtered 1990–2023).
- **Cleaned outputs:** `literacy_rates`, `illiteracy_population`, `gdp_schooling`.

## Key Insights

### 1. Literacy and economic development
- *Example:* Countries with higher GDP per capita tend to have higher adult literacy rates. Outliers (e.g. high literacy, lower GDP) may reflect strong education policy with lagging economic growth.

### 2. Gender gap in youth literacy
- *Example:* Query 2 and 13 highlight countries where female youth literacy &lt; 80% or where the male–female gap is largest among high-GDP countries. These are priority regions for targeted programs.

### 3. Illiteracy and schooling
- *Example:* Query 11 shows countries with high illiterate population despite &gt; 10 years of average schooling, suggesting quality or access issues rather than years alone.

### 4. Regional and temporal trends
- *Example:* Global average adult literacy has improved over time; continental/regional breakdowns (Query 3) and country profiles show where progress is fastest or stagnant.

### 5. Business and policy use
- **Policy:** Use literacy vs GDP and illiteracy % to prioritize funding (SDG 4).
- **CSR / NGOs:** Target high illiteracy and large illiterate population (Query 6) for programs.
- **EdTech / Workforce:** Use schooling and literacy trends for market and talent forecasting.

## Limitations
- Missing or sparse data for some countries/years.
- OWID “country” may include regions/aggregates; filter to actual countries if needed for reporting.

## Recommendations
- Combine with population data to estimate absolute numbers of illiterate individuals.
- Extend with conflict/crisis years to analyze impact on literacy (project idea 10).
- Re-run EDA and SQL after refreshing data from OWID.
