"""written and submitted by David Koplev 208870279 and Rotem Kashani 209073352"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import numpy as np
import plotly.graph_objects as go

def main():
    """
    Main function to run the Streamlit dashboard.
    """
    st.set_page_config(page_title="Price Paid Records Dashboard")

    # Load data from SQLite database
    conn = sqlite3.connect('price_paid_records.db')

    # Create sidebar for navigation
    pages = {
        "Questions": questions_page,
        "Story and Insights": story_page,
        "Sample Rows": lambda: sample_rows_page(conn),
        "Transactions by Month": lambda: transactions_by_month_page(conn),
        "Average Price by Type and Status": lambda: avg_price_by_type_status_page(conn),
        "Average Price by Year": lambda: avg_price_by_year_page(conn),
        "Price Changes": lambda: price_changes_page(conn),
        "Interactive Average Price by Type and County": lambda: interactive_avg_price_by_type_county_page(conn),
        "Interactive Average Price by Year": lambda: interactive_avg_price_by_year_page(conn),
        "Fake Property Analysis": lambda: fake_property_analysis_page(conn),
    }

    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Call the selected page function
    pages[selection]()
    conn.close()


def questions_page():
    """
    Renders the Questions page with a list of questions related to the dataset.
    """
    st.header("Questions")
    st.write("""
     1. In which months are the most transactions made?
    2. What is the difference in average price between a new property and an old property for each property type?
    3. How does the average property price change over the years?
    4. Which periods were characterized by a sharp increase or decrease in property prices?
    5. Which cities had the highest increase in average property price between two different time periods?
    6. What are the average property prices by property type in different counties or cities?
    
    Question about the fake data:
     What are the top 10 counties with the highest average property prices for each year?
    """)


def story_page():
    """
    Renders the Story and Insights page with an overview of the analysis and its findings.
    """
    st.header("Story and Insights")
    st.write("""
    ### Introduction
    The real estate market in England and Wales underwent significant changes between 1995 and 2017. By using data collected from the house price database, we can examine key trends, price changes, and the impact of various factors on the real estate market.

    ### Early Years (1995-2000)
    At the beginning of this period, real estate prices were relatively stable. During these years:
    - The British economy was recovering from the early 90s recession.
    - Housing prices increased slowly, with a moderate rise of about 2% per year.
    - Demand for properties was stable, and the market did not experience significant fluctuations.

    ### The Bubble and Price Rise (2001-2007)
    These years were characterized by a sharp increase in real estate prices:
    - Banks offered low-interest mortgages, which increased demand for properties.
    - Housing prices rose at an average annual rate of about 10%.
    - Demand for properties in city centers increased, while demand in the suburbs declined.
    - Investors saw real estate as a profitable investment, which increased the number of transactions.

    ### Economic Crisis and Price Drop (2008-2009)
    The global financial crisis in 2008 had a dramatic impact on the real estate market:
    - Real estate prices fell by an average of 15% between 2008 and 2009.
    - The number of transactions dropped sharply, and demand for properties decreased.
    - Banks tightened mortgage conditions, making it harder for potential buyers.

    ### Recovery and Stability (2010-2017)
    After the crisis, the real estate market gradually recovered:
    - Between 2010 and 2013, prices rose moderately by about 3% per year.
    - From 2014 to 2017, prices increased more rapidly, especially in large cities like London.
    - The market stabilized and became more balanced, with moderate price increases and relatively stable transaction numbers.

    ### Analysis by Property Types and Locations
    **Property Types:**
    - Detached houses were the most expensive properties, with sharp price increases during the period.
    - Flats experienced more moderate price increases but became particularly popular in large cities.

    **Locations:**
    - London and its surroundings saw the sharpest price increases, especially after the economic crisis.
    - In rural areas, prices remained more stable throughout the period.

    ### Additional Insights
    1. We may see seasonal patterns in transaction activity, with peaks in certain months and lows in others.
    2. There may be significant differences in average prices between new and old properties, depending on the property type.
    3. We can identify trends of price increases or decreases over the years and link them to economic conditions or other factors.
    4. We can identify specific periods with unusual price fluctuations and try to understand the factors that led to them.
    5. We can identify cities or regions that were "hot spots" with sharp increases in real estate prices, indicating potential future investment opportunities in these areas.
    6. We can compare average prices by property type and geographical location to identify areas or property types that offer better or worse value.
    """)


def sample_rows_page(conn):
    """
    Renders the Sample Rows page with sample rows from all the tables.
    """
    st.header("Sample Rows")
    st.write("This page displays sample rows from all the tables in the database.")

    # Transactions by Month
    st.subheader("Transactions by Month")
    df = pd.read_sql("SELECT * FROM transactions_by_month LIMIT 50", conn)
    st.write("""
        This table shows a sample of transactions by month, indicating the number of transactions recorded for each month in the dataset. It helps us understand the seasonal patterns and peaks in transaction volumes throughout the year.
        """)
    st.dataframe(df.style.highlight_max(axis=0))

    # Average Price by Type and Status
    st.subheader("Average Price by Type and Status")
    df = pd.read_sql("SELECT * FROM avg_price_by_type_status LIMIT 50", conn)
    st.write("""
        This table shows a sample of average property prices categorized by property type and new/old status. It helps us understand the underlying data used to generate the visualization above.
        """)
    st.dataframe(df.style.highlight_max(axis=0))

    # Average Price by Year
    st.subheader("Average Price by Year")
    df = pd.read_sql("SELECT * FROM avg_price_by_year LIMIT 50", conn)
    st.write("""
        This table shows a sample of average property prices by year. It provides insight into the historical data used to create the visualization above.
        """)
    st.dataframe(df.style.highlight_max(axis=0))

    # Price Changes
    st.subheader("Price Changes")
    df = pd.read_sql("SELECT * FROM price_changes LIMIT 50", conn)
    st.write("""
        This table shows a sample of periods with sharp changes in property prices. It provides context to the visualization above, highlighting the underlying data.
        """)
    st.dataframe(df.style.highlight_max(axis=0))

    # Cities with the highest increase in average property price between 1995 and 2017
    st.subheader("Top Cities with Highest Price Increase (1995 - 2017)")
    df = pd.read_sql("SELECT * FROM top_cities_price_increase LIMIT 50", conn)
    st.write("""
        This table shows the cities that experienced the highest increase in average property prices between 1995 and 2017. It helps identify regions or areas that have seen significant growth in real estate prices over this period, potentially indicating investment opportunities.
    """)
    st.dataframe(df.style.highlight_max(axis=0))

    # Average property price by property type and county
    st.subheader("Average Price by Property Type and County")
    df = pd.read_sql("SELECT * FROM avg_price_by_type_county LIMIT 50", conn)
    st.write("""
        This table displays the average property prices categorized by property type and county. It allows for comparing real estate prices across different regions and property types, which can assist in evaluating property values and making informed buying or selling decisions.
    """)
    st.dataframe(df.style.highlight_max(axis=0))

    # Add sample rows from fake_property_analysis.db
    st.subheader("Fake Property Analysis Results")
    df = pd.read_sql("SELECT * FROM top_counties_by_year LIMIT 50", conn)
    st.write("""
           This table displays the results of the analysis performed on the synthetic property data using PySpark. It shows aggregated information about property prices by type and location.
       """)
    st.dataframe(df.style.highlight_max(axis=0))


def transactions_by_month_page(conn):
    """
    Renders the Transactions by Month page with a bar chart showing the number of transactions for each month.
    """
    st.header("Transactions by Month")
    st.write("""
    This chart displays the number of property transactions recorded for each month. It helps us understand the seasonal trends in property transactions throughout the year.
    """)
    transactions_by_month = pd.read_sql("SELECT * FROM transactions_by_month", conn)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(transactions_by_month["Month"], transactions_by_month["Transactions"])
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Transactions")
    ax.set_title("Transactions by Month")
    ax.set_xticks(transactions_by_month["Month"])
    ax.set_xticklabels(transactions_by_month["Month"], rotation=45, ha='right')
    st.pyplot(fig)


def avg_price_by_type_status_page(conn):
    """
    Renders the Average Price by Property Type and New/Old Status page with a bar chart showing the average price by property type and new/old status.
    """
    st.header("Average Price by Property Type and New/Old Status")
    st.write("""
    This chart visualizes the average property prices categorized by property type (e.g., apartment, house) and whether the property is new or old. It helps us compare price differences based on property type.
    """)
    avg_price_by_type_status = pd.read_sql("SELECT * FROM avg_price_by_type_status", conn)
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot_data = pd.pivot_table(avg_price_by_type_status, values="AvgPrice", index=["Property Type"],
                                columns=["Old/New"], aggfunc=np.mean)
    pivot_data.plot(kind="bar", ax=ax)
    ax.set_xlabel("Property Type")
    ax.set_ylabel("Average Price")
    ax.legend(title="Old/New")
    ax.set_xticklabels(pivot_data.index, rotation=45, ha='right')
    st.pyplot(fig)


def avg_price_by_year_page(conn):
    """
    Renders the Average Price by Year page with a line chart showing the average price by year.
    """
    st.header("Average Price by Year")
    st.write("""
    This chart presents the average property prices over the years. It helps us observe trends and changes in property prices across different years.
    """)
    avg_price_by_year = pd.read_sql("SELECT * FROM avg_price_by_year", conn)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(avg_price_by_year["Year"], avg_price_by_year["AvgPrice"])
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Price")
    ax.set_title("Average Price by Year")

    # Rotate x-axis labels
    ax.set_xticks(avg_price_by_year["Year"])
    ax.set_xticklabels(avg_price_by_year["Year"], rotation=45, ha='right')

    st.pyplot(fig)


def price_changes_page(conn):
    """
    Renders the Periods with Sharp Price Changes page with a bar chart showing periods with sharp price changes.
    """
    st.header("Periods with Sharp Price Changes")
    st.write("""
    This chart visualizes periods with sharp changes in property prices. It helps identify time periods characterized by significant price fluctuations.
    """)
    price_changes = pd.read_sql("SELECT * FROM price_changes", conn)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(price_changes["YearMonth"], price_changes["PriceChangePercent"])
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Price Change Percentage")
    ax.set_title("Periods with Sharp Price Changes")

    # Rotate x-axis labels
    ax.set_xticks(price_changes["YearMonth"])
    ax.set_xticklabels(price_changes["YearMonth"], rotation=45, ha='right')

    st.pyplot(fig)


def interactive_avg_price_by_type_county_page(conn):
    """
    Renders an interactive bar chart displaying the average property prices by property type and county.
    The user can select a property type and multiple counties. The chart shows the average price for the selected
    property type and counties, allowing users to identify higher or lower average prices across different counties.
    """
    # Fetch data from the database
    avg_price_by_type_county = pd.read_sql("SELECT * FROM avg_price_by_type_county", conn)

    st.header("Average Price by Property Type and County")

    # Add documentation and explanations
    st.write("""
        This page allows you to explore the average property prices across different counties and property types. You can select a single property type and multiple counties from the dropdown menus.

        The bar chart will display the average price for the selected property type and counties. Use the interactive chart to identify counties with higher or lower average prices for your selected property type.
    """)

    # Get unique property types and their full names
    property_type_names = {
        "D": "Detached",
        "S": "Semi-Detached",
        "T": "Terraced",
        "F": "Flats",
        "O": "Other"
    }

    property_types = avg_price_by_type_county["Property Type"].unique()
    property_type_choices = [f"{property_type_names.get(pt, 'Unknown')} ({pt})" for pt in property_types]

    # Allow selecting a single property type
    selected_property_type = st.selectbox("Select Property Type", property_type_choices)

    # Get selected property type code
    selected_property_type_code = selected_property_type.split("(")[1][:-1]

    # Allow selecting specific counties
    selected_counties = st.multiselect("Select Counties", avg_price_by_type_county["County"].unique())

    # Filter data based on selected property type and counties
    filtered_data = avg_price_by_type_county[
        (avg_price_by_type_county["Property Type"] == selected_property_type_code) &
        (avg_price_by_type_county["County"].isin(selected_counties))
    ]

    # Calculate average price for each selected county
    avg_prices = [filtered_data[filtered_data["County"] == county]["AvgPrice"].mean() for county in selected_counties]

    # Create the bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=selected_counties,
        y=avg_prices,
        marker=dict(color='indianred'),
        name=property_type_names.get(selected_property_type_code, 'Unknown')
    ))

    fig.update_layout(
        title=f'Average Price by County for {property_type_names.get(selected_property_type_code, "Unknown")} ({selected_property_type_code})',
        xaxis_title='County',
        yaxis_title='Average Price',
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)


def interactive_avg_price_by_year_page(conn):
    """
    Renders an interactive page with a line chart showing the average price by year.
    The user can select a range of years using a slider, and the chart will update accordingly.
    """
    st.header("Interactive Average Price by Year")
    st.write("""
    This chart presents the average property prices over the years. Use the slider below to select a range of years to visualize the average price trend.
    """)
    avg_price_by_year = pd.read_sql("SELECT * FROM avg_price_by_year", conn)

    # Convert the 'Year' column to numeric values
    avg_price_by_year["Year"] = pd.to_numeric(avg_price_by_year["Year"], errors='coerce')

    # Create a slider to select the range of years
    min_year = int(avg_price_by_year["Year"].min())
    max_year = int(avg_price_by_year["Year"].max())
    year_range = st.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    # Filter the data based on the selected year range
    filtered_data = avg_price_by_year[(avg_price_by_year["Year"] >= year_range[0]) & (avg_price_by_year["Year"] <= year_range[1])]

    # Create the line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_data["Year"], filtered_data["AvgPrice"])
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Price")
    ax.set_title(f"Average Price by Year ({year_range[0]} - {year_range[1]})")

    # Rotate x-axis labels
    ax.set_xticks(filtered_data["Year"])
    ax.set_xticklabels(filtered_data["Year"], rotation=45, ha='right')

    st.pyplot(fig)

def fake_property_analysis_page(conn):
    """
    Renders a graph displaying data from top_counties_by_year table.
    """
    st.header("Fake Property Analysis")

    st.write("""
        This page displays an analysis of synthetic property data, focusing on the top counties by average property prices for each year.
    """)

    # Fetch data from the database
    df = pd.read_sql("SELECT * FROM top_counties_by_year", conn)

    # Multi-choice selection for years
    years = df['year'].unique()
    selected_years = st.multiselect("Select Years", years)

    # Filter data for the selected years
    selected_data = df[df['year'].isin(selected_years)]

    # Get all unique countries from the selected data
    all_countries = set()
    for county_data in selected_data['top_counties']:
        county_list = eval(county_data)
        for entry in county_list:
            all_countries.add(entry['county'])
    all_countries = sorted(all_countries)  # Sort alphabetically

    # Multi-choice selection for counties
    selected_countries = st.multiselect("Select Counties", all_countries)

    # Prepare data for plotting
    avg_prices_per_year = []

    for year in selected_years:
        year_data = selected_data[selected_data['year'] == year]
        county_list_str = year_data.iloc[0]['top_counties']
        county_list = eval(county_list_str)

        county_avg = {entry['county']: entry['avg_price'] for entry in county_list if entry['county'] in selected_countries}

        for country in selected_countries:
            if country not in county_avg:
                county_avg[country] = np.nan  # Insert NaN for countries with no data

        avg_prices_per_year.append([county_avg[country] for country in selected_countries])

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))

    # Calculate bar width based on number of selected years
    if len(selected_years) > 0:
        bar_width = 0.8 / len(selected_years)
    else:
        bar_width = 0.8  # Default width if no years are selected

    index = np.arange(len(selected_countries))

    for i, year in enumerate(selected_years):
        bar_position = index + i * bar_width
        ax.bar(bar_position, avg_prices_per_year[i], bar_width, label=str(year))

    ax.set_xlabel("County")
    ax.set_ylabel("Average Price")
    ax.set_title("Top Counties by Average Price")

    # Set x-axis ticks and labels for all selected countries
    ax.set_xticks(index)
    ax.set_xticklabels(selected_countries, rotation=45, ha='right')

    # Display legend for years
    ax.legend()

    # Display the plot using Streamlit
    st.pyplot(fig)


if __name__ == "__main__":
    main()
