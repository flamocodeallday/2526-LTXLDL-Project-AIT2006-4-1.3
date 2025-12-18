import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def compute_kpi_zone_time(df: pd.DataFrame, qa_flags: pd.DataFrame) -> pd.DataFrame:
    df_calc = df.copy()
    qa_flags = qa_flags.copy()

    # Define time bins
    bin = [0, 4, 7, 10, 16, 19, 24]
    labels = ['Early Morning', 'Morning','Morning Rush', 'Midday', 'Evening Rush', 'Late Night']

    # Assign time bins based on pickup hour
    df_calc['time_bin'] = pd.cut(df_calc['tpep_pickup_datetime'].dt.hour, bins=bin, labels=labels, right=False)

    # Use PU_Zone as zone
    df_calc['zone'] = df_calc['PU_Zone']

    # Calculation functions
    def p50(x): return x.quantile(0.5)
    def p95(x): return x.quantile(0.95)

    # Define aggregation rules
    agg_rules = {
        'duration_p50': ('trip_duration_minutes', p50),
        'duration_p95': ('trip_duration_minutes', p95),
        'speed_p50': ('avg_speed_mph', p50),
        'avg_trip_distance': ('trip_distance', 'mean'),
        'trips': ('trip_distance', 'count'),
    }

    # Group by zone and time_bin
    df_kpi = df_calc.groupby(['zone', 'time_bin']).agg(**agg_rules).reset_index()

    # Compute trips_index_100: normalize trips to index 100
    # Assuming base is the overall average trips per zone-time
    base_value = df_kpi['trips'].mean()
    df_kpi['trips_index_100'] = (df_kpi['trips'] / base_value) * 100

    return df_kpi

def cluster_zone_time(df_kpi_zone_time: pd.DataFrame, n_clusters: int = 4) -> tuple:
    features = ['duration_p50', 'duration_p95', 'trips_index_100']

    df_cluster = (
        df_kpi_zone_time
        .set_index(['zone', 'time_bin'])
        [features]
        .dropna()
    )

    # Scale data
    scaler = StandardScaler()
    X = scaler.fit_transform(df_cluster)

    # Fit KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_cluster['cluster'] = kmeans.fit_predict(X)

    # Analyze centroids
    centroids = pd.DataFrame(
        scaler.inverse_transform(kmeans.cluster_centers_),
        columns=features
    )
    centroids['cluster'] = centroids.index

    # Name clusters based on rules
    def name_cluster(row):
        if row['trips_index_100'] > 500 and row['duration_p95'] > 20:
            return 'High Demand – Congested'
        elif row['trips_index_100'] < 50 and row['duration_p50'] < 30:
            return 'Low Demand – Smooth Flow'
        elif row['duration_p95'] > 50:
            return 'Unstable Traffic'
        else:
            return 'Efficient High Volume'

    centroids['cluster_name'] = centroids.apply(name_cluster, axis=1)

    # Add descriptions
    descriptions = {
        'High Demand – Congested': 'Zones and time bins with high trip volume and long 95th percentile durations, indicating congestion and high demand.',
        'Low Demand – Smooth Flow': 'Zones and time bins with low trip volume and short median durations, suggesting smooth traffic flow.',
        'Unstable Traffic': 'Zones and time bins with very long 95th percentile durations, indicating traffic instability.',
        'Efficient High Volume': 'Zones and time bins with balanced high volume and reasonable durations, efficient operations.'
    }

    centroids['description'] = centroids['cluster_name'].map(descriptions)

    # Map cluster names back to df_cluster
    cluster_name_map = centroids.set_index('cluster')['cluster_name']
    df_cluster['cluster_name'] = df_cluster['cluster'].map(cluster_name_map)

    # Reset index to have zone and time_bin as columns
    df_cluster = df_cluster.reset_index()

    return df_cluster, centroids

def cluster_zones_with_kpi(df: pd.DataFrame, qa_flags: pd.DataFrame, n_clusters: int = 4) -> tuple:
    # Compute KPIs
    kpi_df = compute_kpi_zone_time(df, qa_flags)
    
    # Perform clustering
    return cluster_zone_time(kpi_df, n_clusters)
