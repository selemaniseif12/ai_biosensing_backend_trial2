from datetime import datetime
from typing import List
import random

def analyze_signal_v2(raw_signal: List[float], sampling_rate: float):
    """
    Dummy ML classifier for V2 analysis.
    Replace with real model later.
    """
    # Fake classification logic
    classification = random.choice(["bacteria", "virus", "clean"])
    score = round(random.uniform(0.7, 0.99), 3)

    return {
        "classification": classification,
        "score": score,
        "timestamp": datetime.utcnow()
    }
