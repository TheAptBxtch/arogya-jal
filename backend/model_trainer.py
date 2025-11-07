import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
import xgboost as xgb
import pickle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def feature_engineering(df):
    """
    Perform feature engineering on the sensor data.

    Args:
        df (pd.DataFrame): Raw sensor data with timestamp

    Returns:
        pd.DataFrame: Data with engineered features
    """
    # Make a copy to avoid modifying original data
    df_fe = df.copy()

    # Convert timestamp to datetime
    df_fe['timestamp'] = pd.to_datetime(df_fe['timestamp'])

    # Sort by timestamp to ensure proper time-based calculations
    df_fe = df_fe.sort_values('timestamp').reset_index(drop=True)

    # Time-based features
    df_fe['hour_of_day'] = df_fe['timestamp'].dt.hour
    df_fe['day_of_week'] = df_fe['timestamp'].dt.dayofweek
    df_fe['month'] = df_fe['timestamp'].dt.month

    # Cyclical encoding for time features
    df_fe['hour_sin'] = np.sin(2 * np.pi * df_fe['hour_of_day'] / 24)
    df_fe['hour_cos'] = np.cos(2 * np.pi * df_fe['hour_of_day'] / 24)
    df_fe['day_sin'] = np.sin(2 * np.pi * df_fe['day_of_week'] / 7)
    df_fe['day_cos'] = np.cos(2 * np.pi * df_fe['day_of_week'] / 7)

    # Rolling window features (72-hour rolling averages)
    # Since data is irregular, we use time-based rolling windows
    df_fe.set_index('timestamp', inplace=True)

    # 72-hour rolling averages for vibration and current
    df_fe['vibration_72h_mean'] = df_fe['vibration'].rolling('72H').mean()
    df_fe['current_72h_mean'] = df_fe['current'].rolling('72H').mean()
    df_fe['temperature_72h_mean'] = df_fe['temperature'].rolling('72H').mean()

    # 24-hour rolling averages for trend calculation
    df_fe['vibration_24h_mean'] = df_fe['vibration'].rolling('24H').mean()
    df_fe['current_24h_mean'] = df_fe['current'].rolling('24H').mean()
    df_fe['temperature_24h_mean'] = df_fe['temperature'].rolling('24H').mean()

    # Reset index to get timestamp back as a column
    df_fe.reset_index(inplace=True)

    # Rate of change features (trends)
    df_fe['vibration_trend'] = df_fe['vibration'] - df_fe['vibration_24h_mean']
    df_fe['current_trend'] = df_fe['current'] - df_fe['current_24h_mean']
    df_fe['temperature_trend'] = df_fe['temperature'] - df_fe['temperature_24h_mean']

    # Interaction features
    df_fe['vibration_current_product'] = df_fe['vibration'] * df_fe['current']
    df_fe['vibration_temp_ratio'] = df_fe['vibration'] / (df_fe['temperature'] + 1e-6)
    df_fe['current_temp_ratio'] = df_fe['current'] / (df_fe['temperature'] + 1e-6)

    # Statistical features
    df_fe['vibration_zscore'] = (df_fe['vibration'] - df_fe['vibration'].mean()) / df_fe['vibration'].std()
    df_fe['current_zscore'] = (df_fe['current'] - df_fe['current'].mean()) / df_fe['current'].std()
    df_fe['temperature_zscore'] = (df_fe['temperature'] - df_fe['temperature'].mean()) / df_fe['temperature'].std()

    # Fill NaN values that result from rolling windows
    df_fe = df_fe.fillna(method='bfill').fillna(method='ffill')

    return df_fe

