from pydantic import BaseModel, Field
from datetime import datetime

# ---------------------------------------------------------
# CREATE USAGE LOG
# ---------------------------------------------------------
class UsageCreate(BaseModel):
    customer_id: int = Field(..., description="ID of the customer making the request")
    endpoint: str = Field(..., description="API endpoint accessed")
    method: str = Field(..., description="HTTP method used")
    status_code: int = Field(..., description="Response status code")
    response_time_ms: float = Field(..., description="Response time in milliseconds")


# ---------------------------------------------------------
# USAGE LOG RESPONSE
# ---------------------------------------------------------
class UsageResponse(BaseModel):
    id: int
    customer_id: int
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    timestamp: datetime

    class Config:
        from_attributes = True
