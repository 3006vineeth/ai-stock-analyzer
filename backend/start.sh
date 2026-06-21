#!/bin/bash
# AI Stock Analyzer - Backend Startup Script for Linux/macOS

set -e

echo "=========================================="
echo "   AI Stock Analyzer - Backend Startup"
echo "=========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.10+ from https://python.org"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo ""
echo "=========================================="
echo "   Starting FastAPI Server on port 8000"
echo "   API Docs: http://localhost:8000/docs"
echo "=========================================="
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
