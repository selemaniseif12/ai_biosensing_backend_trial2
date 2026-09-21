from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from enum import Enum

router = APIRouter(prefix="/analyze", tags=["Analysis"])


class AnalyzerVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"
    V4 = "v4"


class MLVersion(str, Enum):
    RF = "random_forest"
    XGB = "xgboost"
    LSTM = "lstm"


class AnalyzerInput(BaseModel):
    sample_id: str
    raw_frequency: float
    raw_damping: float
    temperature_c: float
    overtone: int = 1
    analyzer_version: AnalyzerVersion = AnalyzerVersion.V3
    ml_version: Optional[MLVersion] = None


class AnalyzerOutput(BaseModel):
    id: int
    sample_id: str
    analyzer_version: AnalyzerVersion
    resonance_frequency_hz: float
    frequency_shift_hz: float
    damping_factor: float
    quality_factor: float
    noise_index: float
    stability_index: float
    ml_version: Optional[MLVersion]
    pathogen_label: Optional[str]
    confidence: Optional[float]
    binding_probability: Optional[float]
    signal_quality: Optional[str]


@router.post("", response_model=AnalyzerOutput)
def analyze_sample(payload: AnalyzerInput):

    resonance_frequency = payload.raw_frequency - (payload.overtone * 12.5)
    frequency_shift = payload.raw_frequency - resonance_frequency
    damping_factor = payload.raw_damping * 1.2
    quality_factor = resonance_frequency / (damping_factor + 1e-6)
    noise_index = abs(frequency_shift) / 1000
    stability_index = 1.0 / (1.0 + noise_index)

    pathogen_label = None
    confidence = None
    binding_probability = None
    signal_quality = None

    if payload.ml_version:
        pathogen_label = "E.coli"
        confidence = 0.87
        binding_probability = 0.91
        signal_quality = "High"

    return AnalyzerOutput(
        id=1,
        sample_id=payload.sample_id,
        analyzer_version=payload.analyzer_version,
        resonance_frequency_hz=resonance_frequency,
        frequency_shift_hz=frequency_shift,
        damping_factor=damping_factor,
        quality_factor=quality_factor,
        noise_index=noise_index,
        stability_index=stability_index,
        ml_version=payload.ml_version,
        pathogen_label=pathogen_label,
        confidence=confidence,
        binding_probability=binding_probability,
        signal_quality=signal_quality,
    )
