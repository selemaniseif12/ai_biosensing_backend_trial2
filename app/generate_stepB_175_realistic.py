import pandas as pd
import numpy as np

OUTPUT_PATH = "app/training_v6_stepB_175_realistic.csv"

NUM_VIRUSES = 175
SAMPLES_PER_VIRUS = 700

rng = np.random.default_rng(42)

def generate_virus_profile(virus_id):
    # Each virus gets its own "center" in feature space
    base_temp = rng.uniform(18, 35)
    base_humidity = rng.uniform(15, 60)
    base_mass = rng.uniform(0.00003, 0.00020)
    base_freq = rng.uniform(1_693_850, 1_694_150)

    return {
        "base_temp": base_temp,
        "base_humidity": base_humidity,
        "base_mass": base_mass,
        "base_freq": base_freq,
    }

def generate_sample(virus_id, profile):
    deposition_rate = rng.normal(0.4, 0.05)
    temperature = rng.normal(profile["base_temp"], 1.0)
    humidity = rng.normal(profile["base_humidity"], 3.0)
    flow_rate = rng.normal(1.5, 0.15)
    time_to_detection = rng.normal(16, 2.0)

    mass_of_virus_fg = rng.normal(profile["base_mass"], profile["base_mass"] * 0.1)
    mass_of_virus_fg = max(mass_of_virus_fg, 0.00001)

    device_id = rng.choice([100, 101, 102, 103])

    delta_m_fg = mass_of_virus_fg * rng.uniform(0.9, 1.1)

    measured_frequency_hz = rng.normal(profile["base_freq"], 20.0)
    delta_f_hz = rng.normal(3.0, 0.7)
    noise_hz = rng.normal(1.0, 0.3)

    q_factor = rng.normal(5000, 120)
    harmonic_strength = rng.normal(0.6, 0.15)
    signal_to_noise_ratio = rng.normal(25, 5.0)
    allan_deviation = rng.normal(0.00003, 0.000005)

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
        "virus_id": virus_id,
    }

def generate_dataset():
    rows = []
    print("Generating realistic synthetic Step‑B dataset for 175 viruses...")

    profiles = {
        virus_id: generate_virus_profile(virus_id)
        for virus_id in range(1, NUM_VIRUSES + 1)
    }

    for virus_id in range(1, NUM_VIRUSES + 1):
        profile = profiles[virus_id]
        for _ in range(SAMPLES_PER_VIRUS):
            rows.append(generate_sample(virus_id, profile))

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Dataset created successfully: {OUTPUT_PATH}")
    print(f"Total samples: {len(df)}")

if __name__ == "__main__":
    generate_dataset()
