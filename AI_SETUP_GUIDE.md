# 🤖 SocialProof Part 2 - AI Integration Setup Guide

## Multi-Provider LLM System with Dynamic Switching

Welcome to Part 2 of the SocialProof backend! This guide will walk you through setting up the sophisticated AI system that powers dynamic scenario generation and the Digital Guardian assistant.

---

## 🎯 What's New in Part 2

### Core Features Added:
1. **Multi-Provider LLM Support** - Seamlessly switch between Google Gemini, Groq, and OpenRouter
2. **Dynamic Scenario Generation** - AI-powered, difficulty-adaptive attack simulations
3. **Digital Guardian** - RAG-powered cybersecurity assistant
4. **Provider Abstraction** - Factory pattern for clean, maintainable code

### New Files Created:
- `app/ai_core.py` - Central AI module with provider factory
- `knowledge_base/` - Directory with cybersecurity knowledge
- Enhanced schemas, CRUD operations, and API endpoints

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Completed Part 1 setup (database, basic API working)
- ✅ Python 3.10+ with Conda environment
- ✅ PostgreSQL running and accessible
- ✅ At least ONE API key from: Google, Groq, or OpenRouter

---

## 🚀 Step-by-Step Setup

### Step 1: Verify Current System

Make sure your Part 1 setup is working:

```bash
cd /Users/bhaskar/Desktop/SocialProof

# Test the API (should return welcome message)
curl http://127.0.0.1:8000/

# If server isn't running, start it:
uvicorn app.main:app --reload
```

**Stop the server** (Ctrl+C) before proceeding.

---

### Step 2: Install AI Dependencies

Install all new AI and machine learning libraries:

```bash
pip install -r requirements.txt
```

**Expected packages installed:**
- google-generativeai (Google Gemini)
- langchain & langchain-core (LLM orchestration)
- langchain-google-genai (Google integration)
- langchain-groq (Groq integration)
- langchain-community (OpenRouter & more)
- chromadb (Vector database)
- sentence-transformers (Embeddings)

**Verify installation:**
```bash
python -c "import langchain; import chromadb; print('✅ AI dependencies installed')"
```

---

### Step 3: Obtain API Keys

You need at least ONE API key. Here's how to get them:

#### Option 1: Google Gemini (Recommended for beginners)
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key (starts with `AIza...`)
4. **Free tier**: 60 requests per minute

#### Option 2: Groq (Recommended for speed)
1. Visit: https://console.groq.com/keys
2. Sign up/login
3. Click "Create API Key"
4. Copy your key (starts with `gsk_...`)
5. **Free tier**: Very generous, ultra-fast

#### Option 3: OpenRouter (Most flexible)
1. Visit: https://openrouter.ai/keys
2. Sign up/login
3. Create a new API key
4. Copy your key (starts with `sk-or-...`)
5. **Free models available**

