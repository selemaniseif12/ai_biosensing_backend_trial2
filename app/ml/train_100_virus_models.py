import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------
# Generate physics-based dataset using your real formulas
# ---------------------------------------------------------

def generate_physics_table(num_viruses=100, samples_per_virus=150):
    np.random.seed(42)

    X = []
    y = []

    for virus_id in range(1, num_viruses + 1):

        # Your real sensor baseline frequency
        base_freq = 1_693_998.5421410522 + np.random.uniform(-200, 200)

        # Your real mass sensitivity constant
        mass_sens = 0.000001 + np.random.uniform(-0.0000002, 0.0000002)

        for _ in range(samples_per_virus):

            # Virus-specific mass change
            delta_m = (virus_id * 0.0001) + np.random.uniform(-0.00002, 0.00002)

            # delta_m / m (mass ratio)
            delta_m_over_m = delta_m / 1.0  # assume normalized mass = 1

            # Δf = S_m * f0 * (Δm/m)
            delta_f_hz = mass_sens * base_freq * delta_m_over_m

            # Noise (your real API noise)
            noise_hz = np.random.uniform(0.5, 3.0)

            # Measured frequency
            measured_frequency_hz = base_freq + delta_f_hz + noise_hz

            # Quality factor (virus dependent)
            quality_factor = 5000 - (virus_id * 5) + np.random.uniform(-10, 10)

            X.append([
                base_freq,
                mass_sens,
                delta_m,
                delta_m_over_m,
                delta_f_hz,
                noise_hz,
                measured_frequency_hz,
                quality_factor
            ])

            y.append(virus_id)

    return np.array(X), np.array(y)


# ---------------------------------------------------------
# Generate the table
# ---------------------------------------------------------

X, y = generate_physics_table()

print("Physics-based 8-column table generated:")
print("X shape:", X.shape)
print("y shape:", y.shape)

# ---------------------------------------------------------
# Train/Test Split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)

# ---------------------------------------------------------
# MODEL VERSION V2 (RandomForest)
# ---------------------------------------------------------

print("Training V2 model...")

model_v2 = RandomForestClassifier(
    n_estimators=600,
    random_state=42,
    n_jobs=-1
)

model_v2.fit(X_train, y_train)
joblib.dump(model_v2, "sim_model_v2_100.pkl")

# ---------------------------------------------------------
# MODEL VERSION V6 (GradientBoosting)
# ---------------------------------------------------------

print("Training V6 model...")

model_v6 = GradientBoostingClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

model_v6.fit(X_train, y_train)
joblib.dump(model_v6, "sim_model_v6_100.pkl")

print("Training complete.")
