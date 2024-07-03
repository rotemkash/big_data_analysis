"""written and submitted by David Koplev 208870279 and Rotem Kashani 209073352"""

import duckdb
import pandas as pd
import sqlite3

# Define the name to our CSV file
csv_file_name = 'price_paid_records.csv'


# Connect to DuckDB
con = duckdb.connect()

# Create the table and load data from the CSV file
con.execute("""
    CREATE TABLE price_paid_records AS 
    SELECT * FROM read_csv_auto(?, 
        types={
            'Transaction unique identifier': 'VARCHAR',
            'Price': 'INTEGER',
            'Date of Transfer': 'DATE',
            'Property Type': 'VARCHAR',
            'Old/New': 'VARCHAR',
            'Duration': 'VARCHAR',
            'Town/City': 'VARCHAR',
            'District': 'VARCHAR',
            'County': 'VARCHAR',
            'PPDCategory Type': 'VARCHAR',
            'Record Status - monthly file only': 'VARCHAR'
        }
    )
    """, [csv_file_name])

# Function to execute DuckDB query and return as pandas DataFrame
def duckdb_to_pandas(query):
    return con.execute(query).df()


# Transactions by month
transactions_by_month = duckdb_to_pandas('''
    SELECT DISTINCT
        strftime('%m', "Date of Transfer") AS Month,
        COUNT(*) OVER (PARTITION BY strftime('%m', "Date of Transfer")) AS Transactions
    FROM price_paid_records
    ORDER BY Month ASC
''')


# Average price by property type and new/old status
avg_price_by_type_status = duckdb_to_pandas('''
    SELECT DISTINCT
        "Property Type", 
        "Old/New", 
        AVG(Price) OVER (PARTITION BY "Property Type", "Old/New") AS AvgPrice 
    FROM price_paid_records
    ORDER BY "Property Type", "Old/New"
''')

# Average price by year
avg_price_by_year = duckdb_to_pandas('''
    SELECT DISTINCT
        strftime('%Y', "Date of Transfer") AS Year, 
        AVG(Price) OVER (PARTITION BY strftime('%Y', "Date of Transfer")) AS AvgPrice 
    FROM price_paid_records
    ORDER BY Year ASC
''')


# Cities with the highest increase in average property price between 1995 and 2017
top_cities_price_increase = duckdb_to_pandas('''
    WITH avg_price_per_city AS (
        SELECT DISTINCT "Town/City", strftime('%Y', "Date of Transfer") AS Year, AVG(Price) OVER (PARTITION BY "Town/City", strftime('%Y', "Date of Transfer")) AS AvgPrice
        FROM price_paid_records
    )
    SELECT a."Town/City", 
           a.AvgPrice AS AvgPrice_1995, 
           b.AvgPrice AS AvgPrice_2017, 
           (b.AvgPrice - a.AvgPrice) AS PriceIncrease
    FROM avg_price_per_city a
    JOIN avg_price_per_city b ON a."Town/City" = b."Town/City"
    WHERE a.Year = '1995' AND b.Year = '2017'
    ORDER BY PriceIncrease DESC
    LIMIT 10
''')


# Identifying periods with sharp increases or decreases in property prices
price_changes = duckdb_to_pandas('''
    WITH monthly_prices AS (
        SELECT 
            strftime('%Y-%m', "Date of Transfer") AS YearMonth, 
            AVG(Price) AS AvgPrice
        FROM price_paid_records
        GROUP BY YearMonth
    ),
    price_changes AS (
        SELECT 
            YearMonth, 
            AvgPrice, 
            LAG(AvgPrice) OVER (ORDER BY YearMonth) AS PrevAvgPrice
        FROM monthly_prices
    )
    SELECT 
        YearMonth, 
        AvgPrice, 
        PrevAvgPrice, 
        (AvgPrice - PrevAvgPrice) AS PriceChange,
        (AvgPrice - PrevAvgPrice) / PrevAvgPrice * 100 AS PriceChangePercent
    FROM price_changes
    WHERE PrevAvgPrice IS NOT NULL
    ORDER BY ABS(PriceChangePercent) DESC
    LIMIT 10
''')

# Average property price by property type and county
avg_price_by_type_county = duckdb_to_pandas('''
    SELECT DISTINCT
        "County", 
        "Property Type", 
        AVG(Price) OVER (PARTITION BY "County", "Property Type") AS AvgPrice 
    FROM price_paid_records
    ORDER BY "County" ASC
''')


# Close the DuckDB connection
con.close()

# Connect to SQLite
sqlite_conn = sqlite3.connect('price_paid_records.db')

# Write DataFrames to SQLite
transactions_by_month.to_sql('transactions_by_month', sqlite_conn, if_exists='replace', index=False)
avg_price_by_type_status.to_sql('avg_price_by_type_status', sqlite_conn, if_exists='replace', index=False)
avg_price_by_year.to_sql('avg_price_by_year', sqlite_conn, if_exists='replace', index=False)
top_cities_price_increase.to_sql('top_cities_price_increase', sqlite_conn, if_exists='replace', index=False)
price_changes.to_sql('price_changes', sqlite_conn, if_exists='replace', index=False)
avg_price_by_type_county.to_sql('avg_price_by_type_county', sqlite_conn, if_exists='replace', index=False)


# Close the SQLite connection
sqlite_conn.close()
