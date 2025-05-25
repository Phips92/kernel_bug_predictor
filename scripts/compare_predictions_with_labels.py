import pandas as pd
import sys

if len(sys.argv) != 3:
    print("Usage: python compare_predictions_with_labels.py <features_with_label_csv> <predictions_csv>")
    sys.exit(1)

features_path = sys.argv[1]
pred_path = sys.argv[2]

# Load both files
df_labels = pd.read_csv(features_path)[["commit_hash", "label"]]
df_preds = pd.read_csv(pred_path)

# Merge on commit_hash
df = pd.merge(df_preds, df_labels, on="commit_hash")

# Filter predictions == 1.0
df_ones = df[df["bugfix_probability"] == 1.0]

# Analyse
correct = df_ones[df_ones["label"] == 1]
incorrect = df_ones[df_ones["label"] == 0]

print("=== Analyse of Bugfix-Predictions with Score 1.0 ===")
print(f"Number Commits with Score 1.0:       {len(df_ones)}")
print(f"Correctly labeled (label=1): {len(correct)}")
print(f"Incorrectly labeled (label=0):  {len(incorrect)}")


