# Streamlit Cloud Deployment - Quick Guide

## Deployment Instructions

### Option 1: Streamlit Cloud (RECOMMENDED - FREE & FASTEST!)

1. **Go to Streamlit Cloud**: https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Fill in details**:
   - Repository: `bhaskardatta/SocialProof`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

5. **Advanced Settings** → **Secrets**:
   Add these secrets:
   ```toml
   DATABASE_URL = "postgresql+asyncpg://user:password@host/database"
   LLM_PROVIDER = "groq"
   GROQ_API_KEY = "your_groq_api_key"
   ```

6. **Click "Deploy"**

✅ Your app will be live at: `https://your-app-name.streamlit.app`

### Database Options for Production:

**Option A: Railway.app (Free PostgreSQL)**
1. Go to https://railway.app
2. Create new project → PostgreSQL
3. Copy DATABASE_URL from Railway
4. Use in Streamlit secrets

**Option B: Supabase (Free PostgreSQL)**
1. Go to https://supabase.com
2. Create project → Get connection string
3. Convert to asyncpg format: `postgresql+asyncpg://...`

**Option C: Neon (Free PostgreSQL)**
1. Go to https://neon.tech
2. Create project → Get connection string

### Backend API Deployment:

**For Backend API**: Deploy on Render.com or Railway.app
- They auto-detect FastAPI
- Add same environment variables
- Backend URL: Update in `streamlit_app.py` line 22

---

## Quick Deploy (Without Backend):

If you just want to test the Streamlit UI without full backend:
1. Comment out API calls in `streamlit_app.py`
2. Deploy on Streamlit Cloud
3. Mock data will be shown

---

**Estimated Time**: 5-10 minutes total! 🚀
