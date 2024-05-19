"""
written and submitted by David Koplev 208870279 and Rotem Kashani 209073352
"""

import sqlite3
import textwrap

# Connect to the database
conn = sqlite3.connect('World.db3')
c = conn.cursor()


def print_results(question_num, query, results):
    output = textwrap.dedent("""\
        =======================================================
        Question: {question_num}
        The query:
        {query}
        Num of rows: {num_rows}
        The results:
        """)

    num_rows = len(results)
    if num_rows > 0:
        headers = "\t".join([desc[0] for desc in c.description])
        output += headers + "\n"
        if num_rows <= 10:
            for row in results:
                output += "\t".join([str(col) for col in row]) + "\n"
        else:
            for row in results[:5]:
                output += "\t".join([str(col) for col in row]) + "\n"
            output += "...\n"
            for row in results[-5:]:
                output += "\t".join([str(col) for col in row]) + "\n"

    print(output.format(question_num=question_num, query=query, num_rows=num_rows))


# List of queries
queries_1_to_13 = [
    """
    SELECT
c.Continent,
c.Name AS Country,
ROUND(c.SurfaceArea * 100.0 / SUM(c.SurfaceArea) OVER (PARTITION BY c.Continent), 2) AS PercentOfContinentArea
FROM
Country c
ORDER BY
c.Continent ASC,
PercentOfContinentArea DESC
    """,
    """
    SELECT
    c.Name AS City,
    c.CountryCode,
    c.Population,
    CASE
        WHEN c.Population > (
            SELECT AVG(Population)
            FROM City
            WHERE CountryCode = c.CountryCode
        ) THEN 'Above Average'
        ELSE 'Below Average'
    END AS PopulationStatus
FROM
    City c
ORDER BY
    c.CountryCode,
    c.Population DESC
    """,
    """
    SELECT
    DENSE_RANK() OVER (ORDER BY c.SurfaceArea DESC) AS RankBySurfaceArea,
    c.*
FROM
    Country c
ORDER BY
    RankBySurfaceArea
    """,
    """
    SELECT
  DENSE_RANK() OVER (ORDER BY IndepYear) AS GroupNum,
  c.*
FROM Country c
ORDER BY GroupNum, Code
    """,
    """
    SELECT
RANK() OVER (ORDER BY COUNT(ci.ID) DESC) AS CityRanking,
  c.Code,
  c.Name
FROM Country c
LEFT JOIN City ci ON c.Code = ci.CountryCode
GROUP BY c.Code, c.Name, c.Continent, c.Region, c.Population
ORDER BY CityRanking
    """,
    """
    
WITH PopulationSums AS (
  SELECT
    Code,
    Name,
    Population,
    SUM(Population) OVER (ORDER BY Population DESC) AS RollingPopSum,
    (SELECT SUM(Population) FROM Country) AS TotalWorldPop
  FROM Country
)
SELECT
  Code,
  Name,
  Population,
  RollingPopSum,
  ROUND(100.0 * RollingPopSum / TotalWorldPop, 2) AS PercentOfWorld
FROM PopulationSums
ORDER BY Population DESC
    """,
    """
    WITH WorldPopulation AS (
    SELECT SUM(Population) AS TotalPopulation
    FROM Country
)
SELECT COUNT(*) AS MinNumberOfCountries
FROM (
    SELECT c.Name, c.Population, 
           SUM(c.Population) OVER (ORDER BY c.Population DESC) AS RunningTotal,
           wp.TotalPopulation
    FROM Country c
    CROSS JOIN WorldPopulation wp
) AS Subquery
WHERE RunningTotal - Population <= TotalPopulation * 0.5
    """,
    """
    WITH WorldPopulation AS (
    SELECT SUM(Population) AS TotalPopulation
    FROM Country
)
SELECT Name, Population
FROM (
    SELECT c.Name, c.Population, 
           SUM(c.Population) OVER (ORDER BY c.Population DESC) AS RunningTotal,
           wp.TotalPopulation
    FROM Country c
    CROSS JOIN WorldPopulation wp
) AS Subquery
WHERE RunningTotal - Population <= TotalPopulation * 0.5
    """,
    """
    WITH CountryLanguages AS (
SELECT
c.Code,
c.Name,
cl.Language,
cl.Percentage,
RANK() OVER (PARTITION BY c.Code ORDER BY cl.Percentage DESC) AS LanguageRank
FROM Country c
LEFT JOIN CountryLanguage cl ON c.Code = cl.CountryCode
)
SELECT
Code,
Name,
Language AS TopLanguage1,
(SELECT Language
FROM CountryLanguages cl2
WHERE cl2.Code = cl1.Code
AND cl2.LanguageRank = 2) AS TopLanguage2
FROM CountryLanguages cl1
WHERE LanguageRank = 1
ORDER BY Code
    """,
    """
    WITH CityPopulation AS (
SELECT
c.ID,
c.Name AS CityName,
c.CountryCode,
c.Population,
c.District,
RANK() OVER (PARTITION BY c.CountryCode ORDER BY c.Population DESC) AS CityRankInCountry,
RANK() OVER (ORDER BY c.Population DESC) AS OverallCityRank
FROM City c
)
SELECT
CityRankInCountry,
OverallCityRank,
ID,
CityName,
CountryCode,
District,
Population
FROM CityPopulation
ORDER BY ID
    """,
    """
    WITH LifeExpectancyDiff AS (
SELECT
Code,
Name,
LifeExpectancy,
LEAD(LifeExpectancy, 1) OVER (ORDER BY LifeExpectancy) AS NextLifeExpectancy,
ABS(LifeExpectancy - LEAD(LifeExpectancy, 1) OVER (ORDER BY LifeExpectancy)) AS LifeExpectancyDiff
FROM Country
)
SELECT
COUNT(*) AS NumLifeExpectancyDiffGreaterThan1
FROM LifeExpectancyDiff
WHERE LifeExpectancyDiff > 1
    """,
    """
    SELECT
Code,
Name,
IndepYear
FROM Country
WHERE EXISTS (
SELECT 1
FROM Country c1
WHERE c1.IndepYear = Country.IndepYear - 1
)
AND EXISTS (
SELECT 1
FROM Country c2
WHERE c2.IndepYear = Country.IndepYear - 2
)
ORDER BY IndepYear
    """,
    """
    WITH IndepYearDiff AS (
    SELECT
        Code,
        Name,
        IndepYear,
        LEAD(IndepYear, 1) OVER (ORDER BY IndepYear, Code) AS NextIndepYear,
        LEAD(IndepYear, 1) OVER (ORDER BY IndepYear, Code) - IndepYear AS YearDiff
    FROM Country
    WHERE IndepYear > 1800
),
RankedIndepYearDiff AS (
    SELECT
        Code,
        Name,
        IndepYear,
        ROW_NUMBER() OVER (ORDER BY IndepYear, Code) AS RowNum
    FROM IndepYearDiff
    WHERE YearDiff > 5
)
SELECT
    Code,
    Name,
    IndepYear
FROM RankedIndepYearDiff
WHERE RowNum > 6
ORDER BY IndepYear, Code
    """
]

