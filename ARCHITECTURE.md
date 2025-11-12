# SocialProof Backend Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                                │
│  (Web Browser, Mobile App, CLI, Postman, curl, etc.)               │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP/HTTPS Requests
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ASGI SERVER (Uvicorn)                          │
│                     Port: 8000 (default)                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FASTAPI APPLICATION                             │
│                        (app/main.py)                                │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  API Routes & Endpoints                                   │     │
│  │  - GET  /                    (Welcome)                    │     │
│  │  - GET  /health              (Health Check)               │     │
│  │  - POST /players/            (Create Player)              │     │
│  │  - GET  /players/            (List Players)               │     │
│  │  - GET  /players/{id}        (Get Player)                 │     │
│  │  - POST /scenarios/          (Create Scenario)            │     │
│  │  - GET  /scenarios/{id}      (Get Scenario)               │     │
│  │  - GET  /players/{id}/scenarios (Get Player Scenarios)    │     │
│  └───────────────────────┬───────────────────────────────────┘     │
│                          │                                          │
│  ┌───────────────────────▼───────────────────────────────────┐     │
│  │  Request/Response Validation Layer                        │     │
│  │  (app/schemas.py - Pydantic Models)                       │     │
│  │  - PlayerCreate, Player                                   │     │
│  │  - ScenarioCreate, Scenario                               │     │
│  └───────────────────────┬───────────────────────────────────┘     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                             │
│                      (app/crud.py)                                  │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  Database Operations (CRUD)                               │     │
│  │  - get_player(), create_player()                          │     │
│  │  - get_players(), get_player_by_email()                   │     │
│  │  - create_player_scenario()                               │     │
│  │  - get_scenario(), get_player_scenarios()                 │     │
│  │  - update_player_skill_rating()                           │     │
│  │  - update_scenario_result()                               │     │
│  └───────────────────────┬───────────────────────────────────┘     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATABASE ACCESS LAYER                            │
│                  (app/database.py)                                  │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  AsyncEngine (SQLAlchemy)                                 │     │
│  │  - Connection Pool Management                             │     │
│  │  - Async Session Factory                                  │     │
│  │  - Database URL from Environment                          │     │
│  └───────────────────────┬───────────────────────────────────┘     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       ORM LAYER                                     │
│                    (app/models.py)                                  │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  SQLAlchemy Models                                        │     │
│  │  ┌──────────────────────┐  ┌──────────────────────┐      │     │
│  │  │   PlayerProfile      │  │   GameScenario       │      │     │
│  │  ├──────────────────────┤  ├──────────────────────┤      │     │
│  │  │ id                   │  │ id                   │      │     │
│  │  │ username             │  │ player_id (FK)       │      │     │
│  │  │ email                │  │ scenario_type        │      │     │
│  │  │ player_skill_rating  │  │ content              │      │     │
│  │  │ created_at           │  │ difficulty_level     │      │     │
│  │  │ scenarios (rel)      │◄─┤ is_successful        │      │     │
│  │  └──────────────────────┘  │ created_at           │      │     │
│  │                             │ player (rel)         │      │     │
│  │                             └──────────────────────┘      │     │
│  └───────────────────────┬───────────────────────────────────┘     │
└────────────────────────────┬────────────────────────────────────────┘
                             │ asyncpg driver
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      POSTGRESQL DATABASE                            │
│                          (Port: 5432)                               │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  Tables:                                                  │     │
│  │  - player_profiles                                        │     │
│  │  - game_scenarios                                         │     │
│  │  - alembic_version (migrations)                           │     │
│  └───────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                    MIGRATION SYSTEM                                 │
│                         (Alembic)                                   │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │  Commands:                                                │     │
│  │  - alembic revision --autogenerate                        │     │
│  │  - alembic upgrade head                                   │     │
│  │  - alembic downgrade -1                                   │     │
│  └───────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

### Creating a Player

```
Client Request
    │
    │ POST /players/
    │ {"username": "user1", "email": "user@example.com"}
    ▼
FastAPI Endpoint (main.py)
    │
    │ Validates request structure
    ▼
Pydantic Schema (schemas.py)
    │
    │ PlayerCreate validation
    │ - username: str
    │ - email: EmailStr (validates email format)
    ▼
CRUD Layer (crud.py)
    │
    │ get_player_by_email() - Check if email exists
    ▼
Database Query
    │
    │ SELECT * FROM player_profiles WHERE email = ?
    ▼
    │ Email not found ✓
    ▼
CRUD Layer (crud.py)
    │
    │ create_player() - Create new player
    ▼
SQLAlchemy ORM (models.py)
    │
    │ PlayerProfile model
    │ - Auto-assigns: id, player_skill_rating (500.0), created_at
    ▼
Database Insert
    │
    │ INSERT INTO player_profiles ...
    ▼
Commit & Refresh
    │
    │ Retrieve generated fields (id, created_at)
    ▼
Pydantic Response (schemas.py)
    │
    │ Player schema with all fields
    ▼
JSON Response
    │
    │ HTTP 201 Created
    │ {
    │   "id": 1,
    │   "username": "user1",
    │   "email": "user@example.com",
    │   "player_skill_rating": 500.0,
    │   "created_at": "2025-11-06T10:30:00Z"
    │ }
    ▼
Client receives response
```

## Database Relationships

