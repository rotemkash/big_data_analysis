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
SELECT *
FROM City
"""
c.execute(query)
results = c.fetchall()
print_results(1, query, results)

# Question 2
query = """
SELECT *
FROM Country
"""
c.execute(query)
results = c.fetchall()
print_results(2, query, results)

# Question 3
query = """
SELECT *
FROM City
WHERE CountryCode = 'NLD'
"""
c.execute(query)
results = c.fetchall()
print_results(3, query, results)

# Question 4
query = """
SELECT *
FROM Country
WHERE Code IN ('LBR', 'IOT', 'TKL')
"""
c.execute(query)
results = c.fetchall()
print_results(4, query, results)

# Question 5
query = """
SELECT *
FROM City
WHERE Population > 4000000
"""
c.execute(query)
results = c.fetchall()
print_results(5, query, results)

# Question 6
query = """
SELECT *
FROM City
WHERE Population > 3000000 AND CountryCode = 'BRA'
"""
c.execute(query)
results = c.fetchall()
print_results(6, query, results)

# Question 7
query = """
SELECT *
FROM City
WHERE Population BETWEEN 150000 AND 170000
"""
c.execute(query)
results = c.fetchall()
print_results(7, query, results)

# Question 8
query = """
SELECT *
FROM Country
WHERE IndepYear IN (1970, 1980, 1990)
"""
c.execute(query)
results = c.fetchall()
print_results(8, query, results)

# Question 9
query = """
SELECT *
FROM Country
WHERE IndepYear = 1980 AND IndepYear = 1990
"""
c.execute(query)
results = c.fetchall()
print_results(9, query, results)

# Question 10
query = """
SELECT *
FROM Country
WHERE IndepYear BETWEEN 1980 AND 1990
"""
c.execute(query)
results = c.fetchall()
print_results(10, query, results)

# Question 11
query = """
SELECT *
FROM Country
WHERE Continent = 'Africa' AND IndepYear = 1964
"""
c.execute(query)
results = c.fetchall()
print_results(11, query, results)

# Question 12
query = """
SELECT *
FROM Country
WHERE Continent = 'Africa' OR IndepYear = 1964
"""
c.execute(query)
results = c.fetchall()
print_results(12, query, results)

# Question 13
query = """
SELECT *
FROM Country
WHERE Continent = 'Asia' 
"""
c.execute(query)
results = c.fetchall()
print_results(13, query, results)

# Question 14
query = """
SELECT *
FROM Country
WHERE Continent NOT IN('Asia')
"""
c.execute(query)
results = c.fetchall()
print_results(14, query, results)

# Question 15
query = """
SELECT *
FROM Country
WHERE Continent NOT IN('Asia', 'Europe')
"""
c.execute(query)
results = c.fetchall()
print_results(15, query, results)

# Question 16
query = """
SELECT *
FROM City
WHERE Name LIKE 'H%'
"""
c.execute(query)
results = c.fetchall()
print_results(16, query, results)

# Question 17
query = """
SELECT *
FROM City
WHERE Name NOT LIKE '%e%'
"""
c.execute(query)
results = c.fetchall()
print_results(17, query, results)

# Question 18
query = """
SELECT DISTINCT Language
FROM CountryLanguage
ORDER BY Language
"""
c.execute(query)
results = c.fetchall()
print_results(18, query, results)

# Question 19
query = """
SELECT *
FROM Country
ORDER BY IndepYear, Name  
"""
c.execute(query)
results = c.fetchall()
print_results(19, query, results)

# Question 20
query = """
SELECT *
FROM Country
ORDER BY LifeExpectancy DESC
"""
c.execute(query)
results = c.fetchall()
print_results(20, query, results)

# Question 21
query = """
SELECT Name, GNP
FROM Country
ORDER BY GNP DESC
LIMIT 10
"""
c.execute(query)
results = c.fetchall()
print_results(21, query, results)

# Question 22
query = """
SELECT Name, GNP
FROM Country
ORDER BY GNP DESC
LIMIT 10 OFFSET 10
"""
c.execute(query)
results = c.fetchall()
print_results(22, query, results)

# Question 23
query = """
SELECT Name, GNP
FROM Country
ORDER BY GNP ASC
LIMIT 10
"""
c.execute(query)
results = c.fetchall()
print_results(23, query, results)

# Question 24
query = """
SELECT Name, Continent || ' (' || Region || ')' AS ContinentAndRegion  
FROM Country
ORDER BY Name
"""
c.execute(query)
results = c.fetchall()
print_results(24, query, results)

# Question 25
query = """
SELECT Name, ROUND(Population / 1000000.0, 1) AS PopulationInMillions
FROM Country
WHERE Name LIKE 'Z%'
"""
c.execute(query)
results = c.fetchall()
print_results(25, query, results)

# Question 26
query = """
SELECT Name
FROM Country
WHERE GNP > (GNPOld * 2)
"""
c.execute(query)
results = c.fetchall()
print_results(26, query, results)

# Question 27
query = """
SELECT Name, Population / SurfaceArea AS PopulationDensity
FROM Country
ORDER BY (Population / SurfaceArea) DESC
"""
c.execute(query)
results = c.fetchall()
print_results(27, query, results)

# Question 28
query = """
SELECT Name, Population / SurfaceArea AS PopulationDensity
FROM Country
WHERE (Population / SurfaceArea) > 2000
ORDER BY Code
"""
c.execute(query)
results = c.fetchall()
print_results(28, query, results)

# Question 29
query = """
SELECT Name, Continent, SurfaceArea
FROM Country
ORDER BY Continent ASC, SurfaceArea DESC
"""
c.execute(query)
results = c.fetchall()
print_results(29, query, results)

# Question 30
query = """
SELECT *
FROM Country
WHERE Name LIKE '%N' AND LENGTH(Name) < 10
"""
c.execute(query)
results = c.fetchall()
print_results(30, query, results)

# Question 31
query = """
SELECT Name , IndepYear
FROM Country
WHERE IndepYear IS NULL
"""
c.execute(query)
results = c.fetchall()
print_results(31, query, results)

# Close the connection
conn.close()
