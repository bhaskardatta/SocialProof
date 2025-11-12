# 🚀 SocialProof Backend - Setup and Execution Guide

**Complete step-by-step instructions to get your SocialProof backend running**

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [x] **Python 3.10 or higher** - Check with `python --version`
- [x] **Conda environment** (you mentioned you're using Conda ✓)
- [x] **PostgreSQL 13 or higher** - Check with `psql --version`
- [x] **PostgreSQL running** - Check with `pg_isready` or check services
- [x] **Git** (optional, but recommended)

---

## 🏗️ Step-by-Step Setup

### Step 1: Install Python Dependencies

Navigate to the project directory and install all required packages:

```bash
cd /Users/bhaskar/Desktop/SocialProof
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 sqlalchemy-2.0.23 ...
```

**Verify installation:**
```bash
python -c "import fastapi; import sqlalchemy; print('✓ Dependencies installed successfully')"
```

---

### Step 2: Set Up PostgreSQL Database

#### 2.1 Start PostgreSQL (if not running)

**On macOS with Homebrew:**
```bash
brew services start postgresql@14
# or
pg_ctl -D /usr/local/var/postgres start
```

**Check if PostgreSQL is running:**
```bash
pg_isready
# Expected: /tmp:5432 - accepting connections
```

#### 2.2 Create Database and User

**Option A: Using psql command line**

```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# Or if postgres user doesn't work, use your system username:
psql -U $(whoami) postgres
```

**Inside psql, run these commands:**

```sql
-- Create database
CREATE DATABASE socialproof_db;

-- Create user with password
CREATE USER socialproof_user WITH PASSWORD 'change_this_password';

-- Grant privileges on database
GRANT ALL PRIVILEGES ON DATABASE socialproof_db TO socialproof_user;

-- Connect to the new database
\c socialproof_db

-- Grant schema privileges (required for PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO socialproof_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO socialproof_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO socialproof_user;

-- Verify setup
\l                                    -- List databases (should see socialproof_db)
\du                                   -- List users (should see socialproof_user)

-- Exit psql
\q
```

**Option B: Using SQL file (easier)**

Create a file `setup_db.sql`:

```sql
CREATE DATABASE socialproof_db;
CREATE USER socialproof_user WITH PASSWORD 'change_this_password';
GRANT ALL PRIVILEGES ON DATABASE socialproof_db TO socialproof_user;
\c socialproof_db
GRANT ALL ON SCHEMA public TO socialproof_user;
```

Then run:
```bash
psql -U postgres -f setup_db.sql
```

#### 2.3 Verify Database Connection

Test the connection with your new credentials:

```bash
psql -U socialproof_user -d socialproof_db
```

If successful, you'll see:
```
socialproof_db=>
```

Type `\q` to exit.

---

### Step 3: Configure Environment Variables

#### 3.1 Create .env file from template

```bash
cp .env.example .env
```

#### 3.2 Edit .env file with your credentials

Open `.env` in your favorite editor:

```bash
nano .env
# or
code .env
# or
vi .env
```

Update the DATABASE_URL with your actual credentials:

```env
DATABASE_URL="postgresql+asyncpg://socialproof_user:change_this_password@localhost:5432/socialproof_db"
```

**Important:** Replace:
- `socialproof_user` → your PostgreSQL username (if different)
- `change_this_password` → your actual password
- `localhost` → your database host (usually localhost)
- `5432` → your PostgreSQL port (default is 5432)
- `socialproof_db` → your database name (if different)

**Save and close the file.**

#### 3.3 Verify environment file

```bash
cat .env
```

You should see your DATABASE_URL (but be careful not to share this publicly!).

---

### Step 4: Initialize Alembic for Database Migrations

#### 4.1 Initialize Alembic

Run this command to create the Alembic directory structure:

```bash
alembic init alembic
```

**Expected output:**
```
Creating directory /Users/bhaskar/Desktop/SocialProof/alembic ... done
Creating directory /Users/bhaskar/Desktop/SocialProof/alembic/versions ... done
Generating /Users/bhaskar/Desktop/SocialProof/alembic.ini ... done
Generating /Users/bhaskar/Desktop/SocialProof/alembic/env.py ... done
```

#### 4.2 Configure alembic.ini

Open `alembic.ini` and find the line (around line 58):

```ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```

**Comment it out or remove it** (we'll use the environment variable instead):

```ini
# sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = 
```

**Save the file.**

#### 4.3 Configure alembic/env.py

This is the most important step. Open `alembic/env.py` and make these modifications:

**A) Add imports at the top (after the existing imports, around line 6-10):**

```python
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import our app
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Import our models
from app.database import Base
from app import models  # This imports all models, triggering their registration
```

**B) Load environment variables (after line ~15, after `config = context.config`):**

```python
# Load environment variables from .env file
load_dotenv()

# Override the sqlalchemy.url with our environment variable
database_url = os.getenv('DATABASE_URL')
if database_url:
    config.set_main_option('sqlalchemy.url', database_url)
```

**C) Set target metadata (find the line `target_metadata = None` around line 21-25):**

