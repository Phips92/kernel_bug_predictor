import pandas as pd
import numpy as np
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers

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

