from data.data_loader import generate_random_price_series
from features.signal_generator import random_signal
from evaluation.metrics import compute_future_return, information_coefficient, sharpe_ratio


def run_experiment():
    df = generate_random_price_series()

    df['signal'] = random_signal(df)
    df['future_return'] = compute_future_return(df)

    ic = information_coefficient(df['signal'], df['future_return'])
    sr = sharpe_ratio(df['future_return'].dropna())

    print("=== Random Signal Test ===")
    print(f"Information Coefficient: {ic:.5f}")
    print(f"Sharpe Ratio (baseline): {sr:.5f}")


if __name__ == "__main__":
    run_experiment()
