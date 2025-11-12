# SocialProof Backend - Quick Reference Guide

## Common Commands

### Development Server
```bash
# Start the development server (with auto-reload)
uvicorn app.main:app --reload

# Start on different port
uvicorn app.main:app --reload --port 8080

# Make accessible from network
uvicorn app.main:app --reload --host 0.0.0.0
```

### Database Migrations
```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current migration version
alembic current

# Show migration history
alembic history
```

### Testing
```bash
# Run the API test suite (make sure server is running first)
./test_api.sh

# Test a specific endpoint manually
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/players/

# Create a player via curl
curl -X POST "http://127.0.0.1:8000/players/" \
     -H "Content-Type: application/json" \
     -d '{"username": "newuser", "email": "user@example.com"}'
```

### PostgreSQL Commands
```bash
# Connect to database
psql -U socialproof_user -d socialproof_db

# Inside psql:
\dt                    # List all tables
\d player_profiles     # Describe table structure
\d game_scenarios      # Describe table structure
SELECT * FROM player_profiles;   # Query data
\q                     # Exit
```

## API Endpoints Quick Reference

### Players
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/players/` | Create new player |
| GET | `/players/` | List all players (paginated) |
| GET | `/players/{id}` | Get specific player |
| GET | `/players/{id}/scenarios` | Get player's scenarios |

### Scenarios
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/scenarios/` | Create new scenario |
| GET | `/scenarios/{id}` | Get specific scenario |

## Example API Calls

### Create Player
```bash
curl -X POST "http://127.0.0.1:8000/players/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "cyber_defender",
       "email": "defender@example.com"
     }'
```

**Response:**
```json
{
  "username": "cyber_defender",
  "email": "defender@example.com",
  "id": 1,
  "player_skill_rating": 500.0,
  "created_at": "2025-11-06T10:30:00.000Z"
}
```

### Get All Players
```bash
curl "http://127.0.0.1:8000/players/?skip=0&limit=10"
```

### Get Specific Player
```bash
curl "http://127.0.0.1:8000/players/1"
```

### Create Scenario
```bash
curl -X POST "http://127.0.0.1:8000/scenarios/" \
     -H "Content-Type: application/json" \
     -d 'player_id=1&scenario_type=EMAIL_PHISH&content=Suspicious email...&difficulty_level=5.5'
```

## Directory Structure Reference

```
/SocialProof
├── app/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # FastAPI app & routes
│   ├── database.py       # DB connection & session
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic validation schemas
│   └── crud.py           # Database operations
├── alembic/              # Database migrations
│   ├── versions/         # Migration files
│   └── env.py            # Alembic configuration
├── .env                  # Environment variables (not in git)
├── .env.example          # Template for .env
├── requirements.txt      # Python dependencies
├── alembic.ini          # Alembic config file
├── setup.sh             # Quick setup script
├── test_api.sh          # API test suite
└── README.md            # Full documentation
```

## Database Schema

### player_profiles
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| username | String | Unique username |
| email | String | Unique email |
| player_skill_rating | Float | Skill rating (default: 500.0) |
| created_at | DateTime | Creation timestamp |

### game_scenarios
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| player_id | Integer | Foreign key to player_profiles |
| scenario_type | String | Type (e.g., EMAIL_PHISH) |
| content | Text | Scenario content |
| difficulty_level | Float | Difficulty rating |
| is_successful | Boolean | Success status |
| created_at | DateTime | Creation timestamp |

## Environment Variables

```bash
# Required
DATABASE_URL="postgresql+asyncpg://user:password@host:port/database"

# Format breakdown:
# postgresql+asyncpg:// - Database driver
# user:password         - Credentials
# @host:port           - Server location
# /database            - Database name
```

## Troubleshooting Quick Fixes

### Import Errors
```bash
# Make sure you're in the project root
cd /Users/bhaskar/Desktop/SocialProof
python -c "import app"  # Should work without errors
```

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -U socialproof_user -d socialproof_db

# Check if PostgreSQL is running
pg_isready
```

### Migration Issues
```bash
# Check current migration status
alembic current

# Force stamp to specific version (if needed)
alembic stamp head

# Recreate migrations from scratch (CAUTION: drops data)
# 1. Drop all tables in database
# 2. Delete alembic/versions/*.py files
# 3. Run: alembic revision --autogenerate -m "Initial"
# 4. Run: alembic upgrade head
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (replace PID)
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --reload --port 8080
```

## URLs & Resources

- **API**: http://127.0.0.1:8000
- **Interactive Docs (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative Docs (ReDoc)**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

## Code Quality Commands

```bash
# Format code with black (if installed)
black app/

# Lint with flake8 (if installed)
flake8 app/

# Type checking with mypy (if installed)
mypy app/

# Sort imports with isort (if installed)
isort app/
```

## Production Checklist

- [ ] Set `echo=False` in database.py
- [ ] Use strong DATABASE_URL credentials
- [ ] Set up proper logging
- [ ] Configure CORS if needed
- [ ] Enable HTTPS
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Set up backup strategy
- [ ] Use production ASGI server config
- [ ] Set up CI/CD pipeline

---

**Quick Start**: `./setup.sh` → `uvicorn app.main:app --reload` → http://127.0.0.1:8000/docs
