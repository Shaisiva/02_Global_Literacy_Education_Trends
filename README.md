# 02_Global_Literacy_Education_Trends
Project 02 - Global Literacy &amp; Education Trends - AIML

# 📊 Global Literacy & Education Trends: An Analytical Study

**Domain:** Education Analytics & Socio-Economic Data Analysis

## Skills Takeaway
- Data Collection & Cleaning
- Exploratory Data Analysis (EDA)
- Feature Engineering
- SQL Database Design & Query Writing
- Power BI / Streamlit Dashboard Development
- Data Storytelling & Insight Presentation

## Problem Statement
Literacy rates are a vital measure of a country's human development, economic growth, and educational outreach. This project analyzes adult literacy, youth literacy, illiteracy population, GDP, and years of schooling data across countries and years to uncover patterns, correlations, and disparities in education globally.

---

## Project Structure

```
Project_02/
├── data/                    # Raw & cleaned CSVs (save after Colab download)
├── notebooks/                # Jupyter notebooks
│   ├── 01_data_collection_colab.ipynb   # Run in Google Colab
│   └── 02_eda_visualizations.ipynb      # EDA & insights
├── sql/                     # SQL scripts
│   ├── 01_create_tables.sql
│   ├── 02_insert_data.sql   # Generated from cleaned data
│   └── 03_queries.sql      # 13 analytical queries
├── src/                     # Python modules
│   ├── data_cleaning.py     # Load, clean, merge, feature engineering
│   └── db_utils.py          # SQLite/MySQL helpers for Streamlit
├── streamlit_app/           # Multi-page Streamlit app
│   ├── app.py               # Entry point
│   ├── pages/
│   │   ├── 1_SQL_Executor.py
│   │   ├── 2_EDA_Visualizations.py
│   │   └── 3_Country_Profile.py
│   └── utils/
├── requirements.txt
└── README.md
```

---

## Workflow

### 1️⃣ Data Collection (Google Colab)
Run `notebooks/01_data_collection_colab.ipynb` in **Google Colab** to download OWID CSVs (external URLs may be blocked in local IDEs). Upload the downloaded CSVs to `data/` or load them in the cleaning step.

### 2️⃣ Data Cleaning & Feature Engineering
Use `src/data_cleaning.py` to:
- Merge datasets (df_literacy, df_illiteracy, df_gdp_schooling)
- Handle missing values, duplicates, standardize country names
- Filter years 1990–2023, rename columns
- Create features: Illiteracy %, Literacy Gender Gap, GDP per Schooling Year, Education Index, Youth Literacy Average, Literacy Growth Rate

### 3️⃣ EDA
Run `notebooks/02_eda_visualizations.ipynb` for univariate/bivariate analysis and visualizations.

### 4️⃣ SQL
- Create tables: `literacy_rates`, `illiteracy_population`, `gdp_schooling` with composite key `(country, year)`.
- Run `sql/01_create_tables.sql`, insert data, then execute `sql/03_queries.sql`.

### 5️⃣ Streamlit App
```bash
streamlit run streamlit_app/app.py
```
- **SQL Query Executor** – Run queries and view tables/charts.
- **EDA Visualizations** – Pre-built charts.
- **Country Profile** – Select country and view indicators over time.

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app (after data is in data/ and DB is set up)
cd streamlit_app && streamlit run app.py
```

---

## Data Sources (Our World in Data)
- Adult Literacy Rate  
- Youth Literacy (Male, Female)  
- Illiterate Population (Total, Male, Female)  
- GDP per Capita  
- Average Years of Schooling  

---

## Technical Tags
Python, Pandas, NumPy, Matplotlib, Seaborn, SQL, MySQL, Data Cleaning, EDA, Streamlit, Data Visualization, Feature Engineering, Education Analytics, Socio-Economic Analysis

