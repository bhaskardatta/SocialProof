# 🛡️ SocialProof - AI Cybersecurity Training Platform

An interactive cybersecurity training platform powered by AI that helps users identify and defend against phishing, smishing, and social engineering attacks through realistic simulations.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🎯 **Interactive Email & SMS Simulations** - Realistic phishing and smishing scenarios
- 🤖 **AI-Powered Scenario Generation** - Groq Llama 3.3 70B creates unique scenarios
- 🧠 **RAG System** - Knowledge base integration for contextual AI responses
- 📊 **Progress Tracking** - Skill ratings, accuracy metrics, and detailed statistics
- 💬 **Digital Guardian** - AI assistant for cybersecurity questions
- 🎨 **Modern UI** - Professional Streamlit interface with dark theme

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL
- Groq API Key ([Get free key](https://console.groq.com))

### Installation

```bash
# Clone repository
git clone https://github.com/bhaskardatta/SocialProof.git
cd SocialProof

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb socialproof

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Initialize database
python init_db.py

# Run backend
uvicorn app.main:app --reload &

# Run frontend
streamlit run streamlit_app.py
```

Access the app at: **http://localhost:8501**

## 📋 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/socialproof
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
```

## 🏗️ Tech Stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic  
**Frontend:** Streamlit, Plotly  
**AI:** Groq Llama 3.3 70B, LangChain, RAG  
**Database:** Async PostgreSQL with Alembic migrations

## 📚 API Documentation

Once running, visit:
- Interactive API Docs: http://127.0.0.1:8000/docs
- Alternative Docs: http://127.0.0.1:8000/redoc

## 🎮 Usage

1. **Training Simulations** - Navigate to Email or SMS simulation pages
2. **Identify Threats** - Review scenarios and decide: Report or Mark Safe
3. **Get Feedback** - Receive instant scoring and skill rating updates
4. **Track Progress** - Monitor statistics and improvement over time
5. **Ask AI Guardian** - Get cybersecurity advice with contextual answers

## 🧠 RAG Implementation

The platform uses Retrieval Augmented Generation with a knowledge base in `knowledge_base/`:
- `phishing.txt` - Email phishing attack information
- `smishing.txt` - SMS-based attack knowledge
- `social_engineering.txt` - General social engineering tactics

AI responses are enhanced with relevant context from these sources.

## 🔒 Security

- Environment variables for sensitive data
- Input validation with Pydantic
- Async database operations
- CORS configuration
- No sensitive data in scenarios

## 📊 Database Schema

- **player_profiles** - User accounts and skill ratings
- **game_scenarios** - AI-generated training scenarios

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with Groq, LangChain, FastAPI, Streamlit, and PostgreSQL

---

**Last Updated:** November 12, 2025
