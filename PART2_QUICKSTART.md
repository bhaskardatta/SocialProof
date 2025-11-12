# ⚡ Part 2 Quick Start Checklist

## Get AI Features Running in 10 Minutes

---

## 📋 Pre-Flight Check

Before starting, ensure:
- [ ] Part 1 is working (database, API endpoints)
- [ ] Server can start with `uvicorn app.main:app --reload`
- [ ] You have at least ONE API key ready

**Don't have an API key yet?** Get Groq (fastest signup):
→ https://console.groq.com/keys

---

## 🚀 Installation Steps

### 1. Install Dependencies (2 minutes)

```bash
cd /Users/bhaskar/Desktop/SocialProof
pip install -r requirements.txt
```

**Verify:**
```bash
python -c "import langchain; import chromadb; print('✅ Ready')"
```

---

### 2. Configure Environment (3 minutes)

**Edit your `.env` file:**
```bash
nano .env
```

**Add these lines:**
```env
# Choose provider: "google", "groq", or "openrouter"
LLM_PROVIDER="groq"

# Add YOUR API key (get from console.groq.com/keys)
GROQ_API_KEY="gsk_YOUR_KEY_HERE"
GOOGLE_API_KEY="AIza_YOUR_KEY_HERE"
```

**Save and exit** (Ctrl+O, Enter, Ctrl+X)

---

### 3. Start the Server (1 minute)

```bash
uvicorn app.main:app --reload
```

**Watch for:**
```
✅ RAG pipeline initialized successfully using 'groq' provider
✅ AI systems ready!
```

---

### 4. Test AI Features (4 minutes)

#### Test 1: Check Provider Status
```bash
curl http://127.0.0.1:8000/ai/provider
```

**Expected:** `"status": "active"`

#### Test 2: Ask Digital Guardian
```bash
curl -X POST http://127.0.0.1:8000/guardian/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is phishing?"}'
```

**Expected:** Detailed answer about phishing

#### Test 3: Generate Scenario
```bash
# First, create a test player
curl -X POST http://127.0.0.1:8000/players/ \
     -H "Content-Type: application/json" \
     -d '{"username": "test_ai", "email": "test@example.com"}'

# Then generate a scenario
curl -X POST http://127.0.0.1:8000/scenarios/generate \
     -H "Content-Type: application/json" \
     -d '{"player_id": 1, "scenario_type": "EMAIL_PHISH"}'
```

**Expected:** AI-generated phishing email

#### Test 4: Explore API Docs
Open browser: **http://127.0.0.1:8000/docs**

Try the new endpoints:
- `/scenarios/generate`
- `/guardian/query`
- `/ai/provider`
- `/ai/validate`

---

## ✅ Success Indicators

You're all set if you see:
- ✅ Server starts without errors
- ✅ "RAG pipeline initialized" in startup logs
- ✅ `/ai/provider` returns "active"
- ✅ Digital Guardian answers questions
- ✅ Scenarios generate successfully

---

## 🆘 Quick Troubleshooting

### Problem: "AI features not available"
**Fix:** Run `pip install -r requirements.txt` again

### Problem: "GROQ_API_KEY is not set"
**Fix:** 
1. Check `.env` file exists in project root
2. Verify key has no quotes: `GROQ_API_KEY=gsk_abc123`
3. Restart server

### Problem: Import errors on startup
**Fix:** This is normal! They'll resolve after `pip install`

### Problem: "Knowledge base directory not found"
**Fix:** The `knowledge_base/` directory should already exist with 3 .txt files

---

## 🔄 Switch Providers (Optional)

Want to try a different AI provider?

**1. Edit .env:**
```env
LLM_PROVIDER="google"  # Change from "groq"
```

**2. Add that provider's API key:**
```env
GOOGLE_API_KEY="AIza_YOUR_KEY_HERE"
```

**3. Restart server**

**4. Verify:**
```bash
curl http://127.0.0.1:8000/ai/provider
# Should show: "provider": "google"
```

---

## 📚 Next Steps

Now that AI is working:

1. **Read the detailed guide:** `AI_SETUP_GUIDE.md`
2. **Understand the implementation:** `PART2_IMPLEMENTATION_SUMMARY.md`
3. **Explore the code:** Start with `app/ai_core.py`
4. **Experiment:** Try different scenarios, difficulty levels
5. **Expand:** Add more knowledge base files

---

## 🎯 Quick Reference

### Key Files:
- `app/ai_core.py` - AI logic (590 lines)
- `knowledge_base/*.txt` - Educational content
- `.env` - Configuration

### Key Endpoints:
- `POST /scenarios/generate` - Generate AI scenario
- `POST /guardian/query` - Ask questions
- `GET /ai/provider` - Check status
- `GET /ai/validate` - Validate config

### Configuration:
- **Provider:** Set `LLM_PROVIDER` in `.env`
- **API Keys:** Add corresponding key
- **Knowledge:** Add .txt files to `knowledge_base/`

---

## 🎉 You're Ready!

**AI features are live!** The SocialProof platform can now:
- Generate adaptive phishing scenarios
- Answer cybersecurity questions
- Switch between multiple AI providers
- Scale with your needs

**Time to build the future of cybersecurity training!** 🛡️🤖

---

*For detailed information, see `AI_SETUP_GUIDE.md` and `PART2_IMPLEMENTATION_SUMMARY.md`*
