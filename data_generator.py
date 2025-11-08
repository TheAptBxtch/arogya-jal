import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_synthetic_pump_data():
    """
    Generate synthetic time-series sensor data for water pumps with realistic failure patterns.

    Returns:
        pd.DataFrame: Dataset with columns: timestamp, vibration, current, temperature, failure_in_72_hours
    """

    print("🔧 Generating synthetic pump sensor data...")

    # Initialize data storage
    data = []

    # Start from a recent timestamp
    current_time = datetime.now() - timedelta(days=42)  # 6 weeks ago
    end_time = datetime.now()

    # Generate time-series data with random intervals
    failure_count = 0
    while current_time < end_time and len(data) < 1000:
        # Random interval between 1-6 hours
        interval_hours = random.uniform(1, 6)
        current_time += timedelta(hours=interval_hours)

        # Base sensor values (normal operating ranges)
        base_vibration = random.uniform(0.1, 2.0)  # mm/s
        base_current = random.uniform(8.0, 15.0)   # A
        base_temperature = random.uniform(45, 75)  # °C

        # Check if this reading should be part of a failure pattern
        failure_in_72_hours = 0

        # Randomly select failure events (15-20 failures in dataset)
        if random.random() < 0.018 and failure_count < 20:  # ~1.8% chance per reading
            failure_count += 1
            failure_time = current_time + timedelta(hours=random.uniform(24, 72))

            # Check if we have enough data points for the failure pattern
            temp_failure_time = failure_time
            failure_readings = []

            while temp_failure_time > current_time and len(failure_readings) < 20:
                failure_readings.append(temp_failure_time)
                temp_failure_time -= timedelta(hours=random.uniform(1, 6))

            # Generate failure pattern readings
            for i, failure_timestamp in enumerate(reversed(failure_readings)):
                hours_to_failure = (failure_timestamp - current_time).total_seconds() / 3600

                if hours_to_failure <= 72 and hours_to_failure > 0:
                    # Exponential increase in vibration and current as failure approaches
                    vibration_multiplier = 1.0 + (2.0 * (1 - hours_to_failure / 72))
                    current_multiplier = 1.0 + (1.5 * (1 - hours_to_failure / 72))

                    # Add temperature increase
                    temp_increase = 5 + (5 * (1 - hours_to_failure / 72))

                    # Calculate final values with multipliers
                    vibration = base_vibration * vibration_multiplier
                    current = base_current * current_multiplier
                    temperature = base_temperature + temp_increase
                    failure_in_72_hours = 1

                    # Add 5-10% random noise to simulate sensor imprecision
                    vibration *= random.uniform(0.95, 1.05)
                    current *= random.uniform(0.95, 1.05)
                    temperature *= random.uniform(0.95, 1.05)

                    data.append({
                        'timestamp': failure_timestamp,
                        'vibration': round(vibration, 3),
                        'current': round(current, 2),
                        'temperature': round(temperature, 1),
                        'failure_in_72_hours': failure_in_72_hours
                    })

        # Add normal reading (if not part of failure pattern)
        if failure_in_72_hours == 0:
            # Add 5-10% random noise to simulate sensor imprecision
            vibration = base_vibration * random.uniform(0.95, 1.05)
            current = base_current * random.uniform(0.95, 1.05)
            temperature = base_temperature * random.uniform(0.95, 1.05)

            data.append({
                'timestamp': current_time,
                'vibration': round(vibration, 3),
                'current': round(current, 2),
                'temperature': round(temperature, 1),
                'failure_in_72_hours': failure_in_72_hours
            })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Sort by timestamp and ensure we have exactly 1000 rows
    df = df.sort_values('timestamp').head(1000)

    # Reset index
    df = df.reset_index(drop=True)

    return df

def main():
    """Main function to generate and save the synthetic dataset."""
    try:
        print("🚀 Starting ArogyaJal Data Generation")
        print("=" * 50)

        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)

        # Generate data
        df = generate_synthetic_pump_data()

        # Display dataset information
        print(f"✅ Dataset generated successfully!")
        print(f"📊 Total records: {len(df)} rows")
        print(f"📅 Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        print(f"⚠️  Failure events: {df['failure_in_72_hours'].sum()} ({df['failure_in_72_hours'].sum()/len(df)*100:.1f}%)")

        # Display sample data
        print("\n📋 Sample data:")
        print(df.head().to_string(index=False))

        # Display statistics
        print("\n📈 Dataset statistics:")
        print(df[['vibration', 'current', 'temperature']].describe().round(2))

        # Verify sensor ranges
        print(f"\n🔍 Sensor value ranges:")
        print(f"   Vibration: {df['vibration'].min():.3f} - {df['vibration'].max():.3f} mm/s")
        print(f"   Current: {df['current'].min():.2f} - {df['current'].max():.2f} A")
        print(f"   Temperature: {df['temperature'].min():.1f} - {df['temperature'].max():.1f} °C")

        # Save to CSV
        output_path = 'data/pump_data.csv'
        df.to_csv(output_path, index=False)
        print(f"\n💾 Dataset saved to: {output_path}")

        # Verify the file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"📁 File size: {file_size} bytes")
            print("✅ Data generation completed successfully!")
        else:
            print("❌ Error: Failed to save dataset")

    except Exception as e:
        print(f"❌ Error during data generation: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()