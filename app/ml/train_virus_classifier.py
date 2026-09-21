import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

MODEL_PATH = "app/ml/models/virus_classifier.pkl"

def load_data():
    base_path = "app/ml/virus_tables"

    print(f"\n📁 Loading virus tables from: {base_path}\n")

    files = [
        "device1a.csv",
        "device1b.csv",
        "device1c.csv",
        "device1d.csv",
        "device1e.csv"
    ]

    tables = []

    for file in files:
        path = os.path.join(base_path, file)

        print(f"📄 Reading: {file}")
        df = pd.read_csv(path)
        print(f"   → {len(df)} rows loaded")

        df.columns = [c.strip().lower() for c in df.columns]

        rename_map = {
            "virus id": "virus_id",
            "mass of virus (fg)": "mass_fg",
            "mass (fg)": "mass_fg",
            "device id": "device_id",
            "device sensitivity (fg)": "device_sensitivity_fg",
            "virus counts per dvice": "virus_count_original",
            "virus counts per device": "virus_count_original"
        }

        df = df.rename(columns=rename_map)

        if "virus_count_computed" not in df.columns:
            df["virus_count_computed"] = df["virus_count_original"]

        numeric_cols = [
            "mass_fg",
            "device_sensitivity_fg",
            "virus_count_original",
            "virus_count_computed"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=numeric_cols)

        df["device_id"] = df["device_id"].astype(str)

        tables.append(df)

    data = pd.concat(tables, ignore_index=True)
    print(f"\n✅ TOTAL CLEAN ROWS LOADED: {len(data)}\n")
    return data


def build_features(df):
    X = df[[
        "virus",
        "antibody",
        "antigen",
        "mass_fg",
        "device_sensitivity_fg",
        "virus_count_original",
        "virus_count_computed",
        "device_id"
    ]]
    y = df["virus_id"]
    return X, y


def build_model():
    categorical = ["virus", "antibody", "antigen", "device_id"]
    numeric = [
        "mass_fg",
        "device_sensitivity_fg",
        "virus_count_original",
        "virus_count_computed"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric),
        ]
    )

    clf = RandomForestClassifier(
        n_estimators=500,
        random_state=42,
        class_weight="balanced"
    )

    return Pipeline([("preprocess", preprocessor), ("clf", clf)])


def train_and_save_model():
    df = load_data()
    X, y = build_features(df)

    stratify = y if y.value_counts().min() > 1 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify
    )

    model = build_model()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"\n🎉 Model saved at {MODEL_PATH}\n")


if __name__ == "__main__":
    train_and_save_model()
