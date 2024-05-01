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


# Question 1
query = """
SELECT COUNT(*) AS num_countries
FROM Country
"""
c.execute(query)
results = c.fetchall()
print_results(1, query, results)

# Question 2
query = """
SELECT COUNT(*) AS num_countries_with_life_expectancy
FROM Country
WHERE LifeExpectancy IS NOT NULL
"""
c.execute(query)
results = c.fetchall()
print_results(2, query, results)

# Question 3
query = """
SELECT COUNT(DISTINCT Continent) AS num_continents
FROM Country
"""
c.execute(query)
results = c.fetchall()
print_results(3, query, results)

# Question 4
query = """
SELECT MAX(IndepYear) AS latest_indep_year
FROM Country
WHERE IndepYear IS NOT NULL
"""
c.execute(query)
results = c.fetchall()
print_results(4, query, results)

# Question 5
query = """
SELECT AVG(LifeExpectancy) AS avg_life_expectancy
FROM Country
WHERE LifeExpectancy IS NOT NULL
"""
c.execute(query)
results = c.fetchall()
print_results(5, query, results)

# Question 6
query = """
SELECT AVG(LifeExpectancy)
FROM Country
WHERE SurfaceArea > 1000000
"""
c.execute(query)
results = c.fetchall()
print_results(6, query, results)

# Question 7
# Way 1: Using a subquery
query1 = """
SELECT Name
FROM Country
WHERE SurfaceArea = (
    SELECT MAX(SurfaceArea)
    FROM Country)
"""
c.execute(query1)
results = c.fetchall()
print_results(7, f"first way: {query1}", results)

# Way 2: Using ORDER BY and LIMIT
query2 = """
SELECT Name
FROM Country
ORDER BY SurfaceArea DESC
LIMIT 1
"""
c.execute(query2)
results = c.fetchall()
print_results(7, f"second way: {query2}", results)

# Question 8
query = """
SELECT Name
FROM Country
ORDER BY SurfaceArea ASC
LIMIT 1
"""
c.execute(query)
results = c.fetchall()
print_results(8, query, results)

# Question 9
query = """
SELECT *
FROM Country
WHERE region = (
    SELECT region
    FROM Country
    WHERE name = 'Armenia')
ORDER BY population DESC
"""
c.execute(query)
results = c.fetchall()
print_results(9, query, results)

# Question 10
query = """
SELECT *
FROM Country
WHERE population < (
    SELECT AVG(population)
    FROM Country)
ORDER BY population DESC
LIMIT 10
"""
c.execute(query)
results = c.fetchall()
print_results(10, query, results)

# Question 11
query = """
SELECT MAX(gnp) AS max_gnp, MIN(gnp) AS min_gnp
FROM Country
WHERE gnp != 0
"""
c.execute(query)
results = c.fetchall()
print_results(11, query, results)

# Question 12
query = """
SELECT 'max_gnp' AS category, gnp AS val
FROM (
    SELECT *
    FROM Country
    WHERE gnp != 0
    ORDER BY gnp DESC
    LIMIT 1) 
UNION 
SELECT 'min_gnp' AS category, gnp AS val
FROM (
    SELECT *
    FROM Country
    WHERE gnp != 0
    ORDER BY gnp ASC
    LIMIT 1)
"""
c.execute(query)
results = c.fetchall()
print_results(12, query, results)

# Question 13
query = """
SELECT *
FROM Country
WHERE Population > 5* (
    SELECT AVG(Population)
    FROM Country AS c2
    WHERE c2.Region = Country.Region
)

"""
c.execute(query)
results = c.fetchall()
print_results(13, query, results)

# Question 14
query = """
SELECT
    (SELECT Population
     FROM Country
     WHERE Name = 'Israel') AS Israel_population,
    ROUND((SELECT Population
           FROM Country
           WHERE Name = 'Israel') * 100.0 /
          (SELECT SUM(Population)
           FROM Country
           WHERE Continent = (SELECT Continent
                             FROM Country
                             WHERE Name = 'Israel')), 2) AS Percentage_of_continent
"""
c.execute(query)
results = c.fetchall()
print_results(14, query, results)

