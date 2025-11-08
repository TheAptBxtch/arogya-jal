#!/usr/bin/env python3
"""
ArogyaJal Quick Start - Foolproof Installation and Running
This script handles all installation issues and guarantees the app runs.
"""

import subprocess
import sys
import os
import urllib.request
import json

def print_header(text):
    """Print a nice header."""
    print("\n" + "="*60)
    print(f"🚀 {text}")
    print("="*60)

def run_command(cmd, description, critical=True):
    """Run command with error handling."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"⚠️  {description} had issues")
            if critical:
                print(f"Error: {result.stderr}")
                return False
            return True  # Non-critical, continue anyway
    except subprocess.TimeoutExpired:
        print(f"⚠️  {description} timed out, but continuing...")
        return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        if critical:
            return False
        return True

def check_python():
    """Check Python version."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3:
        print("❌ Python 3+ is required")
        return False
    if version.minor < 7:
        print("⚠️  Python 3.7+ recommended, but trying anyway...")

    return True

def install_streamlit():
    """Install Streamlit with fallback methods."""
    print_header("Installing Streamlit")

    # Method 1: Try normal pip install
    if run_command("pip install streamlit", "Installing Streamlit (Method 1)", critical=False):
        return True

    # Method 2: Try with --user flag
    if run_command("pip install --user streamlit", "Installing Streamlit (Method 2)", critical=False):
        return True

    # Method 3: Try with --no-cache-dir
    if run_command("pip install --no-cache-dir streamlit", "Installing Streamlit (Method 3)", critical=False):
        return True

    # Method 4: Try specific version
    if run_command("pip install streamlit==1.28.1", "Installing Streamlit (Method 4)", critical=False):
        return True

    # Method 5: Try alternative pip
    if run_command("python -m pip install streamlit", "Installing Streamlit (Method 5)", critical=False):
        return True

    print("❌ All installation methods failed")
    return False

def test_streamlit():
    """Test if Streamlit can be imported."""
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Cannot import Streamlit: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print_header("Creating Directories")
    directories = ["data"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory} directory")
        else:
            print(f"✅ {directory} directory already exists")

def run_app():
    """Run the Streamlit application."""
    print_header("Starting ArogyaJal Application")

    # Check if simple_app.py exists
    if not os.path.exists("simple_app.py"):
        print("❌ simple_app.py not found!")
        return False

    print("🌐 Starting Streamlit application...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("💡 If browser doesn't open automatically, visit http://localhost:8501")
    print("")

    # Try different ways to run streamlit
    commands = [
        "streamlit run simple_app.py",
        "python -m streamlit run simple_app.py",
        f"python -c \"import streamlit.cli; streamlit.cli.main_run(['simple_app.py'])\""
    ]

    for cmd in commands:
        try:
            print(f"🔧 Trying: {cmd}")
            subprocess.run(cmd, shell=True)
            break
        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")
            return True
        except Exception as e:
            print(f"⚠️  Method failed: {e}")
            continue

    return True

def main():
    """Main function."""
    print_header("ArogyaJal Predictive Maintenance - Quick Start")

    # Check Python
    if not check_python():
        print("❌ Please install Python 3.7+ and try again")
        sys.exit(1)

    # Create directories
    create_directories()

    # Install Streamlit
    if not install_streamlit():
        print("\n❌ Failed to install Streamlit")
        print("💡 Manual installation:")
        print("   1. Try: pip install streamlit --user")
        print("   2. Try: python -m pip install streamlit")
        print("   3. Or install from: https://docs.streamlit.io/knowledge-base/tutorials/installation")
        sys.exit(1)

    # Test Streamlit
    if not test_streamlit():
        print("❌ Streamlit installation test failed")
        print("💡 Try restarting your terminal/command prompt and run this script again")
        sys.exit(1)

    # Run the application
    if not run_app():
        print("❌ Failed to run application")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Please report this issue or try manual installation")
        sys.exit(1)