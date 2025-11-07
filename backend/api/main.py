from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import os

from .models import SensorReading, PredictionResponse, HealthResponse, ErrorResponse
from .predictor import predictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ArogyaJal Predictive Maintenance API",
    description="API for predicting water pump failures using machine learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API status and model loading.
    """
    try:
        model_info = predictor.get_model_info()

        return HealthResponse(
            status="healthy" if predictor.model_loaded else "unhealthy",
            timestamp=datetime.now().isoformat(),
            model_loaded=model_info.get('model_loaded', False),
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unavailable: {str(e)}"
        )

@app.post("/api/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_failure(sensor_reading: SensorReading):
    """
    Predict the probability of pump failure within 72 hours based on sensor readings.

    - **vibration**: Vibration measurement in mm/s (0-10)
    - **current**: Current consumption in Amperes (0-50)
    - **temperature**: Temperature measurement in Celsius (-20 to 150)
    """
    try:
        logger.info(f"Prediction request: vibration={sensor_reading.vibration}, "
                   f"current={sensor_reading.current}, temperature={sensor_reading.temperature}")

        # Make prediction
        result = predictor.predict_failure_probability(
            vibration=sensor_reading.vibration,
            current=sensor_reading.current,
            temperature=sensor_reading.temperature,
            timestamp=datetime.now()
        )

        logger.info(f"Prediction result: {result}")

        if result['status'] == 'error':
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get('error', 'Prediction failed')
            )

        return PredictionResponse(
            probability_of_failure=result['probability_of_failure'],
            timestamp=result['timestamp'],
            status=result['status'],
            confidence_level=result.get('confidence_level')
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error during prediction: {str(e)}"
        )

@app.get("/api/model-info", tags=["Model"])
async def get_model_info():
    """
    Get information about the loaded machine learning model.
    """
    try:
        model_info = predictor.get_model_info()
        return model_info
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving model info: {str(e)}"
        )

@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    """Handle validation errors for invalid input data."""
    return {
        "error": "Validation Error",
        "detail": str(exc),
        "timestamp": datetime.now().isoformat(),
        "status_code": 422
    }

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {str(exc)}")
    return {
        "error": "Internal Server Error",
        "detail": "An unexpected error occurred",
        "timestamp": datetime.now().isoformat(),
        "status_code": 500
    }

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    logger.info("Starting ArogyaJal Predictive Maintenance API")

    # Check if model files exist
    required_files = [
        './final_model.pkl',
        './feature_scaler.pkl',
        './feature_columns.pkl'
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        logger.warning(f"Model files missing: {missing_files}")
        logger.warning("Please run model_trainer.py to generate the required model files")
    else:
        logger.info("All model files found")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down ArogyaJal Predictive Maintenance API")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "ArogyaJal Predictive Maintenance API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/api/predict",
            "model_info": "/api/model-info",
            "docs": "/docs"
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn

    # Run the API server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )