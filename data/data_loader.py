import numpy as np
import pandas as pd
from config import SEED, N_SAMPLES


def generate_random_price_series():
    np.random.seed(SEED)
    returns = np.random.normal(0, 0.01, N_SAMPLES)
    price = 100 * (1 + returns).cumprod()
    df = pd.DataFrame({
        'price': price,
        'returns': returns
    })
    return df


def generate_momentum_price_series(alpha=0.3):
    """
    Generates price series with momentum (positive autocorrelation in returns)
    """
    np.random.seed(SEED)

    noise = np.random.normal(0, 0.01, N_SAMPLES)
    returns = np.zeros(N_SAMPLES)

    for t in range(1, N_SAMPLES):
        returns[t] = noise[t] + alpha * returns[t - 1]

    price = 100 * (1 + returns).cumprod()

    df = pd.DataFrame({
        'price': price,
        'returns': returns
    })
    return df


def generate_mean_reverting_price_series_AR1(alpha=0.3):
    """
    Generates AR(1) returns process (negative autocorrelation)
    """
    np.random.seed(SEED)

    noise = np.random.normal(0, 0.01, N_SAMPLES)
    returns = np.zeros(N_SAMPLES)

    for t in range(1, N_SAMPLES):
        returns[t] = noise[t] - alpha * returns[t - 1]

    price = 100 * (1 + returns).cumprod()

    df = pd.DataFrame({
        'price': price,
        'returns': returns
    })
    return df


def generate_mean_reverting_price_series(theta=0.05, mu=100):
    """
    Ornstein-Uhlenbeck style mean-reverting price process
    """
    np.random.seed(SEED)

    price = np.zeros(N_SAMPLES)
    price[0] = mu

    for t in range(1, N_SAMPLES):
        noise = np.random.normal(0, 1)
        price[t] = price[t - 1] + theta * (mu - price[t - 1]) + noise

    returns = np.diff(price, prepend=price[0]) / price

    df = pd.DataFrame({
        'price': price,
        'returns': returns
    })
    return df

