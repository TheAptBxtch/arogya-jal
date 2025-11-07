import React, { useState } from 'react';

interface SensorData {
  vibration: number;
  current: number;
  temperature: number;
}

interface PredictionFormProps {
  onSubmit: (data: SensorData) => void;
  loading: boolean;
}

interface FormErrors {
  vibration?: string;
  current?: string;
  temperature?: string;
}

const PredictionForm: React.FC<PredictionFormProps> = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState<SensorData>({
    vibration: 1.0,
    current: 10.0,
    temperature: 60.0
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const validateField = (name: keyof SensorData, value: number): string | null => {
    switch (name) {
      case 'vibration':
        if (value < 0 || value > 10) {
          return 'Vibration must be between 0 and 10 mm/s';
        }
        if (isNaN(value)) {
          return 'Vibration must be a valid number';
        }
        break;
      case 'current':
        if (value < 0 || value > 50) {
          return 'Current must be between 0 and 50 A';
        }
        if (isNaN(value)) {
          return 'Current must be a valid number';
        }
        break;
      case 'temperature':
        if (value < -20 || value > 150) {
          return 'Temperature must be between -20 and 150°C';
        }
        if (isNaN(value)) {
          return 'Temperature must be a valid number';
        }
        break;
    }
    return null;
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
    let isValid = true;

    (Object.keys(formData) as Array<keyof SensorData>).forEach(field => {
      const error = validateField(field, formData[field]);
      if (error) {
        newErrors[field] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const numValue = parseFloat(value) || 0;

    setFormData(prev => ({
      ...prev,
      [name]: numValue
    }));

    // Validate field if it has been touched
    if (touched[name]) {
      const error = validateField(name as keyof SensorData, numValue);
      setErrors(prev => ({
        ...prev,
        [name]: error || undefined
      }));
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const { name } = e.target;
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));

    const error = validateField(name as keyof SensorData, formData[name as keyof SensorData]);
    setErrors(prev => ({
      ...prev,
      [name]: error || undefined
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Mark all fields as touched
    const allTouched = { vibration: true, current: true, temperature: true };
    setTouched(allTouched);

    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleReset = () => {
    setFormData({
      vibration: 1.0,
      current: 10.0,
      temperature: 60.0
    });
    setErrors({});
    setTouched({});
  };

  const isFormValid = Object.keys(errors).length === 0 &&
    Object.values(touched).some(touched => touched) ||
    (formData.vibration > 0 && formData.current > 0 && formData.temperature > 0);

  return (
    <div className="prediction-form">
      <h2>Sensor Readings</h2>
      <p className="form-description">
        Enter the current sensor readings from your water pump system.
      </p>

      <form onSubmit={handleSubmit} className="sensor-form">
        <div className="form-group">
          <label htmlFor="vibration">
            Vibration
            <span className="unit">mm/s</span>
            <span className="tooltip" title="Vibration measurement in millimeters per second">
              ℹ️
            </span>
          </label>
          <input
            type="number"
            id="vibration"
            name="vibration"
            value={formData.vibration}
            onChange={handleInputChange}
            onBlur={handleBlur}
            step="0.1"
            min="0"
            max="10"
            className={`form-input ${errors.vibration ? 'error' : ''} ${touched.vibration && !errors.vibration ? 'valid' : ''}`}
            disabled={loading}
            placeholder="0.0 - 10.0"
          />
          {errors.vibration && (
            <span className="error-message">{errors.vibration}</span>
          )}
          <small className="range-hint">Normal range: 0.1 - 2.0 mm/s</small>
        </div>

        <div className="form-group">
          <label htmlFor="current">
            Current
            <span className="unit">A</span>
            <span className="tooltip" title="Electrical current consumption in Amperes">
              ℹ️
            </span>
          </label>
          <input
            type="number"
            id="current"
            name="current"
            value={formData.current}
            onChange={handleInputChange}
            onBlur={handleBlur}
            step="0.1"
            min="0"
            max="50"
            className={`form-input ${errors.current ? 'error' : ''} ${touched.current && !errors.current ? 'valid' : ''}`}
            disabled={loading}
            placeholder="0.0 - 50.0"
          />
          {errors.current && (
            <span className="error-message">{errors.current}</span>
          )}
          <small className="range-hint">Normal range: 8.0 - 15.0 A</small>
        </div>

        <div className="form-group">
          <label htmlFor="temperature">
            Temperature
            <span className="unit">°C</span>
            <span className="tooltip" title="Operating temperature in Celsius">
              ℹ️
            </span>
          </label>
          <input
            type="number"
            id="temperature"
            name="temperature"
            value={formData.temperature}
            onChange={handleInputChange}
            onBlur={handleBlur}
            step="0.1"
            min="-20"
            max="150"
            className={`form-input ${errors.temperature ? 'error' : ''} ${touched.temperature && !errors.temperature ? 'valid' : ''}`}
            disabled={loading}
            placeholder="-20.0 to 150.0"
          />
          {errors.temperature && (
            <span className="error-message">{errors.temperature}</span>
          )}
          <small className="range-hint">Normal range: 45 - 75°C</small>
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="submit-button"
            disabled={loading || !isFormValid}
          >
            {loading ? (
              <>
                <span className="button-spinner"></span>
                Analyzing...
              </>
            ) : (
              'Predict Failure Risk'
            )}
          </button>

          <button
            type="button"
            className="reset-button"
            onClick={handleReset}
            disabled={loading}
          >
            Reset Values
          </button>
        </div>
      </form>

      <div className="quick-presets">
        <h4>Quick Presets</h4>
        <div className="preset-buttons">
          <button
            type="button"
            className="preset-button"
            onClick={() => {
              setFormData({ vibration: 1.2, current: 10.5, temperature: 55.3 });
              setTouched({ vibration: true, current: true, temperature: true });
            }}
            disabled={loading}
          >
            Normal Operation
          </button>
          <button
            type="button"
            className="preset-button"
            onClick={() => {
              setFormData({ vibration: 3.5, current: 20.0, temperature: 85.0 });
              setTouched({ vibration: true, current: true, temperature: true });
            }}
            disabled={loading}
          >
            Elevated Risk
          </button>
          <button
            type="button"
            className="preset-button"
            onClick={() => {
              setFormData({ vibration: 6.0, current: 35.0, temperature: 110.0 });
              setTouched({ vibration: true, current: true, temperature: true });
            }}
            disabled={loading}
          >
            Critical Risk
          </button>
        </div>
      </div>
    </div>
  );
};

export default PredictionForm;