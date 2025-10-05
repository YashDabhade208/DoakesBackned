#!/bin/bash

# AI Audio Listener - Initial Setup Script

set -e

echo "🔧 Setting up AI Audio Listener..."

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if [ -f requirements/base.txt ]; then
    pip install -r requirements/base.txt
fi

if [ -f requirements/dev.txt ]; then
    pip install -r requirements/dev.txt
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p temp logs

# Check Redis installation
echo "🔴 Checking Redis..."
if command -v redis-server >/dev/null 2>&1; then
    echo "✅ Redis is installed"
    redis_version=$(redis-server --version | awk '{print $2}')
    echo "✅ Redis version: $redis_version"
else
    echo "⚠️  Redis not found. Please install Redis for full functionality."
    echo "   On Ubuntu/Debian: sudo apt-get install redis-server"
    echo "   On macOS: brew install redis"
fi

# Check FFmpeg installation
echo "🎵 Checking FFmpeg..."
if command -v ffmpeg >/dev/null 2>&1; then
    echo "✅ FFmpeg is installed"
    ffmpeg_version=$(ffmpeg -version | head -n1 | awk '{print $3}')
    echo "✅ FFmpeg version: $ffmpeg_version"
else
    echo "⚠️  FFmpeg not found. Please install FFmpeg for audio processing."
    echo "   On Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "   On macOS: brew install ffmpeg"
fi

# Setup complete
echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the .env file with your configuration:"
echo "   - Set your OpenAI API key"
echo "   - Configure Redis settings"
echo "   - Adjust other settings as needed"
echo ""
echo "2. Start the application:"
echo "   - Development: ./scripts/start.sh"
echo "   - Production: ./scripts/start-prod.sh"
echo ""
echo "3. Access the application:"
echo "   - API: http://localhost:8000"
echo "   - WebSocket: ws://localhost:8000/ws/audio"
echo "   - Health: http://localhost:8000/health"
echo ""
echo "📚 For more information, see README.md"
