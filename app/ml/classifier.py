from app.ml.model_loader import load_rf

EXPECTED_FEATURES = 8  # your model expects 8 inputs

def classify(features, version: str | None = None):
    print("DEBUG: classify() called with features:", features)

    # Validate input length
    if len(features) != EXPECTED_FEATURES:
        raise ValueError(
            f"Model expects {EXPECTED_FEATURES} features, but received {len(features)}"
        )

    rf = load_rf(version=version)
    if rf is None:
        raise ValueError("RF model failed to load")

    pred = rf.predict([features])
    print("DEBUG: Prediction result:", pred)

    return "Positive" if pred[0] > 0.5 else "Negative"
