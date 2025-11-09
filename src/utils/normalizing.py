import pandas as pd
import numpy as np
import os

"""
This function normalize a dataframe of a month
Columns before: ['VendorID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime','passenger_count', 
                'trip_distance', 'RatecodeID', 'store_and_fwd_flag','PULocationID', 'DOLocationID', 
                'payment_type', 'fare_amount', 'extra','mta_tax', 'tip_amount', 'tolls_amount', 
                'improvement_surcharge','total_amount', 'congestion_surcharge', 'airport_fee']
Columns after: ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 
                'trip_distance', 'RatecodeID','PULocationID', 'DOLocationID', 
                'payment_type', 'fare_amount', 'extra', 'tip_amount', 'tolls_amount', 
                'total_amount', 'congestion_surcharge', 'ratecodeID_name', 'payment_type_name', 
                'trip_duration_seconds', 'trip_duration_minutes', 'avg_speed_mph', 
                'PU_Borough', 'PU_Zone', 'DO_Borough', 'DO_Zone', 'pickup_day_of_week']

"""

# Load and prepare the taxi zone lookup table for merging
zones_df_raw = pd.read_csv(os.path.join('../raw/', 'taxi_zone_lookup.csv'))
zones_lookup = zones_df_raw[['LocationID', 'Borough', 'Zone']].copy()

# Define mappings for categorical features based on the official data dictionary.
payment_map = {0: 'Flex Fare trip', 1: 'Credit card', 2: 'Cash', 3: 'No charge', 4: 'Dispute', 5: 'Unknown', 6: 'Voided trip'}
ratecodeID_map = {1: 'Standard rate', 2: 'JFK', 3: 'Newark', 4: 'Nassau or Westchester', 5: 'Negotiated fare', 6: 'Group ride'}

def normalize(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()

    # Normalize RatecodeID 
    df['ratecodeID_name'] = df['RatecodeID'].map(ratecodeID_map)
    # Normalize Payment type
    df['payment_type_name'] = df['payment_type'].map(payment_map)
    # Normalize PULocationID 
    df = df.merge(
        zones_lookup,
        left_on='PULocationID',
        right_on='LocationID',
        how='left'  
    )
    df.rename(columns={'Borough': 'PU_Borough', 'Zone': 'PU_Zone'}, inplace=True)
    df.drop(columns=['LocationID'], inplace=True) 
    # Normalize DOLocationID 
    df = df.merge(
        zones_lookup,
        left_on='DOLocationID',
        right_on='LocationID',
        how='left'
    )
    df.rename(columns={'Borough': 'DO_Borough', 'Zone': 'DO_Zone'}, inplace=True)
    df.drop(columns=['LocationID'], inplace=True)

    # Create new feature: trip's duration
    df['trip_duration_seconds'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()
    df['trip_duration_minutes'] = round(df['trip_duration_seconds']/60)
    # Create new feature: trip's average speed
    df['avg_speed_mph'] = round(df['trip_distance'] / (df['trip_duration_seconds'] / 3600), 2)
    df['avg_speed_mph'].replace([np.inf, -np.inf], np.nan, inplace=True)
    # Create new feture: trip's day in week (based on pick up time)
    df['pickup_day_of_week'] = df['tpep_pickup_datetime'].dt.day_name()

    # Remove columns due to the number of NA values and based on the purpose of analysing
    cols_to_drop = [
    'airport_fee',           # Dropped: only 5 nonnull values
    'store_and_fwd_flag',    # Dropped: Irrelevant to analysis
    'VendorID',              # Dropped: Irrelevant to analysis
    'mta_tax',               # Dropped: Low variance / Irrelevant
    'improvement_surcharge'  # Dropped: Low variance / Irrelevant
    ]
    df.drop(columns=cols_to_drop, axis=1, inplace=True)

    return df