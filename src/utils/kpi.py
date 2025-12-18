import pandas as pd

def kpi(df: pd.DataFrame, qa_flags: pd.DataFrame) -> dict:
    df_calc = df.copy()
    qa_flags = qa_flags.copy()

    # Define time bins
    bin = [0, 4, 7, 10, 16, 19, 24]
    labels = ['Early Morning', 'Morning','Morning Rush', 'Midday', 'Evening Rush', 'Late Night']  
    
    # Assign time bins based on pickup and dropoff hours
    df_calc['pickup_bin'] = pd.cut(df_calc['tpep_pickup_datetime'].dt.hour, bins=bin, labels=labels, right=False)
    df_calc['dropoff_bin'] = pd.cut(df_calc['tpep_dropoff_datetime'].dt.hour, bins=bin, labels=labels, right=False)

    # Calculation functions for 50th percentiles
    def p50(x): return x.quantile(0.5)

    # Convenience function for 95th percentile
    def p95(x): return x.quantile(0.95)

    # Define aggregation rules
    agg_rules = {
        'Date': ('tpep_pickup_datetime', lambda x: x.dt.date.iloc[0]),
        'Day_of_Week': ('pickup_day_of_week', 'first'),
        'Total_trips': ('tpep_pickup_datetime', 'count'),
        'Total_fare': ('fare_amount', lambda x: x[~qa_flags.loc[x.index, 'invalid_fare_amount']].sum()),
        'Total amount': ('total_amount', lambda x: x[(~qa_flags.loc[x.index, 'invalid_total_amount']) & (~qa_flags.loc[x.index, 'fare_total_mismatch'])].sum()),
        'duration_p50': ('trip_duration_minutes', lambda x: p50(x[(~qa_flags.loc[x.index, 'excessive_duration']) & (~qa_flags.loc[x.index, 'short_duration_long_distance'])])),
        'duration_p95': ('trip_duration_minutes', lambda x: p95(x[(~qa_flags.loc[x.index, 'excessive_duration']) & (~qa_flags.loc[x.index, 'short_duration_long_distance'])])),
        'speed_p50': ('avg_speed_mph', lambda x: p50(x[~qa_flags.loc[x.index, 'excessive_speed']])),
        'distance_p50': ('trip_distance', lambda x: p50(x[(~qa_flags.loc[x.index, 'suspicious_zero_fare']) & (~qa_flags.loc[x.index, 'short_duration_long_distance'])])),
        'distance_p95': ('trip_distance', lambda x: p95(x[(~qa_flags.loc[x.index, 'suspicious_zero_fare']) & (~qa_flags.loc[x.index, 'short_duration_long_distance'])])),
        'avg_distance': ('trip_distance', lambda x: x[(~qa_flags.loc[x.index, 'suspicious_zero_fare']) & (~qa_flags.loc[x.index, 'short_duration_long_distance'])].mean()),
        'trips': ('trip_distance', 'count'),
        'revenue_per_trip': ('fare_amount', lambda x: x[~qa_flags.loc[x.index, 'invalid_fare_amount']].sum() / x[~qa_flags.loc[x.index, 'invalid_fare_amount']].count()),
        'revenue_per_mile': ('fare_amount', lambda x: x[~qa_flags.loc[x.index, 'invalid_fare_amount']].sum() / df_calc.loc[x[~qa_flags.loc[x.index, 'invalid_fare_amount']].index, 'trip_distance'].sum())
    }

    # Create binary columns for each time bin
    for lb in labels:
        df_calc[f'pickup_bin_{lb}'] = (df_calc['pickup_bin'] == lb).astype(int)
        df_calc[f'dropoff_bin_{lb}'] = (df_calc['dropoff_bin'] == lb).astype(int)

    # Add aggregation rules for trips per hour in each time bin
    for i, lb in enumerate(labels):
        bin_hours = bin[i+1] - bin[i]

        agg_rules[f'{lb}'] = (
            'trip_distance',
            lambda x, lb=lb, h=bin_hours: (
                f"{round(df_calc.loc[x.index, f'pickup_bin_{lb}'].sum() / h, 2)} / {round(df_calc.loc[x.index, f'dropoff_bin_{lb}'].sum() / h, 2)}"
            )
        )

    # A. Daily
    df_daily = df_calc.groupby(pd.Grouper(key='tpep_pickup_datetime', freq='D')).agg(**agg_rules).reset_index()

    # B. Weekly
    df_weekly = df_calc.groupby(pd.Grouper(key='tpep_pickup_datetime', freq='W')).agg(**agg_rules).reset_index()

    # C. Monthly
    df_monthly = df_calc.groupby(pd.Grouper(key='tpep_pickup_datetime', freq='M')).agg(**agg_rules).reset_index()

    results = {
        "Daily": df_daily,
        "Weekly": df_weekly,
        "Monthly": df_monthly,
    }

    return results

def index_100_by_day(df : pd.DataFrame, value_col):
    df = df.copy()

    # Get the base value from the first day
    base_value = df.iloc[0][value_col]

    # Calculate index for each day
    df[f'index_100_by_day_by_{value_col}'] = df[value_col] / base_value * 100

    return df

def index_dow(df, value_col):
    df = df.copy()

    # Aggregate total value by day of the week
    agg = df.groupby('pickup_day_of_week')[value_col].sum().reset_index(name = 'total_trips')

    # Calculate average value across all days
    avg_value = agg['total_trips'].sum() / 7

    # Calculate index for each day of the week
    agg[f'index_dow_{value_col}'] = agg['total_trips'] / avg_value * 100

    return agg