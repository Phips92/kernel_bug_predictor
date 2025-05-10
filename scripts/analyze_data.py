import pandas as pd
import sys
import seaborn as sns
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Usage: python analyze_data.py <features_csv>")
    sys.exit(1)

csv_path = sys.argv[1]

df = pd.read_csv(csv_path)

print("=== Feature Overview ===")
print(df.head())

print("\n=== Datenform ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n=== Verteilung des Labels ===")
print(df['label'].value_counts())

print("\n=== Statistische Zusammenfassung ===")
print(df.describe())

# Bugfix Dist over time
# df["author_date"] = pd.to_datetime(df["author_date"], unit="s")
# df["year_month"] = df["author_date"].dt.to_period("M").astype(str)
# df.groupby("year_month")["label"].mean().plot()

# Correlation
numeric_df = df.select_dtypes(include="number")
plt.figure(figsize=(12, 10))
sns.heatmap(numeric_df.corr(), annot=False, cmap="coolwarm")
plt.title("Korrelationsmatrix")
plt.tight_layout() 
plt.show()

# Feature distribution
filtered = df[df["message_length"] < df["message_length"].quantile(0.99)]
sns.boxplot(data=filtered, x="label", y="message_length")
plt.title("Message Length (99% Bereich)")

plt.show()