def prepare_features(df):
    """
    Prepare features for modeling by selecting relevant columns and handling categorical variables.

    Args:
        df (pd.DataFrame): Data with engineered features

    Returns:
        tuple: (X, y) features and target
    """
    # Select feature columns (exclude timestamp and target)
    feature_columns = [
        'vibration', 'current', 'temperature',
        'hour_of_day', 'day_of_week', 'month',
        'hour_sin', 'hour_cos', 'day_sin', 'day_cos',
        'vibration_72h_mean', 'current_72h_mean', 'temperature_72h_mean',
        'vibration_24h_mean', 'current_24h_mean', 'temperature_24h_mean',
        'vibration_trend', 'current_trend', 'temperature_trend',
        'vibration_current_product', 'vibration_temp_ratio', 'current_temp_ratio',
        'vibration_zscore', 'current_zscore', 'temperature_zscore'
    ]

    X = df[feature_columns].copy()
    y = df['failure_in_72_hours']

    return X, y

def train_model(X_train, y_train):
    """
    Train XGBoost classifier with specified hyperparameters.

    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training target

    Returns:
        xgb.XGBClassifier: Trained model
    """
    # Initialize XGBoost classifier with specified parameters
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
        eval_metric='logloss'
    )

    # Train the model
    model.fit(X_train, y_train)

    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance on test data.

    Args:
        model: Trained model
        X_test (pd.DataFrame): Test features
        y_test (pd.Series): Test target

    Returns:
        dict: Evaluation metrics
    """
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='binary'),
        'recall': recall_score(y_test, y_pred, average='binary'),
        'f1_score': f1_score(y_test, y_pred, average='binary'),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }

    return metrics, y_pred, y_pred_proba

def main():
    """Main function to train and evaluate the predictive maintenance model."""
    print("=== ArogyaJal Predictive Maintenance Model Training ===\n")

    # Load the dataset
    print("Loading dataset...")
    try:
        df = pd.read_csv('../data/pump_data.csv')
        print(f"Dataset loaded successfully: {len(df)} rows, {len(df.columns)} columns")
    except FileNotFoundError:
        print("Error: Dataset not found. Please run data_generator.py first.")
        return

    # Display basic information
    print(f"Target distribution:")
    print(df['failure_in_72_hours'].value_counts())
    print(f"Failure rate: {df['failure_in_72_hours'].mean():.3f}\n")

    # Perform feature engineering
    print("Performing feature engineering...")
    df_fe = feature_engineering(df)
    print(f"Features engineered: {len(df_fe.columns)} columns")

    # Prepare features and target
    X, y = prepare_features(df_fe)
    print(f"Feature matrix shape: {X.shape}")

    # Time-based split (80% training, 20% testing)
    split_index = int(len(X) * 0.8)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    print(f"Training failure rate: {y_train.mean():.3f}")
    print(f"Test failure rate: {y_test.mean():.3f}\n")

    # Feature scaling
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Convert back to DataFrame to maintain column names
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns)

    # Train the model
    print("Training XGBoost model...")
    model = train_model(X_train_scaled, y_train)
    print("Model training completed.\n")

    # Evaluate the model
    print("Evaluating model performance...")
    metrics, y_pred, y_pred_proba = evaluate_model(model, X_test_scaled, y_test)

    print("Evaluation Results:")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1_score']:.4f}")
    print(f"ROC AUC: {metrics['roc_auc']:.4f}\n")

    # Feature importance
    print("Top 10 Important Features:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print(feature_importance.head(10).to_string(index=False))
    print()

    # Classification report
    print("Detailed Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model and scaler
    print("Saving model and preprocessing components...")

    # Save model
    model_path = './final_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    # Save scaler
    scaler_path = './feature_scaler.pkl'
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)

    # Save feature columns
    feature_columns_path = './feature_columns.pkl'
    with open(feature_columns_path, 'wb') as f:
        pickle.dump(list(X.columns), f)

    print(f"Model saved to: {model_path}")
    print(f"Scaler saved to: {scaler_path}")
    print(f"Feature columns saved to: {feature_columns_path}")

    # Verify files were created
    import os
    if all(os.path.exists(path) for path in [model_path, scaler_path, feature_columns_path]):
        print("\n✓ Model training completed successfully!")
        print(f"✓ Model performance: ROC AUC = {metrics['roc_auc']:.4f}")
    else:
        print("\n✗ Error: Failed to save model files")

if __name__ == "__main__":
    main()