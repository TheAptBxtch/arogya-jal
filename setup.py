#!/usr/bin/env python3
"""
ArogyaJal Predictive Maintenance System - Setup Script
This script helps with common installation issues and sets up the environment.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Please upgrade Python.")
        return False

    print("✅ Python version is compatible")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")

    # Try installing packages individually to avoid dependency conflicts
    packages = [
        "pandas>=2.0.0",
        "numpy>=1.20.0",
        "scikit-learn>=1.0.0",
        "joblib>=1.0.0",
        "plotly>=5.0.0",
        "streamlit>=1.20.0"
    ]

    for package in packages:
        if not run_command(f"pip install \"{package}\"", f"Installing {package}"):
            print(f"⚠️  Failed to install {package}. You may need to install it manually.")
            print(f"   Try: pip install {package}")

    return True

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")

    directories = ["data", "models"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory} directory")
        else:
            print(f"✅ {directory} directory already exists")

def test_imports():
    """Test if all required packages can be imported."""
    print("\n🧪 Testing package imports...")

    required_packages = {
        'pandas': 'pd',
        'numpy': 'np',
        'sklearn': 'sklearn',
        'joblib': 'joblib',
        'plotly': 'plotly',
        'streamlit': 'st'
    }

    all_good = True
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {package_name}: {e}")
            all_good = False

    return all_good

def main():
    """Main setup function."""
    print("🚀 ArogyaJal Predictive Maintenance System - Setup")
    print("=" * 60)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Create directories
    create_directories()

    # Install dependencies
    install_dependencies()

    # Test imports
    if test_imports():
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python data_generator.py")
        print("2. Run: python model_trainer.py")
        print("3. Run: streamlit run app.py")
        print("\n🌐 Or just run: streamlit run app.py and use the built-in buttons!")
    else:
        print("\n⚠️  Some packages failed to install. Please check the errors above.")
        print("💡 You can still try running the app, some features may not work.")
        print("🌐 Run: streamlit run app.py")

if __name__ == "__main__":
    main()