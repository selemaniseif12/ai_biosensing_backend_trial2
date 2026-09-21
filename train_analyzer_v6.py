# train_analyzer_v6.py

import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# 1) Load data
df = pd.read_csv("data/analyzer_v6_training_data.csv")

# 2) Features and target
feature_cols = [
    "deposition_rate",
    "temperature",
    "humidity",
    "flow_rate",
    "mass_of_virus",
]

X = df[feature_cols]
y = df["time_to_detection"]

# 3) Train/validation split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4) Model
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=None,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

# 5) Quick evaluation
y_pred = model.predict(X_val)
print("R2:", r2_score(y_val, y_pred))
print("MAE:", mean_absolute_error(y_val, y_pred))

# 6) Save model
dump(model, "app/models/analyzer_v6_model.joblib")
print("Saved model to app/models/analyzer_v6_model.joblib")
