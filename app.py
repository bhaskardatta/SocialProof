"""
SocialProof - Interactive Cybersecurity Training Platform
Professional, clean UI suitable for all age groups
"""

import streamlit as st
import requests
from datetime import datetime
import plotly.express as px

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="SocialProof - Cybersecurity Training",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "http://127.0.0.1:8000"

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session():
    """Initialize session state variables"""
    if 'player_id' not in st.session_state:
        st.session_state.player_id = 1
    
    if 'current_score' not in st.session_state:
        st.session_state.current_score = 0
    
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    
    if 'active_scenario' not in st.session_state:
        st.session_state.active_scenario = None
    
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

init_session()

# ============================================================================
# PROFESSIONAL STYLING - CLEAN & ACCESSIBLE
# ============================================================================

st.markdown("""
<style>
    /* Clean, professional theme for all ages */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main theme */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Cards */
    .info-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #3498db;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2980b9;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Scenario display */
    .scenario-container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #e8e8e8;
        margin: 1.5rem 0;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Message box */
    .message-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-left: 4px solid #27ae60;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        padding: 1.5rem;
        border-left: 4px solid #ffc107;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        padding: 1.5rem;
        border-left: 4px solid #dc3545;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    /* AI Assistant */
    .ai-assistant {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .ai-response {
        background: white;
        color: #2c3e50;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    /* Progress bar */
    .progress-container {
        background: #e9ecef;
        height: 30px;
        border-radius: 15px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #3498db, #2ecc71);
        height: 100%;
        transition: width 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        background: #3498db;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 6px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: #2980b9;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        background: #3498db;
        color: white;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-success { background: #27ae60; }
    .badge-warning { background: #f39c12; }
    .badge-danger { background: #e74c3c; }
    .badge-info { background: #3498db; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# API FUNCTIONS
# ============================================================================

def get_player_stats():
    """Fetch player statistics"""
    try:
        response = requests.get(f"{API_BASE}/players/{st.session_state.player_id}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return {'total_score': 0, 'scenarios_completed': 0, 'correct_answers': 0, 'accuracy': 0}

def generate_scenario(scenario_type: str, difficulty: str):
    """Generate new scenario"""
    try:
        response = requests.post(
            f"{API_BASE}/scenarios/generate",
            json={
                "player_id": st.session_state.player_id,
                "scenario_type": scenario_type,
                "difficulty": difficulty
            },
            timeout=15
        )
        if response.status_code in [200, 201]:
            return response.json()
    except Exception as e:
        st.error(f"Error generating scenario: {str(e)}")
    return None

def ask_ai_assistant(question: str):
    """Ask AI Guardian for help"""
    try:
        response = requests.post(
            f"{API_BASE}/guardian/query",
            json={"question": question},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error contacting AI Assistant: {str(e)}")
    return None

def submit_answer(scenario_id: int, is_threat: bool):
    """Submit player answer"""
    try:
        action = "reported_phish" if is_threat else "deleted_safe"
        response = requests.post(
            f"{API_BASE}/scenarios/{scenario_id}/resolve",
            json={"action": action},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# ============================================================================
# UI COMPONENTS
# ============================================================================

def show_header():
    """Display main header with stats"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div style='padding: 1rem 0;'>
            <h1 style='margin: 0; color: #2c3e50;'>🛡️ SocialProof Training</h1>
            <p style='color: #7f8c8d; font-size: 1.1rem; margin: 0.5rem 0;'>
                Learn to identify and protect against cyber threats
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.session_state.active_scenario = None
            st.rerun()
    
    # Stats bar
    stats = get_player_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-label'>Score</div>
            <div class='stat-number'>{stats.get('total_score', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-label'>Completed</div>
            <div class='stat-number'>{stats.get('scenarios_completed', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        accuracy = stats.get('accuracy', 0)
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-label'>Accuracy</div>
            <div class='stat-number'>{accuracy:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-label'>Streak</div>
            <div class='stat-number'>{st.session_state.streak}</div>
        </div>
        """, unsafe_allow_html=True)

def show_ai_assistant_sidebar():
    """AI Assistant in sidebar"""
    with st.sidebar:
        st.markdown("""
        <div class='ai-assistant'>
            <h3 style='margin: 0; color: white;'>🤖 AI Assistant</h3>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Ask me anything about cybersecurity</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick tips
        with st.expander("💡 Quick Tips", expanded=False):
            st.markdown("""
            - Check the sender's email address carefully
            - Look for spelling and grammar errors
            - Be cautious of urgent or threatening language
            - Verify unexpected requests independently
            - Hover over links to see actual URLs
            - Never share passwords or sensitive info
            """)
        
        st.markdown("---")
        
        # Ask AI Assistant
        st.markdown("### 💬 Ask a Question")
        question = st.text_area(
            "What would you like to know?",
            placeholder="e.g., How can I spot a phishing email?",
            height=100,
            label_visibility="collapsed"
        )
        
        if st.button("Get Answer", use_container_width=True):
            if question:
                with st.spinner("AI Assistant is thinking..."):
                    response = ask_ai_assistant(question)
                    if response:
                        st.markdown(f"""
                        <div class='ai-response'>
                            {response.get('answer', 'Unable to answer at the moment.')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if response.get('sources'):
                            st.caption(f"📚 Sources: {', '.join(response['sources'])}")

def show_home_page():
    """Home page with mission selection"""
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-card'>
        <h2>Welcome to Your Cybersecurity Training</h2>
        <p style='font-size: 1.1rem; color: #555; line-height: 1.8;'>
            Cybercriminals use emails and text messages to steal personal information, 
            money, and identities. Learn to recognize these threats through interactive, 
            AI-generated scenarios that mimic real-world attacks.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Choose Your Training Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='info-card'>
            <h3>📧 Email Phishing</h3>
            <p>Learn to identify fraudulent emails designed to steal your information.</p>
            <ul>
                <li>Recognize suspicious sender addresses</li>
                <li>Spot fake links and attachments</li>
                <li>Identify social engineering tactics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Email Training", key="email_training", use_container_width=True):
            st.session_state.current_page = 'email_training'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='info-card'>
            <h3>📱 SMS Smishing</h3>
            <p>Practice detecting malicious text messages (smishing attacks).</p>
            <ul>
                <li>Identify suspicious text messages</li>
                <li>Recognize urgent or threatening tactics</li>
                <li>Spot fake links in SMS</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start SMS Training", key="sms_training", use_container_width=True):
            st.session_state.current_page = 'sms_training'
            st.rerun()

def show_training_page(training_type: str):
    """Main training interface"""
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = 'home'
        st.session_state.active_scenario = None
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # If no active scenario, show difficulty selection
    if not st.session_state.active_scenario:
        show_difficulty_selection(training_type)
    else:
        show_active_scenario(training_type)

def show_difficulty_selection(training_type: str):
    """Difficulty selection screen"""
    
    icon = "📧" if training_type == "email" else "📱"
    title = "Email Phishing" if training_type == "email" else "SMS Smishing"
    
    st.markdown(f"""
    <div class='info-card'>
        <h2>{icon} {title} Training</h2>
        <p>Select a difficulty level to begin. Each level presents unique, AI-generated scenarios.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Select Difficulty Level")
    
    difficulty_info = {
        "beginner": {
            "name": "🟢 Beginner",
            "desc": "Multiple obvious red flags, easier to spot",
            "points": "10 points"
        },
        "easy": {
            "name": "🔵 Easy",
            "desc": "Several warning signs, good for learning",
            "points": "20 points"
        },
        "medium": {
            "name": "🟡 Medium",
            "desc": "Fewer red flags, requires attention",
            "points": "30 points"
        },
        "hard": {
            "name": "🔴 Hard",
            "desc": "Subtle indicators, looks professional",
            "points": "50 points"
        },
        "expert": {
            "name": "🟣 Expert",
            "desc": "Very realistic, requires expertise",
            "points": "100 points"
        }
    }
    
    selected_difficulty = st.select_slider(
        "Difficulty",
        options=list(difficulty_info.keys()),
        value="beginner",
        format_func=lambda x: difficulty_info[x]["name"],
        label_visibility="collapsed"
    )
    
    st.markdown(f"""
    <div class='message-box'>
        <strong>{difficulty_info[selected_difficulty]["name"]}</strong><br>
        {difficulty_info[selected_difficulty]["desc"]}<br>
        <span class='badge badge-success'>{difficulty_info[selected_difficulty]["points"]}</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎯 Generate New Scenario", type="primary", use_container_width=True):
            with st.spinner("AI is creating a unique scenario for you..."):
                scenario = generate_scenario(training_type, selected_difficulty)
                if scenario:
                    st.session_state.active_scenario = scenario
                    st.session_state.scenario_difficulty = selected_difficulty
                    st.session_state.show_explanation = False
                    st.rerun()
                else:
                    st.error("Unable to generate scenario. Please try again.")

def show_active_scenario(training_type: str):
    """Display active scenario and interaction"""
    
    scenario = st.session_state.active_scenario
    
    icon = "📧" if training_type == "email" else "📱"
    
    st.markdown(f"""
    <div class='info-card'>
        <h2>{icon} Analyze This Message</h2>
        <p>Read the message below carefully and decide: Is it a <strong>THREAT</strong> or <strong>SAFE</strong>?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display scenario
    st.markdown(f"""
    <div class='scenario-container'>
        {scenario.get('content', 'Loading scenario...')}
    </div>
    """, unsafe_allow_html=True)
    
    # AI Assistant hint section
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### What do you think?")
    
    with col2:
        if st.button("💡 Get AI Hint"):
            with st.spinner("AI Assistant analyzing..."):
                hint = ask_ai_assistant(f"What should I look for to identify if this {training_type} message is a threat? Don't give away the answer, just provide helpful hints.")
                if hint:
                    st.markdown(f"""
                    <div class='warning-box'>
                        <strong>💡 AI Hint:</strong><br>
                        {hint.get('answer', 'Unable to provide hint.')}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Answer buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🚨 This is a THREAT", type="primary", use_container_width=True):
            handle_answer(scenario['scenario_id'], True, training_type)
    
    with col3:
        if st.button("✅ This is SAFE", use_container_width=True):
            handle_answer(scenario['scenario_id'], False, training_type)

def handle_answer(scenario_id: int, is_threat: bool, training_type: str):
    """Process player's answer"""
    
    result = submit_answer(scenario_id, is_threat)
    
    if result:
        correct = result.get('action_correct', False)
        
        if correct:
            # Correct answer
            points = {
                'beginner': 10, 'easy': 20, 'medium': 30,
                'hard': 50, 'expert': 100
            }.get(st.session_state.scenario_difficulty, 20)
            
            st.session_state.current_score += points
            st.session_state.streak += 1
            
            st.markdown(f"""
            <div class='message-box'>
                <h3 style='color: #27ae60; margin: 0;'>✅ Correct!</h3>
                <p style='margin: 0.5rem 0;'>{result.get('message', 'Well done!')}</p>
                <span class='badge badge-success'>+{points} points</span>
                <span class='badge badge-info'>{st.session_state.streak} streak</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
        else:
            # Incorrect answer
            st.session_state.streak = 0
            
            st.markdown(f"""
            <div class='error-box'>
                <h3 style='color: #e74c3c; margin: 0;'>❌ Not Quite</h3>
                <p style='margin: 0.5rem 0;'>{result.get('message', 'Try again!')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get AI explanation
            with st.spinner("AI Assistant preparing detailed explanation..."):
                explanation = ask_ai_assistant(
                    f"Explain why this {training_type} message was actually a {'threat' if not is_threat else 'safe message'}. "
                    f"Provide specific red flags or reasons. Be educational and supportive."
                )
                
                if explanation:
                    st.markdown(f"""
                    <div class='ai-response'>
                        <strong>📚 Learning Moment:</strong><br>
                        {explanation.get('answer', '')}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Next scenario button
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("➡️ Next Scenario", use_container_width=True):
                st.session_state.active_scenario = None
                st.session_state.show_explanation = False
                st.rerun()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    show_header()
    show_ai_assistant_sidebar()
    
    st.markdown("---")
    
    # Route to appropriate page
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'email_training':
        show_training_page('email')
    elif st.session_state.current_page == 'sms_training':
        show_training_page('sms')

if __name__ == "__main__":
    main()
