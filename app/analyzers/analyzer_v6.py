from app.ml.ml_integration import classify_features
from app.services.interpretation_service import interpret_result

def extract_features(data):
    return [float(x) for x in data]

def analyze_v6(data):
    features = extract_features(data)
    ml_result = classify_features(features)

    interpretation = interpret_result(
        prediction=ml_result["prediction"],
        confidence=ml_result["confidence"]
    )

    return {
        "features": features,
        "prediction": ml_result["prediction"],
        "confidence": ml_result["confidence"],
        "interpretation": interpretation
    }
