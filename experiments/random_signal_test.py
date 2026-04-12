from data.data_loader import (
generate_random_price_series,
generate_momentum_price_series,
generate_mean_reverting_price_series,
load_ibkr_price_series,
)
from features.signal_generator import (
    random_signal,
    momentum_signal,
    mean_reversion_signal,
)
from evaluation.metrics import (
    compute_future_return,
    information_coefficient,
    sharpe_ratio,
)


def evaluate_signal(df, signal_func, name):
    df = df.copy()

    # Generate signal
    df["signal"] = signal_func(df)

    # Compute forward returns
    df["future_return"] = compute_future_return(df)

    # Drop NaNs to ensure proper alignment
    df = df.dropna(subset=["signal", "future_return"])

    # Compute IC
    ic = information_coefficient(df["signal"], df["future_return"])

    # Compute strategy returns (THIS is the important fix)
    df["strategy_return"] = df["signal"] * df["future_return"]

    sr = sharpe_ratio(df["strategy_return"])

    print(f"=== {name} ===")
    print(f"Information Coefficient: {ic:.5f}")
    print(f"Sharpe Ratio: {sr:.5f}")
    print()


def run_experiment():

    print("generating random walk price series data")
    df = generate_random_price_series()

    evaluate_signal(df, random_signal, "Random Signal Test")
    evaluate_signal(df, momentum_signal, "Momentum Signal Test")
    evaluate_signal(df, mean_reversion_signal, "Mean Reversion Signal Test")

    print("generating random walk price series data with some momentum")

    df = generate_momentum_price_series()

    evaluate_signal(df, random_signal, "Random Signal Test")
    evaluate_signal(df, momentum_signal, "Momentum Signal Test")
    evaluate_signal(df, mean_reversion_signal, "Mean Reversion Signal Test")

    print("generating random walk price series data with some mean reversion")

    df = generate_mean_reverting_price_series()

    evaluate_signal(df, random_signal, "Random Signal Test")
    evaluate_signal(df, momentum_signal, "Momentum Signal Test")
    evaluate_signal(df, mean_reversion_signal, "Mean Reversion Signal Test")

    print("loading actual AAPL stock data with IB Gateway")

    df = load_ibkr_price_series()

    evaluate_signal(df, random_signal, "Random Signal Test")
    evaluate_signal(df, momentum_signal, "Momentum Signal Test")
    evaluate_signal(df, mean_reversion_signal, "Mean Reversion Signal Test")




if __name__ == "__main__":
    run_experiment()