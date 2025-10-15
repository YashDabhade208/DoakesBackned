# 🎙️ Doakes - Your Paranoid Digital Stalker

> *"Surprise, motherf***er! I've been listening to everything you said today."* - James Doakes, probably

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🤔 What Fresh Hell Is This?

Ever wonder what you actually do all day? Spoiler alert: probably nothing productive. **Doakes** is your personal NSA agent, except you're paying for it voluntarily. This beautiful nightmare records your entire day, sends it to our server (yes, *our* server), and returns a brutally honest summary of your existence.

Think of it as a FitBit for your mouth. Except instead of steps, we're counting your bad decisions.

## ✨ Features

- **🎙️ 24/7 Audio Recording** - Captures every word, sigh, and existential crisis
- **☁️ Cloud Sync** - Your data, but make it someone else's problem
- **🤖 AI-Powered Analysis** - Get roasted by our brutally honest AI
- **📊 Daily Summaries** - TL;DR of your life's greatest hits (and misses)
- **🔄 Background Operation** - Runs quietly in the background, just like your anxiety
- **📱 Cross-Platform** - Works on your machine (probably)

### 🎯 Perfect For

- 🧠 People with memory issues (or selective amnesia)
- 🎭 Anyone who wants evidence of their productivity theater
- 😅 Masochists who enjoy being confronted with reality
- 🎮 That person who says "I'm so busy" but has 200+ hours in Stardew Valley
- 🕵️‍♂️ Wannabe detectives who want to analyze their own conversations

## 🏗️ Tech Stack

| Component       | Technology | Why We Chose It |
|-----------------|------------|-----------------|
| Backend         | FastAPI    | Because async is fun |
| Database        | SQLite     | It's basically magic |
| ORM             | SQLAlchemy | For when raw SQL gives you hives |
| Data Validation | Pydantic   | Because users are unpredictable |
| AI              | OpenAI API | For when you want to feel inferior to a machine |
| Audio Processing| PyDub      | Turns sound into 1s and 0s |

## 📁 Project Structure

```
doakes/
├── app/                    # Main application package
│   ├── api/               # API routes and endpoints
│   │   └── routes.py      # All the HTTP endpoints
│   │
│   ├── core/              # Core application logic
│   │   ├── config.py      # Configuration management
│   │   └── security.py    # Authentication and security
│   │
│   ├── db/                # Database models and connections
│   │   ├── models/        # SQLAlchemy models
│   │   └── database.py    # Database connection and session management
│   │
│   ├── services/          # Business logic
│   │   ├── audio.py       # Audio processing service
│   │   └── summary.py     # AI summarization service
│   │
│   ├── utils/             # Utility functions
│   │   ├── audio_utils.py # Audio processing helpers
│   │   └── logger.py      # Logging configuration
│   │
│   └── main.py            # FastAPI application entry point
│
├── tests/                 # Tests (you write those, right?)
├── scripts/               # Utility scripts
├── .env.example           # Environment template
├── requirements.txt       # Project dependencies
├── README.md              # This file
└── run_server.bat         # Quick start script (Windows)
```

### Key Files

- `app/main.py` - The heart of the application where FastAPI is configured
- `app/api/routes.py` - API endpoints for audio uploads and summaries
- `app/services/audio.py` - Handles all audio processing logic
- `app/services/summary.py` - AI-powered summary generation
- `app/db/models/` - Database models (User, Session, etc.)
- `.env` - Configuration (not committed to version control)



## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A microphone (or a good imagination)
- An AI API key (OpenAI, Anthropic, etc.)
- A healthy disregard for privacy

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/doakes.git
   cd doakes
   ```

2. **Set up a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment**:
   ```bash
   # Windows
   copy .env.example .env
   
   # Mac/Linux
   cp .env.example .env
   ```
   Then edit `.env` with your favorite text editor and add your API keys.

### Configuration

Edit your `.env` file with the following settings:

```ini
# Database configuration
DATABASE_URL=sqlite:///./doakes.db  # Or use PostgreSQL if you're fancy

# Security
SECRET_KEY=change-this-to-something-secure

# AI Settings
AI_API_KEY=your-ai-api-key-here
AI_MODEL=gpt-4  # or your preferred model

# File Storage
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=104857600  # 100MB in bytes

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=True  # Set to False in production!
```

### Running the Server

Start the development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the provided script:

```bash
# Windows
.\run_server.bat

# Mac/Linux
chmod +x run_server.sh
./run_server.sh
```

Once running, you can access:
- **API Documentation**: http://localhost:8000/docs
- **Interactive API Docs**: http://localhost:8000/redoc
- **Your Application**: http://localhost:8000

### First Run

1. Open your browser to http://localhost:8000
2. Grant microphone permissions when prompted
3. Start talking (or don't, we're not your boss)
4. Check back later for your personalized life summary


## 📡 API Endpoints (The Good Stuff)

### Upload Audio
POST /api/audio/upload
Content-Type: multipart/form-data

{
"audio_file": <your-audio-file>,
"user_id": "uuid-or-whatever",
"session_date": "2025-10-15"
}

text

### Get Summary
GET /api/summary/{session_id}

Response:
{
"session_id": "uuid",
"date": "2025-10-15",
"summary": "You talked about pizza 47 times. Seek help.",
"duration": "8 hours of your life you'll never get back",
"highlight": "Most used phrase: 'I'll do it tomorrow'"
}

text

## 🧪 Testing (For People Who Care About Quality)

Run tests
pytest

Run with coverage (for the overachievers)
pytest --cov=app tests/

Ignore tests and YOLO to production
(not recommended but we won't judge)
text

## 🔐 Security Notes

- Don't commit your `.env` file (we already added it to `.gitignore`, you're welcome)
- Use HTTPS in production (or don't, live dangerously)
- Rotate your API keys regularly (or when they leak on GitHub)
- This app literally records everything you say. Think about that.

## 🐛 Known Issues

- The AI sometimes gets sarcastic (we consider this a feature)
- Audio processing might take a while (patience, young grasshopper)
- Your life summary might be depressing (not our fault)
- Server might crash if you talk too much (consider therapy)

## 🤝 Contributing

Pull requests welcome! We accept:
- Bug fixes
- New features
- Existential rants in commit messages
- Coffee donations

## 📜 License

MIT License - Do whatever you want, we're not your parents.

## ⚠️ Disclaimer

This project is for educational purposes. We are not responsible for:
- Your shattered illusions of productivity
- Relationship damage from recording conversations
- Legal issues from recording people without consent
- Existential crises from hearing your own voice
- AI roasting you harder than your friends do

**Use responsibly. Or don't. We're a README, not a cop.**

## 🙏 Acknowledgments

- James Doakes from Dexter (RIP, you suspicious legend)
- Every privacy advocate having a heart attack reading this
- Coffee, Red Bull, and questionable life choices
- Stack Overflow (because who actually reads documentation?)

---

*"Some people's idea of free speech is that they are free to say what they like, but if anyone says anything back, that is an outrage."* - Winston Churchill (probably not about this project, but it fits)

Built with 💀 and concerning amounts of caffeine.