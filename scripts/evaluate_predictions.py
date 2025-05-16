import pandas as pd
import sys
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Usage: python evaluate_predictions.py <predictions_csv>")
    sys.exit(1)

pred_path = sys.argv[1]
df = pd.read_csv(pred_path)

print("=== Prediction Summary ===")
print(df["bugfix_probability"].describe())

# Top-N wahrscheinlichste Bugfixes
top_n = 20
print(f"\n=== Top {top_n} highest scoring commits ===")
print(df.sort_values("bugfix_probability", ascending=False).head(top_n))

# Schwellenanalyse (z. B. Top 5 %)
threshold = df["bugfix_probability"].quantile(0.95)
top_5p = df[df["bugfix_probability"] >= threshold]
print(f"\nTop 5% Threshold: {threshold:.3f}")
print(f"{len(top_5p)} commits above threshold")

# Histogramm
plt.hist(df["bugfix_probability"], bins=30, color="green", edgecolor="black")
plt.title("Distribution of Bugfix-Probability")
plt.xlabel("Probability")
plt.ylabel("Number Commits")
plt.tight_layout()
plt.show()
