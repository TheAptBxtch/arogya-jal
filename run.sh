#!/bin/bash

# ArogyaJal Predictive Maintenance System - Quick Run Script

echo "🚀 ArogyaJal Predictive Maintenance System"
echo "=========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python3 found"

# Navigate to script directory
cd "$(dirname "$0")"

# Setup function
setup() {
    echo "🔧 Setting up environment..."
    python3 setup.py
}

# Run app function
run_app() {
    echo "🌐 Starting Streamlit application..."
    echo "📱 The app will open in your browser at http://localhost:8501"
    echo "🛑 Press Ctrl+C to stop the application"
    echo ""
    streamlit run app.py
}

# Main menu
case "${1:-menu}" in
    "setup")
        setup
        ;;
    "run")
        run_app
        ;;
    "menu"|*)
        echo "Please choose an option:"
        echo "1) Setup environment (install dependencies)"
        echo "2) Run application"
        echo "3) Quick start (setup + run)"
        echo "4) Exit"
        echo ""
        read -p "Enter your choice (1-4): " choice

        case $choice in
            1)
                setup
                ;;
            2)
                run_app
                ;;
            3)
                setup
                echo ""
                echo "🎯 Setup completed! Starting application..."
                run_app
                ;;
            4)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid choice. Please run the script again."
                exit 1
                ;;
        esac
        ;;
esac