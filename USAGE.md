# SocialProof - Usage Guide

## ✅ Current Status

**EVERYTHING IS RUNNING AND READY!**

- Backend API: http://localhost:8000
- Training Platform: http://localhost:8501
- API Documentation: http://localhost:8000/docs

## 🚀 How to Use

### For Users

1. **Open the application**: http://localhost:8501
2. **Choose training type**: Email or SMS
3. **Select difficulty**: From beginner to expert
4. **Analyze scenarios**: Read AI-generated threats
5. **Make decisions**: Click "THREAT" or "SAFE"
6. **Learn from feedback**: Get instant AI explanations
7. **Ask questions**: Use AI Assistant in sidebar anytime

### Key Features

✨ **AI-Generated Scenarios**
- Every scenario is completely unique
- Generated in real-time using Groq Llama 3.3 70B
- Tailored to difficulty level

🤖 **AI Assistant (Always Available)**
- Ask any cybersecurity question
- Get instant, contextual answers
- Powered by RAG (knowledge base)
- Available on every page in sidebar

📊 **Progress Tracking**
- Score points for correct answers
- Track accuracy percentage
- Build streaks
- Monitor completed scenarios

🎓 **5 Difficulty Levels**
1. Beginner - Easy to spot, many red flags
2. Easy - Some obvious indicators
3. Medium - Requires attention
4. Hard - Subtle, professional-looking
5. Expert - Nearly perfect mimicry

## 🎯 What Makes It Special

### 100% Generative AI
- No pre-written scenarios
- Every message is unique
- AI adapts to create variety
- Educational and realistic

### Interactive Learning
- Instant feedback on answers
- Detailed AI explanations for mistakes
- Contextual hints available
- Ask questions anytime

### Professional & Accessible
- Clean, modern interface
- Suitable for all age groups
- No overwhelming game aesthetics
- Focus on education

## 🔧 Backend API Endpoints

Available at http://localhost:8000/docs

- `GET /health` - Check API status
- `GET /players/{id}/stats` - Get player statistics  
- `POST /scenarios/generate` - Generate new scenario
- `POST /scenarios/{id}/resolve` - Submit answer
- `POST /guardian/query` - Ask AI Assistant

## 💡 Tips for Best Experience

1. **Take your time** - Read scenarios carefully
2. **Use AI Assistant** - Ask questions when unsure
3. **Learn from mistakes** - Read the explanations
4. **Progress gradually** - Start with beginner level
5. **Stay curious** - The AI can answer any security question

## 📝 Project Structure

```
SocialProof/
├── app.py                    # Main Streamlit UI
├── app/
│   ├── main.py              # FastAPI backend
│   ├── ai_core_advanced.py  # AI scenario generation
│   ├── models.py            # Database models
│   └── ...
├── knowledge_base/          # RAG training data
└── alembic/                 # Database migrations
```

## 🎨 Design Philosophy

- **Clean over flashy** - Professional appearance
- **Educational over game-like** - Focus on learning
- **Accessible to all** - Simple, intuitive interface
- **AI-powered** - Heavily uses generative AI
- **Interactive** - Real-time feedback and help

## 🚦 Next Steps

The platform is ready to use! Just:
1. Open http://localhost:8501
2. Start training
3. Learn and improve your skills

Both services are running in the background and will continue running until you stop them.

To stop: `pkill -f streamlit && pkill -f uvicorn`

---

**Happy Learning! 🛡️**
