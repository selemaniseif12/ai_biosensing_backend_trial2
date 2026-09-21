import pandas as pd
import numpy as np

OUTPUT_PATH = "app/training_v6_stepB_175.csv"

NUM_VIRUSES = 175
SAMPLES_PER_VIRUS = 700   # 175 × 700 ≈ 122,500 samples

def generate_stepB_sample(virus_id):
    # Physics-based synthetic ranges (matching v6 Step B)
    deposition_rate = np.random.uniform(0.25, 0.55)
    temperature = np.random.uniform(18, 35)
    humidity = np.random.uniform(15, 60)
    flow_rate = np.random.uniform(1.0, 2.0)
    time_to_detection = np.random.uniform(10, 22)

    # Virus mass (fg) — realistic ranges
    mass_of_virus_fg = np.random.uniform(0.00002, 0.00025)

    # Device ID (categorical encoded as integer)
    device_id = np.random.choice([100, 101, 102, 103])

    # Delta mass (fg)
    delta_m_fg = mass_of_virus_fg * np.random.uniform(0.8, 1.2)

    # Measured frequency (Hz)
    measured_frequency_hz = np.random.uniform(1_693_800, 1_694_200)

    # Delta frequency (Hz)
    delta_f_hz = np.random.uniform(0.5, 5.0)

    # Noise (Hz)
    noise_hz = np.random.uniform(0.2, 3.0)

    # Quality factor
    q_factor = np.random.uniform(4800, 5200)

    # Harmonic strength
    harmonic_strength = np.random.uniform(0.1, 1.0)

    # Signal-to-noise ratio
    signal_to_noise_ratio = np.random.uniform(10, 40)

    # Allan deviation
    allan_deviation = np.random.uniform(0.00001, 0.00005)

    return {
        "deposition_rate": deposition_rate,
        "temperature": temperature,
        "humidity": humidity,
        "flow_rate": flow_rate,
        "time_to_detection": time_to_detection,
        "mass_of_virus_fg": mass_of_virus_fg,
        "device_id": device_id,
        "delta_m_fg": delta_m_fg,
        "measured_frequency_hz": measured_frequency_hz,
        "delta_f_hz": delta_f_hz,
        "noise_hz": noise_hz,
        "q_factor": q_factor,
        "harmonic_strength": harmonic_strength,
        "signal_to_noise_ratio": signal_to_noise_ratio,
        "allan_deviation": allan_deviation,
        "virus_id": virus_id
    }


def generate_dataset():
    rows = []

    print("Generating synthetic Step‑B dataset for 175 viruses...")

    for virus_id in range(1, NUM_VIRUSES + 1):
        for _ in range(SAMPLES_PER_VIRUS):
            rows.append(generate_stepB_sample(virus_id))

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Dataset created successfully: {OUTPUT_PATH}")
    print(f"Total samples: {len(df)}")


if __name__ == "__main__":
    generate_dataset()
