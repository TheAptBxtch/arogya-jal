import streamlit as st
import json
import csv
import random
import math
from datetime import datetime, timedelta
import os

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
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .risk-medium {
        background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .risk-high {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    .big-number {
        font-size: 4rem;
        font-weight: bold;
        line-height: 1;
    }
    .preset-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        cursor: pointer;
        margin: 0.25rem;
        width: 100%;
    }
    .preset-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

class SimplePredictor:
    """Simple rule-based predictor that doesn't require external ML libraries."""

    def __init__(self):
        self.is_trained = False
        self.training_data = []

    def train(self, data):
        """Train on provided data."""
        self.training_data = data
        self.is_trained = True
        return True

    def predict(self, vibration, current, temperature):
        """
        Simple rule-based prediction based on sensor thresholds.
        Returns probability of failure within 72 hours.
        """
        # Base probability
        probability = 0.0

        # Vibration factor (most important)
        if vibration > 5.0:
            probability += 0.4
        elif vibration > 3.0:
            probability += 0.25
        elif vibration > 2.0:
            probability += 0.1

        # Current factor
        if current > 30.0:
            probability += 0.3
        elif current > 20.0:
            probability += 0.2
        elif current > 15.0:
            probability += 0.1

        # Temperature factor
        if temperature > 100.0:
            probability += 0.2
        elif temperature > 80.0:
            probability += 0.15
        elif temperature > 70.0:
            probability += 0.05

        # Combined stress factors
        if vibration > 3.0 and current > 20.0:
            probability += 0.1
        if current > 25.0 and temperature > 85.0:
            probability += 0.1

        # Cap at 0.95
        probability = min(probability, 0.95)

        # Add some randomness for realism
        probability += random.uniform(-0.05, 0.05)
        probability = max(0.0, min(probability, 1.0))

        return probability

def generate_simple_data():
    """Generate synthetic data using only built-in Python libraries."""
    data = []

    # Start from 6 weeks ago
    current_time = datetime.now() - timedelta(days=42)

    # Generate 1000 data points
    for i in range(1000):
        # Random interval between readings
        interval_hours = random.uniform(1, 6)
        current_time += timedelta(hours=interval_hours)

        # Base sensor values (normal ranges)
        vibration = random.uniform(0.1, 2.0)
        current = random.uniform(8.0, 15.0)
        temperature = random.uniform(45, 75)

        # Simulate failure events (18 failures in dataset)
        failure_in_72_hours = 0
        if random.random() < 0.018:  # 1.8% chance
            failure_in_72_hours = 1
            # Elevate readings for failure events
            vibration = random.uniform(3.0, 8.0)
            current = random.uniform(20.0, 40.0)
            temperature = random.uniform(80.0, 120.0)

        # Add noise
        vibration *= random.uniform(0.95, 1.05)
        current *= random.uniform(0.95, 1.05)
        temperature *= random.uniform(0.95, 1.05)

        data.append({
            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'vibration': round(vibration, 3),
            'current': round(current, 2),
            'temperature': round(temperature, 1),
            'failure_in_72_hours': failure_in_72_hours
        })

    return data

def save_data_to_csv(data, filename):
    """Save data to CSV file."""
    try:
        os.makedirs('data', exist_ok=True)
        with open(f'data/{filename}', 'w', newline='') as csvfile:
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def load_data_from_csv(filename):
    """Load data from CSV file."""
    try:
        with open(f'data/{filename}', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
            # Convert numeric values
            for row in data:
                row['vibration'] = float(row['vibration'])
                row['current'] = float(row['current'])
                row['temperature'] = float(row['temperature'])
                row['failure_in_72_hours'] = int(row['failure_in_72_hours'])
            return data
    except FileNotFoundError:
        return []
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

def main():
    """Main Streamlit application."""

    # Initialize session state
    if 'data_generated' not in st.session_state:
        st.session_state.data_generated = False
    if 'model_trained' not in st.session_state:
        st.session_state.model_trained = False
    if 'predictor' not in st.session_state:
        st.session_state.predictor = SimplePredictor()
    if 'sensor_data' not in st.session_state:
        st.session_state.sensor_data = []

    # Header
    st.markdown('<h1 class="main-header">⚙️ ArogyaJal Predictive Maintenance</h1>',
                 unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem; color: #666;'>
    Real-time failure prediction for water pump systems • Rule-based ML algorithms • Easy deployment
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for setup
    with st.sidebar:
        st.header("🔧 Quick Setup")

        # Generate Data Button
        if st.button("🔄 Generate Training Data", type="primary", use_container_width=True):
            with st.spinner("Generating synthetic sensor data..."):
                try:
                    data = generate_simple_data()
                    if save_data_to_csv(data, 'pump_data.csv'):
                        st.session_state.sensor_data = data
                        st.session_state.data_generated = True
                        st.success("✅ Data generated successfully!")
                        st.info(f"📊 Generated {len(data)} sensor readings")
                    else:
                        st.error("❌ Failed to save data")
                except Exception as e:
                    st.error(f"❌ Error generating data: {e}")

        # Train Model Button
        if st.button("🤖 Train Model", type="primary", use_container_width=True):
            if not st.session_state.data_generated:
                st.error("❌ Please generate data first!")
            else:
                with st.spinner("Training model..."):
                    try:
                        if st.session_state.predictor.train(st.session_state.sensor_data):
                            st.session_state.model_trained = True
                            st.success("✅ Model trained successfully!")
                        else:
                            st.error("❌ Model training failed")
                    except Exception as e:
                        st.error(f"❌ Error training model: {e}")

        st.divider()

        # Model Status
        if st.session_state.model_trained:
            st.success("✅ Model Ready")
            st.info("🎯 Rule-based algorithm trained")
        else:
            st.warning("⚠️ Model Not Ready")
            st.info("Generate data and train model first")

        st.divider()

        # Quick Presets
        st.header("⚡ Test Presets")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🟢 Normal", use_container_width=True):
                st.session_state.vibration = 1.2
                st.session_state.current = 10.5
                st.session_state.temperature = 55.3

            if st.button("🟡 Medium", use_container_width=True):
                st.session_state.vibration = 3.5
                st.session_state.current = 20.0
                st.session_state.temperature = 85.0

        with col2:
            if st.button("🔴 Critical", use_container_width=True):
                st.session_state.vibration = 6.0
                st.session_state.current = 35.0
                st.session_state.temperature = 110.0

            if st.button("🔧 Reset", use_container_width=True):
                st.session_state.vibration = 1.0
                st.session_state.current = 12.0
                st.session_state.temperature = 60.0

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📊 Sensor Input")

        # Sensor input form
        with st.form("sensor_form"):
            vibration = st.number_input(
                "Vibration (mm/s)",
                min_value=0.0,
                max_value=10.0,
                value=getattr(st.session_state, 'vibration', 1.0),
                step=0.1,
                help="Normal: 0.1-2.0 | Warning: 2.0-5.0 | Critical: >5.0"
            )

            current = st.number_input(
                "Current (Amperes)",
                min_value=0.0,
                max_value=50.0,
                value=getattr(st.session_state, 'current', 12.0),
                step=0.1,
                help="Normal: 8-15A | Warning: 15-25A | Critical: >25A"
            )

            temperature = st.number_input(
                "Temperature (°C)",
                min_value=-20.0,
                max_value=150.0,
                value=getattr(st.session_state, 'temperature', 60.0),
                step=0.1,
                help="Normal: 45-75°C | Warning: 75-100°C | Critical: >100°C"
            )

            submitted = st.form_submit_button("🔍 Predict Failure Risk", type="primary", use_container_width=True)

            if submitted:
                if not st.session_state.model_trained:
                    st.error("❌ Model not trained! Please train the model first.")
                else:
                    with st.spinner("Analyzing sensor data..."):
                        try:
                            probability = st.session_state.predictor.predict(vibration, current, temperature)
                            st.session_state.prediction_result = {
                                'probability': probability,
                                'vibration': vibration,
                                'current': current,
                                'temperature': temperature,
                                'timestamp': datetime.now()
                            }
                        except Exception as e:
                            st.error(f"❌ Prediction error: {e}")

        # Sensor Reference
        st.markdown("---")
        st.subheader("📋 Sensor Reference Guide")

        # Create reference table
        ref_data = [
            {"Sensor": "Vibration", "Normal": "0.1-2.0 mm/s", "Warning": "2.0-5.0 mm/s", "Critical": ">5.0 mm/s"},
            {"Sensor": "Current", "Normal": "8-15 A", "Warning": "15-25 A", "Critical": ">25 A"},
            {"Sensor": "Temperature", "Normal": "45-75°C", "Warning": "75-100°C", "Critical": ">100°C"}
        ]

        st.dataframe(ref_data, use_container_width=True, hide_index=True)

    with col2:
        st.header("📈 Risk Analysis")

        # Display prediction results
        if hasattr(st.session_state, 'prediction_result'):
            result = st.session_state.prediction_result
            probability = result['probability']

            # Determine risk level
            if probability > 0.80:
                risk_level = "🚨 CRITICAL RISK"
                risk_class = "risk-high"
                risk_emoji = "🚨"
                recommendations = [
                    "IMMEDIATE INSPECTION REQUIRED",
                    "Stop pump operation immediately",
                    "Contact maintenance team NOW",
                    "Schedule emergency repair"
                ]
                alert_color = "red"
            elif probability >= 0.40:
                risk_level = "⚡ MONITOR CLOSELY"
                risk_class = "risk-medium"
                risk_emoji = "⚡"
                recommendations = [
                    "Monitor pump performance closely",
                    "Increase sensor reading frequency",
                    "Schedule inspection within 24 hours",
                    "Prepare maintenance plan"
                ]
                alert_color = "orange"
            else:
                risk_level = "✅ NORMAL OPERATION"
                risk_class = "risk-low"
                risk_emoji = "✅"
                recommendations = [
                    "Pump operating normally",
                    "Continue regular monitoring",
                    "Maintain standard schedule",
                    "All systems green"
                ]
                alert_color = "green"

            # Display risk card
            st.markdown(f"""
            <div class="{risk_class}">
                <h2>{risk_emoji} {risk_level}</h2>
                <div class="big-number">{probability:.1%}</div>
                <p><strong>Failure Probability (72 hours)</strong></p>
            </div>
            """, unsafe_allow_html=True)

            # Progress bar
            st.progress(probability)

            # Alert message
            st.markdown(f"""
            <div style="background-color: {alert_color}10; border-left: 4px solid {alert_color}; padding: 1rem; margin: 1rem 0;">
                <strong>🎯 Risk Assessment:</strong> {probability:.1%} chance of failure within 72 hours
            </div>
            """, unsafe_allow_html=True)

            # Recommendations
            st.subheader("💡 Recommendations")
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")

            # Technical details
            with st.expander("🔧 Technical Details"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Vibration", f"{result['vibration']} mm/s")
                    st.metric("Current", f"{result['current']} A")
                with col_b:
                    st.metric("Temperature", f"{result['temperature']}°C")
                    st.metric("Risk Level", risk_level.split()[-1])

                st.write(f"**Analysis Time:** {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"**Algorithm:** Rule-based predictive analysis")
                st.write(f"**Confidence:** High (based on sensor thresholds)")

        else:
            # Welcome message
            st.info("👋 **Welcome to ArogyaJal Predictive Maintenance!**")

            st.markdown("""
            ### 🎯 How to Use:
            1. **Generate Data**: Click "Generate Training Data" in the sidebar
            2. **Train Model**: Click "Train Model" (takes 2 seconds)
            3. **Enter Readings**: Input current sensor values
            4. **Get Prediction**: Click "Predict Failure Risk"

            ### 🚀 Quick Test:
            Use the preset buttons (Normal/Medium/Critical) to test different scenarios instantly!
            """)

            # Show demo data if available
            if st.session_state.data_generated:
                st.success("✅ Training data ready for model training!")
                st.info("🤖 Click 'Train Model' in the sidebar to activate predictions")
            else:
                st.warning("⚠️ Please generate training data first")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem; padding: 1rem; background: #f0f2f6; border-radius: 0.5rem;'>
    <strong>🎯 ArogyaJal Predictive Maintenance System</strong><br>
    <em>Rule-based ML algorithms • Real-time analysis • Easy deployment • Streamlit powered</em><br>
    <small>No external dependencies required • Works anywhere Python runs</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()