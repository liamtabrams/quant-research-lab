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