Replace:
```python
target_metadata = None
```

With:
```python
target_metadata = Base.metadata
```

**Complete modified section should look like this:**

```python
# ... existing imports ...
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import Base
from app import models

# this is the Alembic Config object
config = context.config

# Load environment variables
load_dotenv()
database_url = os.getenv('DATABASE_URL')
if database_url:
    config.set_main_option('sqlalchemy.url', database_url)

# ... existing code ...

# target_metadata = None  # DELETE OR COMMENT THIS
target_metadata = Base.metadata  # ADD THIS

# ... rest of the file ...
```

**Save the file.**

#### 4.4 Verify Alembic Configuration

Test that Alembic can see your models:

```bash
alembic check
```

If configured correctly, you should see no errors.

---

### Step 5: Create and Apply Database Migrations

#### 5.1 Generate Initial Migration

Create the first migration that will create all your database tables:

```bash
alembic revision --autogenerate -m "Initial database schema"
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'player_profiles'
INFO  [alembic.autogenerate.compare] Detected added table 'game_scenarios'
  Generating /Users/bhaskar/Desktop/SocialProof/alembic/versions/xxxx_initial_database_schema.py ... done
```

#### 5.2 Review the Migration (Optional but Recommended)

Open the generated migration file:

```bash
ls alembic/versions/
# You'll see a file like: xxxxxxxxxxxx_initial_database_schema.py

# View the file:
cat alembic/versions/*_initial_database_schema.py
```

You should see `create_table` statements for `player_profiles` and `game_scenarios`.

#### 5.3 Apply the Migration

Run the migration to create the tables in your database:

```bash
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> xxxxxxxxxxxx, Initial database schema
```

---

### Step 6: Verify Database Tables Were Created

Connect to your database and verify the tables exist:

```bash
psql -U socialproof_user -d socialproof_db
```

**Inside psql:**

```sql
-- List all tables
\dt

-- You should see:
--  Schema |      Name         | Type  |      Owner
-- --------+-------------------+-------+------------------
--  public | alembic_version   | table | socialproof_user
--  public | game_scenarios    | table | socialproof_user
--  public | player_profiles   | table | socialproof_user

-- View player_profiles structure
\d player_profiles

-- View game_scenarios structure
\d game_scenarios

-- Exit
\q
```

**✅ If you see these tables, your database is ready!**

---

### Step 7: Start the Development Server

Now start your FastAPI server:

```bash
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/Users/bhaskar/Desktop/SocialProof']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**🎉 Your server is now running!**

**Keep this terminal open** - the server needs to stay running.

---

### Step 8: Test the API

Open a **new terminal window** and run these tests:

#### 8.1 Test Welcome Endpoint

```bash
curl http://127.0.0.1:8000/
```

**Expected response:**
```json
{
  "message": "Welcome to the SocialProof API",
  "version": "1.0.0",
  "documentation": "/docs"
}
```

#### 8.2 Test Health Check

```bash
curl http://127.0.0.1:8000/health
```

**Expected response:**
```json
{
  "status": "healthy"
}
```

#### 8.3 Create a Test Player

```bash
curl -X POST "http://127.0.0.1:8000/players/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "test_player",
       "email": "test@example.com"
     }'
```

**Expected response:**
```json
{
  "username": "test_player",
  "email": "test@example.com",
  "id": 1,
  "player_skill_rating": 500.0,
  "created_at": "2025-11-06T12:34:56.789Z"
}
```

#### 8.4 Retrieve the Player

```bash
curl http://127.0.0.1:8000/players/1
```

**Expected response:**
```json
{
  "username": "test_player",
  "email": "test@example.com",
  "id": 1,
  "player_skill_rating": 500.0,
  "created_at": "2025-11-06T12:34:56.789Z"
}
```

#### 8.5 List All Players

```bash
curl http://127.0.0.1:8000/players/
```

**Expected response:**
```json
[
  {
    "username": "test_player",
    "email": "test@example.com",
    "id": 1,
    "player_skill_rating": 500.0,
    "created_at": "2025-11-06T12:34:56.789Z"
  }
]
```

#### 8.6 Run Comprehensive Test Suite

Run the automated test script:

```bash
./test_api.sh
```

**Expected output:**
```
==========================================
  SocialProof Backend Test Suite
==========================================

1. Testing API connectivity...
✓ API is accessible

2. Testing root endpoint...
✓ Root endpoint working

3. Testing health check...
✓ Health check passed

4. Creating a test player...
✓ Player created successfully

5. Retrieving the created player...
✓ Player retrieved successfully

6. Listing all players...
✓ Players list retrieved

7. Testing duplicate email validation...
✓ Duplicate email correctly rejected

8. Testing 404 for non-existent player...
✓ 404 error correctly returned

==========================================
  All Tests Completed! ✨
