import numpy as np

def random_signal(df):
    return np.random.normal(0, 1, len(df))

def lagged_return_signal(df, lag=1):
    return df['returns'].shift(lag)

def momentum_signal(prices, lookback=5):
    prices = prices["price"].values

    returns = np.diff(prices) / prices[:-1]

    signal = np.zeros_like(returns)

    for t in range(lookback, len(returns)):
        signal[t] = np.mean(returns[t - lookback:t])

    # ✅ FIX: pad to match original length
    signal = np.insert(signal, 0, 0.0)

    return signal

def mean_reversion_signal(prices, lookback=5):
    prices = prices["price"].values

    returns = np.diff(prices) / prices[:-1]

    signal = np.zeros_like(returns)

    for t in range(lookback, len(returns)):
        signal[t] = -np.mean(returns[t - lookback:t])

    # ✅ FIX: pad to match original length
    signal = np.insert(signal, 0, 0.0)

    return signal

