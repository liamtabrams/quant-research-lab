import numpy as np


def compute_future_return(df, horizon=1):
    return df['returns'].shift(-horizon)


def information_coefficient(signal, future_returns):
    valid = ~(signal.isna() | future_returns.isna())
    if valid.sum() == 0:
        return np.nan
    return np.corrcoef(signal[valid], future_returns[valid])[0, 1]


def sharpe_ratio(returns):
    if returns.std() == 0:
        return 0
    return returns.mean() / returns.std()