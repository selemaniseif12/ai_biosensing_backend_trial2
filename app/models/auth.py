from pydantic import BaseModel

class APIKeyRequest(BaseModel):
    api_key: str

class APIKeyValidationResponse(BaseModel):
    valid: bool
    customer_id: int | None = None
    message: str
