# ============================================================
# File: sensor_simulate.py
# Description: Realistic high‑precision biosensor simulation
# Author: Selemani
# ============================================================

from fastapi import APIRouter
import random
import math

router = APIRouter()

# ------------------------------------------------------------
# Helper: realistic resonator frequency generator
# ------------------------------------------------------------
def generate_measured_frequency():
    """
    Generates a realistic resonator frequency around 1.694 MHz
    with high‑precision noise and no trailing zeros.
    """

    # Base resonator frequency (±800 Hz drift)
    base_freq = 1_694_000 + random.uniform(-800, 800)

    # High‑precision noise (±1 micro‑Hz)
    noise = random.uniform(-0.000001, 0.000001)

    measured = base_freq + noise

    # Format with 12 decimal digits
    measured_str = f"{measured:.12f}"

    # Ensure no trailing zeros in decimal part
    measured_str = measured_str.rstrip("0").rstrip(".")

    return float(measured_str), base_freq, noise


# ------------------------------------------------------------
# Main Simulation Endpoint
# ------------------------------------------------------------
@router.get("/sensor/simulate")
def simulate_sensor(virus_id: int, device_id: int):
    """
    Generates realistic Step‑B physics values for biosensing.
    Used internally by:
      - /classify/stepB
      - /detect/realtime
      - /detect/live-stream
    """

    # Generate realistic resonator frequency
    measured_frequency_hz, base_freq, noise = generate_measured_frequency()

    # Δf = measured - base
    delta_f_hz = measured_frequency_hz - base_freq

    # Noise magnitude
    noise_hz = abs(noise)

    # Realistic Q-factor (80–120)
    q_factor = random.uniform(80, 120)

    # Harmonic strength (0.3–0.8)
    harmonic_strength = random.uniform(0.3, 0.8)

    # Signal-to-noise ratio (10–30)
    signal_to_noise_ratio = random.uniform(10, 30)

    # Allan deviation (1e‑9 to 1e‑7)
    allan_deviation = random.uniform(1e-9, 1e-7)

    # Device sensitivity (placeholder — real value comes from device DB)
    delta_m_fg = random.uniform(0.00000001, 0.000001)

    return {
        "virus_id": virus_id,
        "device_id": device_id,

        # High‑precision resonator physics
        "measured_frequency_hz": measured_frequency_hz,
        "delta_f_hz": delta_f_hz,
        "noise_hz": noise_hz,

        # Additional physics features
        "q_factor": q_factor,
        "harmonic_strength": harmonic_strength,
        "signal_to_noise_ratio": signal_to_noise_ratio,
        "allan_deviation": allan_deviation,

        # Device mass sensitivity (fg)
        "delta_m_fg": delta_m_fg,

        "message": "Realistic high‑precision sensor simulation completed."
    }
