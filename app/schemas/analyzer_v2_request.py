from pydantic import BaseModel, Field
from typing import List, Optional

# ---------------------------------------------------------
# ANALYZER V2 REQUEST SCHEMA
# ---------------------------------------------------------

class AnalyzerV2Request(BaseModel):
    """Schema for analyzer v2 request payload."""
    sample_id: str = Field(..., description="Unique identifier for the sample")
    sensor_data: List[float] = Field(..., description="List of sensor readings from QCM biosensor")
    model_version: Optional[str] = Field("v2", description="Version of ML model to use for analysis")
    metadata: Optional[dict] = Field(None, description="Additional metadata for advanced analysis")


# ---------------------------------------------------------
# ANALYZER V2 RESPONSE SCHEMA
# ---------------------------------------------------------

class AnalyzerV2Response(BaseModel):
    """Schema for analyzer v2 response payload."""
    sample_id: str = Field(..., description="Unique identifier for the sample")
    classification: str = Field(..., description="Predicted class or pathogen type")
    confidence: float = Field(..., description="Prediction confidence score")
    model_version: str = Field(..., description="Version of ML model used")
    timestamp: Optional[str] = Field(None, description="Time of analysis completion")
    notes: Optional[str] = Field(None, description="Additional notes or comments from analyzer")