**💡 Pro Tip**: Get a Groq key for development (it's blazing fast!) and Google for production.

---

### Step 4: Configure Environment Variables

#### 4.1 Update your .env file

Open your `.env` file:
```bash
nano .env
# or
code .env
```

#### 4.2 Add AI Configuration

Add these lines to your `.env` (the `.env.example` already has them):

```env
# ============================================================================
# AI PROVIDER CONFIGURATION
# ============================================================================

# Choose your provider: "google", "groq", or "openrouter"
LLM_PROVIDER="groq"

# ============================================================================
# API KEYS - Only fill the one(s) you're using
# ============================================================================

# Google Gemini API Key
GOOGLE_API_KEY="AIza..."

# Groq API Key (recommended for development - ultra fast!)
GROQ_API_KEY="gsk_..."

# OpenRouter API Key
OPENROUTER_API_KEY="sk-or-..."
```

**Important Configuration Notes:**

1. **LLM_PROVIDER**: Set this to your chosen provider
   - `"google"` - Uses Gemini 1.5 Flash (balanced, multimodal)
   - `"groq"` - Uses Llama 3.1 8B (ultra-fast inference)
   - `"openrouter"` - Uses free tier models (maximum flexibility)

2. **API Keys**: You only need to fill in the key for your chosen provider
   - For example, if `LLM_PROVIDER="groq"`, only `GROQ_API_KEY` is required
   - Google key is also needed for embeddings (free, no quota issues)

3. **Multiple Keys**: You can have all three keys configured and switch providers by changing `LLM_PROVIDER`

#### 4.3 Example Configurations

**For Groq (Recommended for development):**
```env
LLM_PROVIDER="groq"
GOOGLE_API_KEY="your_google_key_here"  # Still needed for embeddings
GROQ_API_KEY="your_groq_key_here"
```

**For Google (Recommended for production):**
```env
LLM_PROVIDER="google"
GOOGLE_API_KEY="your_google_key_here"
```

**For OpenRouter (Maximum flexibility):**
```env
LLM_PROVIDER="openrouter"
GOOGLE_API_KEY="your_google_key_here"  # For embeddings
OPENROUTER_API_KEY="your_openrouter_key_here"
```

---

### Step 5: Verify Knowledge Base

The knowledge base files should already be created. Verify:

```bash
ls -la knowledge_base/

# You should see:
# phishing.txt
# smishing.txt
# social_engineering.txt
```

If missing, the files are already created in the `knowledge_base/` directory.

**Optional**: Add more knowledge files:
```bash
# Create a new topic
nano knowledge_base/vishing.txt
# Add information about voice phishing
```

---

### Step 6: Start the Server

Start the FastAPI server with AI features:

```bash
uvicorn app.main:app --reload
```

**Watch the startup logs carefully:**

```
🚀 Starting SocialProof Backend API...
🤖 Initializing AI systems...
✅ AI Core module loaded successfully
   Provider: groq
   Model: ChatGroq
📚 Loaded 3 documents from knowledge base
✅ RAG pipeline initialized successfully using 'groq' provider
   Model: ChatGroq
   Vector DB: ChromaDB with 3 documents
✅ AI systems ready!
✅ SocialProof API startup complete!
```

**✅ Success Indicators:**
- "RAG pipeline initialized successfully"
- "AI systems ready"
- Your chosen provider name appears

**⚠️ Warning Signs:**
- "AI features not available" - Missing dependencies
- "not properly configured" - API key issue
- Python import errors - Reinstall dependencies

---

### Step 7: Test AI Endpoints

#### 7.1 Check AI Provider Status

```bash
curl http://127.0.0.1:8000/ai/provider
```

**Expected response:**
```json
{
  "provider": "groq",
  "status": "active",
  "model_class": "ChatGroq",
  "rag_initialized": true,
  "error": null
}
```

#### 7.2 Validate AI Configuration

```bash
curl http://127.0.0.1:8000/ai/validate
```

**Expected response:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "provider": "groq",
  "rag_ready": true
}
```

#### 7.3 Test Digital Guardian

Query the AI assistant:

```bash
curl -X POST "http://127.0.0.1:8000/guardian/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is phishing?"
     }'
```

**Expected response:**
```json
{
  "answer": "Phishing is a type of social engineering attack where...",
  "sources": ["knowledge_base/phishing.txt"],
  "provider": "groq",
  "timestamp": "2025-11-06T..."
}
```

#### 7.4 Generate AI Scenario

First, create a test player (if you haven't):

```bash
curl -X POST "http://127.0.0.1:8000/players/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "ai_test_user",
       "email": "aitest@example.com"
     }'
```

Then generate a scenario:

```bash
curl -X POST "http://127.0.0.1:8000/scenarios/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "player_id": 1,
       "scenario_type": "EMAIL_PHISH"
     }'
