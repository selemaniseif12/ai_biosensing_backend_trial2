import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# -----------------------------
# Load original dataset
# -----------------------------
orig_df = pd.read_csv("app/models/data/virus_multiclass.csv")
print("Original CSV rows:", len(orig_df))

# -----------------------------
# Jitter helper
# -----------------------------
def jitter(value, pct):
    return value * (1 + np.random.uniform(-pct, pct))

# -----------------------------
# Augment: 20 samples per original row
# -----------------------------
rows = []

for _, row in orig_df.iterrows():
    virus_id = int(row["virus_id"])
    virus_name = str(row["virus_name"])
    antibody = str(row["antibody"])
    antigen = str(row["antigen"])

    mass_fg = float(row["mass_fg"])
    deposition_rate_s = float(row["deposition_rate_s"])
    temperature_c = float(row["temperature_c"])
    humidity_pct = float(row["humidity_pct"])
    flow_rate = float(row["flow_rate"])
    time_to_detection_s = float(row["time_to_detection_s"])
    frequency_mhz = float(row["frequency_mhz"])

    for _ in range(20):
        rows.append({
            "virus_id": virus_id,
            "virus_name": virus_name,
            "antibody": antibody,
            "antigen": antigen,
            "mass_fg": jitter(mass_fg, 0.10),
            "deposition_rate_s": jitter(deposition_rate_s, 0.05),
            "temperature_c": jitter(temperature_c, 0.02),
            "humidity_pct": jitter(humidity_pct, 0.05),
            "flow_rate": jitter(flow_rate, 0.10),
            "time_to_detection_s": jitter(time_to_detection_s, 0.10),
            "frequency_mhz": frequency_mhz,
        })

df = pd.DataFrame(rows)
print("Augmented dataset size:", len(df))

# -----------------------------
# Clean categorical columns
# -----------------------------
def clean_text_column(col):
    df[col] = df[col].astype(str)
    df[col] = df[col].str.replace(r"[^\x00-\x7F]+", "", regex=True)
    df[col] = df[col].str.strip()
    df[col] = df[col].astype("category").cat.codes

clean_text_column("antibody")
clean_text_column("antigen")
clean_text_column("virus_name")

df["virus_id"] = pd.to_numeric(df["virus_id"], errors="coerce").fillna(-1).astype(int)

# -----------------------------
# Features
# -----------------------------
features = [
    "mass_fg",
    "frequency_mhz",
    "deposition_rate_s",
    "temperature_c",
    "humidity_pct",
    "flow_rate",
    "time_to_detection_s",
    "antibody",
    "antigen",
    "virus_name",
]

X = df[features]
y = df["virus_id"]

if len(X) == 0:
    raise ValueError("Dataset is empty after processing.")

# -----------------------------
# Scale
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# Train/test split (stratified)
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# -----------------------------
# RandomForest
# -----------------------------
model = RandomForestClassifier(
    n_estimators=600,
    max_depth=None,
    class_weight="balanced",
    n_jobs=-1,
    random_state=42,
)

model.fit(X_train, y_train)

# -----------------------------
# Evaluate
# -----------------------------
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
print("Accuracy:", acc)

# -----------------------------
# Save
# -----------------------------
joblib.dump(model, "app/models/virus_multiclassify_V7_175.pkl")
joblib.dump(scaler, "app/models/virus_multiclassify_V7_175_scaler.pkl")

print("Model saved: Virus Multi-classify V7-175")
