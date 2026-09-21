import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split

# -----------------------------
# Load CSV
# -----------------------------
csv_path = "app/models/data/virus_multiclass.csv"
df = pd.read_csv(csv_path)

id_col = "virus_id"
target = "virus_id"

numeric_features = [
    "mass_fg",
    "frequency_mhz",
    "deposition_rate_s",
    "temperature_c",
    "humidity_pct",
    "flow_rate",
    "time_to_detection_s",
]

categorical_features = ["antibody", "antigen"]

# -----------------------------
# Recreate dataset (20 samples per virus)
# -----------------------------
def augment_row(row, n_samples=20):
    base_numeric = row[numeric_features].values.astype(float)
    cat_vals = row[categorical_features].values

    noise_scales = np.array([
        abs(0.10 * base_numeric[0]) if base_numeric[0] != 0 else 1e-6,
        0.0005,
        abs(0.15 * base_numeric[2]) if base_numeric[2] != 0 else 0.02,
        2.0,
        4.0,
        0.2,
        abs(0.15 * base_numeric[6]) if base_numeric[6] != 0 else 0.5,
    ])

    samples = []
    for _ in range(n_samples):
        noise = np.random.normal(0.0, noise_scales)
        noisy_numeric = base_numeric + noise

        sample_dict = {target: int(row[id_col])}
        for i, col in enumerate(numeric_features):
            sample_dict[col] = noisy_numeric[i]
        for j, col in enumerate(categorical_features):
            sample_dict[col] = cat_vals[j]

        samples.append(sample_dict)

    return samples

augmented_rows = []
for _, row in df.iterrows():
    augmented_rows.extend(augment_row(row, n_samples=20))

aug_df = pd.DataFrame(augmented_rows)

# -----------------------------
# Prepare data
# -----------------------------
X = aug_df[numeric_features + categorical_features]
y = aug_df[target]

# For XGBoost (V10)
y_shifted = y - 1

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

X_train10, X_test10, y_train10, y_test10 = train_test_split(
    X, y_shifted,
    test_size=0.2,
    stratify=y_shifted,
    random_state=42
)

# -----------------------------
# Load models
# -----------------------------
models = {
    "V7": "app/models/virus_multiclassify_V7_175_prob.pkl",
    "V8": "app/models/virus_multiclassify_V8_175_prob.pkl",
    "V10": "app/models/virus_multiclassify_V10_175_prob.pkl",
}

for name, path in models.items():
    print(f"\nLoading {name} model...")
    model = joblib.load(path)

    if name == "V10":
        acc = model.score(X_test10, y_test10)
    else:
        acc = model.score(X_test, y_test)

    print(f"{name} recovered accuracy: {acc:.3f}")
