# Deployment Guide - Render (Free Hosting)# Streamlit Cloud Deployment - Quick Guide



## Why Render?## Deployment Instructions



✅ **Single Platform** - Hosts both backend and database  ### Option 1: Streamlit Cloud (RECOMMENDED - FREE & FASTEST!)

✅ **100% Free Tier** - No credit card required  

✅ **PostgreSQL Included** - Free managed database  1. **Go to Streamlit Cloud**: https://share.streamlit.io/

✅ **Auto-Deploy** - Deploys from GitHub automatically  

✅ **HTTPS** - Free SSL certificates  2. **Sign in** with your GitHub account

✅ **Easy Setup** - 5-minute deployment  

3. **Click "New app"**

## Step-by-Step Deployment

4. **Fill in details**:

### 1. Push Code to GitHub   - Repository: `bhaskardatta/SocialProof`

   - Branch: `main`

```bash   - Main file path: `streamlit_app.py`

# Add all files

git add .5. **Advanced Settings** → **Secrets**:

   Add these secrets:

# Commit   ```toml

git commit -m "Production ready - PhishGuard complete"   DATABASE_URL = "postgresql+asyncpg://user:password@host/database"

   LLM_PROVIDER = "groq"

# Push to GitHub   GROQ_API_KEY = "your_groq_api_key"

git push origin main   ```

```

6. **Click "Deploy"**

### 2. Create Render Account

✅ Your app will be live at: `https://your-app-name.streamlit.app`

1. Go to https://render.com

2. Sign up with GitHub (free)### Database Options for Production:

3. Authorize Render to access your repositories

**Option A: Railway.app (Free PostgreSQL)**

### 3. Create PostgreSQL Database1. Go to https://railway.app

2. Create new project → PostgreSQL

1. Click **"New +"** → **"PostgreSQL"**3. Copy DATABASE_URL from Railway

2. Settings:4. Use in Streamlit secrets

   - **Name:** `phishguard-db`

   - **Database:** `phishguard`**Option B: Supabase (Free PostgreSQL)**

   - **User:** `phishguard_user`1. Go to https://supabase.com

   - **Region:** Choose closest to you2. Create project → Get connection string

   - **Plan:** **Free** (0GB storage, good for demo)3. Convert to asyncpg format: `postgresql+asyncpg://...`

3. Click **"Create Database"**

4. Wait 2-3 minutes for provisioning**Option C: Neon (Free PostgreSQL)**

5. **Copy the "Internal Database URL"** (starts with `postgresql://`)1. Go to https://neon.tech

2. Create project → Get connection string

### 4. Deploy Backend (Web Service)

### Backend API Deployment:

1. Click **"New +"** → **"Web Service"**

2. Connect your GitHub repository: `bhaskardatta/SocialProof`**For Backend API**: Deploy on Render.com or Railway.app

3. Settings:- They auto-detect FastAPI

   - **Name:** `phishguard-api`- Add same environment variables

   - **Region:** Same as database- Backend URL: Update in `streamlit_app.py` line 22

   - **Branch:** `main`

   - **Root Directory:** Leave blank---

   - **Runtime:** `Python 3`

   - **Build Command:** ## Quick Deploy (Without Backend):

     ```

     pip install -r requirements.txt && alembic upgrade headIf you just want to test the Streamlit UI without full backend:

     ```1. Comment out API calls in `streamlit_app.py`

   - **Start Command:**2. Deploy on Streamlit Cloud

     ```3. Mock data will be shown

     uvicorn app.main:app --host 0.0.0.0 --port $PORT

     ```---

   - **Plan:** **Free**

**Estimated Time**: 5-10 minutes total! 🚀

4. **Environment Variables** (Click "Advanced" → "Add Environment Variable"):
   ```
   DATABASE_URL = <paste Internal Database URL from step 3>
   GROQ_API_KEY = <your Groq API key>
   SECRET_KEY = <generate random string>
   ```

5. Click **"Create Web Service"**
6. Wait 5-10 minutes for deployment
7. **Copy your API URL** (e.g., `https://phishguard-api.onrender.com`)

### 5. Deploy Frontend (Web Service)

1. Click **"New +"** → **"Web Service"** again
2. Same repository: `bhaskardatta/SocialProof`
3. Settings:
   - **Name:** `phishguard-app`
   - **Region:** Same as backend
   - **Branch:** `main`
   - **Root Directory:** Leave blank
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     streamlit run app_final.py --server.port $PORT --server.address 0.0.0.0
     ```
   - **Plan:** **Free**

4. **Environment Variable:**
   ```
   API_BASE = <your backend URL from step 4>
   ```
   
5. Click **"Create Web Service"**
6. Wait 5-10 minutes for deployment

### 6. Update Frontend Config

Once frontend is deployed, you need to update `app_final.py` to use the backend URL:

1. Edit `app_final.py` line 21:
   ```python
   # Change from:
   API_BASE = "http://localhost:8000"
   
   # To:
   API_BASE = os.getenv("API_BASE", "http://localhost:8000")
   ```

2. Add at top of file:
   ```python
   import os
   ```

3. Commit and push:
   ```bash
   git add app_final.py
   git commit -m "Use environment variable for API URL"
   git push origin main
   ```

4. Render will auto-deploy the update!

### 7. Access Your App! 🎉

Your app is now live at:
- **Frontend:** `https://phishguard-app.onrender.com`
- **API Docs:** `https://phishguard-api.onrender.com/docs`

## Important Notes

### Free Tier Limitations
- **Spin Down:** Services sleep after 15 min of inactivity
- **Cold Start:** First request takes 30-60 seconds to wake up
- **Database:** 90 days then auto-deletes (upgrade to $7/month for persistence)

### Keep Services Awake (Optional)
Use a service like **UptimeRobot** (free) to ping your app every 5 minutes:
1. Go to https://uptimerobot.com
2. Add monitor for your frontend URL
3. Set interval to 5 minutes

## Troubleshooting

### Build Fails
- Check logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version is 3.10+

### Database Connection Error
- Verify `DATABASE_URL` in environment variables
- Use "Internal Database URL" not "External"
- Check database is in same region

### Frontend Can't Reach Backend
- Verify `API_BASE` environment variable
- Check backend is deployed and running
- Open backend URL + `/health` to test

### AI Not Working
- Verify `GROQ_API_KEY` is set correctly
- Check Groq API key has credits
- View logs for specific error messages

## Cost Breakdown

| Service | Free Tier | Paid Option |
|---------|-----------|-------------|
| Web Service (Backend) | ✅ Free | $7/month |
| Web Service (Frontend) | ✅ Free | $7/month |
| PostgreSQL | ✅ Free (90 days) | $7/month |
| **Total** | **$0/month** | **$21/month** |

## Alternative: All-in-One Deployment

If you want to run both backend and frontend in one service:

1. Create single Web Service
2. Build command:
   ```
   pip install -r requirements.txt && alembic upgrade head
   ```
3. Start command:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT & streamlit run app_final.py --server.port 8501 --server.address 0.0.0.0
   ```
4. Environment variables: DATABASE_URL, GROQ_API_KEY, SECRET_KEY

**Note:** This might be less stable as both services share resources.

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy database on Render
3. ✅ Deploy backend on Render
4. ✅ Deploy frontend on Render
5. ✅ Test your live app!
6. 🎉 Share with friends and family!

---

**Need Help?** Check Render's docs: https://render.com/docs
