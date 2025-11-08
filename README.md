# ArogyaJal Predictive Maintenance System

A comprehensive predictive maintenance system for water pumps using Python machine learning and Streamlit. The system predicts pump failures within 72 hours using real-time sensor data analysis.

## 🚀 Features

- **🤖 Machine Learning**: Random Forest classifier trained on synthetic sensor data
- **📊 Real-time Analysis**: Instant failure probability predictions
- **🎯 Color-coded Alerts**: Visual risk indicators (Green/Yellow/Red)
- **🖥️ Streamlit Dashboard**: Easy-to-use web interface
- **🔍 Sensor Validation**: Input validation for all sensor readings
- **📈 Feature Importance**: Visual insights into model decision-making
- **📱 Responsive Design**: Mobile-friendly dashboard
- **⚡ One-Click Setup**: Simple installation and running

## 📋 System Requirements

- **Python 3.8+** - Only requirement!
- **pip** - Package installer (comes with Python)

## 🏗️ Simplified Architecture

```
arogya-jal/
├── 📄 app.py                     # Main Streamlit application
├── 📄 data_generator.py          # Synthetic data generation
├── 📄 model_trainer.py           # ML model training
├── 📄 requirements.txt           # Python dependencies
├── 📁 data/                      # Generated datasets
│   └── pump_data.csv            # Training data
├── 📁 models/                    # Trained models
│   ├── final_model.joblib       # Trained ML model
│   ├── feature_scaler.joblib    # Feature scaler
│   └── feature_columns.joblib   # Feature names
└── 📄 README.md                  # This file
```

## ⚡ Super Quick Start (3 Steps!)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd arogya-jal

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Generate Data & Train Model

The Streamlit app has built-in buttons to do this automatically! But if you want to do it manually:

```bash
# Generate synthetic training data
python data_generator.py

# Train the machine learning model
python model_trainer.py
```

### Step 3: Run the Application

```bash
# Start the Streamlit web application
streamlit run app.py
```

That's it! 🎉 The app will open in your browser at http://localhost:8501

## 🎯 Using the Dashboard

### First Time Setup
1. Open the app in your browser
2. Click **"🔄 Generate New Data"** in the sidebar
3. Click **"🤖 Train Model"** in the sidebar
4. Wait for the model to train (shows ✅ Model Loaded when ready)

### Making Predictions
1. **Enter sensor readings**:
   - Vibration (mm/s): 0.1 - 2.0 is normal, up to 10 max
   - Current (A): 8.0 - 15.0 is normal, up to 50 max
   - Temperature (°C): 45 - 75 is normal, -20 to 150 valid range

2. **Click "🔍 Predict Failure Risk"**

3. **View results**:
   - 🟢 **Green**: Low Risk (< 40%)
   - 🟡 **Yellow**: Medium Risk (40-80%)
   - 🔴 **Red**: High Risk (> 80%)

### Quick Presets
Use the preset buttons in the sidebar to test different scenarios:
- **🟢 Normal Operation**: Typical healthy pump readings
- **🟡 Medium Risk**: Elevated readings requiring monitoring
- **🔴 Critical Risk**: Dangerous readings requiring immediate action

## 📊 Expected Outputs

### Data Generation
```
🚀 Starting ArogyaJal Data Generation
==================================================
✅ Dataset generated successfully!
📊 Total records: 1000 rows
📅 Date range: 2024-01-01 to 2024-02-12
⚠️  Failure events: 18 (1.8%)
💾 Dataset saved to: data/pump_data.csv
✅ Data generation completed successfully!
```

### Model Training
```
🚀 Starting ArogyaJal Model Training
==================================================
✅ Dataset loaded successfully: 1000 rows, 5 columns
📊 Target distribution:
0    982
1     18
⚠️  Failure rate: 0.018 (1.8%)

🔧 Performing feature engineering...
✅ Feature engineering completed. Created 26 features.

🤖 Training Random Forest model...
✅ Model training completed.

🎯 Evaluation Results:
   Accuracy: 0.9850
   Precision: 0.8333
   Recall: 0.8333
   F1-Score: 0.8333
   ROC AUC: 0.9896

💾 Model saved to: models/final_model.joblib
🎉 Model training completed successfully!
```

