#this is model-autopsy-ai/run.sh file used to run the application on unix based systems

#!/bin/bash

# Model Autopsy AI - Run Script
# This script sets up and runs the application

# Navigate to project root
cd "$(dirname "$0")/.."

echo "🔬 Model Autopsy AI - Starting..."

# Check Python version
python_version=$(python --version 2>&1)
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your API keys"
fi

# Run the application
echo ""
echo "🚀 Starting FastAPI server..."
echo "📖 API Documentation will be available at: http://127.0.0.1:8000/docs"
echo "🏥 Health Check: http://127.0.0.1:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
