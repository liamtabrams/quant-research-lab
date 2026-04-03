import numpy as np

def random_signal(df):
    return np.random.normal(0, 1, len(df))

def lagged_return_signal(df, lag=1):
    return df['returns'].shift(lag)