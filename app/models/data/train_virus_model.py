import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ============================================================
# 1. Load dataset
# ============================================================

CSV_PATH = "app/models/data/virus_multiclass.csv"
print(f"Loading dataset from: {CSV_PATH}")

df = pd.read_csv(CSV_PATH, encoding="utf-8", engine="python")
print("CSV loaded successfully!")
print("Initial dataset shape:", df.shape)

label_column = "virus_name"

# ============================================================
# 2. Remove NaN labels ONLY
# ============================================================

df = df.dropna(subset=[label_column])
print("After removing NaN labels:", df.shape)

# ============================================================
# 3. Select numeric features
# ============================================================

feature_columns = [
    "mass_fg",
    "frequency_mhz",
    "deposition_rate_s",
    "temperature_c",
    "humidity_pct",
    "flow_rate",
    "time_to_detection_s"
]

X = df[feature_columns].values
y = df[label_column].values

print("Feature matrix shape:", X.shape)
print("Labels shape:", y.shape)

# ============================================================
# 4. Train on FULL dataset (no split)
# ============================================================

clf = RandomForestClassifier(
    n_estimators=500,
    max_depth=30,
    min_samples_split=2,
    min_samples_leaf=1,
    bootstrap=True,
    random_state=42
)

print("Training model on FULL dataset...")
clf.fit(X, y)
print("Training complete!")

# ============================================================
# 5. Evaluate using training accuracy (only option)
# ============================================================

y_pred = clf.predict(X)
acc = accuracy_score(y, y_pred)
print(f"Training accuracy: {acc * 100:.2f}%")

# ============================================================
# 6. Clean class labels for FastAPI router
# ============================================================

clf.classes_ = np.arange(len(clf.classes_))
print("Cleaned class labels:", clf.classes_)

# ============================================================
# 7. Save model
# ============================================================

MODEL_PATH = "app/models/virus_multiclassify_V7_175.pkl"
joblib.dump(clf, MODEL_PATH)

print(f"Model saved as {MODEL_PATH}")
