import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_summary(df_month: pd.DataFrame, kpi_month: pd.DataFrame) -> None: 
    df = df_month.copy()
    kpi = kpi_month.copy()

    # Plot revenue per day of the month.
    # LinePlot
    revenue_per_day = kpi['Total_fare']

    fig1 = plt.figure(figsize=(10, 6))
    plt.plot(kpi['Date'].dt.day, revenue_per_day.values, marker='o')
    plt.title('Revenue per day in month')
    plt.xlabel('Day of month')
    plt.ylabel('Total Revenue')
    plt.grid()
    plt.tight_layout()

    # Plot trips per day of the month.   
    # BarPlot
    trips_per_day = kpi['Total_trips']

    fig2 = plt.figure(figsize=(10, 6))
    plt.bar(kpi['Date'].dt.day, trips_per_day.values)
    plt.title('Trips per day in month')
    plt.xlabel('Day of month')
    plt.ylabel('Total Trips')
    plt.grid()
    plt.tight_layout()

    # Plot trips per day of week
    # Heatmap with 7 days of week
    day_map = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    weekday_counts = df['pickup_day_of_week'].value_counts().reindex(day_map)

    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour

    fig3 = plt.figure(figsize=(10, 6))
    sns.heatmap(data=df.groupby(['pickup_day_of_week', 'pickup_hour']).size().unstack(fill_value=0).reindex(day_map), cmap="viridis")
    plt.title('Trip per week')
    plt.xlabel('Day of week')
    plt.ylabel('Total amount of trip')

def visualize_customer_segments(df_month: pd.DataFrame, qa_flags: pd.DataFrame) -> None:
    df = df_month.copy()
    qa = qa_flags.copy()

    # Plot distribution of payment types
    # Pie chart
    payment_counts =  df.loc[~qa['invalid_payment_type'], 'payment_type_name'].value_counts()

    fig1 = plt.figure(figsize=(10, 6))
    plt.pie(payment_counts.values, labels=None, autopct=None, startangle=90, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
    plt.title("Distribution of Payment type", fontsize=18)
    plt.legend(payment_counts.index, title="Payment type", loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=4)
    plt.tight_layout()

    # Plot trips with passenger count more than 2 
    # Bar plot
    passenger_counts = df.loc[(~qa['unusual_passenger_count']) & (df['passenger_count'] > 2), 'passenger_count'].value_counts().sort_index()

    fig2 = plt.figure(figsize=(10, 6))
    plt.bar(passenger_counts.index, passenger_counts.values)
    plt.title('Trips with more than 2 passengers')
    plt.xlabel('Number of passengers')
    plt.ylabel('Total trips')
    plt.grid()
    plt.tight_layout()

    # Plot tip amount correlation with distance and duration
    # Correlation matrix (3x3)
    # TODO

def visualize_temporal_trends(df_month: pd.DataFrame, qa_flags: pd.DataFrame) -> None:
    df = df_month.copy()
    qa = qa_flags.copy()

    # Plot average speed per hour of day
    # Histogram
    avg_speed_per_hour = df.loc[(~qa['invalid_speed']) & (~qa['excessive_speed'])].groupby(df['tpep_pickup_datetime'].dt.hour)['avg_speed_mph'].mean()
    fig1 = plt.figure(figsize=(10, 6))
    plt.hist(avg_speed_per_hour.index, weights=avg_speed_per_hour.values, bins = 24, rwidth=0.8)
    plt.title('Average Speed per Hour')
    plt.xlabel('Hour of day')
    plt.ylabel('Average Speed (mph)')

    # Number of trips per Hour
    # Barchart
    trip_count_per_hour = df.loc[(~qa['suspicious_zero_fare']) & (~qa['short_duration_long_distance']) & (~qa['excessive_speed']) & (~qa['excessive_duration'])].groupby(df['tpep_pickup_datetime'].dt.hour)['tpep_pickup_datetime'].count()
    fig2 = plt.figure()
    sns.barplot(x=trip_count_per_hour.index, y=trip_count_per_hour.values, palette="viridis")
    plt.title('Trip per hour')
    plt.xlabel('Hour of day')
    plt.ylabel('Total amount of trip')

    # Revenue per Hour
    # LinePlot
    revenue_per_hour = df.loc[(~qa['suspicious_zero_fare']) & (~qa['short_duration_long_distance']) & (~qa['excessive_speed']) & (~qa['excessive_duration'])].groupby(df['tpep_pickup_datetime'].dt.hour)['total_amount'].sum()
    fig3 = plt.figure()
    plt.plot(revenue_per_hour.index, revenue_per_hour.values, marker='o')
    plt.title('Revenue per hour')
    plt.xlabel('Hour of day')
    plt.ylabel('Total Revenue') 

def visualize_trip_characteristics(df_month: pd.DataFrame, qa_flags: pd.DataFrame) -> None:
    df = df_month.copy()
    qa = qa_flags.copy()
    # Plot distance distribution
    # Histogram
    # TODO


    # Plot duration distribution
    # Histogram
    # TODO

def visualize_geographical_analysis(df_month: pd.DataFrame, qa_flags: pd.DataFrame) -> None:
    df = df_month.copy()
    qa = qa_flags.copy()
    # Top 10 pick up zones 
    # Horizontal Bar plot
    # TODO

    # Top 10 drop off zones
    # Horizontal Bar plot
    # TODO

