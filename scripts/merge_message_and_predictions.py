import pandas as pd
import sys

if len(sys.argv) != 4:
    print("Usage: python merge_features_and_predictions.py <features_with_message.csv> <predictions.csv> <output_merged.csv>")
    sys.exit(1)

features_path = sys.argv[1]
predictions_path = sys.argv[2]
output_path = sys.argv[3]


df_features = pd.read_csv(features_path)[["commit_hash", "message"]]  
df_predictions = pd.read_csv(predictions_path)


df = pd.merge(df_predictions, df_features, on="commit_hash", how="left")


df.to_csv(output_path, index=False)
print(f"Merged file saved to {output_path}")

