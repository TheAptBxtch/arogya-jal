#!/bin/bash

# ArogyaJal Easy Run for Linux/Mac - Bypasses all installation issues

echo "🚀 ArogyaJal Predictive Maintenance System"
echo "=========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not found. Please install Python 3.7+ first."
    echo "💡 On Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "💡 On macOS: brew install python3"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo "✅ Python found: $PYTHON_CMD"

# Create data directory
mkdir -p data
echo "✅ Created data directory"

# Try to install streamlit with multiple methods
echo
echo "🔧 Installing Streamlit (this may take a minute)..."

# Method 1: Standard pip
if $PIP_CMD install streamlit &> /dev/null; then
    echo "✅ Streamlit installed successfully"
elif $PIP_CMD install --user streamlit &> /dev/null; then
    echo "✅ Streamlit installed successfully (user installation)"
elif $PIP_CMD install --no-cache-dir streamlit &> /dev/null; then
    echo "✅ Streamlit installed successfully (no cache)"
elif $PIP_CMD install streamlit==1.28.1 &> /dev/null; then
    echo "✅ Streamlit installed successfully (specific version)"
elif $PYTHON_CMD -m pip install streamlit &> /dev/null; then
    echo "✅ Streamlit installed successfully (python -m pip)"
else
    echo "❌ Failed to install Streamlit automatically"
    echo
    echo "💡 Please try manual installation:"
    echo "   $PIP_CMD install streamlit"
    echo "   or: $PIP_CMD install --user streamlit"
    echo
    echo "For more help: https://docs.streamlit.io/knowledge-base/tutorials/installation"
    exit 1
fi

# Run the application
echo
echo "🌐 Starting ArogyaJal Application..."
echo "📱 Opening browser at http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo
echo "💡 If browser doesn't open automatically, visit: http://localhost:8501"
echo

# Try different run methods
if command -v streamlit &> /dev/null; then
    streamlit run simple_app.py
elif $PYTHON_CMD -m streamlit run simple_app.py &> /dev/null; then
    $PYTHON_CMD -m streamlit run simple_app.py
else
    echo "❌ Failed to start Streamlit"
    echo "💡 Please try running manually:"
    echo "   streamlit run simple_app.py"
    echo "   or: $PYTHON_CMD -m streamlit run simple_app.py"
fi

echo
echo "👋 Thank you for using ArogyaJal!"