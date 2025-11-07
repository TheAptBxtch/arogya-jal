import React from 'react';

interface PredictionResult {
  probability_of_failure: number;
  timestamp: string;
  status: string;
  confidence_level?: string;
}

interface PredictionCardProps {
  prediction: PredictionResult;
}

const PredictionCard: React.FC<PredictionCardProps> = ({ prediction }) => {
  const { probability_of_failure, timestamp, status, confidence_level } = prediction;

  // Determine risk level and color
  const getRiskLevel = () => {
    if (probability_of_failure > 0.80) {
      return {
        level: 'Critical Risk',
        color: '#ff4444',
        bgColor: '#ffe0e0',
        borderColor: '#ff6666',
        status: '⚠️'
      };
    } else if (probability_of_failure >= 0.40) {
      return {
        level: 'Monitor Closely',
        color: '#ffaa00',
        bgColor: '#fff4e0',
        borderColor: '#ffcc33',
        status: '⚡'
      };
    } else {
      return {
        level: 'Normal Operation',
        color: '#44ff44',
        bgColor: '#e0ffe0',
        borderColor: '#66ff66',
        status: '✅'
      };
    }
  };

  const risk = getRiskLevel();
  const percentage = Math.round(probability_of_failure * 100);

  // Calculate circle progress bar
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (probability_of_failure * circumference);

  // Format timestamp
  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  // Get confidence level display
  const getConfidenceDisplay = () => {
    if (!confidence_level) return null;

    const confidenceConfig = {
      high: { text: 'High Confidence', color: '#44ff44' },
      medium: { text: 'Medium Confidence', color: '#ffaa00' },
      low: { text: 'Low Confidence', color: '#ff4444' }
    };

    const config = confidenceConfig[confidence_level as keyof typeof confidenceConfig];
    if (!config) return null;

    return (
      <div className="confidence-indicator" style={{ color: config.color }}>
        📊 {config.text}
      </div>
    );
  };

  return (
    <div
      className={`prediction-card ${risk.level.toLowerCase().replace(' ', '-')}`}
      style={{
        backgroundColor: risk.bgColor,
        borderColor: risk.borderColor,
        animation: 'slideIn 0.5s ease-out'
      }}
    >
      <div className="prediction-header">
        <h3>
          <span className="risk-status">{risk.status}</span>
          {risk.level}
        </h3>
        <div className="prediction-time">
          {formatTimestamp(timestamp)}
        </div>
      </div>

      <div className="prediction-content">
        <div className="probability-display">
          <div className="circular-progress">
            <svg width="140" height="140" className="progress-ring">
              <circle
                cx="70"
                cy="70"
                r={radius}
                fill="none"
                stroke="#e0e0e0"
                strokeWidth="8"
              />
              <circle
                cx="70"
                cy="70"
                r={radius}
                fill="none"
                stroke={risk.color}
                strokeWidth="8"
                strokeLinecap="round"
                style={{
                  strokeDasharray: circumference,
                  strokeDashoffset,
                  transform: 'rotate(-90deg)',
                  transformOrigin: '50% 50%',
                  transition: 'stroke-dashoffset 0.8s ease-in-out'
                }}
              />
            </svg>
            <div className="probability-text">
              <div className="percentage" style={{ color: risk.color }}>
                {percentage}%
              </div>
              <div className="label">
                Failure Probability
              </div>
            </div>
          </div>
        </div>

        <div className="prediction-details">
          <div className="probability-breakdown">
            <h4>Risk Assessment</h4>
            <div className="risk-metrics">
              <div className="metric">
                <span className="metric-label">Failure Risk:</span>
                <span className="metric-value" style={{ color: risk.color }}>
                  {percentage}%
                </span>
              </div>
              <div className="metric">
                <span className="metric-label">Time Window:</span>
                <span className="metric-value">Next 72 hours</span>
              </div>
              <div className="metric">
                <span className="metric-label">Status:</span>
                <span className="metric-value" style={{ color: risk.color }}>
                  {risk.level}
                </span>
              </div>
            </div>
          </div>

          {getConfidenceDisplay()}

          <div className="recommendations">
            <h4>Recommendations</h4>
            {percentage > 80 ? (
              <ul>
                <li>🚨 Immediate inspection required</li>
                <li>🔧 Schedule maintenance as soon as possible</li>
                <li>📉 Consider reducing pump load</li>
                <li>📞 Contact maintenance team</li>
              </ul>
            ) : percentage >= 40 ? (
              <ul>
                <li>👀 Monitor pump performance closely</li>
                <li>📊 Increase sensor reading frequency</li>
                <li>🔍 Schedule routine inspection soon</li>
                <li>📋 Document current operating conditions</li>
              </ul>
            ) : (
              <ul>
                <li>✅ Pump operating normally</li>
                <li>📅 Continue regular maintenance schedule</li>
                <li>📊 Maintain standard monitoring</li>
                <li>📋 Keep normal operation logs</li>
              </ul>
            )}
          </div>
        </div>
      </div>

      <div className="prediction-footer">
        <button
          className="action-button"
          style={{ backgroundColor: risk.color }}
          onClick={() => window.print()}
        >
          📄 Print Report
        </button>
        <button
          className="secondary-button"
          onClick={() => navigator.clipboard.writeText(
            `ArogyaJal Pump Analysis - ${formatTimestamp(timestamp)}\n` +
            `Failure Probability: ${percentage}%\n` +
            `Risk Level: ${risk.level}\n` +
            `Confidence: ${confidence_level || 'Unknown'}`
          )}
        >
          📋 Copy Results
        </button>
      </div>
    </div>
  );
};

export default PredictionCard;