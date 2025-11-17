import pandas as pd
import numpy as np

def kpi(df: pd.DataFrame) -> dict:
    """
    Tính toán KPI (Trips, Duration p50/p95, Speed p50) theo Ngày, Tuần, Tháng.
    
    Args:
        df (pd.DataFrame): DataFrame đầu vào chứa dữ liệu đã normalize (trip logs).
        
    Returns:
        dict: Dictionary chứa 3 keys 'daily', 'weekly', 'monthly' tương ứng với 3 DataFrames kết quả.
    """
    
    # --- 1. CẤU HÌNH TÊN CỘT (Cần đảm bảo khớp với dữ liệu đầu vào) ---
    col_date = 'tpep_pickup_datetime'   # Thời gian bắt đầu

    # --- 2. CHUẨN BỊ ---
    # Tạo bản sao để tránh warning "SettingWithCopy" trên df gốc
    df_calc = df.copy()
    
    # Định nghĩa hàm tính phân vị (Percentile)
    def p50(x): return x.quantile(0.5)
    def p95(x): return x.quantile(0.95)

    # Quy tắc tính toán (Aggregation rules)
    agg_rules = {
        'trip_duration_minutes' : [p50, p95],  # Thời gian: lấy trung vị và p95
        'avg_speed_mph': [p50]           # Tốc độ: lấy trung vị
    }

    # Helper function: Làm phẳng MultiIndex columns (ví dụ: (duration, p50) -> duration_p50)
    def process_agg_result(agg_df):
        # Nối tên cột cấp 1 và cấp 2
        agg_df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in agg_df.columns.values]
        agg_df = agg_df.reset_index()
        
        # Đổi tên cột sang tiếng Anh chuẩn chỉnh (tùy chọn)
        rename_map = {
            f'{'trip_duration_minutes'}_p50': 'duration_p50',
            f'{'trip_duration_minutes'}_p95': 'duration_p95',
            f'{'avg_speed_mph'}_p50': 'speed_p50'
        }
        agg_df.rename(columns=rename_map, inplace=True)
        return agg_df

    # --- 3. TÍNH TOÁN ---
    
    # A. Theo NGÀY (Daily)
    df_daily = df_calc.groupby(pd.Grouper(key=col_date, freq='D')).agg(agg_rules)
    df_daily = process_agg_result(df_daily)

    # B. Theo TUẦN (Weekly)
    df_weekly = df_calc.groupby(pd.Grouper(key=col_date, freq='W')).agg(agg_rules)
    df_weekly = process_agg_result(df_weekly)

    # C. Theo THÁNG (Monthly)
    df_monthly = df_calc.groupby(pd.Grouper(key=col_date, freq='M')).agg(agg_rules)
    df_monthly = process_agg_result(df_monthly)

    # Trả về kết quả dạng dictionary
    return {
        "daily": df_daily,
        "weekly": df_weekly,
        "monthly": df_monthly
    }

# --- VÍ DỤ SỬ DỤNG ---
# results = kpi(df_cleaned)
# print(results['daily'].head())
# print(results['monthly'])