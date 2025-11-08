import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="ArogyaJal Predictive Maintenance",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-low {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
    }
    .risk-medium {
        background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
    }
    .risk-high {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

class MaintenancePredictor:
    """Simplified predictor for the Streamlit app."""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.model_loaded = False
        self.load_model()

    def load_model(self):
        """Load the trained model and preprocessing components."""
        try:
            model_path = 'models/final_model.joblib'
            scaler_path = 'models/feature_scaler.joblib'
            feature_columns_path = 'models/feature_columns.joblib'

            if not all(os.path.exists(path) for path in [model_path, scaler_path, feature_columns_path]):
                return False

            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.feature_columns = joblib.load(feature_columns_path)
            self.model_loaded = True
            return True
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return False

    def create_features_from_reading(self, vibration, current, temperature):
        """Create features from a single sensor reading."""
        timestamp = datetime.now()

        features = {
            'vibration': vibration,
            'current': current,
            'temperature': temperature,
            'hour_of_day': timestamp.hour,
            'day_of_week': timestamp.weekday(),
            'month': timestamp.month,
        }

        # Cyclical encoding
        features['hour_sin'] = np.sin(2 * np.pi * timestamp.hour / 24)
        features['hour_cos'] = np.cos(2 * np.pi * timestamp.hour / 24)
        features['day_sin'] = np.sin(2 * np.pi * timestamp.weekday() / 7)
        features['day_cos'] = np.cos(2 * np.pi * timestamp.weekday() / 7)

        # Simplified rolling features (using current reading as approximation)
        features['vibration_72h_mean'] = vibration * 0.9
        features['current_72h_mean'] = current * 0.95
        features['temperature_72h_mean'] = temperature - 2

        features['vibration_24h_mean'] = vibration * 0.95
        features['current_24h_mean'] = current * 0.98
        features['temperature_24h_mean'] = temperature - 1

        # Trend features
        features['vibration_trend'] = vibration * 0.05
        features['current_trend'] = current * 0.03
        features['temperature_trend'] = temperature * 0.01

        # Interaction features
        features['vibration_current_product'] = vibration * current
        features['vibration_temp_ratio'] = vibration / (temperature + 1e-6)
        features['current_temp_ratio'] = current / (temperature + 1e-6)

        # Z-score features (using assumed population means)
        features['vibration_zscore'] = (vibration - 1.0) / 0.5
        features['current_zscore'] = (current - 11.5) / 2.0
        features['temperature_zscore'] = (temperature - 60) / 10

        # Create DataFrame
        df = pd.DataFrame([features])

        # Ensure all required columns are present
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0

        # Reorder columns to match training data
        df = df[self.feature_columns]

        return df

    def predict_failure_probability(self, vibration, current, temperature):
        """Predict the probability of pump failure within 72 hours."""
        if not self.model_loaded:
            return None, "Model not loaded"

        try:
            # Validate input ranges
            if not (0 <= vibration <= 10):
                return None, "Vibration must be between 0 and 10 mm/s"
            if not (0 <= current <= 50):
                return None, "Current must be between 0 and 50 A"
            if not (-20 <= temperature <= 150):
                return None, "Temperature must be between -20 and 150°C"

            # Create features
            features_df = self.create_features_from_reading(vibration, current, temperature)

            # Scale features
            features_scaled = self.scaler.transform(features_df)

            # Make prediction
            prediction_proba = self.model.predict_proba(features_scaled)[0]
            probability_of_failure = float(prediction_proba[1])

            return probability_of_failure, "success"

        except Exception as e:
            return None, f"Prediction error: {str(e)}"

# Initialize predictor
predictor = MaintenancePredictor()

def main():
    """Main Streamlit application."""

    # Header
    st.markdown('<h1 class="main-header">⚙️ ArogyaJal Predictive Maintenance</h1>',
                 unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem; color: #666;'>
    Real-time failure prediction for water pump systems using machine learning.
    Enter current sensor readings to get an instant failure probability assessment.
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for model setup
    with st.sidebar:
        st.header("🔧 Model Setup")

        if st.button("🔄 Generate New Data", type="primary"):
            with st.spinner("Generating synthetic data..."):
                try:
                    exec(open('data_generator.py').read())
                    st.success("✅ Data generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error generating data: {str(e)}")

        if st.button("🤖 Train Model", type="primary"):
            with st.spinner("Training model..."):
                try:
                    exec(open('model_trainer.py').read())
                    st.success("✅ Model trained successfully!")
                    predictor.load_model()  # Reload the model
                except Exception as e:
                    st.error(f"❌ Error training model: {str(e)}")

        st.divider()

        # Model status
        if predictor.model_loaded:
            st.success("✅ Model Loaded")
        else:
            st.warning("⚠️ Model Not Loaded")
            st.info("Please train the model first.")

        st.divider()

        # Quick presets
        st.header("⚡ Quick Presets")

        if st.button("🟢 Normal Operation"):
            st.session_state.vibration = 1.2
            st.session_state.current = 10.5
            st.session_state.temperature = 55.3

        if st.button("🟡 Medium Risk"):
            st.session_state.vibration = 3.5
            st.session_state.current = 20.0
            st.session_state.temperature = 85.0

        if st.button("🔴 Critical Risk"):
            st.session_state.vibration = 6.0
            st.session_state.current = 35.0
            st.session_state.temperature = 110.0

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📊 Sensor Readings")

        # Input form
        with st.form("sensor_form"):
            vibration = st.number_input(
                "Vibration (mm/s)",
                min_value=0.0,
                max_value=10.0,
                value=getattr(st.session_state, 'vibration', 1.2),
                step=0.1,
                help="Vibration measurement in millimeters per second"
            )

            current = st.number_input(
                "Current (A)",
                min_value=0.0,
                max_value=50.0,
                value=getattr(st.session_state, 'current', 10.5),
                step=0.1,
                help="Electrical current consumption in Amperes"
            )

            temperature = st.number_input(
                "Temperature (°C)",
                min_value=-20.0,
                max_value=150.0,
                value=getattr(st.session_state, 'temperature', 55.3),
                step=0.1,
                help="Operating temperature in Celsius"
            )

            submitted = st.form_submit_button("🔍 Predict Failure Risk", type="primary")

            if submitted:
                if not predictor.model_loaded:
                    st.error("❌ Model not loaded. Please train the model first.")
                else:
                    with st.spinner("Analyzing sensor data..."):
                        probability, status = predictor.predict_failure_probability(
                            vibration, current, temperature
                        )

                        if status == "success":
                            st.session_state.prediction_result = {
                                'probability': probability,
                                'vibration': vibration,
                                'current': current,
                                'temperature': temperature,
                                'timestamp': datetime.now()
                            }
                        else:
                            st.error(f"❌ {status}")

        # Display sensor ranges info
        st.markdown("---")
        st.subheader("📋 Normal Operating Ranges")

        ranges_df = pd.DataFrame({
            'Sensor': ['Vibration', 'Current', 'Temperature'],
            'Normal Range': ['0.1 - 2.0 mm/s', '8.0 - 15.0 A', '45 - 75°C'],
            'Valid Range': ['0 - 10 mm/s', '0 - 50 A', '-20 - 150°C']
        })

        st.dataframe(ranges_df, use_container_width=True, hide_index=True)

    with col2:
        st.header("📈 Risk Assessment")

        # Display prediction results
        if hasattr(st.session_state, 'prediction_result'):
            result = st.session_state.prediction_result
            probability = result['probability']

            # Determine risk level
            if probability > 0.80:
                risk_level = "Critical Risk"
                risk_class = "risk-high"
                risk_emoji = "🚨"
                recommendations = [
                    "Immediate inspection required",
                    "Schedule maintenance ASAP",
                    "Consider reducing pump load",
                    "Contact maintenance team"
                ]
            elif probability >= 0.40:
                risk_level = "Monitor Closely"
                risk_class = "risk-medium"
                risk_emoji = "⚡"
                recommendations = [
                    "Monitor pump performance closely",
                    "Increase sensor reading frequency",
                    "Schedule routine inspection soon",
                    "Document operating conditions"
                ]
            else:
                risk_level = "Normal Operation"
                risk_class = "risk-low"
                risk_emoji = "✅"
                recommendations = [
                    "Pump operating normally",
                    "Continue regular monitoring",
                    "Maintain standard schedule",
                    "Keep normal operation logs"
                ]

            # Display risk card
            st.markdown(f"""
            <div class="{risk_class}">
                <h2>{risk_emoji} {risk_level}</h2>
                <h1>{probability:.1%}</h1>
                <p>Failure Probability (within 72 hours)</p>
            </div>
            """, unsafe_allow_html=True)

            # Progress bar
            st.progress(probability)

            # Recommendations
            st.subheader("💡 Recommendations")
            for rec in recommendations:
                st.write(f"• {rec}")

            # Details
            with st.expander("📊 Detailed Analysis"):
                st.write(f"**Timestamp:** {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"**Sensor Readings:**")
                st.write(f"• Vibration: {result['vibration']} mm/s")
                st.write(f"• Current: {result['current']} A")
                st.write(f"• Temperature: {result['temperature']}°C")
                st.write(f"**Risk Level:** {risk_level}")
                st.write(f"**Probability:** {probability:.1%}")

        else:
            # Welcome message
            st.info("👋 Enter sensor readings and click 'Predict Failure Risk' to get started.")

            # Feature importance (if model is loaded)
            if predictor.model_loaded:
                st.subheader("🔍 Feature Importance")

                # Create a simple feature importance plot
                importances = predictor.model.feature_importances_
                feature_names = predictor.feature_columns

                # Get top 10 features
                top_idx = np.argsort(importances)[-10:]
                top_features = [feature_names[i] for i in top_idx]
                top_importances = importances[top_idx]

                fig = px.bar(
                    x=top_importances,
                    y=top_features,
                    orientation='h',
                    title="Top 10 Important Features"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
    <strong>ArogyaJal Predictive Maintenance System</strong><br>
    Powered by Machine Learning • Real-time Analysis • Risk Assessment
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()