==========================================
```

---

### Step 9: Explore the Interactive Documentation

Open your web browser and visit these URLs:

#### 9.1 Swagger UI (Interactive API Docs)

**URL:** http://127.0.0.1:8000/docs

This provides an interactive interface where you can:
- ✅ See all available endpoints
- ✅ View request/response schemas
- ✅ Test API calls directly from the browser
- ✅ See example data

**Try it:**
1. Click on "POST /players/"
2. Click "Try it out"
3. Edit the example JSON
4. Click "Execute"
5. See the response

#### 9.2 ReDoc (Alternative Documentation)

**URL:** http://127.0.0.1:8000/redoc

This provides a cleaner, read-only documentation view.

#### 9.3 OpenAPI Schema

**URL:** http://127.0.0.1:8000/openapi.json

Raw OpenAPI schema in JSON format (useful for generating client libraries).

---

## 🎓 Advanced Usage

### Running on a Different Port

```bash
uvicorn app.main:app --reload --port 8080
```

Then access at: http://127.0.0.1:8080

### Making Server Accessible from Network

```bash
uvicorn app.main:app --reload --host 0.0.0.0
```

Then access from other devices at: http://YOUR_IP:8000

### Running Without Auto-Reload (Production-like)

```bash
uvicorn app.main:app
```

### Creating More Migrations (After Model Changes)

1. **Modify a model in `app/models.py`**
   
   For example, add a new field to PlayerProfile:
   ```python
   total_games_played = Column(Integer, default=0)
   ```

2. **Generate migration:**
   ```bash
   alembic revision --autogenerate -m "Add total_games_played to player"
   ```

3. **Review the migration file** in `alembic/versions/`

4. **Apply the migration:**
   ```bash
   alembic upgrade head
   ```

### Rolling Back a Migration

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

### Checking Migration Status

```bash
# Current version
alembic current

# Migration history
alembic history --verbose
```

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "sqlalchemy.exc.OperationalError: could not connect to server"

**Solutions:**
1. Check PostgreSQL is running: `pg_isready`
2. Check credentials in `.env` file
3. Try connecting manually: `psql -U socialproof_user -d socialproof_db`

### Problem: "relation 'player_profiles' does not exist"

**Solution:**
```bash
# Run migrations
alembic upgrade head
```

### Problem: "alembic: command not found"

**Solution:**
```bash
# Reinstall alembic
pip install alembic
```

### Problem: Port 8000 already in use

**Solutions:**

**Option 1:** Find and kill the process
```bash
lsof -i :8000
kill -9 <PID>
```

**Option 2:** Use a different port
```bash
uvicorn app.main:app --reload --port 8080
```

### Problem: "ImportError" when running alembic

**Solution:**
Make sure you're in the project root directory:
```bash
cd /Users/bhaskar/Desktop/SocialProof
pwd  # Should show: /Users/bhaskar/Desktop/SocialProof
alembic upgrade head
```

### Problem: Alembic doesn't detect model changes

**Solutions:**
1. Make sure models are imported in `alembic/env.py`:
   ```python
   from app import models
   ```

2. Make sure `target_metadata = Base.metadata` is set

3. Try with verbose flag:
   ```bash
   alembic revision --autogenerate -m "description" --verbose
   ```

### Problem: Database connection works in psql but not in app

**Check these:**
1. `.env` file exists in project root
2. DATABASE_URL uses `postgresql+asyncpg://` (not just `postgresql://`)
3. No typos in `.env` file
4. Application loads `.env` correctly (check with print statement)

---

## ✅ Verification Checklist

After completing setup, verify these:

- [ ] All Python packages installed (`pip list | grep fastapi`)
- [ ] PostgreSQL is running (`pg_isready`)
- [ ] Database `socialproof_db` exists
- [ ] User `socialproof_user` can connect
- [ ] `.env` file exists with correct DATABASE_URL
- [ ] Alembic is initialized (`ls alembic/`)
- [ ] Tables are created (`psql -U socialproof_user -d socialproof_db -c "\dt"`)
- [ ] Server starts without errors
- [ ] `curl http://127.0.0.1:8000/` returns welcome message
- [ ] Can create a player via API
- [ ] Can retrieve players via API
- [ ] Swagger docs accessible at http://127.0.0.1:8000/docs

---

## 🎉 Success!

If you've completed all steps and all tests pass, you now have:

✅ **A fully functional FastAPI backend**
✅ **PostgreSQL database with proper schema**
✅ **Working API endpoints**
✅ **Interactive API documentation**
✅ **Database migration system**
✅ **Testing capabilities**

---

## 📚 Next Steps

Now that your backend is running, you can:

1. **Explore the API** using the Swagger docs at http://127.0.0.1:8000/docs
2. **Create more players and scenarios** to test functionality
3. **Read the code** to understand how everything works
4. **Start building Part 2 features** (AI-generated scenarios, etc.)
5. **Integrate with a frontend** application
6. **Add authentication** (JWT tokens)
7. **Deploy to production** (Docker, cloud platforms)

---

## 🆘 Getting Help

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review the **QUICK_REFERENCE.md** for common commands
3. Check the **README.md** for detailed documentation
4. Look at **ARCHITECTURE.md** to understand the system design
5. Review server logs for error messages

---

**Congratulations! Your SocialProof backend is ready to defend against cyber threats! 🛡️🎮**
