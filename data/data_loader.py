import numpy as np
import pandas as pd
import requests
from ib_insync import IB, Stock
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


from pathlib import Path


def load_alpha_vantage_daily(ticker="AAPL"):
    import requests
    import pandas as pd
    from pathlib import Path

    key_path = Path(__file__).parent / "alpha_vantage_key.txt"

    with open(key_path, "r") as f:
        api_key = f.read().strip()

    url = (
        "https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY"
        f"&symbol={ticker}"
        f"&outputsize=compact"
        f"&apikey={api_key}"
    )

    response = requests.get(url)
    data = response.json()

    # --- HARD FAILS ---
    if "Note" in data:
        raise ValueError(f"Rate limit hit: {data['Note']}")

    if "Information" in data:
        raise ValueError(f"API limitation: {data['Information']}")

    if "Time Series (Daily)" not in data:
        raise ValueError(f"Unexpected API response: {data}")

    # --- Build DataFrame ---
    ts = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(ts, orient="index")

    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Find close column
    close_col = next((c for c in df.columns if "close" in c), None)

    if close_col is None:
        raise ValueError(f"No close column found: {df.columns}")

    df = df.rename(columns={close_col: "price"})

    df["price"] = df["price"].astype(float)
    df["returns"] = df["price"].pct_change()

    df = df[["price", "returns"]].dropna().reset_index(drop=True)

    print(f"Loaded {ticker} (rows={len(df)})")

    return df

def load_ibkr_price_series(symbol="AAPL", duration="5 Y", bar_size="1 day"):
    """
    Load historical data from IBKR
    """

    ib = IB()
    ib.connect("127.0.0.1", 7497, clientId=1)  # Gateway port

    contract = Stock(symbol, "SMART", "USD")

    bars = ib.reqHistoricalData(
        contract,
        endDateTime="",
        durationStr=duration,
        barSizeSetting=bar_size,
        whatToShow="TRADES",
        useRTH=True,
        formatDate=1
    )

    ib.disconnect()

    if not bars:
        raise ValueError("No data returned from IBKR")

    df = pd.DataFrame(bars)

    df = df.rename(columns={"close": "price"})
    df["returns"] = df["price"].pct_change()

    df = df[["price", "returns"]].dropna().reset_index(drop=True)

    print(f"Loaded {symbol} from IBKR (rows={len(df)})")

    return df

