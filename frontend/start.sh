#!/bin/bash
# AI Stock Analyzer - Frontend Startup Script for Linux/macOS

set -e

echo "=========================================="
echo "   AI Stock Analyzer - Frontend Startup"
echo "=========================================="

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed."
    echo "Please install Node.js 18+ from https://nodejs.org"
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install --no-audit --no-fund
fi

# Build the frontend
echo "Building frontend..."
npm run build

echo ""
echo "=========================================="
echo "   Frontend built successfully!"
echo "   Output: ./dist/"
echo "   You can serve it with any static server"
echo "=========================================="
echo ""

# Optionally serve with a simple HTTP server
echo "Starting preview server on port 3000..."
python3 -m http.server 3000 --directory dist
