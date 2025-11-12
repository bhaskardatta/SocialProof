"""
SocialProof Enhanced - Interactive Cybersecurity Training Platform
With Multi-Level Difficulty, Variety, and Advanced Features
"""

import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="SocialProof Enhanced - Cybersecurity Training",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"
PLAYER_ID = 1

# Initialize session state
if 'selected_email' not in st.session_state:
    st.session_state.selected_email = None
if 'selected_sms' not in st.session_state:
    st.session_state.selected_sms = None
if 'current_level' not in st.session_state:
    st.session_state.current_level = "beginner"

# Enhanced CSS
st.markdown("""
<style>
    /* Dark theme with modern colors */
    :root {
        --primary: #0ea5e9;
        --success: #22c55e;
        --danger: #ef4444;
        --warning: #f59e0b;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .big-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0ea5e9, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .level-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin: 4px;
    }
    
    .level-beginner { background: #22c55e; color: white; }
    .level-easy { background: #3b82f6; color: white; }
    .level-medium { background: #f59e0b; color: white; }
    .level-hard { background: #ef4444; color: white; }
    .level-expert { background: #8b5cf6; color: white; }
    
    .stat-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        text-align: center;
        border-top: 4px solid var(--primary);
    }
    
    .scenario-card {
        background: #1e293b;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid var(--primary);
        transition: all 0.3s;
    }
    
    .scenario-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_player_stats():
    """Fetch player statistics with proper error handling"""
    try:
        response = requests.get(f"{API_BASE_URL}/players/{PLAYER_ID}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Map API fields to UI fields
            return {
                "score": int(data.get("current_skill_rating", 0)),
                "scenarios_attempted": data.get("total_scenarios_resolved", 0),
                "correct_identifications": data.get("correctly_identified_phish", 0),
                "accuracy": data.get("accuracy_percentage", 0)
            }
    except Exception as e:
        print(f"Error fetching stats: {e}")
    
    # Safe fallback
    return {
        "score": 0,
        "scenarios_attempted": 0,
        "correct_identifications": 0,
        "accuracy": 0
    }

def generate_new_scenario(scenario_type: str, difficulty: str):
    """Generate a new scenario"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/scenarios/generate",
            json={
                "player_id": PLAYER_ID,
                "scenario_type": scenario_type,
                "difficulty": difficulty
            }
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error generating scenario: {e}")
    return None

def get_scenarios():
    """Fetch all scenarios for the player with error handling"""
    try:
        response = requests.get(f"{API_BASE_URL}/players/{PLAYER_ID}/scenarios", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching scenarios: {e}")
    return []

# Main Dashboard
def show_dashboard():
    st.markdown('<div class="big-title">🛡️ SocialProof Enhanced</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #94a3b8;">Master Cybersecurity Through Interactive Training</p>', unsafe_allow_html=True)
    
    # Stats
    stats = get_player_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #0ea5e9;">🎯 Score</h3>
            <h1>{stats['score']}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #22c55e;">📊 Attempts</h3>
            <h1>{stats['scenarios_attempted']}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #f59e0b;">✅ Correct</h3>
            <h1>{stats['correct_identifications']}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        accuracy = stats.get('accuracy', 0)
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #8b5cf6;">🎓 Accuracy</h3>
            <h1>{accuracy:.1f}%</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Level Selection & Scenario Generation
    st.markdown("### 🎮 Training Mode")
    
    col_controls, col_info = st.columns([2, 1])
    
    with col_controls:
        # Difficulty selector with 5 levels
        difficulty = st.select_slider(
            "Select Difficulty Level",
            options=["beginner", "easy", "medium", "hard", "expert"],
            value=st.session_state.current_level
        )
        st.session_state.current_level = difficulty
        
        # Scenario type
        scenario_type = st.radio(
            "Choose Training Type",
            ["email", "sms"],
            horizontal=True,
            format_func=lambda x: "📧 Email Phishing" if x == "email" else "📱 SMS Smishing"
        )
        
        # Generate button
        if st.button("🚀 Generate New Scenario", type="primary", use_container_width=True):
            with st.spinner(f"Generating {difficulty} level {scenario_type} scenario..."):
                result = generate_new_scenario(scenario_type, difficulty)
                if result:
                    st.success(f"✅ New {difficulty} scenario created! Go to the training tab to try it.")
                    st.balloons()
    
    with col_info:
        # Difficulty descriptions
        difficulty_info = {
            "beginner": "🟢 Multiple obvious red flags, grammar errors, clear urgency tactics",
            "easy": "🔵 Several red flags, some grammar issues, noticeable urgency",
            "medium": "🟡 Few subtle red flags, proper grammar, moderate urgency",
            "hard": "🔴 Minimal red flags, professional tone, looks very legitimate",
            "expert": "🟣 Nearly perfect mimicry, requires expert knowledge to detect"
        }
        
        st.info(f"**{difficulty.upper()} Level**\n\n{difficulty_info[difficulty]}")
    
    # Recent scenarios
    st.markdown("### 📚 Recent Training Scenarios")
    scenarios = get_scenarios()[:5]  # Show last 5
    
    if scenarios:
        for scenario in scenarios:
            difficulty_class = f"level-{scenario.get('difficulty_label', 'medium').lower()}"
            st.markdown(f"""
            <div class="scenario-card">
                <span class="level-badge {difficulty_class}">{scenario.get('difficulty_label', 'MEDIUM').upper()}</span>
                <strong>{scenario['scenario_type'].upper()}</strong> - 
                ID: {scenario['id']} - 
                {datetime.fromisoformat(scenario['created_at'].replace('Z', '+00:00')).strftime('%b %d, %I:%M %p')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No scenarios yet. Generate one above to get started!")

# Email Training Page
def show_email_training():
    st.markdown("## 📧 Email Phishing Detection Training")
    
    scenarios = [s for s in get_scenarios() if s['scenario_type'] == 'email']
    
    if not scenarios:
        st.info("🎯 No email scenarios yet. Go to Dashboard and generate one!")
        return
    
    # Scenario selector
    scenario_options = {f"Scenario {s['id']} - {s.get('difficulty_label', 'MEDIUM').upper()}": s for s in scenarios}
    selected_label = st.selectbox("Select a scenario", list(scenario_options.keys()))
    scenario = scenario_options[selected_label]
    
    # Display email
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📬 Email Content")
        st.markdown(f"""
        <div style="background: #1e293b; padding: 20px; border-radius: 8px; border-left: 4px solid #0ea5e9;">
            <pre style="white-space: pre-wrap; font-family: monospace; color: #f8fafc;">{scenario['content']}</pre>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🚨 Report as Phishing", type="primary", use_container_width=True):
                st.success("✅ Correct! This is a phishing email. Well done!")
                st.session_state.last_action = "correct"
        
        with col_btn2:
            if st.button("✅ Mark as Safe", use_container_width=True):
                st.error("❌ This was actually a phishing email. Review the red flags!")
                st.session_state.last_action = "incorrect"
        
        with col_btn3:
            if st.button("💡 Show Hints", use_container_width=True):
                st.session_state.show_hints = not st.session_state.get('show_hints', False)
    
    with col2:
        # Difficulty badge
        difficulty = scenario.get('difficulty_label', 'MEDIUM').lower()
        difficulty_class = f"level-{difficulty}"
        st.markdown(f'<span class="level-badge {difficulty_class}">{difficulty.upper()} LEVEL</span>', unsafe_allow_html=True)
        
        # Hints
        if st.session_state.get('show_hints', False):
            st.markdown("### 💡 Red Flag Hints")
            st.info("""
            Look for:
            - Suspicious sender email addresses
            - Grammar or spelling errors
            - Urgent language or threats
            - Suspicious links
            - Requests for sensitive information
            - Generic greetings
            """)

# SMS Training Page
def show_sms_training():
    st.markdown("## 📱 SMS Smishing Detection Training")
    
    scenarios = [s for s in get_scenarios() if s['scenario_type'] == 'sms']
    
    if not scenarios:
        st.info("🎯 No SMS scenarios yet. Go to Dashboard and generate one!")
        return
    
    # Scenario selector
    scenario_options = {f"Scenario {s['id']} - {s.get('difficulty_label', 'MEDIUM').upper()}": s for s in scenarios}
    selected_label = st.selectbox("Select a scenario", list(scenario_options.keys()))
    scenario = scenario_options[selected_label]
    
    # Display SMS
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📲 SMS Message")
        
        # WhatsApp-style message bubble
        st.markdown(f"""
        <div style="background: #075e54; padding: 16px; border-radius: 18px; border-bottom-left-radius: 4px; max-width: 70%; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
            <p style="color: white; margin: 0; font-size: 1.1rem;">{scenario['content']}</p>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.75rem; text-align: right; margin: 8px 0 0 0;">
                {datetime.fromisoformat(scenario['created_at'].replace('Z', '+00:00')).strftime('%I:%M %p')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Action buttons
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚨 Report as Smishing", type="primary", use_container_width=True):
                st.success("✅ Correct! This is a smishing attempt. Great job!")
        
        with col_btn2:
            if st.button("✅ Mark as Legitimate", use_container_width=True):
                st.error("❌ This was actually smishing. Check the red flags!")
    
    with col2:
        difficulty = scenario.get('difficulty_label', 'MEDIUM').lower()
        difficulty_class = f"level-{difficulty}"
        st.markdown(f'<span class="level-badge {difficulty_class}">{difficulty.upper()} LEVEL</span>', unsafe_allow_html=True)

# AI Guardian Page
def show_ai_guardian():
    st.markdown("## 🤖 AI Guardian - Your Cybersecurity Assistant")
    
    st.info("Ask me anything about phishing, smishing, or social engineering attacks!")
    
    question = st.text_area("Your question:", placeholder="e.g., How can I identify a phishing email?")
    
    if st.button("🔍 Ask Guardian", type="primary"):
        if question:
            with st.spinner("AI Guardian is thinking..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/guardian/query",
                        json={"question": question}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown("### 💡 Guardian's Response")
                        st.success(data['answer'])
                        
                        if data.get('sources'):
                            st.markdown(f"**Sources:** {', '.join(data['sources'])}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question first!")

# Main App
def main():
    # Sidebar navigation
    st.sidebar.markdown("## 🎯 Navigation")
    page = st.sidebar.radio(
        "Choose a section:",
        ["🏠 Dashboard", "📧 Email Training", "📱 SMS Training", "🤖 AI Guardian"]
    )
    
    st.sidebar.markdown("---")
    
    # Player info
    stats = get_player_stats()
    st.sidebar.markdown(f"""
    ### 👤 Player Stats
    **Score:** {stats.get('score', 0)}  
    **Completed:** {stats.get('scenarios_attempted', 0)}  
    **Accuracy:** {stats.get('accuracy', 0):.1f}%
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎓 Progress")
    
    # Progress bar
    attempts = stats.get('scenarios_attempted', 0)
    progress = min(attempts / 20, 1.0)  # Cap at 20 scenarios
    st.sidebar.progress(progress)
    st.sidebar.caption(f"{attempts}/20 scenarios completed")
    
    # Route to pages
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📧 Email Training":
        show_email_training()
    elif page == "📱 SMS Training":
        show_sms_training()
    elif page == "🤖 AI Guardian":
        show_ai_guardian()

if __name__ == "__main__":
    main()
