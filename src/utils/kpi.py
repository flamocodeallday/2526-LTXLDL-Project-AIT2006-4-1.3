import pandas as pd
import numpy as np

def kpi(df: pd.DataFrame) -> dict:
    df_calc = df.copy()

    def p50(x): return x.quantile(0.5)
    def p95(x): return x.quantile(0.95)

    agg_rules = {
        'duration_p50': ('trip_duration_minutes', p50),
        'duration_p95': ('trip_duration_minutes', p95),
        'speed_p50':    ('avg_speed_mph', p50),
        'distance_p50': ('trip_distance', p50),
        'distance_p95': ('trip_distance', p95),
        'avg_distance': ('trip_distance', 'mean'),
        'trips':        ('trip_distance', 'count'),
        'revuenue_per_trip':     ('total_amount', lambda x: x.sum() / x.count()),
        'revenue_per_mile':     ('total_amount', lambda x: x.sum() / df_calc.loc[x.index, 'trip_distance'].sum()),
        'avg_pickup_per_hour': ('tpep_pickup_datetime', lambda x: x.count() / ((x.max() - x.min()).total_seconds() / 3600)),
        'avg_dropoff_per_hour': ('tpep_dropoff_datetime', lambda x: x.count() / ((x.max() - x.min()).total_seconds() / 3600)),
    }
    
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

    # D. Time Bin
    bin = [0, 4, 7, 10, 16, 19]
    labels = ['Early Morning', 'Morning Rush', 'Midday', 'Evening Rush', 'Late Night']  
    df_calc['time_bin'] = pd.cut(df_calc['tpep_pickup_datetime'].dt.hour, bins=bin, labels=labels, right=False)

    df_time_bin = df_calc.groupby('time_bin').agg(**agg_rules).reset_index()

    for index, row in df_time_bin.iterrows():
        results[row['time_bin']] = (pd.DataFrame(row).T.set_index('time_bin')).reset_index(drop=True)

    return results