```

**Expected response:**
```json
{
  "scenario_id": 1,
  "content": "Dear valued customer,\n\nWe have detected unusual activity...",
  "difficulty_level": 3.0,
  "difficulty_label": "Beginner",
  "scenario_type": "EMAIL_PHISH",
  "player_id": 1,
  "provider": "groq",
  "created_at": "2025-11-06T..."
}
```

---

### Step 8: Explore Interactive Documentation

Open your browser to: **http://127.0.0.1:8000/docs**

**New endpoints available:**

#### AI Features Section:
1. **POST /scenarios/generate** - Generate AI-powered scenario
   - Try it: Click "Try it out", enter player_id and scenario_type
   - See the AI generate a realistic phishing email!

2. **POST /guardian/query** - Ask the Digital Guardian
   - Try it: Ask "How do I identify smishing attacks?"
   - See the RAG system provide contextual answers

3. **GET /ai/provider** - Check current provider
4. **GET /ai/validate** - Validate AI configuration

---

## 🔄 Switching LLM Providers

One of the most powerful features is dynamic provider switching:

### To Switch Providers:

1. **Edit .env file:**
   ```bash
   nano .env
   ```

2. **Change LLM_PROVIDER:**
   ```env
   # Change from groq to google
   LLM_PROVIDER="google"
   ```

3. **Restart server:**
   ```bash
   # Stop server (Ctrl+C)
   uvicorn app.main:app --reload
   ```

4. **Verify change:**
   ```bash
   curl http://127.0.0.1:8000/ai/provider
   ```

### Provider Comparison:

| Provider | Speed | Quality | Cost | Best For |
|----------|-------|---------|------|----------|
| **Groq** | ⚡️⚡️⚡️ Fastest | ⭐️⭐️⭐️ Great | 💰 Free | Development, testing |
| **Google** | ⚡️⚡️ Fast | ⭐️⭐️⭐️⭐️ Excellent | 💰 Free tier | Production, multimodal |
| **OpenRouter** | ⚡️ Variable | ⭐️⭐️⭐️⭐️ Varies | 💰 Free & paid | Flexibility, experiments |

**Recommendation**: Use Groq for development (speed), Google for production (quality).

---

## 🐛 Troubleshooting

### Problem: "AI features not available"

**Cause**: Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
python -c "import langchain; print('OK')"
```

---

### Problem: "GOOGLE_API_KEY is not set"

**Cause**: Missing or incorrect API key in .env

**Solution:**
1. Check .env file exists: `cat .env | grep GOOGLE_API_KEY`
2. Verify key is correct (no quotes, no spaces)
3. Restart server after editing .env

---

### Problem: "Knowledge base directory not found"

**Cause**: knowledge_base/ directory missing

**Solution:**
```bash
ls knowledge_base/
# If missing, it should already exist from the setup
```

---

### Problem: "Failed to initialize RAG pipeline"

**Possible causes:**
1. No .txt files in knowledge_base/
2. Google API key missing (needed for embeddings)
3. Permission issues

**Solution:**
```bash
# Check files exist
ls -la knowledge_base/*.txt

# Check Google key
grep GOOGLE_API_KEY .env

# Check file permissions
chmod -R 755 knowledge_base/
```

---

### Problem: "Unsupported LLM provider"

**Cause**: LLM_PROVIDER value is invalid

**Solution:**
- Must be exactly: "google", "groq", or "openrouter" (lowercase)
- Check for typos, extra spaces, or quotes
- Example correct .env line: `LLM_PROVIDER="groq"`

---

### Problem: Rate limiting / API errors

**Symptoms**: 429 errors, slow responses

**Solutions:**
1. **Google**: Free tier has 60 requests/min
   - Wait a minute between tests
   - Consider paid tier for production

2. **Groq**: Very generous free tier
   - Rarely an issue
   - Switch to Groq for testing

3. **OpenRouter**: Depends on model
   - Use free tier models
   - Check your balance

---

## 📊 Testing the System

### Comprehensive Test Script

Create a test file `test_ai.sh`:

```bash
#!/bin/bash

echo "🧪 Testing SocialProof AI Features"
echo ""

# Test 1: Provider status
echo "1. Checking provider status..."
curl -s http://127.0.0.1:8000/ai/provider | python -m json.tool
echo ""

# Test 2: Validation
echo "2. Validating configuration..."
curl -s http://127.0.0.1:8000/ai/validate | python -m json.tool
echo ""

# Test 3: Digital Guardian
echo "3. Querying Digital Guardian..."
curl -s -X POST "http://127.0.0.1:8000/guardian/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are red flags in phishing emails?"}' \
     | python -m json.tool
echo ""

# Test 4: Scenario generation
echo "4. Generating AI scenario..."
curl -s -X POST "http://127.0.0.1:8000/scenarios/generate" \
     -H "Content-Type: application/json" \
     -d '{"player_id": 1, "scenario_type": "EMAIL_PHISH"}' \
     | python -m json.tool

echo ""
echo "✅ All tests complete!"
```

