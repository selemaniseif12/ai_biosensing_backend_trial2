import pandas as pd
import numpy as np
import random
from fft_features import extract_fft_features


BASE_FREQUENCY_HZ = 1693998.5421410522

def simulate_sample(virus_id):
    # Generate time-series noise (64 samples)
    noise_series = np.random.normal(0, 1.5, 64)

    # FFT features
    fft_features = extract_fft_features(noise_series)

    # Physics features
    noise = noise_series[-1]
    delta_f = noise
    measured_f = BASE_FREQUENCY_HZ + delta_f

    return {
        "base_frequency_hz": BASE_FREQUENCY_HZ,
        "noise_hz": noise,
        "delta_f_hz": delta_f,
        "measured_frequency_hz": measured_f,
        **{f"fft_{i}": fft_features[i] for i in range(10)},
        "virus_id": virus_id
    }

def build_dataset(n=5000):
    rows = []
    for _ in range(n):
        virus_id = random.choice([1, 12, 37, 5])
        rows.append(simulate_sample(virus_id))

    df = pd.DataFrame(rows)
    df.to_csv("app/ml/simulation_training_data.csv", index=False)
    print("Saved simulation_training_data.csv with", len(df), "rows")

if __name__ == "__main__":
    build_dataset()
