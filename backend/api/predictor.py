import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta
import os
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MaintenancePredictor:
    """Predictive maintenance predictor for water pump failures."""

    def __init__(self):
        """Initialize the predictor with loaded model and preprocessing components."""
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.model_loaded = False
        self.load_model()

    def load_model(self):
        """Load the trained model and preprocessing components."""
        try:
            # Load model
            model_path = './final_model.pkl'
            if not os.path.exists(model_path):
                logger.error(f"Model file not found: {model_path}")
                return False

            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)

            # Load scaler
            scaler_path = './feature_scaler.pkl'
            if not os.path.exists(scaler_path):
                logger.error(f"Scaler file not found: {scaler_path}")
                return False

            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)

            # Load feature columns
            feature_columns_path = './feature_columns.pkl'
            if not os.path.exists(feature_columns_path):
                logger.error(f"Feature columns file not found: {feature_columns_path}")
                return False

            with open(feature_columns_path, 'rb') as f:
                self.feature_columns = pickle.load(f)

            self.model_loaded = True
            logger.info("Model and preprocessing components loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.model_loaded = False
            return False

    def create_features_from_reading(self, vibration: float, current: float, temperature: float,
                                   timestamp: Optional[datetime] = None) -> pd.DataFrame:
        """
        Create engineered features from a single sensor reading.

        Args:
            vibration: Vibration reading in mm/s
            current: Current reading in Amperes
            temperature: Temperature reading in Celsius
            timestamp: Reading timestamp (defaults to current time)

        Returns:
            pd.DataFrame: DataFrame with engineered features
        """
        if timestamp is None:
            timestamp = datetime.now()

        # Create base features
        features = {
            'vibration': vibration,
            'current': current,
            'temperature': temperature,
            'hour_of_day': timestamp.hour,
            'day_of_week': timestamp.weekday(),
            'month': timestamp.month,
        }

        # Cyclical encoding for time features
        features['hour_sin'] = np.sin(2 * np.pi * timestamp.hour / 24)
        features['hour_cos'] = np.cos(2 * np.pi * timestamp.hour / 24)
        features['day_sin'] = np.sin(2 * np.pi * timestamp.weekday() / 7)
        features['day_cos'] = np.cos(2 * np.pi * timestamp.weekday() / 7)

        # For real-time predictions, we need to estimate rolling features
        # Use the current reading with some assumed baseline values
        # This is an approximation since we don't have historical data in real-time

        # Simulated rolling averages (using current reading as approximation)
        # In a real system, these would be calculated from recent historical data
        features['vibration_72h_mean'] = vibration * 0.9  # Slightly lower baseline
        features['current_72h_mean'] = current * 0.95    # Slightly lower baseline
        features['temperature_72h_mean'] = temperature - 2  # Slightly lower baseline

        features['vibration_24h_mean'] = vibration * 0.95
        features['current_24h_mean'] = current * 0.98
        features['temperature_24h_mean'] = temperature - 1

        # Rate of change features (trends)
        # For real-time, assume small changes based on reading magnitude
        features['vibration_trend'] = vibration * 0.05   # 5% increase trend
        features['current_trend'] = current * 0.03       # 3% increase trend
        features['temperature_trend'] = temperature * 0.01  # 1% increase trend

        # Interaction features
        features['vibration_current_product'] = vibration * current
        features['vibration_temp_ratio'] = vibration / (temperature + 1e-6)
        features['current_temp_ratio'] = current / (temperature + 1e-6)

        # Z-score features (using assumed population means from training data)
        # These are approximate based on typical sensor ranges
        features['vibration_zscore'] = (vibration - 1.0) / 0.5    # Assuming mean=1.0, std=0.5
        features['current_zscore'] = (current - 11.5) / 2.0      # Assuming mean=11.5, std=2.0
        features['temperature_zscore'] = (temperature - 60) / 10  # Assuming mean=60, std=10

        # Create DataFrame
        df = pd.DataFrame([features])

        # Ensure all required columns are present and in correct order
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0  # Default value for missing features

        # Reorder columns to match training data
        df = df[self.feature_columns]

        return df

    def predict_failure_probability(self, vibration: float, current: float, temperature: float,
                                  timestamp: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Predict the probability of pump failure within 72 hours.

        Args:
            vibration: Vibration reading in mm/s
            current: Current reading in Amperes
            temperature: Temperature reading in Celsius
            timestamp: Reading timestamp (defaults to current time)

        Returns:
            dict: Prediction result with probability and metadata
        """
        if not self.model_loaded:
            return {
                'probability_of_failure': 0.0,
                'status': 'error',
                'error': 'Model not loaded',
                'timestamp': datetime.now().isoformat(),
                'confidence_level': 'low'
            }

        try:
            # Validate input ranges
            if not (0 <= vibration <= 10):
                raise ValueError(f"Vibration {vibration} out of valid range [0, 10]")
            if not (0 <= current <= 50):
                raise ValueError(f"Current {current} out of valid range [0, 50]")
            if not (-20 <= temperature <= 150):
                raise ValueError(f"Temperature {temperature} out of valid range [-20, 150]")

            # Create features
            features_df = self.create_features_from_reading(vibration, current, temperature, timestamp)

            # Scale features
            features_scaled = self.scaler.transform(features_df)

            # Make prediction
            prediction_proba = self.model.predict_proba(features_scaled)[0]
            probability_of_failure = float(prediction_proba[1])  # Probability of class 1 (failure)

            # Determine confidence level based on prediction confidence
            max_proba = max(prediction_proba)
            if max_proba > 0.8:
                confidence_level = 'high'
            elif max_proba > 0.6:
                confidence_level = 'medium'
            else:
                confidence_level = 'low'

            return {
                'probability_of_failure': round(probability_of_failure, 3),
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'confidence_level': confidence_level,
                'raw_probabilities': {
                    'normal_operation': round(float(prediction_proba[0]), 3),
                    'failure_predicted': round(float(prediction_proba[1]), 3)
                }
            }

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {
                'probability_of_failure': 0.0,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'confidence_level': 'low'
            }

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if not self.model_loaded:
            return {
                'model_loaded': False,
                'error': 'Model not loaded'
            }

        return {
            'model_loaded': True,
            'model_type': type(self.model).__name__,
            'feature_count': len(self.feature_columns) if self.feature_columns else 0,
            'feature_columns': self.feature_columns[:10] if self.feature_columns else [],  # Show first 10
            'timestamp': datetime.now().isoformat()
        }

# Global predictor instance
predictor = MaintenancePredictor()