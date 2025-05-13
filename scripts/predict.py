import pandas as pd
import numpy as np
import sys
import joblib
from tensorflow.keras.models import load_model

if len(sys.argv) != 3:
    print("Usage: python predict.py <input_features_csv> <output_predictions_csv>")
    sys.exit(1)

input_csv = sys.argv[1]
output_csv = sys.argv[2]

df = pd.read_csv(input_csv)

# Keep commit_hash for output
ids = df["commit_hash"]

# Drop unused / non-numeric columns
drop_cols = ["commit_hash", "author", "committer", "author_date", "commit_date", "label"]
X = df.drop(columns=[col for col in drop_cols if col in df.columns])

# Load scaler and apply
scaler = joblib.load("models/scaler.pkl")
X_scaled = scaler.transform(X)

# Load model
model = load_model("models/bugfix_model.keras")

# Predict
y_pred_proba = model.predict(X_scaled).flatten()

# Combine result
output = pd.DataFrame({
    "commit_hash": ids,
    "bugfix_probability": y_pred_proba
})

# Save
output.to_csv(output_csv, index=False)
print(f"Predictions saved to {output_csv}")
