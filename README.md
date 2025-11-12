# SocialProof Backend API

A sophisticated cybersecurity simulation game backend built with FastAPI, PostgreSQL, and SQLAlchemy. This system provides the foundational infrastructure for a game that helps users identify and defend against social engineering attacks.

## Technology Stack

### Core Backend (Part 1)
- **Web Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy 2.0+ (async support)
- **Data Validation**: Pydantic 2.5+
- **Database Migrations**: Alembic
- **ASGI Server**: Uvicorn

### AI System (Part 2)
- **LLM Orchestration**: LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: sentence-transformers
- **AI Providers**: 
  - Google Gemini (gemini-1.5-flash)
  - Groq (llama-3.1-8b-instant)
  - OpenRouter (multiple models)

## Project Structure

```
/SocialProof
│
├── alembic/                    # Database migration scripts (generated)
├── alembic.ini                 # Alembic configuration (generated)
│
├── app/
│   ├── __init__.py            # Package initialization
│   ├── main.py                # FastAPI app entry point & API routes
│   ├── database.py            # Database engine, session management
│   ├── crud.py                # Database CRUD operations
│   ├── models.py              # SQLAlchemy ORM table definitions
│   ├── schemas.py             # Pydantic data validation schemas
│   └── ai_core.py             # 🆕 AI system with multi-provider support
│
├── knowledge_base/             # 🆕 Educational content for RAG
│   ├── phishing.txt           #     Email phishing knowledge
│   ├── smishing.txt           #     SMS phishing knowledge
│   └── social_engineering.txt #     Social engineering knowledge
│
├── .env                       # Environment variables (create from .env.example)
├── .env.example               # Template for environment variables
├── requirements.txt           # Python dependencies
│
├── README.md                  # Project overview (you are here)
├── SETUP_GUIDE.md             # Detailed Part 1 setup instructions
├── AI_SETUP_GUIDE.md          # 🆕 Part 2 AI integration guide
├── PART2_QUICKSTART.md        # 🆕 10-minute AI setup
├── PART2_IMPLEMENTATION_SUMMARY.md  # 🆕 Technical deep-dive
├── QUICK_REFERENCE.md         # API endpoints cheat sheet
├── ARCHITECTURE.md            # System design documentation
└── PROJECT_SUMMARY.md         # Executive summary
```

## Features

### Part 1: Core Backend
- ✅ Async/await support throughout the entire stack
- ✅ RESTful API design with automatic OpenAPI documentation
- ✅ Comprehensive input validation using Pydantic
- ✅ Database migrations with Alembic
- ✅ Type hints and extensive documentation
- ✅ Production-ready error handling
- ✅ Pagination support for list endpoints

### Part 2: AI Integration 🆕
- ✅ **Multi-Provider LLM Support** - Seamlessly switch between Google Gemini, Groq, and OpenRouter
- ✅ **Dynamic Scenario Generation** - AI creates realistic phishing attacks adapted to player skill
- ✅ **Digital Guardian** - RAG-powered cybersecurity assistant
- ✅ **Difficulty Adaptation** - Scenarios scale from beginner to elite based on player rating
- ✅ **Factory Pattern** - Clean provider abstraction, easy to extend
- ✅ **Knowledge Base RAG** - ChromaDB vector search with educational content

## API Endpoints

### Root
- `GET /` - Welcome message
- `GET /health` - Health check

### Players
- `POST /players/` - Create a new player
- `GET /players/` - List all players (paginated)
- `GET /players/{player_id}` - Get a specific player

### Scenarios
- `POST /scenarios/` - Create a new game scenario
- `GET /scenarios/{scenario_id}` - Get a specific scenario
- `GET /players/{player_id}/scenarios` - Get all scenarios for a player

### AI Features 🆕
- `POST /scenarios/generate` - Generate AI-powered scenario (adapts to player skill)
- `POST /guardian/query` - Ask the Digital Guardian cybersecurity questions
- `GET /ai/provider` - Check current LLM provider status
- `GET /ai/validate` - Validate AI configuration

## Setup and Execution Guide

### Part 1: Core Backend Setup

Follow these steps carefully to set up and run the SocialProof backend:

**📖 For detailed step-by-step instructions, see:** `SETUP_GUIDE.md`

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher installed and running
- Conda environment (as you mentioned you're using Conda)

### Step 1: Install Dependencies

Since you're using Conda, activate your environment first, then install the required packages:

```bash
pip install -r requirements.txt
```

### Step 2: Set Up PostgreSQL Database

1. Start PostgreSQL server (if not already running)
2. Create a new database for SocialProof:

```bash
# Login to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE socialproof_db;
CREATE USER socialproof_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE socialproof_db TO socialproof_user;

# Grant schema privileges (PostgreSQL 15+)
\c socialproof_db
GRANT ALL ON SCHEMA public TO socialproof_user;

# Exit psql
\q
```

### Step 3: Configure Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your actual database credentials:

```env
DATABASE_URL="postgresql+asyncpg://socialproof_user:your_secure_password@localhost:5432/socialproof_db"
```

**Important**: Make sure to replace:
- `socialproof_user` with your PostgreSQL username
- `your_secure_password` with your actual password
- `localhost` with your database host (if different)
- `5432` with your PostgreSQL port (if different)
- `socialproof_db` with your database name (if different)

### Step 4: Initialize Alembic for Database Migrations

1. Initialize Alembic (this creates the `alembic/` directory and `alembic.ini` file):

```bash
alembic init alembic
```

2. Configure `alembic.ini`:

Open `alembic.ini` and find the line that starts with `sqlalchemy.url`. Comment it out or replace it with:

```ini
# sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = 
```

We'll use the environment variable instead, which is more secure.

3. Configure `alembic/env.py`:

Open `alembic/env.py` and make the following modifications:

**a) Add imports at the top** (around line 6-10):

