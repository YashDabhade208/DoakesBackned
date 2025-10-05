#!/bin/bash

# AI Audio Listener - Production Startup Script

set -e

echo "🚀 Starting AI Audio Listener (Production Mode)"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

# Source environment variables
source .env

# Check required environment variables
REQUIRED_VARS=("OPENAI_API_KEY" "REDIS_PASSWORD")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Required environment variable $var is not set"
        exit 1
    fi
done

echo "✅ Environment configuration validated"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p temp logs ssl

# Start the application with Gunicorn
echo "🎯 Starting AI Audio Listener with Gunicorn..."
echo "📍 Application will be available at: http://localhost:8000"
echo "🔗 WebSocket endpoint: ws://localhost:8000/ws/audio"
echo "❤️  Health check: http://localhost:8000/health"
echo ""

# Start Gunicorn
exec gunicorn --config deployment/gunicorn.conf.py app.main:app