Make it executable and run:
```bash
chmod +x test_ai.sh
./test_ai.sh
```

---

## 🎓 Understanding the Architecture

### Factory Pattern (Key Innovation)

The `get_llm_client()` function is the cornerstone:

```python
def get_llm_client():
    if LLM_PROVIDER == "google":
        return ChatGoogleGenerativeAI(...)
    elif LLM_PROVIDER == "groq":
        return ChatGroq(...)
    elif LLM_PROVIDER == "openrouter":
        return ChatOpenRouter(...)
```

**Benefits:**
- ✅ Single configuration point
- ✅ Easy to add new providers
- ✅ Application code doesn't know which LLM it uses
- ✅ Runtime provider switching

### RAG Pipeline Flow

```
User Query
    ↓
Load knowledge base documents
    ↓
Create embeddings (Google)
    ↓
Store in ChromaDB
    ↓
Retrieve relevant docs
    ↓
Pass to LLM with prompt
    ↓
Generate contextual answer
    ↓
Return with sources
```

### Scenario Generation Flow

```
Player requests scenario
    ↓
Get player skill rating
    ↓
Calculate difficulty params
    ↓
Build generation prompt
    ↓
Call configured LLM
    ↓
Clean & format content
    ↓
Save to database
    ↓
Return to player
```

---

## 📈 Performance Tips

### 1. Provider Selection
- **Development**: Use Groq (10x faster responses)
- **Production**: Use Google (better quality, reliability)

### 2. Caching
Consider implementing caching for:
- Common Guardian queries
- Scenario templates
- Provider responses

### 3. Knowledge Base
- Keep files focused and concise
- Use clear, structured content
- Add more files as needed

### 4. Monitoring
Watch for:
- API rate limits
- Response times
- Error rates
- Provider costs

---

## 🚀 Next Steps

Now that Part 2 is working:

1. **Experiment with providers** - Try all three, compare results
2. **Expand knowledge base** - Add more cybersecurity topics
3. **Test different scenarios** - EMAIL_PHISH, SMS_SCAM, etc.
4. **Adjust difficulty** - Create players with different skill ratings
5. **Build frontend** - Connect a React/Vue app to these endpoints
6. **Add analytics** - Track scenario success rates
7. **Enhance Guardian** - Add more knowledge sources

---

## 📚 API Endpoint Summary

### New AI Endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/scenarios/generate` | POST | Generate AI scenario |
| `/guardian/query` | POST | Ask Digital Guardian |
| `/ai/provider` | GET | Check active provider |
| `/ai/validate` | GET | Validate AI config |

### Request Examples:

**Generate Scenario:**
```json
POST /scenarios/generate
{
  "player_id": 1,
  "scenario_type": "EMAIL_PHISH"
}
```

**Query Guardian:**
```json
POST /guardian/query
{
  "query": "How do I identify phishing?"
}
```

---

## ✅ Success Checklist

After completing this guide, verify:

- [ ] All AI dependencies installed
- [ ] At least one API key configured
- [ ] LLM_PROVIDER set in .env
- [ ] Server starts without errors
- [ ] "RAG pipeline initialized" message appears
- [ ] `/ai/provider` returns "active" status
- [ ] `/ai/validate` returns valid: true
- [ ] Digital Guardian answers questions
- [ ] Scenarios generate successfully
- [ ] Can switch providers by editing .env

---

## 🎉 Congratulations!

You've successfully integrated a world-class, multi-provider AI system into SocialProof!

**What you've accomplished:**
- ✅ Multi-provider LLM architecture
- ✅ RAG-powered AI assistant
- ✅ Dynamic scenario generation
- ✅ Production-ready AI pipeline
- ✅ Fully documented, maintainable code

**The AI system is live and ready for cybersecurity training!** 🛡️🤖

---

*Built with architectural excellence and attention to detail by a world-class Staff Software Engineer.*
