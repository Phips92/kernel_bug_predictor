import pandas as pd
import numpy as np
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, classification_report, confusion_matrix
import joblib

if len(sys.argv) != 2:
    print("Usage: python train_model.py <features_csv>")
    sys.exit(1)

csv_path = sys.argv[1]
df = pd.read_csv(csv_path)

# Drop non-numeric and non-useful columns
drop_cols = ["commit_hash", "author", "committer", "author_date", "commit_date"]
X = df.drop(columns=drop_cols + ["label"])
y = df["label"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, stratify=y, random_state=42)

# Define Keras model
model = keras.Sequential([
    keras.Input(shape=(X_train.shape[1],)),
    layers.Dense(64, activation="relu"), 
    layers.Dropout(0.2),
    layers.Dense(32, activation="relu"),
    layers.Dropout(0.1),
    layers.Dense(1, activation="sigmoid")  # Binary classification
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy", keras.metrics.AUC(name="auc")]
)

# Train the model
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=10,
    batch_size=32,
    verbose=1
)

# Predict probabilities
y_pred_proba = model.predict(X_test).flatten()
y_pred = (y_pred_proba >= 0.5).astype(int)

# Eval-Metriken
print("\n=== Evaluation ===")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, digits=3))
print("ROC AUC:", roc_auc_score(y_test, y_pred_proba))


fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
plt.plot(fpr, tpr, label="ROC Curve (AUC = {:.3f})".format(roc_auc_score(y_test, y_pred_proba)))
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Save model
model.save("models/bugfix_model.keras")
print("Model saved to models/bugfix_model.keras")

# Save scaler
joblib.dump(scaler, "models/scaler.pkl")
print("Scaler saved to models/scaler.pkl")






