import pandas as pd
import sys
from sklearn.metrics import confusion_matrix, classification_report

if len(sys.argv) != 3:
    print("Usage: python evaluate_prediction_quality.py <features_with_label.csv> <predictions.csv>")
    sys.exit(1)

features_path = sys.argv[1]
predictions_path = sys.argv[2]

# Load data
df_labels = pd.read_csv(features_path)[["commit_hash", "label"]]
df_preds = pd.read_csv(predictions_path)

# Merge
df = pd.merge(df_preds, df_labels, on="commit_hash")

# Klassifizieren mit Schwelle 0.5
df["predicted_label"] = (df["bugfix_probability"] >= 0.95).astype(int)

# Confusion Matrix
print("=== Confusion Matrix ===")
cm = confusion_matrix(df["label"], df["predicted_label"])
print(cm)

# Klassifikationsreport
print("\n=== Classification Report ===")
print(classification_report(df["label"], df["predicted_label"], digits=3))

# False Negatives analysieren
false_negatives = df[(df["label"] == 1) & (df["predicted_label"] == 0)]
print(f"\nFalse Negatives (true bugfix, predicted non-bugfix): {len(false_negatives)}")
print(false_negatives[["commit_hash", "bugfix_probability"]].head(10))
