import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from physics_engine import simulate_physics_event

# Generate dataset
def generate_dataset(num_viruses=100, samples_per_virus=200):
    X = []
    y = []

    for virus_id in range(1, num_viruses + 1):
        for _ in range(samples_per_virus):
            features = simulate_physics_event(virus_id)
            X.append(features)
            y.append(virus_id - 1)  # shift labels

    return np.array(X), np.array(y)

X, y = generate_dataset()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)

os.makedirs("app/ml/models/classify/v2", exist_ok=True)
os.makedirs("app/ml/models/classify/v6", exist_ok=True)

# Train V2
model_v2 = RandomForestClassifier(n_estimators=600, n_jobs=-1)
model_v2.fit(X_train, y_train)
joblib.dump(model_v2, "app/ml/models/classify/v2/sim_model_v2_100.pkl")

# Train V6
model_v6 = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="multi:softprob",
    num_class=100,
    tree_method="hist"
)
model_v6.fit(X_train, y_train)
joblib.dump(model_v6, "app/ml/models/classify/v6/sim_model_v6_100.pkl")

print("=== TRAINING COMPLETE ===")
