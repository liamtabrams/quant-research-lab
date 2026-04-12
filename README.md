# Quant Research Starter

A research environment for detecting statistical structure in financial time series.

---

## 📦 Setup

From the repo root:

```bash
pip install -r requirements.txt
```

or perhaps 

```bash
python3 -m pip install -r requirements.txt
```

depending on how pip is installed. 
---

## ▶️ How to Run (Important)

Run experiments **as a module from the repo root**:

```bash
python3 -m experiments.random_signal_test
```

❗ Do NOT run the file directly like:

```bash
python3 experiments/random_signal_test.py
```

This will cause import errors due to Python path resolution.

---

## 🧠 What This Does

This experiment tests your research pipeline against **pure noise**.

It:

1. Generates a random price series (random walk)
2. Generates a random signal (no predictive power)
3. Computes future returns
4. Measures alignment (Information Coefficient)

---

## 📊 Expected Output

You should see something like:

```text
=== Random Signal Test ===
Information Coefficient: ~0.00000
Sharpe Ratio (baseline): ~0.00000
```

Interpretation:

- IC ≈ 0 → no predictive power (correct)
- Confirms your pipeline is not hallucinating signals

---

## 🔬 Why This Matters

Before testing real ideas, you must verify:

> “Does my system correctly detect *no signal* when none exists?”

If this fails, all future experiments are unreliable.

---

## 🚀 Next Steps

1. Replace random signal with simple hypotheses:

```python
signal = df['returns']      # momentum test
signal = -df['returns']     # mean reversion test
```

2. Run multiple random signals to observe false positives

3. Implement your first real idea (e.g., curvature)

---

## 🧭 Philosophy

This repo is intentionally:

- minimal
- transparent
- statistically grounded

It focuses on:

> signal → statistical relationship → validation

NOT:

- trading bots
- overfit backtests
- complex infrastructure

---

## 📁 Project Structure

```
quant_research/
├── README.md
├── requirements.txt
├── config.py
├── data/
├── features/
├── evaluation