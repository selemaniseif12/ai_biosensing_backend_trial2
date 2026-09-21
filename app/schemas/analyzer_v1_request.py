from pydantic import BaseModel, Field
from typing import List, Optional

# ---------------------------------------------------------
# ANALYZER V1 REQUEST SCHEMA
# ---------------------------------------------------------

class AnalyzerV1Request(BaseModel):
    """Schema for analyzer v1 request payload."""
    sample_id: str = Field(..., description="Unique identifier for the sample")
    sensor_data: List[float] = Field(..., description="List of sensor readings from QCM biosensor")
    model_version: Optional[str] = Field(None, description="Version of ML model to use for analysis")


# ---------------------------------------------------------
# ANALYZER V1 RESPONSE SCHEMA
# ---------------------------------------------------------

class AnalyzerV1Response(BaseModel):
    """Schema for analyzer v1 response payload."""
    sample_id: str = Field(..., description="Unique identifier for the sample")
    classification: str = Field(..., description="Predicted class or pathogen type")
    confidence: float = Field(..., description="Prediction confidence score")
    timestamp: Optional[str] = Field(None, description="Time of analysis completion")
