-- Global Literacy & Education Trends
-- Table definitions with composite key (country, year)

-- 1. Literacy rates (adult + youth male/female, optional engineered columns)
DROP TABLE IF EXISTS literacy_rates;
CREATE TABLE literacy_rates (
    country         VARCHAR(100) NOT NULL,
    year            SMALLINT NOT NULL,
    code            VARCHAR(10),
    adult_literacy_rate     DECIMAL(6,2),
    youth_literacy_male     DECIMAL(6,2),
    youth_literacy_female   DECIMAL(6,2),
    illiteracy_pct          DECIMAL(6,2),
    literacy_gender_gap     DECIMAL(6,2),
    youth_literacy_avg      DECIMAL(6,2),
    literacy_growth_rate    DECIMAL(8,2),
    PRIMARY KEY (country, year)
);

-- 2. Illiteracy population (total, male, female; optional illiteracy_pct)
DROP TABLE IF EXISTS illiteracy_population;
CREATE TABLE illiteracy_population (
    country                      VARCHAR(100) NOT NULL,
    year                         SMALLINT NOT NULL,
    code                         VARCHAR(10),
    illiterate_population_total  BIGINT,
    illiterate_population_male   BIGINT,
    illiterate_population_female BIGINT,
    literate_population_total    BIGINT,
    illiteracy_pct               DECIMAL(6,2),
    PRIMARY KEY (country, year)
);

-- 3. GDP per capita & average years of schooling
DROP TABLE IF EXISTS gdp_schooling;
CREATE TABLE gdp_schooling (
    country                 VARCHAR(100) NOT NULL,
    year                    SMALLINT NOT NULL,
    code                    VARCHAR(10),
    gdp_per_capita          DECIMAL(14,2),
    avg_years_schooling     DECIMAL(5,2),
    gdp_per_schooling_year  DECIMAL(14,2),
    education_index         DECIMAL(5,3),
    PRIMARY KEY (country, year)
);
