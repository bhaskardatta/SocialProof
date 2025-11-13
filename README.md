# 🛡️ PhishGuard - AI Cybersecurity Training Platform# SocialProof - Cybersecurity Training Platform# 🛡️ SocialProof - AI Cybersecurity Training Platform



An interactive, AI-powered platform that helps users identify phishing emails and SMS scams through realistic training simulations with Gmail and iMessage interfaces.



![Python](https://img.shields.io/badge/python-3.10+-blue.svg)Professional, AI-powered platform for learning to identify phishing and smishing attacks. Suitable for all ages and skill levels.An interactive cybersecurity training platform powered by AI that helps users identify and defend against phishing, smishing, and social engineering attacks through realistic simulations.

![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)

![Streamlit](https://img.shields.io/badge/Streamlit-1.51-red.svg)

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Quick Start![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

## ✨ Features

![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)

### Training Modules

- 📧 **Email Phishing Training** - Realistic Gmail UI with India-specific scenarios```bash![Streamlit](https://img.shields.io/badge/Streamlit-1.51-red.svg)

- 💬 **SMS Phishing Training** - Authentic iMessage interface with Indian scams

- 🎯 **5 Difficulty Levels** - From Beginner to Expert# Install dependencies![License](https://img.shields.io/badge/license-MIT-blue.svg)



### AI Assistantpip install -r requirements.txt

- 🤖 **Scenario-Specific Help** - 4 quick questions + custom queries

- 💡 **General AI Chat** - RAG-powered cybersecurity knowledge base## ✨ Features

- 📚 **Educational Feedback** - Detailed explanations for wrong answers

# Setup environment

### Performance Tracking

- 📊 **Detailed Statistics** - Accuracy, skill rating, completion countscp .env.example .env- 🎯 **Interactive Email & SMS Simulations** - Realistic phishing and smishing scenarios

- 🎖️ **Skill Badges** - Beginner to Expert levels

- 💯 **Personalized Insights** - Custom recommendations based on performance# Add your GROQ_API_KEY to .env- 🤖 **AI-Powered Scenario Generation** - Groq Llama 3.3 70B creates unique scenarios



### India-Specific Content- 🧠 **RAG System** - Knowledge base integration for contextual AI responses

- 🇮🇳 **Local Context** - SBI, HDFC, ICICI, UPI, Paytm, PhonePe scenarios

- 🏦 **Banking Scams** - Aadhaar, PAN card, GST verification phishing# Run database migrations- 📊 **Progress Tracking** - Skill ratings, accuracy metrics, and detailed statistics

- 📱 **Mobile Scams** - OTP, package delivery, and payment frauds

alembic upgrade head- 💬 **Digital Guardian** - AI assistant for cybersecurity questions

## 🚀 Quick Start

- 🎨 **Modern UI** - Professional Streamlit interface with dark theme

### Prerequisites

- Python 3.10+# Start backend

- PostgreSQL

- Groq API Key ([Get free key](https://console.groq.com))uvicorn app.main:app --reload &## 🚀 Quick Start



### Installation



```bash# Start application### Prerequisites

# Clone repository

git clone https://github.com/bhaskardatta/SocialProof.gitstreamlit run app.py- Python 3.10+

cd SocialProof

```- PostgreSQL

# Install dependencies

pip install -r requirements.txt- Groq API Key ([Get free key](https://console.groq.com))



# Setup databaseAccess at: **http://localhost:8501**

createdb socialproof

### Installation

# Configure environment

cp .env.example .env## Features

# Edit .env and add your GROQ_API_KEY and DATABASE_URL

```bash

# Run database migrations

alembic upgrade head- Interactive training scenarios# Clone repository



# Start backend (Terminal 1)- AI-generated unique threatsgit clone https://github.com/bhaskardatta/SocialProof.git

uvicorn app.main:app --host 0.0.0.0 --port 8000

- Real-time feedbackcd SocialProof

# Start frontend (Terminal 2)

streamlit run app_final.py --server.port 8501- AI assistant for questions

```

- Progress tracking# Install dependencies

### Access the App

- **Frontend:** http://localhost:8501- 5 difficulty levelspip install -r requirements.txt

- **API Docs:** http://localhost:8000/docs



## 📋 Environment Variables

## Tech Stack# Setup database

Create `.env` file with:

createdb socialproof

```env

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/socialproofFastAPI • PostgreSQL • Streamlit • Groq AI • LangChain

GROQ_API_KEY=your_groq_api_key_here

SECRET_KEY=your_secret_key_here# Configure environment

```cp .env.example .env

# Edit .env and add your GROQ_API_KEY

## 🏗️ Tech Stack

# Initialize database

**Backend:**python init_db.py

- FastAPI - High-performance async API framework

- PostgreSQL - Relational database# Run backend

- SQLAlchemy 2.0 - Async ORMuvicorn app.main:app --reload &

- Alembic - Database migrations

# Run frontend

**Frontend:**streamlit run streamlit_app.py

- Streamlit - Interactive web interface```

- Custom CSS - Gmail & iMessage replicas

Access the app at: **http://localhost:8501**

**AI:**

- Groq Llama 3.3 70B - Large language model## 📋 Environment Variables

- LangChain - RAG implementation

- Custom Knowledge Base - Cybersecurity documentsCreate a `.env` file:



## 📁 Project Structure```env

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/socialproof

```LLM_PROVIDER=groq

├── app/                    # Backend FastAPI applicationGROQ_API_KEY=your_groq_api_key_here

│   ├── main.py            # API routes and endpoints```

│   ├── models.py          # Database models

│   ├── schemas.py         # Pydantic schemas## 🏗️ Tech Stack

│   ├── crud.py            # Database operations

│   ├── ai_core_advanced.py # AI and RAG system**Backend:** FastAPI, PostgreSQL, SQLAlchemy 2.0, Pydantic  

│   └── database.py        # Database configuration**Frontend:** Streamlit, Plotly  

├── app_final.py           # Streamlit frontend application**AI:** Groq Llama 3.3 70B, LangChain, RAG  

├── knowledge_base/        # RAG knowledge documents**Database:** Async PostgreSQL with Alembic migrations

│   ├── phishing.txt       # Email phishing knowledge

│   ├── smishing.txt       # SMS phishing knowledge## 📚 API Documentation

│   └── social_engineering.txt

├── alembic/              # Database migration filesOnce running, visit:

├── requirements.txt       # Python dependencies- Interactive API Docs: http://127.0.0.1:8000/docs

└── .env.example          # Environment template- Alternative Docs: http://127.0.0.1:8000/redoc

```

## 🎮 Usage

## 🎮 How to Use

1. **Training Simulations** - Navigate to Email or SMS simulation pages

1. **Start Training**2. **Identify Threats** - Review scenarios and decide: Report or Mark Safe

   - Choose Email or SMS training3. **Get Feedback** - Receive instant scoring and skill rating updates

   - Select difficulty level4. **Track Progress** - Monitor statistics and improvement over time

   - Generate scenario5. **Ask AI Guardian** - Get cybersecurity advice with contextual answers



2. **Analyze Scenario**## 🧠 RAG Implementation

   - Review the message carefully

   - Look for red flagsThe platform uses Retrieval Augmented Generation with a knowledge base in `knowledge_base/`:

   - Make your decision- `phishing.txt` - Email phishing attack information

- `smishing.txt` - SMS-based attack knowledge

3. **Get Feedback**- `social_engineering.txt` - General social engineering tactics

   - See if you were correct

   - Read detailed explanationAI responses are enhanced with relevant context from these sources.

   - Learn what to watch for

## 🔒 Security

4. **Ask AI Assistant**

   - Click quick question buttons- Environment variables for sensitive data

   - Or type custom questions- Input validation with Pydantic

   - Get instant help- Async database operations

- CORS configuration

5. **Track Progress**- No sensitive data in scenarios

   - View your statistics

   - See skill level## 📊 Database Schema

   - Get personalized tips

- **player_profiles** - User accounts and skill ratings

## 🤖 AI Features- **game_scenarios** - AI-generated training scenarios



### Scenario Generation## 🤝 Contributing

- Dynamic AI-generated phishing scenarios

- India-specific context and threatsContributions welcome! Please open an issue or submit a pull request.

- Multiple difficulty levels

- No repeated content## 📝 License



### AI AssistantMIT License - see LICENSE file for details

**Scenario-Specific Mode:**

- Analyzes current training scenario## 🙏 Acknowledgments

- 4 pre-made quick questions

- Custom question supportBuilt with Groq, LangChain, FastAPI, Streamlit, and PostgreSQL

- Context-aware responses

---

**General Chat Mode:**

- Cybersecurity knowledge base**Last Updated:** November 12, 2025

- 6 quick topic buttons
- RAG-powered accurate answers
- Source attribution

### Educational System
- Detailed feedback on wrong answers
- Red flag identification
- Learning points extraction
- Reinforcement on correct answers

## 📊 Performance Metrics

- **Total Scenarios:** Track completion count
- **Accuracy Rate:** Percentage of correct identifications
- **Skill Rating:** ELO-style rating (500-800)
- **Skill Level:** Beginner → Intermediate → Advanced → Expert
- **Insights:** Personalized strengths and areas to improve

## 🔒 Security Features

- Environment variables for sensitive data
- Input validation with Pydantic
- Async database operations
- Secure password handling
- No sensitive user data stored

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

**Bhaskar Datta**
- GitHub: [@bhaskardatta](https://github.com/bhaskardatta)

## 🙏 Acknowledgments

- Groq for AI infrastructure
- LangChain for RAG framework
- FastAPI and Streamlit communities
- PostgreSQL team

---

**Built with ❤️ to make the internet safer for everyone**
