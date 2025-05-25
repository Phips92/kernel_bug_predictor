import pandas as pd
import numpy as np
import sys
import joblib
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Usage: python visualize_model_evaluation.py <features_csv>")
    sys.exit(1)

csv_path = sys.argv[1]
df = pd.read_csv(csv_path)

drop_cols = ["commit_hash", "author", "committer", "author_date", "commit_date", "label"]
X = df.drop(columns=[col for col in drop_cols if col in df.columns])
y = df["label"]

# Load scaler
scaler = joblib.load("models/scaler.pkl")
X_scaled = scaler.transform(X)

# Load model
model = load_model("models/bugfix_model.keras")

# Predict
y_pred_proba = model.predict(X_scaled).flatten()
y_pred = (y_pred_proba >= 0.7).astype(int)

# Evaluation
print("\n=== Evaluation ===")
print("Confusion Matrix:")
print(confusion_matrix(y, y_pred))
print("\nClassification Report:")
print(classification_report(y, y_pred, digits=3))
print("ROC AUC:", roc_auc_score(y, y_pred_proba))

# Plot ROC curve
fpr, tpr, _ = roc_curve(y, y_pred_proba)
plt.figure()
plt.plot(fpr, tpr, label="ROC Curve (AUC = {:.3f})".format(roc_auc_score(y, y_pred_proba)))
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("roc_curve.png")
print("Saved ROC curve to roc_curve.png")

# Plot model architecture
plot_model(model, show_shapes=True, to_file="model_architecture.png")
print("Saved model architecture to model_architecture.png")


plt.hist(y_pred_proba[y == 1], bins=30, alpha=0.7, label="True Bugfixes")
plt.hist(y_pred_proba[y == 0], bins=30, alpha=0.7, label="Non-Bugfixes")
plt.legend()
plt.xlabel("Predicted Probability")
plt.title("Prediction Distribution by Class")
plt.savefig("prediction_histogram_by_class.png")
print("Saved bug prediction histogram to prediction_histogram_by_class.png")









