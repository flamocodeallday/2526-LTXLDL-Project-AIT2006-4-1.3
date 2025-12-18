import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')


def aggregate_trips(df1, freq='H'):
    if freq == 'H':
        time_col = 'hour'
        floor_freq = 'h'
    elif freq == 'D':
        time_col = 'day'
        floor_freq = 'D'
    
    df_agg = (
        df1
        .assign(
            **{time_col: lambda x: pd.to_datetime(x['tpep_pickup_datetime']).dt.floor(floor_freq)}
        )
        .groupby(time_col)
        .size()
        .rename('trips')
        .to_frame()
    )
    return df_agg


def forecast_and_evaluate(df1, freq, test_periods, arima_order=(1, 0, 1)):
    # Aggregate trips
    df = aggregate_trips(df1, freq)
    value_col = 'trips'
    
    # Split train/test
    train = df.iloc[:-test_periods]
    test = df.iloc[-test_periods:]
    
    # Baseline: same day of week, same hour (for hourly), previous week
    baseline_preds = []
    for idx in test.index:
        if freq == 'D':
            # Same weekday, previous week
            lag_days = 7
            baseline_idx = idx - pd.Timedelta(days=lag_days)
        elif freq == 'H':
            # Same weekday, same hour, previous week
            lag_hours = 168  # 7*24
            baseline_idx = idx - pd.Timedelta(hours=lag_hours)
        else:
            raise ValueError("Unsupported freq")
        
        if baseline_idx in train.index:
            baseline_preds.append(train.loc[baseline_idx, value_col])
        else:
            # If not available, use train mean
            baseline_preds.append(train[value_col].mean())
    
    baseline_preds = pd.Series(baseline_preds, index=test.index)
    
    # ARIMA model
    model = ARIMA(train[value_col], order=arima_order)
    model_fit = model.fit()
    arima_preds = model_fit.forecast(steps=test_periods)
    arima_preds.index = test.index
    
    # Linear Regression (simple: time as feature)
    # Create time feature: days since start
    train_time = (train.index - train.index[0]).total_seconds() / (24*3600)
    test_time = (test.index - train.index[0]).total_seconds() / (24*3600)
    
    lr = LinearRegression()
    lr.fit(train_time.values.reshape(-1, 1), train[value_col])
    lr_preds = lr.predict(test_time.values.reshape(-1, 1))
    lr_preds = pd.Series(lr_preds, index=test.index)
    
    # Calculate metrics
    def calc_metrics(actual, pred):
        mae = mean_absolute_error(actual, pred)
        mape = mean_absolute_percentage_error(actual, pred)
        rmse = np.sqrt(mean_squared_error(actual, pred))
        return {'MAE': mae, 'MAPE': mape, 'RMSE': rmse}
    
    baseline_metrics = calc_metrics(test[value_col], baseline_preds)
    arima_metrics = calc_metrics(test[value_col], arima_preds)
    lr_metrics = calc_metrics(test[value_col], lr_preds)
    
    metrics_df = pd.DataFrame({
        'Baseline': baseline_metrics,
        'ARIMA': arima_metrics,
        'Linear Regression': lr_metrics
    }).T
    
    predictions_df = pd.DataFrame({
        'Actual': test[value_col],
        'Baseline': baseline_preds,
        'ARIMA': arima_preds,
        'Linear Regression': lr_preds
    })
    
    return {
        'metrics': metrics_df,
        'predictions': predictions_df
    }