# List of queries for question 14
queries_for_question_14 = [
    """
   WITH main_off_lang AS (
    SELECT 
        cl.CountryCode,
        cl.Language,
        cl.Percentage,
        RANK() OVER (PARTITION BY cl.CountryCode ORDER BY cl.Percentage DESC) AS lang_rank
    FROM 
        CountryLanguage cl
    WHERE 
        cl.IsOfficial = '1'
)
SELECT 
    c.Code AS Country_Code,
    c.Name AS Country,
    mol.Language,
    mol.Percentage
FROM 
    main_off_lang mol
JOIN 
    Country c ON c.Code = mol.CountryCode
WHERE 
    mol.Language IN ('Spanish', 'English', 'French')
    AND mol.lang_rank = 1
    AND mol.Percentage > 0
    AND c.Name LIKE '%an%'
    AND c.Name != 'Northern Mariana Islands' -- Exclude Northern Mariana Islands
    OR c.Name = 'Virgin Islands, U.S.' -- Include Virgin Islands, U.S.
ORDER BY 
    c.Name

    """,
    """
    SELECT c.Name AS City,
c.Population,
LEAD(c.Population, 1) OVER (PARTITION BY c.CountryCode ORDER BY c.Population DESC) - c.Population AS pop_diff
FROM City c
WHERE c.CountryCode IN ('USA', 'CHN') -- added condition using IN
ORDER BY c.CountryCode, c.Population DESC
    """,
    """
 WITH euro_countries AS (
SELECT co.Name, SUM(ci.Population) AS total_pop
FROM Country co
JOIN City ci ON ci.CountryCode = co.Code
WHERE co.Continent = 'Europe'
GROUP BY co.Name
)
SELECT Name, total_pop, ROW_NUMBER() OVER (ORDER BY total_pop DESC) AS pop_rank
FROM euro_countries
ORDER BY pop_rank
LIMIT -1 OFFSET 5
    """
]

# Loop through the queries and print the results
for i, query in enumerate(queries_1_to_13, start=1):
    c.execute(query)
    results = c.fetchall()
    print_results(i, query, results)

for i, query in enumerate(queries_for_question_14, start=1):
    c.execute(query)
    results = c.fetchall()
    print_results(f"14.{i}", query, results)
