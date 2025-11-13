"""
PhishGuard - Professional Cybersecurity Training Platform
Realistic Gmail and iMessage UI for Indian phishing scenarios
"""

import streamlit as st
import requests
import html
import re
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="PhishGuard - Cybersecurity Training",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

# ============================================================================
# PROFESSIONAL CSS - GMAIL & iMESSAGE REPLICAS
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=SF+Pro+Display:wght@300;400;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
    }
    
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 1400px;
    }
    
    /* Force all text to be dark and visible */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li {
        color: #1e293b !important;
    }
    
    /* Header */
    .app-header {
        background: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .app-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0891b2 !important;
        margin: 0;
    }
    
    /* Stats Cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #64748b !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a !important;
    }
    
    /* Content Cards */
    .content-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0891b2, #06b6d4) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(8, 145, 178, 0.3) !important;
    }
    
    /* Difficulty Buttons */
    .difficulty-button {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        margin: 0.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        border: 2px solid #e2e8f0;
        background: white;
        color: #475569 !important;
    }
    
    .difficulty-button:hover {
        border-color: #0891b2;
        background: #f0f9ff;
    }
    
    .difficulty-button.selected {
        background: #0891b2;
        color: white !important;
        border-color: #0891b2;
    }
    
    /* GMAIL REPLICA */
    .gmail-container {
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        margin: 1rem 0;
        font-family: 'Roboto', sans-serif;
    }
    
    .gmail-header {
        padding: 1.5rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .gmail-subject {
        font-size: 1.375rem;
        font-weight: 400;
        color: #202124 !important;
        margin-bottom: 1rem;
    }
    
    .gmail-from {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .gmail-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #0891b2;
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-right: 0.75rem;
    }
    
    .gmail-sender {
        flex: 1;
    }
    
    .gmail-sender-name {
        font-weight: 500;
        color: #202124 !important;
        font-size: 0.875rem;
    }
    
    .gmail-sender-email {
        color: #5f6368 !important;
        font-size: 0.75rem;
    }
    
    .gmail-body {
        padding: 1.5rem;
        color: #202124 !important;
        font-size: 0.875rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    
    .gmail-footer {
        padding: 1rem 1.5rem;
        border-top: 1px solid #e5e7eb;
        display: flex;
        gap: 0.5rem;
    }
    
    .gmail-action-btn {
        padding: 0.5rem 1rem;
        border: 1px solid #dadce0;
        border-radius: 4px;
        background: white;
        color: #5f6368 !important;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
    }
    
    /* iMESSAGE REPLICA */
    .imessage-container {
        background: white;
        border-radius: 24px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        margin: 1rem auto;
        max-width: 400px;
        font-family: 'SF Pro Display', -apple-system, sans-serif;
        overflow: hidden;
    }
    
    .imessage-header {
        background: #f7f7f7;
        padding: 0.75rem 1rem;
        text-align: center;
        border-bottom: 1px solid #d1d1d6;
    }
    
    .imessage-contact {
        font-weight: 600;
        color: #000 !important;
        font-size: 0.875rem;
    }
    
    .imessage-messages {
        padding: 1rem;
        background: white;
        min-height: 200px;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .imessage-bubble {
        max-width: 80%;
        margin-bottom: 0.5rem;
        clear: both;
    }
    
    .imessage-bubble-content {
        background: #007AFF;
        color: white !important;
        padding: 0.625rem 0.875rem;
        border-radius: 18px;
        font-size: 0.9375rem;
        line-height: 1.4;
        word-wrap: break-word;
        display: inline-block;
    }
    
    .imessage-time {
        font-size: 0.6875rem;
        color: #8e8e93 !important;
        margin-top: 0.25rem;
    }
    
    .imessage-keyboard {
        background: #f7f7f7;
        padding: 0.5rem;
        border-top: 1px solid #d1d1d6;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .imessage-input {
        flex: 1;
        background: white;
        border: 1px solid #d1d1d6;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
        color: #000 !important;
    }
    
    /* Feedback Messages */
    .feedback-success {
        background: #dcfce7;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #166534 !important;
        font-weight: 600;
    }
    
    .feedback-error {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #991b1b !important;
        font-weight: 600;
    }
    
    /* AI Chatbot Popup */
    .ai-popup {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 350px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        z-index: 1000;
    }
    
    .ai-popup-header {
        background: #0891b2;
        color: white !important;
        padding: 1rem;
        border-radius: 12px 12px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .ai-popup-body {
        padding: 1rem;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .ai-message {
        background: #f3f4f6;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        color: #1f2937 !important;
        font-size: 0.875rem;
    }
    
    .user-message {
        background: #0891b2;
        color: white !important;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
    }
    
    /* Floating AI Button */
    .ai-float-btn {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 60px;
        height: 60px;
        background: #0891b2;
        border-radius: 50%;
        box-shadow: 0 4px 12px rgba(8, 145, 178, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 999;
        font-size: 1.5rem;
    }
    
    /* Radio buttons styling */
    .stRadio > div {
        display: flex;
        gap: 1rem;
    }
    
    .stRadio label {
        color: #1e293b !important;
    }
    
    /* Input fields */
    .stTextInput input, .stTextArea textarea {
        color: #1e293b !important;
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'player_id' not in st.session_state:
    st.session_state.player_id = 1
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'active_scenario' not in st.session_state:
    st.session_state.active_scenario = None
if 'selected_difficulty' not in st.session_state:
    st.session_state.selected_difficulty = 'beginner'
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False
if 'feedback_message' not in st.session_state:
    st.session_state.feedback_message = ''
if 'feedback_type' not in st.session_state:
    st.session_state.feedback_type = ''
if 'show_ai_chat' not in st.session_state:
    st.session_state.show_ai_chat = False
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'scenario_content_only' not in st.session_state:
    st.session_state.scenario_content_only = ''

# ============================================================================
# API FUNCTIONS
# ============================================================================

def get_player_stats():
    """Fetch player statistics"""
    try:
        response = requests.get(f"{API_BASE}/players/{st.session_state.player_id}/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return {
        'total_scenarios_resolved': 0,
        'correctly_identified_phish': 0,
        'current_skill_rating': 500,
        'accuracy_percentage': 0
    }

def generate_scenario(scenario_type: str, difficulty: str):
    """Generate scenario and extract clean content"""
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
            scenario = response.json()
            # Extract only the email/sms content, remove red flags section
            content = scenario.get('content', '')
            clean_content = extract_clean_content(content)
            scenario['display_content'] = clean_content
            scenario['full_content'] = content  # Keep for AI analysis
            return scenario
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None

def extract_clean_content(content: str) -> str:
    """Remove red flags and extra analysis from scenario content"""
    # Split by common markers
    markers = [
        'Red flags:',
        'Red flag:',
        'Grammar errors:',
        'Urgency level:',
        'Link subtlety:',
        'Educational Notes:',
        'This email is different',
        'This message has',
        'Note:',
        'INDIA-SPECIFIC',
        '---'
    ]
    
    clean = content
    for marker in markers:
        if marker in clean:
            clean = clean.split(marker)[0]
    
    # Clean up extra newlines
    clean = re.sub(r'\n{3,}', '\n\n', clean.strip())
    return clean

def resolve_scenario(scenario_id: int, action: str):
    """Submit answer"""
    try:
        response = requests.post(
            f"{API_BASE}/scenarios/{scenario_id}/resolve",
            json={"action": action},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return None

def ask_ai_about_scenario(question: str, scenario_content: str):
    """Ask AI about current scenario"""
    try:
        # Build enhanced query with scenario context
        enhanced_query = f"""I'm analyzing this message:

{scenario_content}

Question: {question}

Please help me understand if this is safe or suspicious."""
        
        # Call the AI guardian endpoint
        response = requests.post(
            f"{API_BASE}/guardian/query",
            json={
                "query": enhanced_query,
                "player_id": st.session_state.player_id
            },
            timeout=15
        )
        
        # Check response status
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"AI Error: Status {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("AI request timed out. Please try again.")
        return None
    except Exception as e:
        st.error(f"AI Error: {str(e)}")
        return None

# ============================================================================
# UI COMPONENTS
# ============================================================================

def show_header():
    """Display header"""
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.markdown("<h1 class='app-title'>🛡️ PhishGuard Training</h1>", unsafe_allow_html=True)
    
    with col2:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.session_state.active_scenario = None
            st.session_state.show_feedback = False
            st.rerun()
    
    with col3:
        if st.button("🤖 AI Chat", key="nav_ai_chat", use_container_width=True):
            st.session_state.current_page = 'ai_chat'
            st.rerun()
    
    with col4:
        if st.button("📊 Stats", key="nav_stats", use_container_width=True):
            st.session_state.current_page = 'stats'
            st.session_state.active_scenario = None
            st.session_state.show_feedback = False
            st.rerun()

def show_stats_bar():
    """Display statistics"""
    stats = get_player_stats()
    
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">SKILL RATING</div>
            <div class="stat-value">{int(stats.get('current_skill_rating', 500))}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">COMPLETED</div>
            <div class="stat-value">{stats.get('total_scenarios_resolved', 0)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">ACCURACY</div>
            <div class="stat-value">{int(stats.get('accuracy_percentage', 0))}%</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">CORRECT</div>
            <div class="stat-value">{stats.get('correctly_identified_phish', 0)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_home_page():
    """Home page"""
    st.markdown("""
    <div class="content-card">
        <h1>Welcome to PhishGuard Training</h1>
        <p>Master the art of detecting phishing attacks through AI-powered, realistic scenarios. 
        Learn to recognize threats in emails and text messages that target Indian users.</p>
        <br>
        <p><strong>What you'll learn:</strong></p>
        <ul>
            <li>Identify fraudulent emails from fake banks and services</li>
            <li>Detect SMS scams and phishing attempts</li>
            <li>Recognize social engineering tactics</li>
            <li>Protect yourself and others from cyber threats</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h2>📧 Email Phishing Training</h2>
            <p>Learn to identify fraudulent emails through realistic Gmail-style scenarios.</p>
            <br>
            <ul>
                <li>Bank account alerts</li>
                <li>Delivery notifications</li>
                <li>Government notices</li>
                <li>Account verification requests</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📧 Start Email Training", key="start_email", use_container_width=True):
            st.session_state.current_page = 'email_training'
            st.session_state.active_scenario = None
            st.session_state.show_feedback = False
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h2>📱 SMS Phishing Training</h2>
            <p>Practice detecting malicious text messages through realistic iMessage-style scenarios.</p>
            <br>
            <ul>
                <li>Payment alerts</li>
                <li>OTP requests</li>
                <li>Delivery updates</li>
                <li>Account warnings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📱 Start SMS Training", key="start_sms", use_container_width=True):
            st.session_state.current_page = 'sms_training'
            st.session_state.active_scenario = None
            st.session_state.show_feedback = False
            st.rerun()

def render_gmail_ui(scenario):
    """Render Gmail-style email"""
    content = scenario.get('display_content', scenario.get('content', ''))
    
    # Parse email parts
    from_match = re.search(r'From:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    
    from_line = from_match.group(1).strip() if from_match else "Unknown Sender"
    subject = subject_match.group(1).strip() if subject_match else "No Subject"
    
    # Extract email address
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', from_line)
    email_address = email_match.group(0) if email_match else "unknown@example.com"
    
    # Get sender name (before email or bracket)
    sender_name = re.sub(r'[\[\(<].*?[\]\)>]', '', from_line).strip()
    if not sender_name or '@' in sender_name:
        sender_name = email_address.split('@')[0].title()
    
    # Get body (remove From and Subject lines)
    body = content
    body = re.sub(r'From:.*?\n', '', body, flags=re.IGNORECASE)
    body = re.sub(r'Subject:.*?\n', '', body, flags=re.IGNORECASE)
    body = body.strip()
    
    # Get initials for avatar
    initials = ''.join([word[0].upper() for word in sender_name.split()[:2]])
    
    st.markdown(f"""
    <div class="gmail-container">
        <div class="gmail-header">
            <div class="gmail-subject">{html.escape(subject)}</div>
            <div class="gmail-from">
                <div class="gmail-avatar">{initials}</div>
                <div class="gmail-sender">
                    <div class="gmail-sender-name">{html.escape(sender_name)}</div>
                    <div class="gmail-sender-email">&lt;{html.escape(email_address)}&gt;</div>
                </div>
            </div>
        </div>
        <div class="gmail-body">{html.escape(body)}</div>
        <div class="gmail-footer">
            <div class="gmail-action-btn">↩ Reply</div>
            <div class="gmail-action-btn">↪ Forward</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_imessage_ui(scenario):
    """Render iMessage-style SMS"""
    content = scenario.get('display_content', scenario.get('content', ''))
    
    # Clean quotes and extra formatting
    message_text = content.strip().strip('"\'')
    
    st.markdown(f"""
    <div class="imessage-container">
        <div class="imessage-header">
            <div class="imessage-contact">Unknown</div>
        </div>
        <div class="imessage-messages">
            <div class="imessage-bubble">
                <div class="imessage-bubble-content">{html.escape(message_text)}</div>
                <div class="imessage-time">10:30 AM</div>
            </div>
        </div>
        <div class="imessage-keyboard">
            <div class="imessage-input">iMessage</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_training_page(scenario_type: str):
    """Training page with realistic UI"""
    if st.button("⬅ Back to Home", key="back_home"):
        st.session_state.current_page = 'home'
        st.session_state.active_scenario = None
        st.session_state.show_feedback = False
        st.rerun()
    
    type_name = "Email" if scenario_type == "email" else "SMS"
    st.markdown(f"""
    <div class="content-card">
        <h2>{'📧' if scenario_type == 'email' else '📱'} {type_name} Phishing Training</h2>
        <p>Analyze realistic scenarios and identify potential threats. Use the AI Assistant if you need help.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Difficulty selection
    st.markdown("<h3 style='color: white !important;'>Select Difficulty Level</h3>", unsafe_allow_html=True)
    
    difficulty_options = {
        'beginner': '🟢 Beginner - Obvious red flags',
        'easy': '🔵 Easy - Multiple clues',
        'medium': '🟡 Medium - Subtle indicators',
        'hard': '🟠 Hard - Challenging to detect',
        'expert': '🔴 Expert - Nearly perfect scams'
    }
    
    selected = st.radio(
        "Choose difficulty:",
        options=list(difficulty_options.keys()),
        format_func=lambda x: difficulty_options[x],
        horizontal=True,
        key=f"difficulty_{scenario_type}"
    )
    
    st.session_state.selected_difficulty = selected
    
    # Generate button
    if st.button("🎲 Generate New Scenario", key="generate", use_container_width=True):
        with st.spinner("Generating scenario..."):
            scenario = generate_scenario(scenario_type, st.session_state.selected_difficulty)
            if scenario:
                st.session_state.active_scenario = scenario
                st.session_state.show_feedback = False
                st.session_state.show_ai_chat = False
                st.session_state.chat_messages = []
                st.rerun()
    
    # Display scenario
    if st.session_state.active_scenario:
        scenario = st.session_state.active_scenario
        
        # Render appropriate UI
        if scenario_type == 'email':
            render_gmail_ui(scenario)
        else:
            render_imessage_ui(scenario)
        
        # Show feedback if available
        if st.session_state.show_feedback:
            if st.session_state.feedback_type == 'success':
                st.markdown(f"""
                <div class="feedback-success">
                    ✅ {html.escape(st.session_state.feedback_message)}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="feedback-error">
                    ❌ {html.escape(st.session_state.feedback_message)}
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("➡ Next Scenario", key="next_scenario", use_container_width=True):
                st.session_state.active_scenario = None
                st.session_state.show_feedback = False
                st.rerun()
        else:
            # Answer options
            st.markdown("<h3 style='color: white !important; margin-top: 1rem;'>What would you do?</h3>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🚨 Report as Phishing", key="report", use_container_width=True):
                    handle_answer('reported_phish')
            
            with col2:
                if st.button("✅ It's Safe", key="safe", use_container_width=True):
                    handle_answer('deleted_safe')
            
            with col3:
                if st.button("👁 Ignore", key="ignore", use_container_width=True):
                    handle_answer('ignored')
        
        # Always show AI Chatbot (no toggle needed)
        st.markdown("<br>", unsafe_allow_html=True)
        show_ai_chatbot(scenario)

def handle_answer(action: str):
    """Process user's answer with detailed explanation"""
    if st.session_state.active_scenario:
        result = resolve_scenario(st.session_state.active_scenario['scenario_id'], action)
        if result:
            st.session_state.show_feedback = True
            
            # Get full scenario content for detailed explanation
            full_content = st.session_state.active_scenario.get('full_content', '')
            
            # Build detailed feedback message
            base_message = result.get('message', '')
            
            if not result.get('correct'):
                # For incorrect answers, add educational explanation
                explanation = "\n\n**Why this is wrong:**\n\n"
                
                # Extract red flags from full content if available
                if 'Red flag' in full_content or 'red flag' in full_content.lower():
                    # Try to extract the red flags section
                    parts = full_content.split('Red flag')
                    if len(parts) > 1:
                        red_flags_section = 'Red flag' + parts[1].split('\n\n')[0]
                        explanation += red_flags_section + "\n\n"
                
                explanation += "**What to look for:**\n"
                explanation += "• Check the sender's email address carefully for misspellings\n"
                explanation += "• Look for grammar and spelling errors\n"
                explanation += "• Be suspicious of urgent or threatening language\n"
                explanation += "• Verify links before clicking (hover to see actual URL)\n"
                explanation += "• Question requests for personal information\n"
                explanation += "• Contact the company directly if unsure\n\n"
                explanation += "**Remember:** Legitimate companies will never ask for sensitive information via email/SMS or create artificial urgency."
                
                st.session_state.feedback_message = base_message + explanation
            else:
                # For correct answers, add reinforcement
                explanation = "\n\n**Why this is correct:**\n\n"
                explanation += "You correctly identified the warning signs! "
                
                if 'Red flag' in full_content or 'red flag' in full_content.lower():
                    parts = full_content.split('Red flag')
                    if len(parts) > 1:
                        red_flags_section = 'Red flag' + parts[1].split('\n\n')[0]
                        explanation += "Here's what made it suspicious:\n\n" + red_flags_section
                
                st.session_state.feedback_message = base_message + explanation
            
            st.session_state.feedback_type = 'success' if result.get('correct') else 'error'
            st.rerun()

def show_ai_chatbot(scenario):
    """Display AI chatbot for scenario analysis with quick questions"""
    st.markdown("""
    <div class="content-card">
        <h3>🤖 AI Security Assistant (Scenario-Specific)</h3>
        <p>Ask me questions about this specific scenario. I can help you identify potential threats.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get scenario content (try full_content first, fall back to content)
    scenario_content = scenario.get('full_content', scenario.get('content', ''))
    
    # Debug: show if we have content
    if not scenario_content:
        st.warning("⚠️ No scenario content available for AI analysis.")
        return
    
    # Pre-made quick questions
    st.markdown("**Quick Questions:**")
    cols = st.columns(2)
    
    quick_questions = [
        "Is the sender legitimate?",
        "What are the red flags here?",
        "Should I click any links?",
        "Is this message urgent or a scam?"
    ]
    
    for idx, question in enumerate(quick_questions):
        col = cols[idx % 2]
        if col.button(f"❓ {question}", key=f"quick_q_{idx}", use_container_width=True):
            # Add to chat
            st.session_state.chat_messages.append({
                'role': 'user',
                'content': question
            })
            
            with st.spinner("AI is analyzing..."):
                try:
                    response = ask_ai_about_scenario(question, scenario_content)
                    
                    if response and isinstance(response, dict) and 'answer' in response:
                        answer = response['answer']
                        st.session_state.chat_messages.append({
                            'role': 'assistant',
                            'content': answer
                        })
                    else:
                        error_msg = f'Sorry, I could not analyze this scenario. Response: {response}'
                        st.session_state.chat_messages.append({
                            'role': 'assistant',
                            'content': error_msg
                        })
                except Exception as e:
                    st.session_state.chat_messages.append({
                        'role': 'assistant',
                        'content': f'Error: {str(e)}'
                    })
            
            st.rerun()
    
    st.markdown("---")
    
    # Display chat history
    for msg in st.session_state.chat_messages:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {html.escape(msg['content'])}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-message">
                <strong>🤖 AI:</strong> {html.escape(msg['content'])}
            </div>
            """, unsafe_allow_html=True)
    
    # Input for new question
    user_question = st.text_input(
        "Or ask your own question:",
        placeholder="e.g., Can you help me analyze this? Is this safe?",
        key="ai_question"
    )
    
    if st.button("🚀 Ask", key="ask_ai"):
        if user_question:
            st.session_state.chat_messages.append({
                'role': 'user',
                'content': user_question
            })
            
            with st.spinner("AI is analyzing..."):
                try:
                    response = ask_ai_about_scenario(user_question, scenario_content)
                    
                    if response and isinstance(response, dict) and 'answer' in response:
                        answer = response['answer']
                        st.session_state.chat_messages.append({
                            'role': 'assistant',
                            'content': answer
                        })
                    else:
                        error_msg = f'Sorry, I could not analyze this scenario. Response: {response}'
                        st.session_state.chat_messages.append({
                            'role': 'assistant',
                            'content': error_msg
                        })
                except Exception as e:
                    st.session_state.chat_messages.append({
                        'role': 'assistant',
                        'content': f'Error: {str(e)}'
                    })
            
            st.rerun()

def show_stats_page():
    """Enhanced statistics page with detailed insights"""
    if st.button("⬅ Back to Home", key="back_from_stats"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    stats = get_player_stats()
    total = stats.get('total_scenarios_resolved', 0)
    correct = stats.get('correctly_identified_phish', 0)
    accuracy = stats.get('accuracy_percentage', 0)
    skill = stats.get('current_skill_rating', 500)
    
    st.markdown("""
    <div class="content-card">
        <h1>📊 Your Progress & Statistics</h1>
        <p>Track your performance and improve your phishing detection skills.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed metrics
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance Breakdown
        st.markdown(f"""
        <div class="content-card">
            <h2>📈 Performance Breakdown</h2>
            <p><strong>Total Scenarios Completed:</strong> {total}</p>
            <p><strong>Correctly Identified Phishing:</strong> {correct}</p>
            <p><strong>Incorrectly Identified:</strong> {total - correct}</p>
            <p><strong>Accuracy Rate:</strong> {int(accuracy)}%</p>
            <p><strong>Current Skill Rating:</strong> {int(skill)}</p>
            <br>
            <h3>🎯 What This Means</h3>
            <p>{'🟢 <strong>Excellent!</strong> You have strong phishing detection skills.' if accuracy >= 80 else '🟡 <strong>Good progress!</strong> Keep practicing to improve.' if accuracy >= 60 else '🔴 <strong>Needs work.</strong> Use the AI Assistant to learn more.'}</p>
            <p><strong>Skill Level:</strong> {'🏆 Expert' if skill >= 700 else '⭐ Advanced' if skill >= 600 else '📈 Intermediate' if skill >= 550 else '🌱 Beginner'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Insights and recommendations
        st.markdown(f"""
        <div class="content-card">
            <h2>💡 Personalized Insights</h2>
            <h3>Your Strengths:</h3>
            <ul>
                <li>{'✅ Consistent practice - Keep it up!' if total > 10 else '⚠️ More practice needed for better insights'}</li>
                <li>{'✅ High accuracy shows good awareness' if accuracy >= 70 else '⚠️ Focus on identifying red flags'}</li>
            </ul>
            
            <h3>Areas to Improve:</h3>
            <ul>
                <li>{'Try harder difficulty levels' if accuracy >= 80 else 'Practice on beginner/easy levels first'}</li>
                <li>Use the AI Assistant to understand red flags better</li>
                <li>Pay close attention to sender email addresses</li>
                <li>Look for grammar and spelling mistakes</li>
                <li>Be skeptical of urgent or threatening messages</li>
            </ul>
            
            <h3>🎯 Next Steps:</h3>
            <p><strong>{'Try Expert difficulty to challenge yourself!' if skill >= 650 else 'Try Medium difficulty to level up!' if skill >= 550 else 'Complete 10 more scenarios to build confidence!'}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress chart placeholder
    st.markdown("""
    <div class="content-card">
        <h2>📊 Your Progress Over Time</h2>
        <p><em>Complete more scenarios to see your improvement trend!</em></p>
    </div>
    """, unsafe_allow_html=True)

def show_ai_chat_page():
    """General AI assistant page with RAG"""
    if st.button("⬅ Back to Home", key="back_from_ai_chat"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("""
    <div class="content-card">
        <h1>🤖 AI Security Expert</h1>
        <p>Ask me anything about phishing, cybersecurity, or online safety. I have access to comprehensive security knowledge!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize general chat if not exists
    if 'general_chat_messages' not in st.session_state:
        st.session_state.general_chat_messages = []
    
    # Display chat history
    for msg in st.session_state.general_chat_messages:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div class="content-card" style="background: #f0f9ff; border-left: 4px solid #0891b2;">
                <p><strong>You:</strong> {html.escape(msg['content'])}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="content-card" style="background: white; border-left: 4px solid #10b981;">
                <p><strong>🤖 AI Expert:</strong> {html.escape(msg['content'])}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick topic buttons
    st.markdown("**Quick Topics:**")
    cols = st.columns(3)
    
    quick_topics = [
        "What is phishing?",
        "How to identify fake emails?",
        "What are common scam tactics?",
        "How to protect my data?",
        "What is two-factor authentication?",
        "How to spot fake websites?"
    ]
    
    for idx, topic in enumerate(quick_topics):
        col = cols[idx % 3]
        if col.button(f"💡 {topic}", key=f"topic_{idx}", use_container_width=True):
            st.session_state.general_chat_messages.append({
                'role': 'user',
                'content': topic
            })
            
            with st.spinner("AI Expert is thinking..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/guardian/query",
                        json={
                            "query": topic,
                            "player_id": st.session_state.player_id
                        },
                        timeout=15
                    )
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get('answer', 'Sorry, I could not find an answer.')
                        st.session_state.general_chat_messages.append({
                            'role': 'assistant',
                            'content': answer
                        })
                except Exception as e:
                    st.session_state.general_chat_messages.append({
                        'role': 'assistant',
                        'content': f'Sorry, there was an error: {str(e)}'
                    })
            
            st.rerun()
    
    st.markdown("---")
    
    # Custom question input
    user_question = st.text_area(
        "Ask your question:",
        placeholder="e.g., How can I tell if a link is safe to click?",
        key="general_ai_question",
        height=100
    )
    
    if st.button("🚀 Ask AI Expert", type="primary", key="ask_general_ai"):
        if user_question:
            st.session_state.general_chat_messages.append({
                'role': 'user',
                'content': user_question
            })
            
            with st.spinner("AI Expert is analyzing your question..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/guardian/query",
                        json={
                            "query": user_question,
                            "player_id": st.session_state.player_id
                        },
                        timeout=15
                    )
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get('answer', 'Sorry, I could not find an answer.')
                        st.session_state.general_chat_messages.append({
                            'role': 'assistant',
                            'content': answer
                        })
                except Exception as e:
                    st.session_state.general_chat_messages.append({
                        'role': 'assistant',
                        'content': f'Sorry, there was an error: {str(e)}'
                    })
            
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", key="clear_general_chat"):
        st.session_state.general_chat_messages = []
        st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application"""
    show_header()
    st.markdown("<br>", unsafe_allow_html=True)
    show_stats_bar()
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Route to pages
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'email_training':
        show_training_page('email')
    elif st.session_state.current_page == 'sms_training':
        show_training_page('sms')
    elif st.session_state.current_page == 'ai_chat':
        show_ai_chat_page()
    elif st.session_state.current_page == 'stats':
        show_stats_page()

if __name__ == "__main__":
    main()
