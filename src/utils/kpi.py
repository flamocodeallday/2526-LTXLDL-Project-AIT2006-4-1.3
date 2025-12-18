import pandas as pd

def aggregate_kpis(df_month: pd.DataFrame, qa_flags: pd.DataFrame) -> dict:
    df_calc = df_month.copy()
    qa_calc = qa_flags.copy()

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
        'Total amount': ('total_amount', lambda x: [(~qa_flags.loc[x.index, 'invalid_total_amount']) & (~qa_flags.loc[x.index, 'fare_total_mismatch'])].sum()),
        'duration_p50': ('trip_duration_minutes', p50, lambda x: x[~qa_flags.loc[x.index, 'excessive_duration']] & (x[~qa_flags.loc[x.index, 'short_duration_long_distance']])),
        'duration_p95': ('trip_duration_minutes', p95, lambda x: x[~qa_flags.loc[x.index, 'excessive_duration']] & (x[~qa_flags.loc[x.index, 'short_duration_long_distance']])),
        'speed_p50':    ('avg_speed_mph', p50, lambda x: x[~qa_flags.loc[x.index, 'excessive_speed']]),
        'distance_p50': ('trip_distance', p50, lambda x: x[~qa_flags.loc[x.index, 'suspicious_zero_fare']] & (x[~qa_flags.loc[x.index, 'short_duration_long_distance']])),
        'distance_p95': ('trip_distance', p95, lambda x: x[~qa_flags.loc[x.index, 'suspicious_zero_fare']] & (x[~qa_flags.loc[x.index, 'short_duration_long_distance']])),
        'avg_distance': ('trip_distance', 'mean', lambda x: x[~qa_flags.loc[x.index, 'suspicious_zero_fare']] & (x[~qa_flags.loc[x.index, 'short_duration_long_distance']])),
        'trips':        ('trip_distance', 'count'),
        'revenue_per_trip': ('fare_amount', lambda x: x[~qa_flags.loc[x.index, 'invalid_fare_amount']].sum() /
                                                        x[~qa_flags.loc[x.index, 'invalid_fare_amount']].count() ),
        'revenue_per_mile': ('fare_amount', lambda x: x[~qa_flags.loc[x.index, 'invalid_fare_amount']].sum() / 
                                                       df_calc.loc[x[~qa_flags.loc[x.index, 'invalid_fare_amount']].index, 'trip_distance'].sum())
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

    base_value = df_daily.loc[0, 'trips']

    if base_value == 0:
        base_value = 1  # To avoid division by zero

    df_daily[f'index_100_by_day_by_trips'] = (
        df_daily['trips'] / base_value * 100
    )

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