# Question 15
query = """
SELECT *
FROM City
WHERE CountryCode IN (
    SELECT Code
    FROM Country
    WHERE IndepYear < 0)
ORDER BY District, Name, CountryCode
"""
c.execute(query)
results = c.fetchall()
print_results(15, query, results)

# Question 16
query = """
SELECT DISTINCT Language
FROM CountryLanguage
WHERE CountryCode IN (
    SELECT Code
    FROM Country
    WHERE Continent = 'Europe')
"""
c.execute(query)
results = c.fetchall()
print_results(16, query, results)

# Question 17
query = """
SELECT DISTINCT Language
FROM CountryLanguage
WHERE CountryCode IN (
    SELECT Code
    FROM Country
    WHERE Continent = 'Europe') 
    AND Language IN (
    SELECT DISTINCT Language
    FROM CountryLanguage
    WHERE CountryCode IN (
        SELECT Code
        FROM Country
        WHERE Continent = 'Asia'))

"""
c.execute(query)
results = c.fetchall()
print_results(17, query, results)

# Question 18
# Way 1:Using a UNION Query
query1 = """
SELECT DISTINCT Language
FROM CountryLanguage
WHERE CountryCode IN (
    SELECT Code
    FROM Country
    WHERE Continent = 'Antarctica'
)
UNION
SELECT DISTINCT Language
FROM CountryLanguage
WHERE CountryCode IN (
    SELECT Code
    FROM Country
    WHERE Continent = 'Oceania'
)

ORDER BY Language
"""
c.execute(query1)
results = c.fetchall()
print_results(18, f"first way: {query1}", results)

# Way 2:Using a Single SELECT Statement with OR Condition
query2 = """
SELECT DISTINCT Language
FROM CountryLanguage
WHERE CountryCode IN (
    SELECT Code
    FROM Country
    WHERE Continent = 'Antarctica' OR Continent = 'Oceania'
)
ORDER BY Language
"""
c.execute(query2)
results = c.fetchall()
print_results(18, f"second way: {query2}", results)

# Question 19
# Way 1: Using LEFT JOIN
query1 = """

SELECT DISTINCT cl.Language
FROM CountryLanguage cl
LEFT JOIN Country c ON cl.CountryCode = c.Code
WHERE c.Continent != 'Europe' OR c.Continent IS NULL
ORDER BY cl.Language
"""
c.execute(query1)
results = c.fetchall()
print_results(19, f"first way: {query1}", results)

# Way 2: Using NOT IN
query2 = """
SELECT DISTINCT Language
FROM CountryLanguage
WHERE CountryCode NOT IN (
    SELECT Code
    FROM Country
    WHERE Continent = 'Europe'
)
ORDER BY Language
"""
c.execute(query2)
results = c.fetchall()
print_results(19, f"second way: {query2}", results)

# Question 20
query = """
SELECT c.Name AS Country, ci.Name AS Capital
FROM Country c
JOIN City ci ON c.Capital = ci.ID
"""
c.execute(query)
results = c.fetchall()
print_results(20, query, results)

# Question 21
query = """
SELECT c.Name AS City, c.Population AS City_Population, co.Population AS Country_Population,
       (c.Population * 100.0 / co.Population) AS Percentage
FROM City c
JOIN Country co ON c.CountryCode = co.Code
WHERE (c.Population * 100.0 / co.Population) > 10

"""
c.execute(query)
results = c.fetchall()
print_results(21, query, results)

# Question 22
query = """
SELECT Name, SurfaceArea
FROM Country
ORDER BY SurfaceArea DESC
LIMIT 1 OFFSET 3
"""
c.execute(query)
results = c.fetchall()
print_results(22, query, results)

# Question 23
query = """
SELECT
    Name,
    LifeExpectancy,
    CASE
        WHEN LifeExpectancy < 40 THEN 'LOW'
        WHEN LifeExpectancy < 70 THEN 'MED'
        ELSE 'HIGH'
    END AS Life_Expectancy_Range
FROM Country
WHERE LifeExpectancy IS NOT NULL
"""
c.execute(query)
results = c.fetchall()
print_results(23, query, results)
