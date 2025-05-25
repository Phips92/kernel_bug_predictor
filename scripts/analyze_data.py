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

print("\n=== Label Distribution ===")
print(df["label"].value_counts())

if "tool_found" in df.columns:
    print("\n=== Tool Found Summary ===")
    tool_count = df["tool_found"].sum()
    print(f"{tool_count} commits were marked as fixed using known tools.")

print("\n=== Statistic summary ===")
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


# for manual check
buggy = df[df["label"] == 1]
print(buggy.head(10)[["commit_hash", "author", "message_length"]])

