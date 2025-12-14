import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def cluster_zone_hour_kpi(
    df: pd.DataFrame,
    feature_cols: list = None,
    n_clusters: int = 4,
    random_state: int = 42
):
    """
    Phân cụm zone / khung giờ dựa trên vector KPI.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa KPI, mỗi dòng là (zone, hour).
        Ví dụ cột:
        - zone_id
        - hour
        - trips_index
        - duration_p50
        - duration_p95

    feature_cols : list
        Danh sách cột KPI dùng để clustering.

    n_clusters : int
        Số cụm KMeans.

    random_state : int
        Random seed cho KMeans.

    Returns
    -------
    df_clustered : pd.DataFrame
        DataFrame gốc + cột cluster + cluster_name.

    cluster_profile : pd.DataFrame
        Trung bình KPI theo từng cluster.

    cluster_description : dict
        Mô tả ngắn gọn cho từng cluster.
    """

    if feature_cols is None:
        feature_cols = [
            "trips_index",
            "duration_p50",
            "duration_p95"
        ]

    # -----------------------
    # 1. Kiểm tra dữ liệu
    # -----------------------
    missing_cols = [c for c in feature_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Thiếu cột KPI: {missing_cols}")

    df = df.copy().reset_index(drop=True)

    # -----------------------
    # 2. Chuẩn hóa
    # -----------------------
    scaler = StandardScaler()
    X = scaler.fit_transform(df[feature_cols])

    # -----------------------
    # 3. KMeans
    # -----------------------
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )

    df["cluster"] = kmeans.fit_predict(X)

    # -----------------------
    # 4. Hồ sơ cụm (profile)
    # -----------------------
    cluster_profile = (
        df
        .groupby("cluster")[feature_cols]
        .mean()
        .round(2)
        .sort_index()
    )

    # -----------------------
    # 5. Đặt tên & mô tả cụm
    # (có thể chỉnh tay cho report)
    # -----------------------
    cluster_names = {}
    cluster_description = {}

    for c in cluster_profile.index:
        row = cluster_profile.loc[c]

        if row["trips_index"] < 0.8 and row["duration_p95"] < 20:
            name = "Low demand – short trips"
            desc = "Nhu cầu thấp, chuyến ngắn, thường là off-peak hoặc khu dân cư."
        elif row["trips_index"] > 1.3 and row["duration_p95"] < 40:
            name = "Peak demand – efficient flow"
            desc = "Nhu cầu cao, thời lượng ổn định, giờ cao điểm."
        elif row["duration_p95"] > 50:
            name = "Congested / long-tail trips"
            desc = "Biến động lớn, dễ tắc nghẽn hoặc chuyến dài."
        else:
            name = "Moderate demand – mixed pattern"
            desc = "Nhu cầu và thời lượng trung bình, hành vi hỗn hợp."

        cluster_names[c] = name
        cluster_description[c] = desc

    df["cluster_name"] = df["cluster"].map(cluster_names)

    return df, cluster_profile, cluster_description
