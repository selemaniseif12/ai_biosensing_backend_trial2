from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class DeviceGeometry:
    device_id: int
    frequency_mhz: float
    diameter_mm: float
    dot_electrode_diameter_mm: float
    chromium_nm: float
    gold_nm: float
    quartz_thickness_mm: float


@dataclass
class DeviceOutput:
    device_id: int
    frequency_mhz: float
    delta_f_mhz: float  # Δf (Af)
    am_g_per_cm2: float  # Am (g/cm²) from table
    mass_g: float        # m (g)


# ---- Patent 1 Table 1a: Input parameters ----
DEVICE_GEOMETRY: Dict[int, DeviceGeometry] = {
    1: DeviceGeometry(1, 1.694, 1.0, 10.0, 50.0, 300.0, 1.0),
    2: DeviceGeometry(2, 1.694, 2.0, 10.0, 50.0, 300.0, 1.0),
    3: DeviceGeometry(3, 1.694, 3.0, 10.0, 50.0, 300.0, 1.0),
    4: DeviceGeometry(4, 1.694, 4.0, 10.0, 50.0, 300.0, 1.0),
    5: DeviceGeometry(5, 1.694, 5.0, 10.0, 50.0, 300.0, 1.0),
}

# ---- Patent 1 Table 1b: Output parameters ----
# NOTE: These Af / Am / m values are taken from your patent table.
# If any OCR typos exist, you can correct the numbers here without changing the logic.
DEVICE_OUTPUTS: Dict[int, DeviceOutput] = {
    1: DeviceOutput(
        device_id=1,
        frequency_mhz=1.694,
        delta_f_mhz=4.47e-6,
        am_g_per_cm2=1.2e-1,
        mass_g=4.55e-6,
    ),
    2: DeviceOutput(
        device_id=2,
        frequency_mhz=1.694,
        delta_f_mhz=1.15e-10,   # check against original PDF if needed
        am_g_per_cm2=1.23e-15,
        mass_g=1.82e-5,
    ),
    3: DeviceOutput(
        device_id=3,
        frequency_mhz=1.694,
        delta_f_mhz=3.73e-8,
        am_g_per_cm2=9e-13,
        mass_g=4.09e-5,
    ),
    4: DeviceOutput(
        device_id=4,
        frequency_mhz=1.694,
        delta_f_mhz=1.63e-8,    # check against original PDF if needed
        am_g_per_cm2=7e-13,
        mass_g=7.27e-5,
    ),
    5: DeviceOutput(
        device_id=5,
        frequency_mhz=1.694,
        delta_f_mhz=7.43e-8,    # check against original PDF if needed
        am_g_per_cm2=5e-13,
        mass_g=1.14e-4,
    ),
}


def analyze_device_v1(device_id: int) -> Dict[str, Any]:
    """
    Analyzer 1 (Patent 1):
    Uses Δf/f = Δm/m  →  Δm = (Δf / f) * m
    Returns full report: geometry + table outputs + computed Δm and Δm/cm².
    """
    if device_id not in DEVICE_GEOMETRY or device_id not in DEVICE_OUTPUTS:
        raise ValueError(f"Device ID {device_id} not defined in Patent 1 tables.")

    geom = DEVICE_GEOMETRY[device_id]
    out = DEVICE_OUTPUTS[device_id]

    f_hz = geom.frequency_mhz  # MHz, but ratio Δf/f is unitless so we can keep MHz consistently
    delta_f = out.delta_f_mhz
    m = out.mass_g

    # Patent equation: Δm = (Δf / f) * m
    delta_m_g = (delta_f / f_hz) * m

    # If you want Δm/cm², you can relate it to Am or compute from geometry.
    # For now, we report both the table Am and the computed Δm.
    result: Dict[str, Any] = {
        "device_id": geom.device_id,
        "frequency_mhz": geom.frequency_mhz,
        "diameter_mm": geom.diameter_mm,
        "dot_electrode_diameter_mm": geom.dot_electrode_diameter_mm,
        "chromium_nm": geom.chromium_nm,
        "gold_nm": geom.gold_nm,
        "quartz_thickness_mm": geom.quartz_thickness_mm,
        "delta_f_mhz": out.delta_f_mhz,
        "mass_g": out.mass_g,
        "am_g_per_cm2_table": out.am_g_per_cm2,
        "computed_delta_m_g": delta_m_g,
    }

    return result
