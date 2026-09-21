from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.schema import Sequence
from app.database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, Sequence('analysis_results_id_seq'), primary_key=True, index=True)

    sample_id = Column(String, index=True)
    analyzer_version = Column(String)
    resonance_frequency_hz = Column(Float)
    frequency_shift_hz = Column(Float)
    damping_factor = Column(Float)
    quality_factor = Column(Float)
    noise_index = Column(Float)
    stability_index = Column(Float)
    ml_version = Column(String, nullable=True)
    pathogen_label = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    binding_probability = Column(Float, nullable=True)
    signal_quality = Column(String, nullable=True)
