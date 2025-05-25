import shap
import joblib
import pandas as pd
import numpy as np
import sys
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

if len(sys.argv) != 4:
    print("Usage: python shap_analysis.py <features_csv> <model_path> <scaler_path>")
    sys.exit(1)

csv_path = sys.argv[1]
model_path = sys.argv[2]
scaler_path = sys.argv[3]

df = pd.read_csv(csv_path)

# Drop non-numeric columns
drop_cols = ["commit_hash", "author", "committer", "author_date", "commit_date", "label", "tool_found"]
X = df.drop(columns=[col for col in drop_cols if col in df.columns])
feature_names = X.columns

# Load scaler
scaler = joblib.load(scaler_path)
X_scaled = scaler.transform(X)

# Load model
model = load_model(model_path)

# subset for speed
X_sample = X_scaled[:10000]

# Explain with SHAP
explainer = shap.Explainer(model, X_sample)
shap_values = explainer(X_sample)

# Summary plot
shap.summary_plot(shap_values, features=X_sample, feature_names=feature_names, show=False)
plt.tight_layout()
plt.savefig("shap_summary_plot.png")
print("Saved SHAP summary plot to shap_summary_plot.png")
