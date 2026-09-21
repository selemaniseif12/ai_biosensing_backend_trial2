import csv
import random
import math
import requests

BASE_URL = "http://127.0.0.1:8000"

VIRUS_TABLE_CSV = "ML Model Analyzer v6 Table.csv"
V2_OUTPUT_CSV = "training_v2_stepB.csv"
V6_OUTPUT_CSV = "training_v6_stepB.csv"

# how many simulations per virus for v2 and v6
SIMS_PER_VIRUS_V2 = 120
SIMS_PER_VIRUS_V6 = 1200


def get_devices():
    resp = requests.get(f"{BASE_URL}/device/all")
    resp.raise_for_status()
    devices = resp.json()
    # map: device_id -> delta_m_fg (mass sensitivity)
    return {d["id"]: d["sensitivity_fg"] for d in devices}


def sensor_simulate(virus_id: int, device_id: int, phys_params: dict, delta_m_fg: float):
    """
    If you already have /sensor/simulate, you can call it here instead of this stub.
    This stub shows the structure you need.
    """
    # Example: call your real endpoint
    resp = requests.get(
        f"{BASE_URL}/sensor/simulate",
        params={"virus_id": virus_id, "device_id": device_id},
    )
    resp.raise_for_status()
    data = resp.json()

    # data is expected to contain:
    # base_frequency_hz, noise_hz, delta_f_hz, measured_frequency_hz
    # You can extend your endpoint to also return q_factor, harmonic_strength, snr, allan_dev
    return {
        "measured_frequency_hz": data["measured_frequency_hz"],
        "delta_f_hz": data["delta_f_hz"],
        "noise_hz": data["noise_hz"],
        "q_factor": data.get("q_factor", random.uniform(50, 150)),
        "harmonic_strength": data.get("harmonic_strength", random.uniform(0.1, 1.0)),
        "signal_to_noise_ratio": data.get("signal_to_noise_ratio", random.uniform(5, 50)),
        "allan_deviation": data.get("allan_deviation", random.uniform(1e-9, 1e-6)),
        "delta_m_fg": delta_m_fg,
    }


def read_virus_table():
    rows = []
    with open(VIRUS_TABLE_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # expected columns from your CSV:
            # virus, device_id, deposition_rate, temperature, humidity,
            # flow_rate, time_to_detection, mass of virus (fg), ID
            rows.append({
                "virus_id": int(r["ID"]),
                "virus_name": r["virus"],
                "device_id": int(r["device_id"].replace("Device-", "").replace("Device‑", "")),
                "deposition_rate": float(r["deposition_rate"]),
                "temperature": float(r["temperature"]),
                "humidity": float(r["humidity"]),
                "flow_rate": float(r["flow_rate"]),
                "time_to_detection": float(r["time_to_detection"]),
                "mass_of_virus_fg": float(r["mass of virus (fg)"]),
            })
    return rows


def generate_table(output_csv: str, sims_per_virus: int):
    devices = get_devices()
    virus_rows = read_virus_table()

    fieldnames = [
        "virus_id",
        "virus_name",
        "device_id",
        "deposition_rate",
        "temperature",
        "humidity",
        "flow_rate",
        "time_to_detection",
        "mass_of_virus_fg",
        "delta_m_fg",
        "measured_frequency_hz",
        "delta_f_hz",
        "noise_hz",
        "q_factor",
        "harmonic_strength",
        "signal_to_noise_ratio",
        "allan_deviation",
    ]

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for vr in virus_rows:
            virus_id = vr["virus_id"]
            base_device_id = vr["device_id"]

            for _ in range(sims_per_virus):
                # you can randomize device choice or keep the one from the table
                device_id = base_device_id
                delta_m_fg = devices[device_id]

                phys_params = {
                    "deposition_rate": vr["deposition_rate"],
                    "temperature": vr["temperature"],
                    "humidity": vr["humidity"],
                    "flow_rate": vr["flow_rate"],
                    "time_to_detection": vr["time_to_detection"],
                    "mass_of_virus_fg": vr["mass_of_virus_fg"],
                }

                sim = sensor_simulate(virus_id, device_id, phys_params, delta_m_fg)

                row = {
                    "virus_id": virus_id,
                    "virus_name": vr["virus_name"],
                    "device_id": device_id,
                    "deposition_rate": vr["deposition_rate"],
                    "temperature": vr["temperature"],
                    "humidity": vr["humidity"],
                    "flow_rate": vr["flow_rate"],
                    "time_to_detection": vr["time_to_detection"],
                    "mass_of_virus_fg": vr["mass_of_virus_fg"],
                    "delta_m_fg": sim["delta_m_fg"],
                    "measured_frequency_hz": sim["measured_frequency_hz"],
                    "delta_f_hz": sim["delta_f_hz"],
                    "noise_hz": sim["noise_hz"],
                    "q_factor": sim["q_factor"],
                    "harmonic_strength": sim["harmonic_strength"],
                    "signal_to_noise_ratio": sim["signal_to_noise_ratio"],
                    "allan_deviation": sim["allan_deviation"],
                }

                writer.writerow(row)


if __name__ == "__main__":
    # v2 table (≈12,000 samples)
    generate_table(V2_OUTPUT_CSV, SIMS_PER_VIRUS_V2)

    # v6 table (≈120,000 samples)
    generate_table(V6_OUTPUT_CSV, SIMS_PER_VIRUS_V6)
