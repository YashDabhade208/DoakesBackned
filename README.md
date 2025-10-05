# AI Audio Listener

A real-time AI-powered audio listener application that provides speech-to-text transcription and AI analysis capabilities through WebSocket connections and REST API endpoints.

## Features

- **Real-time Audio Processing**: Stream audio data via WebSocket for real-time transcription
- **Speech-to-Text**: Powered by OpenAI Whisper for accurate transcription
- **AI Analysis**: GPT-powered text analysis and insights
- **REST API**: Full REST API for audio file upload and processing
- **Health Monitoring**: Comprehensive health checks and monitoring endpoints
- **Docker Support**: Ready for containerized deployment
- **Redis Caching**: High-performance caching and session management

## Architecture

```
ai-audio-listener/
├── app/                    # Main application package
│   ├── api/               # API endpoints (REST & WebSocket)
│   ├── core/              # Core functionality (WebSocket manager, audio processor, STT engine)
│   ├── models/            # Data models (Pydantic models)
│   ├── services/          # Business logic (transcription, analysis)
│   └── utils/             # Utility functions (audio processing, logging)
├── deployment/            # Deployment configurations
├── scripts/               # Startup and setup scripts
├── tests/                 # Test files
├── requirements/          # Dependency management
└── docs/                  # Documentation
```

## Quick Start

### Prerequisites

- Python 3.11+
- Redis server
- FFmpeg (for audio processing)
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-audio-listener
   ```

2. **Setup the environment**
   ```bash
   ./scripts/setup.sh
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements/dev.txt
   ```

5. **Start the application**
   ```bash
   # Development mode
   ./scripts/start.sh

   # Production mode
   ./scripts/start-prod.sh
   ```

## API Endpoints

### WebSocket Endpoints

- `ws://localhost:8000/ws/audio` - Real-time audio streaming

### REST Endpoints

- `GET /` - Root endpoint
- `POST /audio/upload` - Upload audio file
- `GET /audio/process/{file_id}` - Get processing status
- `POST /audio/transcribe` - Transcribe audio
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed health check

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `API_HOST` | API host | `0.0.0.0` |
| `API_PORT` | API port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Audio Configuration

- **Sample Rate**: 16kHz (configurable)
- **Channels**: Mono (configurable)
- **Chunk Size**: 1024 samples (configurable)
- **Supported Formats**: WAV, MP3, FLAC, M4A

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/

# Type check
mypy app/
```

### Docker Development

```bash
# Build and run with Docker Compose
docker-compose up --build

# Production deployment
docker-compose -f deployment/docker-compose.prod.yml up -d
```

## Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Copy and configure production environment
   cp .env.example .env.prod
   # Edit .env.prod with production values
   ```

2. **Docker Deployment**
   ```bash
   # Build and deploy
   docker-compose -f deployment/docker-compose.prod.yml up -d --build
   ```

3. **Nginx Configuration**
   - SSL certificates should be placed in `deployment/ssl/`
   - Update `nginx.conf` with your domain configuration

### Monitoring

- Health checks: `GET /health`
- Detailed status: `GET /health/detailed`
- Application logs: `logs/ai_audio_listener.log`

## WebSocket Usage

### Client Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/audio');

// Send audio data
const audioData = new Float32Array(1024); // Your audio chunk
ws.send(audioData);

// Receive transcription results
ws.onmessage = (event) => {
    const result = JSON.parse(event.data);
    if (result.type === 'transcription_result') {
        console.log('Transcription:', result.data.text);
    }
};
```

### Audio Format Requirements

- **Encoding**: 16-bit PCM
- **Sample Rate**: 16kHz (recommended)
- **Channels**: Mono
- **Chunk Size**: 1024 samples (configurable)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API examples

## Roadmap

- [ ] Real-time audio visualization
- [ ] Multiple language support
- [ ] Audio filtering and noise reduction
- [ ] Integration with external STT services
- [ ] Mobile app support
- [ ] Kubernetes deployment templates
