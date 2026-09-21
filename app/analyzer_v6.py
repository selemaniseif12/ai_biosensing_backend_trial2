from app.ml.ml_integration import classify_features

def extract_features(data):
    # Replace with your real feature extraction logic
    return [float(x) for x in data]

def analyze_v6(data):
    features = extract_features(data)
    ml_result = classify_features(features)

    return {
        "features": features,
        "prediction": ml_result["prediction"],
        "confidence": ml_result["confidence"]
    }
