from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SensorReading(BaseModel):
    """Model for incoming sensor reading requests."""
    vibration: float = Field(..., ge=0, le=10, description="Vibration in mm/s")
    current: float = Field(..., ge=0, le=50, description="Current in Amperes")
    temperature: float = Field(..., ge=-20, le=150, description="Temperature in Celsius")

    class Config:
        schema_extra = {
            "example": {
                "vibration": 1.5,
                "current": 12.3,
                "temperature": 65.2
            }
        }

class PredictionResponse(BaseModel):
    """Model for prediction response."""
    probability_of_failure: float = Field(..., ge=0, le=1, description="Probability of failure within 72 hours")
    timestamp: str = Field(..., description="Prediction timestamp")
    status: str = Field(..., description="Prediction status: success/error")
    confidence_level: Optional[str] = Field(None, description="Confidence level: high/medium/low")

    class Config:
        schema_extra = {
            "example": {
                "probability_of_failure": 0.75,
                "timestamp": "2024-01-15T10:30:00Z",
                "status": "success",
                "confidence_level": "high"
            }
        }

class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str = Field(..., description="API health status")
    timestamp: str = Field(..., description="Health check timestamp")
    model_loaded: bool = Field(..., description="Whether the ML model is loaded")
    version: str = Field(..., description="API version")

    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00Z",
                "model_loaded": True,
                "version": "1.0.0"
            }
        }

class ErrorResponse(BaseModel):
    """Model for error responses."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: str = Field(..., description="Error timestamp")
    status_code: int = Field(..., description="HTTP status code")

    class Config:
        schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "Vibration value out of range",
                "timestamp": "2024-01-15T10:30:00Z",
                "status_code": 422
            }
        }