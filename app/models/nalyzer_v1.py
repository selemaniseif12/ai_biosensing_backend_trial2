from sqlalchemy import Column, Integer, Float
from app.db_core import Base

class Analyzer1Device(Base):
    __tablename__ = "analyzer1_devices"

    device_id = Column(Integer, primary_key=True, index=True)

    # Input parameters
    frequency_mhz = Column(Float)
    center_electrode_mm = Column(Float)
    diameter_mm = Column(Float)
    chromium_nm = Column(Float)
    gold_nm = Column(Float)
    thickness_mm = Column(Float)

    # Output parameters
    delta_f_mhz = Column(Float)
    m_g = Column(Float)
