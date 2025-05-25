import pandas as pd
import sys

if len(sys.argv) != 4:
    print("Usage: python merge_predictions_and_labels.py <pred_csv> <tool_label_csv> <output_csv>")
    sys.exit(1)

pred_path = sys.argv[1]
tool_path = sys.argv[2]
output_path = sys.argv[3]

# Load both
df_pred = pd.read_csv(pred_path)
df_tool = pd.read_csv(tool_path)

# Merge on commit_hash
merged = pd.merge(df_pred, df_tool, on="commit_hash", how="inner")

print(f"Merged {len(merged)} entries.")

# Save
merged.to_csv(output_path, index=False)
print(f"Saved merged file to {output_path}")
