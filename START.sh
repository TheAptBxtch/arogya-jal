#!/bin/bash

# ArogyaJal - Click to Start (NO installation needed!)

echo ""
echo "================================================================"
echo "     ArogyaJal Predictive Maintenance System"
echo "================================================================"
echo "     ZERO Dependencies - NO pip installs needed!"
echo "================================================================"
echo ""

# Check if Python exists
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found!"
    echo ""
    echo "💡 OPTION 1: Install Python 3"
    echo "   - Ubuntu/Debian: sudo apt install python3"
    echo "   - macOS: brew install python3"
    echo ""
    echo "💡 OPTION 2: Just open 'index.html' in your browser!"
    echo "   (Double-click index.html - works without Python)"
    echo ""
    exit 1
fi

echo "✅ Python found - Starting server..."
echo ""

# Run the app
$PYTHON_CMD run_app.py