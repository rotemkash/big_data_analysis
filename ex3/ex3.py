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
queries = [
    """
SELECT c1.Code as Country1, c2.Code as Country2
FROM CountryLanguage cl1
JOIN CountryLanguage cl2 ON cl1.Language = cl2.Language AND cl1.CountryCode != cl2.CountryCode
JOIN Country c1 ON cl1.CountryCode = c1.Code
JOIN Country c2 ON cl2.CountryCode = c2.Code 
""",
    """
SELECT c.Name as CountryName
FROM Country c
JOIN CountryLanguage cl ON c.Code = cl.CountryCode
GROUP BY c.Code
HAVING COUNT(DISTINCT cl.Language) > 3 
""",
    """
SELECT COUNT(*) as NumOfCountries
FROM (
  SELECT c.Code
  FROM Country c
  JOIN CountryLanguage cl ON c.Code = cl.CountryCode
  GROUP BY c.Code
  HAVING COUNT(DISTINCT cl.Language) > 3
) AS temp
""",
    """
SELECT COUNT(*) 
FROM (
  SELECT CountryCode
  FROM CountryLanguage
  WHERE IsOfficial = '1'
  GROUP BY CountryCode
  HAVING COUNT(DISTINCT Language) = 1
) temp
""",
    """
SELECT COUNT(*) AS "Num of countries with official languages"
FROM Country AS c
WHERE(SELECT COUNT(*) FILTER(WHERE c.Code = cl.CountryCode AND cl.IsOfficial = 0)
      FROM CountryLanguage AS cl) = 0
""",
    """
SELECT c.Name
FROM Country c
JOIN CountryLanguage cl ON c.Code = cl.CountryCode
WHERE cl.Language = 'Hebrew'
GROUP BY c.Code, c.Name
""",
    """
SELECT c.Name as CountryName
FROM Country c
INNER JOIN CountryLanguage cl1 ON c.Code = cl1.CountryCode AND cl1.Language = 'Arabic'
INNER JOIN CountryLanguage cl2 ON c.Code = cl2.CountryCode AND cl2.Language = 'English'
GROUP BY c.Code, c.Name
""",
    """
SELECT DISTINCT c.Name
FROM Country c
JOIN CountryLanguage cl ON c.Code = cl.CountryCode
WHERE cl.Language IN ('Arabic', 'English')
GROUP BY c.Code, c.Name
""",
    """
SELECT c.Name
FROM Country c
JOIN CountryLanguage cl ON c.Code = cl.CountryCode
GROUP BY c.Code, c.Name
HAVING SUM(CASE WHEN cl.Language IN ('Arabic', 'English') THEN 0 ELSE 1 END) = 0
   AND SUM(CASE WHEN cl.Language IN ('Arabic', 'English') THEN 1 ELSE 0 END) = 2
""",
    """
SELECT c.Name
FROM Country c
JOIN CountryLanguage cl ON c.Code = cl.CountryCode
WHERE cl.Language IN ('Arabic', 'English')
GROUP BY c.Code, c.Name
HAVING SUM(CASE WHEN cl.Language = 'Arabic' THEN 1 ELSE 0 END) +
       SUM(CASE WHEN cl.Language = 'English' THEN 1 ELSE 0 END) = 1
ORDER BY c.Name 
""",
    """
SELECT c.Name
FROM Country c
WHERE c.Code NOT IN (
    SELECT CountryCode
    FROM CountryLanguage
    WHERE Language = 'English'
) 
""",
    """
SELECT c.Name
FROM Country c
INNER JOIN CountryLanguage cl1 ON c.Code = cl1.CountryCode AND cl1.Language = 'Arabic'
LEFT JOIN CountryLanguage cl2 ON c.Code = cl2.CountryCode AND cl2.Language = 'English'
WHERE cl2.CountryCode IS NULL
GROUP BY c.Code, c.Name
""",
    """
SELECT Language
FROM CountryLanguage
GROUP BY Language
HAVING COUNT(DISTINCT CountryCode) >= 2 
""",
    """
SELECT Language
FROM CountryLanguage
GROUP BY Language
HAVING COUNT(DISTINCT CountryCode) = 2
""",
    """
SELECT SUBSTR(Name, 1, 1) AS InitialLetter, COUNT(*) AS NumberOfCities
FROM City
GROUP BY InitialLetter
ORDER BY InitialLetter 
""",
    """
SELECT c.Name AS Country
FROM Country c
JOIN (
    SELECT CountryCode
    FROM CountryLanguage
    GROUP BY CountryCode
    HAVING COUNT(DISTINCT SUBSTR(Language, 1, 1)) = 1
       AND COUNT(DISTINCT Language) > 1
) cl ON c.Code = cl.CountryCode
""",
    """
SELECT 
    c.Name AS Country,
    (
        SELECT Language
        FROM CountryLanguage cl
        WHERE cl.CountryCode = c.Code
        ORDER BY Percentage DESC, Language
        LIMIT 1
    ) AS Language
FROM Country c 
""",
    """
SELECT 
    c.Name AS Country,
    GROUP_CONCAT(cl.Language) AS OfficialLanguages
FROM Country c
LEFT JOIN CountryLanguage cl ON c.Code = cl.CountryCode
WHERE cl.IsOfficial = '1'
GROUP BY c.Name
""",
    """
SELECT 
    c.Name AS Country,
    COUNT(cl.Language) AS NumberOfLanguages
FROM Country c
LEFT JOIN CountryLanguage cl ON c.Code = cl.CountryCode
GROUP BY c.Name
ORDER BY NumberOfLanguages DESC
LIMIT 3
""",
    """
SELECT 
    c.Name AS Country,
    (c.SurfaceArea / total_area.ContinentArea) * 100 AS PercentageOfContinentArea
FROM Country c
JOIN (
    SELECT 
        Continent,
        SUM(SurfaceArea) AS ContinentArea
    FROM Country
    GROUP BY Continent
) AS total_area ON c.Continent = total_area.Continent
""",
    """
SELECT AVG(num_languages) AS AverageNumberOfLanguages
FROM (
    SELECT COUNT(Language) AS num_languages
    FROM CountryLanguage
    GROUP BY CountryCode
) AS language_counts
""",
    """
SELECT
    -- (a) Number of countries that gained independence after 1950
    (SELECT COUNT(*) FROM Country WHERE IndepYear > 1950) AS CountriesAfter1950,
    
    -- (b) Average life expectancy in Africa
    (SELECT AVG(LifeExpectancy) FROM Country WHERE Continent = 'Africa') AS AvgLifeExpectancyInAfrica,
    
    -- (c) Difference between the population of the largest and smallest countries in Europe
    (SELECT MAX(Population) - MIN(Population) FROM Country WHERE Continent = 'Europe') AS PopulationDifferenceEurope
""",
    """
SELECT 
    ci.Name AS City,
    co.Name AS Country,
    GROUP_CONCAT(cl.Language) AS Languages
FROM 
    City ci
JOIN 
    Country co ON ci.CountryCode = co.Code
JOIN 
    CountryLanguage cl ON ci.CountryCode = cl.CountryCode
WHERE 
    ci.Population > 500000
GROUP BY 
    ci.ID 
""",
    """
SELECT 
    cl1.CountryCode AS Country1,
    cl2.CountryCode AS Country2
FROM 
    CountryLanguage cl1
JOIN 
    CountryLanguage cl2 ON cl1.Language = cl2.Language
WHERE 
    cl1.CountryCode < cl2.CountryCode
GROUP BY 
    cl1.CountryCode, cl2.CountryCode
HAVING 
    COUNT(DISTINCT cl1.Language) >= 2
""",
    """
SELECT 
    Name AS Country,
    GNP as GNP_orig,
    Numbers.Number AS v,
    GNP * Numbers.Number AS GNP_new
FROM 
    Country
CROSS JOIN (
    SELECT 3 AS Number
    UNION ALL
    SELECT 11 AS Number
    UNION ALL
    SELECT 20 AS Number
) AS Numbers
""",
    """
WITH AggregatedPercentages AS (
    SELECT 
        CountryCode,
        Language,
        Percentage AS percent
    FROM 
        CountryLanguage
    ORDER BY 
        CountryCode, Percentage ASC
)
SELECT 
    t1.CountryCode,
    t1.Language,
    t1.percent,
    SUM(t2.percent) AS percent_agg_sum
FROM 
    AggregatedPercentages t1
INNER JOIN 
    AggregatedPercentages t2 ON t1.CountryCode = t2.CountryCode AND t1.percent >= t2.percent
GROUP BY 
    t1.CountryCode, t1.Language, t1.percent
ORDER BY 
    t1.CountryCode, percent_agg_sum, t1.Language 
""",
    """
SELECT 
    cl.CountryCode,
    cl.Language,
    cl.Percentage
FROM 
    CountryLanguage cl
WHERE 
    cl.Percentage = (
        SELECT MAX(cl2.Percentage)
        FROM CountryLanguage cl2
        WHERE cl.CountryCode = cl2.CountryCode
    )
"""
]

# Loop through the queries and print the results
for i, query in enumerate(queries, start=1):
    c.execute(query)
    results = c.fetchall()
    print_results(i, query, results)
