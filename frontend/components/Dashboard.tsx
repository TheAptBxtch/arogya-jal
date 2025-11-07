import React, { useState } from 'react';
import PredictionForm from './PredictionForm';
import PredictionCard from './PredictionCard';
import '../styles/globals.css';

interface PredictionResult {
  probability_of_failure: number;
  timestamp: string;
  status: string;
  confidence_level?: string;
}

const Dashboard: React.FC = () => {
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handlePredictionSubmit = async (sensorData: {
    vibration: number;
    current: number;
    temperature: number;
  }) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(sensorData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setPrediction(result);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>ArogyaJal Predictive Maintenance</h1>
        <p className="dashboard-description">
          Real-time failure prediction for water pump systems using machine learning.
          Enter current sensor readings to get an instant failure probability assessment.
        </p>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-grid">
          <div className="dashboard-form-section">
            <PredictionForm
              onSubmit={handlePredictionSubmit}
              loading={loading}
            />
          </div>

          <div className="dashboard-results-section">
            {error && (
              <div className="error-message">
                <h3>Error</h3>
                <p>{error}</p>
                <small>Please check your sensor readings and try again.</small>
              </div>
            )}

            {loading && (
              <div className="loading-message">
                <h3>Analyzing Sensor Data</h3>
                <div className="loading-spinner"></div>
                <p>Processing your sensor readings...</p>
              </div>
            )}

            {prediction && !loading && (
              <PredictionCard prediction={prediction} />
            )}

            {!prediction && !loading && !error && (
              <div className="welcome-message">
                <h3>Ready for Analysis</h3>
                <p>Enter sensor readings on the left to get started with failure prediction analysis.</p>
                <div className="feature-highlights">
                  <div className="feature-item">
                    <strong>🔍 Real-time Analysis</strong>
                    <p>Instant predictions based on current sensor data</p>
                  </div>
                  <div className="feature-item">
                    <strong>📊 Probability Scoring</strong>
                    <p>Failure probability within the next 72 hours</p>
                  </div>
                  <div className="feature-item">
                    <strong>🚨 Risk Assessment</strong>
                    <p>Color-coded alerts for quick decision making</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="dashboard-footer">
        <div className="info-section">
          <h4>How It Works</h4>
          <ul>
            <li><strong>Vibration (mm/s):</strong> Measures pump vibration levels</li>
            <li><strong>Current (A):</strong> Electrical current consumption</li>
            <li><strong>Temperature (°C):</strong> Operating temperature</li>
          </ul>
        </div>
        <div className="info-section">
          <h4>Risk Levels</h4>
          <ul>
            <li><span className="risk-indicator risk-low"></span> <strong>Low Risk:</strong> {'<'} 40% failure probability</li>
            <li><span className="risk-indicator risk-medium"></span> <strong>Medium Risk:</strong> 40-80% failure probability</li>
            <li><span className="risk-indicator risk-high"></span> <strong>High Risk:</strong> {'>'} 80% failure probability</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;