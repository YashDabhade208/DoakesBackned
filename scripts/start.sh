#!/bin/bash

# AI Audio Listener - Development Startup Script

set -e

echo "🚀 Starting AI Audio Listener (Development Mode)"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p temp logs

# Install dependencies if requirements files exist
if [ -f requirements/dev.txt ]; then
    echo "📦 Installing development dependencies..."
    pip install -r requirements/dev.txt
fi

# Start Redis (if not already running)
echo "🔴 Starting Redis..."
if ! pgrep -x "redis-server" > /dev/null; then
    redis-server --daemonize yes
    echo "✅ Redis started"
else
    echo "✅ Redis already running"
fi

# Start the application
echo "🎯 Starting AI Audio Listener..."
echo "📍 Application will be available at: http://localhost:8000"
echo "🔗 WebSocket endpoint: ws://localhost:8000/ws/audio"
echo "❤️  Health check: http://localhost:8000/health"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level info