```python
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import our app
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import Base
from app import models  # This imports all models
```

**b) Load environment variables** (around line 15-20, after the Alembic config):

```python
# Load environment variables
load_dotenv()

# Get the database URL from environment
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
```

**c) Set target metadata** (find the line `target_metadata = None` around line 20-25 and replace it):

```python
# target_metadata = None
target_metadata = Base.metadata
```

4. Create the initial migration:

```bash
alembic revision --autogenerate -m "Initial database schema"
```

This will generate a migration file in `alembic/versions/` that contains the SQL commands to create your tables.

5. Apply the migration to create tables:

```bash
alembic upgrade head
```

You should see output indicating that the tables were created successfully.

### Step 5: Verify Database Setup

Connect to PostgreSQL and verify the tables were created:

```bash
psql -U socialproof_user -d socialproof_db

# Inside psql:
\dt  # List all tables - you should see player_profiles and game_scenarios

# Exit
\q
```

### Step 6: Run the Development Server

Start the FastAPI development server with auto-reload:

```bash
uvicorn app.main:app --reload
```

You should see output similar to:

```
INFO:     Will watch for changes in these directories: ['/path/to/SocialProof']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 7: Test the API

1. **Open the interactive API documentation**:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

2. **Test the welcome endpoint**:

```bash
curl http://127.0.0.1:8000/
```

Expected response:
```json
{
  "message": "Welcome to the SocialProof API",
  "version": "1.0.0",
  "documentation": "/docs"
}
```

3. **Create a test player**:

```bash
curl -X POST "http://127.0.0.1:8000/players/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "test_player",
       "email": "test@example.com"
     }'
```

Expected response:
```json
{
  "username": "test_player",
  "email": "test@example.com",
  "id": 1,
  "player_skill_rating": 500.0,
  "created_at": "2025-11-06T..."
}
```

4. **Retrieve the player**:

```bash
curl http://127.0.0.1:8000/players/1
```

## Development Workflow

### Making Database Schema Changes

When you modify the models in `app/models.py`:

1. Create a new migration:
```bash
alembic revision --autogenerate -m "Description of your changes"
```

2. Review the generated migration file in `alembic/versions/`

3. Apply the migration:
```bash
alembic upgrade head
```

4. To rollback one migration:
```bash
alembic downgrade -1
```

### Running with Custom Host/Port

```bash
# Custom port
uvicorn app.main:app --reload --port 8080

# Custom host (accessible from network)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Issue: "Import errors" when running the server

**Solution**: Make sure you're in the project root directory (where `app/` folder is located) when running uvicorn.

### Issue: "Database connection failed"

**Solutions**:
1. Verify PostgreSQL is running: `pg_isready`
2. Check your `.env` file has the correct credentials
3. Ensure the database exists: `psql -U postgres -l`
4. Test connection manually: `psql -U socialproof_user -d socialproof_db`

### Issue: "relation does not exist" errors

**Solution**: Run the Alembic migrations:
```bash
alembic upgrade head
```

### Issue: Alembic can't find models

**Solution**: Make sure `alembic/env.py` correctly imports the models and sets `target_metadata = Base.metadata`

## Next Steps (Part 2)

### 🤖 AI Integration Complete! ✅

The SocialProof backend now includes a sophisticated multi-provider AI system:

**Quick Start (10 minutes):**
1. Read: `PART2_QUICKSTART.md` - Get AI running fast
2. Then: `AI_SETUP_GUIDE.md` - Complete setup guide
3. Deep-dive: `PART2_IMPLEMENTATION_SUMMARY.md` - Technical details

**What's New:**
- ✅ Multi-provider LLM support (Google, Groq, OpenRouter)
- ✅ RAG-powered Digital Guardian assistant
- ✅ Adaptive scenario generation
- ✅ Dynamic provider switching
- ✅ Factory pattern architecture
- ✅ Production-ready AI pipeline

**Getting Started with AI:**
```bash
# 1. Install AI dependencies
pip install -r requirements.txt

# 2. Get an API key (Groq is fastest: console.groq.com/keys)

# 3. Configure .env
LLM_PROVIDER="groq"
GROQ_API_KEY="your_key_here"

# 4. Start server and test!
uvicorn app.main:app --reload
```

### Future Enhancements (Part 3+)

The foundation is complete. Future development could include:

- 🔐 Authentication and authorization (JWT)
- 🎮 Real-time game mechanics (WebSockets)
- 🏆 Leaderboard and achievements
- 📈 Advanced analytics dashboard
- 🎨 Frontend application (React/Vue)
- 📧 Email/SMS integration for realistic scenarios
- � Multi-language support
- 🧪 Comprehensive test suite
- � Machine learning-based player profiling
- 🔄 Caching layer (Redis)
- 🎯 Advanced difficulty algorithms
- 🤖 Fine-tuned models for cybersecurity

## Production Deployment Considerations

Before deploying to production:

1. Set `echo=False` in `app/database.py` to disable SQL logging
2. Use environment-specific configuration
3. Set up proper logging with rotation
4. Configure CORS if needed
5. Use a production ASGI server configuration
6. Set up monitoring and health checks
7. Implement rate limiting
8. Add comprehensive error logging
9. Set up database connection pooling
10. Configure SSL/TLS for database connections

## Contributing

This is a foundational backend structure. When contributing:

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Add tests for new features
- Update this README with new setup steps

## License

This project is part of the SocialProof cybersecurity simulation game.

---

**Built with ❤️ using FastAPI, SQLAlchemy, and PostgreSQL**
