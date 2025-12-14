import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA


def forecast_and_evaluate(
    df: pd.DataFrame,
    value_col: str = "trips",
    test_periods: int = 7,
    freq: str = "D",
    arima_order: tuple = (1, 0, 1)
) -> dict:

    df = df.copy().sort_index()

    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("Index phải là DatetimeIndex")

    if freq == "H":
        seasonal_shift = 24 * 7
        features = ['hour', 'dow', 'is_weekend']
    elif freq == "D":
        seasonal_shift = 7
        features = ['dow', 'is_weekend']
    else:
        raise ValueError("freq phải là 'H' hoặc 'D'")

    train = df.iloc[:-test_periods]
    test = df.iloc[-test_periods:]

    df['baseline_pred'] = df[value_col].shift(seasonal_shift)
    test['baseline_pred'] = df.loc[test.index, 'baseline_pred']

    def add_time_features(x):
        x = x.copy()
        x['dow'] = x.index.dayofweek
        x['is_weekend'] = (x['dow'] >= 5).astype(int)
        if freq == "H":
            x['hour'] = x.index.hour
        return x

    train_feat = add_time_features(train)
    test_feat = add_time_features(test)

    lr = LinearRegression()
    lr.fit(train_feat[features], train_feat[value_col])
    test['lr_pred'] = lr.predict(test_feat[features])

    arima = ARIMA(train[value_col], order=arima_order).fit()
    test['arima_pred'] = arima.forecast(len(test)).values

    def mae(y, yhat):
        return np.mean(np.abs(y - yhat))

    def mape(y, yhat):
        return np.mean(np.abs((y - yhat) / y)) * 100

    metrics = pd.DataFrame({
        "MAE": [
            mae(test[value_col], test['baseline_pred']),
            mae(test[value_col], test['lr_pred']),
            mae(test[value_col], test['arima_pred'])
        ],
        "MAPE (%)": [
            mape(test[value_col], test['baseline_pred']),
            mape(test[value_col], test['lr_pred']),
            mape(test[value_col], test['arima_pred'])
        ]
    }, index=["Baseline", "Linear Regression", "ARIMA"])

    return {
        "metrics": metrics,
        "predictions": test[[value_col, 'baseline_pred', 'lr_pred', 'arima_pred']]
    }