## 📋 Sensor Data Reference

| Sensor | Normal Range | Valid Range | Units |
|--------|-------------|-------------|-------|
| Vibration | 0.1 - 2.0 | 0 - 10 | mm/s |
| Current | 8.0 - 15.0 | 0 - 50 | A |
| Temperature | 45 - 75 | -20 - 150 | °C |

## 🚨 Risk Level Interpretation

### 🟢 Low Risk (< 40%)
- Pump operating normally
- Continue regular monitoring
- Maintain standard maintenance schedule

### 🟡 Medium Risk (40-80%)
- Monitor pump performance closely
- Increase sensor reading frequency
- Schedule routine inspection soon
- Document operating conditions

### 🔴 High Risk (> 80%)
- Immediate inspection required
- Schedule maintenance ASAP
- Consider reducing pump load
- Contact maintenance team

## 🐛 Troubleshooting

### Installation Issues

**Problem:** `pip install -r requirements.txt` fails
```bash
# Try upgrading pip first
pip install --upgrade pip

# If still failing, try installing one by one
pip install streamlit pandas numpy scikit-learn plotly joblib
```

**Problem:** ModuleNotFoundError
```bash
# Make sure you're in the right directory
cd arogya-jal

# Check Python path
python -c "import streamlit; print('Streamlit installed successfully')"
```

### Runtime Issues

**Problem:** Model loading fails
- Click "🤖 Train Model" button in the sidebar
- Wait for training to complete
- Look for "✅ Model Loaded" message

**Problem:** Predictions not working
- Ensure model is trained and loaded
- Check that sensor values are within valid ranges
- Try the preset buttons first

**Problem:** Streamlit won't start
```bash
# Check if port is available
streamlit run app.py --server.port 8502

# Or kill existing Streamlit processes
pkill -f streamlit
```

## 📈 Model Performance

The Random Forest model typically achieves:
- **Accuracy**: > 95%
- **Precision**: > 80%
- **Recall**: > 80%
- **ROC AUC**: > 0.95

## 🚀 Deployment Options

### Local Deployment
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically!

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

## 🔄 Model Retraining

To improve the model with new data:

1. **Add new data** to `data/pump_data.csv`
2. **Click "🤖 Train Model"** in the sidebar
3. Model will retrain automatically with updated data

## 📄 Project Structure Details

### Core Files

- **`app.py`**: Main Streamlit application with interactive dashboard
- **`data_generator.py`**: Creates realistic synthetic sensor data with failure patterns
- **`model_trainer.py`**: Trains Random Forest model with feature engineering
- **`requirements.txt`**: All Python dependencies (only 6 packages!)

### Generated Files

- **`data/pump_data.csv`**: Training dataset with 1,000 sensor readings
- **`models/final_model.joblib`**: Trained machine learning model
- **`models/feature_scaler.joblib`**: Feature scaling parameters
- **`models/feature_columns.joblib`**: Feature engineering pipeline

## 🎯 Key Features Explained

### Machine Learning Pipeline
1. **Feature Engineering**: Time-based features, rolling averages, trends, interactions
2. **Model Training**: Random Forest with 100 trees
3. **Validation**: Time-based train/test split
4. **Evaluation**: Multiple metrics including ROC AUC

### Dashboard Features
1. **Real-time Predictions**: Instant failure probability calculation
2. **Visual Risk Indicators**: Color-coded risk levels
3. **Feature Importance**: Understand what drives predictions
4. **Quick Presets**: Test different scenarios instantly
5. **Responsive Design**: Works on all devices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test the application thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check this README first
2. Review the troubleshooting section
3. Try the preset buttons to test functionality
4. Check that all files are generated properly

---

**🎉 Congratulations!** You now have a fully functional predictive maintenance system that's incredibly easy to run and showcase. Just 3 commands and you're ready to demonstrate ML-powered pump failure prediction!