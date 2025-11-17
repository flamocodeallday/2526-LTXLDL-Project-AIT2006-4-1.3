import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Analyze one month
    # Count the number of trips on each day of the week.
    # Barchart with 7 days of week
    day_map = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    weekday_counts = df['pickup_day_of_week'].value_counts().reindex(day_map)

    fig1 = plt.figure(figsize=(10, 6))
    sns.barplot(x=weekday_counts.index, y=weekday_counts.values, palette="viridis", order=day_map)
    plt.title('Trip per week')
    plt.xlabel('Day of week')
    plt.ylabel('Total amount of trip')

    # Count the number of uses of payment types
    # Piechart with 7 type of payment
    payment_map = {0: 'Flex Fare trip', 1: 'Credit card', 2: 'Cash', 3: 'No charge', 4: 'Dispute', 5: 'Unknown', 6: 'Voided trip'}

    df['payment_type_mapped'] = df['payment_type'].map(payment_map)
    payment_counts = df['payment_type_mapped'].value_counts()

    fig2 = plt.figure(figsize=(10, 6))

    plt.pie(payment_counts.values, labels=None, autopct=None, startangle=90, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})

    plt.title("Distribution of Payment type", fontsize=18)

    plt.legend(payment_counts.index, title="Payment type", loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=4)

    plt.tight_layout()

    # Calculate revenue per day of the month.
    # LinePlot
    revenue_per_day = df.groupby(df['tpep_pickup_datetime'].dt.day)['total_amount'].sum()

    fig3 = plt.figure(figsize=(10, 6))
    plt.plot(revenue_per_day.index.astype(str), revenue_per_day.values, marker='o')
    plt.title('Revenue per day in month')
    plt.xlabel('Day of month')
    plt.ylabel('Total Revenue')
    plt.grid()
    plt.tight_layout()


    # Number of trips for each number of guests
    # Barchart
    trip_count_per_passenger_count = df['passenger_count'].value_counts()

    fig4 = plt.figure(figsize=(10, 6))
    sns.barplot(x=trip_count_per_passenger_count.index, y=trip_count_per_passenger_count.values, palette="viridis")
    plt.title('Trip per passanger amount')
    plt.xlabel('Passanger amount')
    plt.ylabel('Total amount of trip')

    # Number of trips per LocationId 
    # Horizontal Barchart with top 10
    LocationID_counts = df['PULocationID'].value_counts().nlargest(10).sort_values(ascending=False)

    fig5 = plt.figure(figsize=(10, 6))
    sns.barplot(x=LocationID_counts.values, y=LocationID_counts.index, palette="viridis", orient='h', order=LocationID_counts.index)
    plt.title('Top 10 most Trips LocationID')
    plt.xlabel('Total amount of trip')
    plt.ylabel('LocationId')

    # Number of trips of each RatecodeID
    # Piechart with 6 type of RatecodeID
    ratecodeID_map = {1: 'Standard rate', 2: 'JFK', 3: 'Newark', 4: 'Nassau or Westchester', 5: 'Negotiated fare', 6: 'Group ride'}

    df['ratecodeID_mapped'] = df['RatecodeID'].map(ratecodeID_map)
    ratecode_counts = df['ratecodeID_mapped'].value_counts()

    fig6 = plt.figure(figsize=(10, 6))

    plt.pie(ratecode_counts.values, labels=None, autopct=None, startangle=90, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})

    plt.title("Distribution of RatecodeID", fontsize=18)

    plt.legend(ratecode_counts.index, title="RatecodeID", loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=4)

    plt.tight_layout()


    # Analyze one day
    # Average Speed ​​per Hour
    # Histogram
    avg_speed_per_hour = df.groupby(df['tpep_pickup_datetime'].dt.hour)['avg_speed_mph'].mean()
    
    fig7 = plt.figure(figsize=(10, 6))
    plt.hist(avg_speed_per_hour.index, weights=avg_speed_per_hour.values, bins = 24, rwidth=0.8)
    plt.title('Average Speed per Hour')
    plt.xlabel('Hour of day')
    plt.ylabel('Average Speed (mph)')

    # Number of trips per Hour
    # Barchart
    trip_count_per_hour = df['tpep_pickup_datetime'].dt.hour.value_counts().sort_index()
    fig8 = plt.figure()
    sns.barplot(x=trip_count_per_hour.index, y=trip_count_per_hour.values, palette="viridis")
    plt.title('Trip per hour')
    plt.xlabel('Hour of day')
    plt.ylabel('Total amount of trip')