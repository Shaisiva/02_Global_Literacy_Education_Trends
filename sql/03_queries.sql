-- Global Literacy & Education Trends – Analytical SQL Queries

-- ========== literacy_rates ==========
-- 1. Top 5 countries with highest adult literacy in 2020
SELECT country, year, adult_literacy_rate
FROM literacy_rates
WHERE year = 2020
  AND adult_literacy_rate IS NOT NULL
ORDER BY adult_literacy_rate DESC
LIMIT 5;

-- 2. Countries where female youth literacy < 80%
SELECT DISTINCT country, youth_literacy_female, year
FROM literacy_rates
WHERE year = (SELECT MAX(year) FROM literacy_rates)
  AND youth_literacy_female IS NOT NULL
  AND youth_literacy_female < 80
ORDER BY youth_literacy_female;

-- 3. Average adult literacy per continent (owid region) – assumes 'country' holds region names like "Africa" or use Code for continent
SELECT country AS region, AVG(adult_literacy_rate) AS avg_adult_literacy
FROM literacy_rates
WHERE adult_literacy_rate IS NOT NULL
  AND country NOT IN ('World', '')
GROUP BY country
ORDER BY avg_adult_literacy DESC;

-- ========== illiteracy_population ==========
-- 4. Countries with illiteracy % > 20% in 2000
SELECT country, year, illiteracy_pct
FROM illiteracy_population
WHERE year = 2000
  AND illiteracy_pct > 20
ORDER BY illiteracy_pct DESC;

-- 5. Trend of illiteracy % for India (2000–2020)
SELECT year, illiteracy_pct
FROM illiteracy_population
WHERE country = 'India'
  AND year BETWEEN 2000 AND 2020
ORDER BY year;

-- 6. Top 10 countries with largest illiterate population in the last year
SELECT country, year, illiterate_population_total
FROM illiteracy_population
WHERE year = (SELECT MAX(year) FROM illiteracy_population)
  AND illiterate_population_total IS NOT NULL
ORDER BY illiterate_population_total DESC
LIMIT 10;

-- ========== gdp_schooling ==========
-- 7. Countries with avg_years_schooling > 7 and gdp_per_capita < 5000
SELECT country, year, avg_years_schooling, gdp_per_capita
FROM gdp_schooling
WHERE avg_years_schooling > 7
  AND gdp_per_capita < 5000
ORDER BY gdp_per_capita;

-- 8. Rank countries by GDP per schooling for the year 2020
SELECT country, year, gdp_per_schooling_year,
       RANK() OVER (ORDER BY gdp_per_schooling_year DESC) AS rk
FROM gdp_schooling
WHERE year = 2020
  AND gdp_per_schooling_year IS NOT NULL
ORDER BY rk;

-- 9. Global average schooling years per year
SELECT year, AVG(avg_years_schooling) AS global_avg_schooling
FROM gdp_schooling
WHERE avg_years_schooling IS NOT NULL
GROUP BY year
ORDER BY year;

-- ========== Join Queries ==========
-- 10. Top 10 countries in 2020 with highest GDP per capita but lowest average years of schooling (less than 6)
SELECT g.country, g.gdp_per_capita, g.avg_years_schooling
FROM gdp_schooling g
WHERE g.year = 2020
  AND g.avg_years_schooling < 6
  AND g.avg_years_schooling IS NOT NULL
  AND g.gdp_per_capita IS NOT NULL
ORDER BY g.gdp_per_capita DESC
LIMIT 10;

-- 11. Countries where illiterate population is high despite > 10 avg years of schooling
SELECT i.country, i.year, i.illiterate_population_total, g.avg_years_schooling
FROM illiteracy_population i
JOIN gdp_schooling g ON i.country = g.country AND i.year = g.year
WHERE g.avg_years_schooling > 10
  AND i.illiterate_population_total IS NOT NULL
ORDER BY i.illiterate_population_total DESC;

-- 12. Compare literacy rates and GDP per capita growth for a selected country over the last 20 years (India)
SELECT l.year, l.adult_literacy_rate, g.gdp_per_capita
FROM literacy_rates l
LEFT JOIN gdp_schooling g ON l.country = g.country AND l.year = g.year
WHERE l.country = 'India'
  AND l.year >= (SELECT MAX(year) - 20 FROM literacy_rates WHERE country = 'India')
ORDER BY l.year;

-- 13. Difference between youth literacy male and female for countries with GDP per capita above $30,000 in 2020
SELECT l.country,
       l.youth_literacy_male,
       l.youth_literacy_female,
       (l.youth_literacy_male - l.youth_literacy_female) AS literacy_gap,
       g.gdp_per_capita
FROM literacy_rates l
JOIN gdp_schooling g ON l.country = g.country AND l.year = g.year
WHERE l.year = 2020
  AND g.gdp_per_capita > 30000
  AND l.youth_literacy_male IS NOT NULL
  AND l.youth_literacy_female IS NOT NULL
ORDER BY literacy_gap DESC;