```
┌─────────────────────────┐
│    PlayerProfile        │
│                         │
│  id (PK)               │
│  username               │
│  email                  │
│  player_skill_rating    │
│  created_at             │
└────────────┬────────────┘
             │ 1
             │
             │ has many
             │ scenarios
             │
             │ *
┌────────────▼────────────┐
│    GameScenario         │
│                         │
│  id (PK)               │
│  player_id (FK)        │
│  scenario_type          │
│  content                │
│  difficulty_level       │
│  is_successful          │
│  created_at             │
└─────────────────────────┘

Relationship Type: One-to-Many
- One PlayerProfile can have many GameScenarios
- One GameScenario belongs to one PlayerProfile
- Cascade delete: If player is deleted, all their scenarios are deleted
```

## Technology Stack Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     Request Processing                        │
└──────────────────────────────────────────────────────────────┘

HTTP Request
    ↓
Uvicorn (ASGI Server)
    ↓
FastAPI (Web Framework)
    ├─→ Route Matching
    ├─→ Dependency Injection (get_db)
    └─→ Request Validation (Pydantic)
        ↓
Business Logic (CRUD functions)
    ↓
SQLAlchemy (ORM) + asyncpg (Driver)
    ├─→ Query Building
    ├─→ Connection Pool
    └─→ Async Execution
        ↓
PostgreSQL Database
    ├─→ Query Execution
    ├─→ Index Lookup
    └─→ Result Set
        ↓
SQLAlchemy Result Processing
    ↓
ORM Model Objects
    ↓
Pydantic Response Validation
    ↓
JSON Serialization
    ↓
HTTP Response
    ↓
Client
```

## Environment Configuration Flow

```
┌──────────────────────────────────────────────────────────────┐
│                  Configuration Loading                        │
└──────────────────────────────────────────────────────────────┘

Application Startup
    ↓
database.py imports dotenv
    ↓
load_dotenv()
    ├─→ Looks for .env file in project root
    ├─→ Loads environment variables
    └─→ Makes available via os.getenv()
        ↓
DATABASE_URL = os.getenv("DATABASE_URL")
    ↓
Validation Check
    │
    ├─→ If None: raise ValueError
    └─→ If set: continue
        ↓
create_async_engine(DATABASE_URL)
    ↓
Database Connection Established
    ↓
Application Ready
```

## File Dependency Graph

```
main.py
  ├─→ imports database.py
  │     ├─→ imports sqlalchemy
  │     ├─→ imports dotenv
  │     └─→ defines Base
  │
  ├─→ imports models.py
  │     ├─→ imports database.py (Base)
  │     └─→ imports sqlalchemy
  │
  ├─→ imports schemas.py
  │     └─→ imports pydantic
  │
  └─→ imports crud.py
        ├─→ imports models.py
        ├─→ imports schemas.py
        └─→ imports sqlalchemy

alembic/env.py
  ├─→ imports database.py (Base)
  ├─→ imports models.py (all models)
  └─→ imports dotenv
```

## Async Execution Flow

```
┌──────────────────────────────────────────────────────────────┐
│              Async Request Handling                           │
└──────────────────────────────────────────────────────────────┘

Async Request Handler
    ↓
async def create_player(...)
    ↓
await crud.create_player(db, player)
    ↓
async def create_player(db: AsyncSession, ...)
    ↓
db.add(db_player)              # Synchronous (in-memory)
    ↓
await db.commit()              # Async (I/O bound)
    │
    ├─→ Releases control to event loop
    ├─→ Other requests can be processed
    └─→ Waits for database response
        ↓
await db.refresh(db_player)    # Async (I/O bound)
    ↓
return db_player               # Synchronous
    ↓
Response sent to client
```

## Error Handling Flow

```
Request
  ↓
Try: Process Request
  │
  ├─→ Email already exists?
  │     └─→ raise HTTPException(400, "Email already registered")
  │
  ├─→ Player not found?
  │     └─→ raise HTTPException(404, "Player not found")
  │
  ├─→ Database error?
  │     └─→ SQLAlchemy raises exception
  │           └─→ FastAPI catches & returns 500
  │
  └─→ Validation error?
        └─→ Pydantic raises ValidationError
              └─→ FastAPI returns 422 Unprocessable Entity
                    ↓
                Error Response JSON
                    ↓
                Client receives error
```

## Security Layers

```
┌──────────────────────────────────────────────────────────────┐
│                    Security Measures                          │
└──────────────────────────────────────────────────────────────┘

Input Validation
  └─→ Pydantic schemas validate all input data
      └─→ Type checking, email validation, required fields

SQL Injection Prevention
  └─→ SQLAlchemy ORM (parameterized queries)
      └─→ Never directly concatenate SQL

Environment Variables
  └─→ .env file (not in git)
      └─→ DATABASE_URL, secrets stored securely

Database Constraints
  └─→ Unique constraints (username, email)
  └─→ Foreign key constraints
  └─→ NOT NULL constraints

API Rate Limiting
  └─→ (Future: to be implemented)

Authentication
  └─→ (Future: JWT tokens to be implemented)
```

---

**This architecture ensures:**
- ✅ Scalability (async operations)
- ✅ Maintainability (clear separation of concerns)
- ✅ Type Safety (Pydantic + SQLAlchemy)
- ✅ Security (validation + ORM + environment variables)
- ✅ Performance (connection pooling + indexing)
- ✅ Reliability (error handling + validation)
