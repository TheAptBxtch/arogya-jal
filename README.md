# ArogyaJal Predictive Maintenance System

A comprehensive predictive maintenance system for water pumps using Python backend, machine learning, and modern web frontend. The system predicts pump failures within 72 hours using real-time sensor data analysis.

## 🚀 Features

- **🤖 Machine Learning**: XGBoost classifier trained on synthetic sensor data
- **📊 Real-time Analysis**: Instant failure probability predictions
- **🎯 Color-coded Alerts**: Visual risk indicators (Green/Yellow/Red)
- **📱 Responsive Design**: Mobile-friendly web dashboard
- **🔍 Sensor Validation**: Input validation for all sensor readings
- **📈 Confidence Scoring**: Prediction confidence levels
- **🔧 REST API**: Clean, documented API endpoints
- **📄 Printable Reports**: Generate maintenance reports

## 📋 System Requirements

- **Python 3.9+** - Backend ML and API services
- **Node.js 16+** and **npm** - Frontend development
- **Git** - Version control

## 🏗️ Architecture

```
arogya-jal/
├── backend/                     # Python backend services
│   ├── data_generator.py        # Synthetic data generation
│   ├── model_trainer.py         # ML model training
│   ├── api/                     # FastAPI application
│   │   ├── main.py             # API server
│   │   ├── models.py           # Pydantic validation
│   │   └── predictor.py        # Prediction logic
│   └── requirements.txt        # Python dependencies
├── frontend/                    # Next.js web application
│   ├── pages/                  # React pages
│   │   ├── index.tsx           # Main dashboard
│   │   └── api/predict.ts      # API proxy
│   ├── components/             # React components
│   │   ├── Dashboard.tsx       # Main container
│   │   ├── PredictionForm.tsx  # Input form
│   │   └── PredictionCard.tsx  # Results display
│   └── styles/                 # CSS styling
├── data/                       # Generated datasets
│   └── pump_data.csv          # Training data
└── README.md                   # This file
```

## ⚙️ Quick Start

Follow these steps to get the system running:

### 1. Setup Backend Environment

```bash
# Navigate to project directory
cd arogya-jal

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt
```

### 2. Generate Training Data

```bash
# Run data generation script
python backend/data_generator.py
```

**Expected Output:**
```
Generating synthetic pump sensor data...
Generated dataset with 1000 rows
Date range: 2024-01-01 08:00:00 to 2024-02-12 14:30:00
Failure events: 18 (1.8%)

Sample data:
   timestamp  vibration  current  temperature  failure_in_72_hours
0 2024-01-01 08:00:00      1.2     10.5         55.3                   0
1 2024-01-01 12:30:00      1.4     11.2         56.1                   0

Dataset saved to: ../data/pump_data.csv
✓ Data generation completed successfully!
```

### 3. Train Prediction Model

```bash
# Run model training script
python backend/model_trainer.py
```

**Expected Output:**
```
=== ArogyaJal Predictive Maintenance Model Training ===

Loading dataset...
Dataset loaded successfully: 1000 rows, 5 columns
Target distribution:
0    982
1     18
Name: failure_in_72_hours, dtype: int64
Failure rate: 0.018

Performing feature engineering...
Features engineered: 26 columns
Feature matrix shape: (1000, 26)

Training set: 800 samples
Test set: 200 samples

Training XGBoost model...
Model training completed.

Evaluating model performance...
Evaluation Results:
Accuracy: 0.9850
Precision: 0.8333
Recall: 0.8333
F1-Score: 0.8333
ROC AUC: 0.9896

Model saved to: ./final_model.pkl
✓ Model training completed successfully!
```

### 4. Start Backend API Server

```bash
# Navigate to backend directory
cd backend

# Start FastAPI server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     For reloader, use --reload
```

### 5. Setup Frontend Environment (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### 6. Start Frontend Development Server

```bash
# Start Next.js development server
npm run dev
```

**Expected Output:**
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

### 7. Access the Application

1. Open your web browser
2. Go to **http://localhost:3000**
3. You should see the "ArogyaJal Predictive Maintenance" dashboard
4. Try entering sensor readings to get predictions!

## 🎯 Testing the System

### Test API Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### Test Prediction Endpoint

```bash
curl -X POST "http://localhost:8000/api/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "vibration": 1.5,
       "current": 12.3,
       "temperature": 65.2
     }'
```

**Expected Response:**
```json
{
  "probability_of_failure": 0.142,
  "timestamp": "2024-01-15T10:30:00.123456",
  "status": "success",
  "confidence_level": "high"
}
```

### Test Different Risk Levels

1. **Normal Operation** (Green - < 40%):
   - Vibration: 1.2, Current: 10.5, Temperature: 55.3

2. **Medium Risk** (Yellow - 40-80%):
   - Vibration: 3.5, Current: 20.0, Temperature: 85.0

3. **Critical Risk** (Red - > 80%):
   - Vibration: 6.0, Current: 35.0, Temperature: 110.0

## 📊 Sensor Data Ranges

| Sensor | Normal Range | Valid Range | Units |
|--------|-------------|-------------|-------|
| Vibration | 0.1 - 2.0 | 0 - 10 | mm/s |
| Current | 8.0 - 15.0 | 0 - 50 | A |
| Temperature | 45 - 75 | -20 - 150 | °C |

## 🚨 Risk Level Interpretation

- **🟢 Green (Low Risk)**: < 40% failure probability
  - Pump operating normally
  - Continue regular monitoring

- **🟡 Yellow (Medium Risk)**: 40-80% failure probability
  - Monitor closely
  - Schedule inspection soon

- **🔴 Red (High Risk)**: > 80% failure probability
  - Immediate inspection required
  - Schedule maintenance ASAP

## 🔧 Configuration

### Backend Environment Variables

Create `.env` file in `backend/` directory:

```env
MODEL_PATH="./final_model.pkl"
API_HOST="0.0.0.0"
API_PORT="8000"
```

### Frontend Environment Variables

Create `.env.local` file in `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

## 📁 File Descriptions

### Backend Files

- **`data_generator.py`**: Creates synthetic pump sensor data with realistic failure patterns
- **`model_trainer.py`**: Trains XGBoost model with feature engineering
- **`api/main.py`**: FastAPI server with prediction endpoints
- **`api/models.py`**: Pydantic models for request/response validation
- **`api/predictor.py`**: Core prediction logic and feature engineering

### Frontend Files

- **`pages/index.tsx`**: Main dashboard page
- **`pages/api/predict.ts`**: API proxy route to backend
- **`components/Dashboard.tsx`**: Main dashboard container component
- **`components/PredictionForm.tsx`**: Sensor input form with validation
- **`components/PredictionCard.tsx`**: Results display with visual indicators

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Module Not Found**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   # Reinstall dependencies
   pip install -r backend/requirements.txt
   ```

3. **Model Files Missing**
   ```bash
   # Ensure data generation and training completed
   python backend/data_generator.py
   python backend/model_trainer.py
   ```

4. **Frontend Build Errors**
   ```bash
   # Clear node_modules and reinstall
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

5. **CORS Issues**
   - Ensure backend server is running
   - Check API URL in frontend `.env.local`

### Debug Mode

**Backend Debugging:**
```bash
# Start with debug logging
uvicorn api.main:app --reload --log-level debug
```

**Frontend Debugging:**
- Open browser developer tools
- Check Network tab for API calls
- Check Console for JavaScript errors

## 📈 Performance Metrics

The trained model typically achieves:
- **Accuracy**: > 95%
- **Precision**: > 80%
- **Recall**: > 80%
- **ROC AUC**: > 0.95

## 🚀 Production Deployment

### Backend (Docker)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY data/ .

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Static Files)

```bash
# Build for production
npm run build
npm start
```

## 🔄 Model Retraining

To retrain the model with new data:

1. Update or replace `data/pump_data.csv`
2. Run training script: `python backend/model_trainer.py`
3. Restart the API server

## 📄 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check this README
2. Review the troubleshooting section
3. Check browser console for errors
4. Verify backend API is accessible

---

**🎉 Congratulations!** You now have a fully functional predictive maintenance system for water pumps. The system can predict pump failures up to 72 hours in advance using machine learning.