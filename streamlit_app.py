"""
SocialProof - Cybersecurity Training Platform
Streamlit Application with Professional UI
"""

import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="SocialProof - Cybersecurity Training",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"
PLAYER_ID = 1  # Hardcoded for now

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #0ea5e9;
        --background-color: #0f172a;
        --secondary-background: #1e293b;
        --text-color: #f8fafc;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom card styling */
    .stCard {
        background-color: var(--secondary-background);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Email card styling */
    .email-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 4px solid #0ea5e9;
        padding: 16px;
        margin: 8px 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .email-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
    }
    
    .email-card.unread {
        border-left: 4px solid #22c55e;
        font-weight: 600;
    }
    
    .email-card.phishing {
        border-left: 4px solid #ef4444;
    }
    
    /* SMS bubble styling */
    .sms-bubble {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 18px;
        margin: 8px 0;
        word-wrap: break-word;
    }
    
    .sms-bubble.received {
        background-color: #374151;
        color: white;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }
    
    .sms-bubble.sent {
        background-color: #0ea5e9;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    /* Stat card styling */
    .stat-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value {
        font-size: 48px;
        font-weight: bold;
        color: #0ea5e9;
    }
    
    .stat-label {
        font-size: 14px;
        color: #94a3b8;
        margin-top: 8px;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
    
    /* Gmail-like header */
    .gmail-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 16px 24px;
        border-bottom: 1px solid #334155;
        margin-bottom: 20px;
    }
    
    /* WhatsApp-like header */
    .whatsapp-header {
        background: #075e54;
        color: white;
        padding: 16px 24px;
        border-radius: 12px 12px 0 0;
        margin-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_email' not in st.session_state:
    st.session_state.selected_email = None
if 'selected_sms' not in st.session_state:
    st.session_state.selected_sms = None

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🛡️ SocialProof")
    st.markdown("**Cybersecurity Training Platform**")
    st.markdown("---")
    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = 'home'
    
    if st.button("📧 Email Simulation", use_container_width=True):
        st.session_state.page = 'email'
    
    if st.button("💬 SMS Simulation", use_container_width=True):
        st.session_state.page = 'sms'
    
    if st.button("📊 My Statistics", use_container_width=True):
        st.session_state.page = 'stats'
    
    if st.button("🤖 AI Guardian", use_container_width=True):
        st.session_state.page = 'guardian'
    
    st.markdown("---")
    st.markdown("**Training Mode Active** ✅")
    st.markdown(f"Player ID: {PLAYER_ID}")

# ============================================================================
# HOME PAGE
# ============================================================================
def show_home_page():
    st.title("🛡️ Welcome to SocialProof")
    st.markdown("### Master Cybersecurity Through Interactive Simulations")
    
    st.markdown("""
    Train yourself to identify and defend against phishing, smishing, and social engineering 
    attacks in a safe, controlled environment.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 48px;">📧</div>
            <h3>Email Phishing</h3>
            <p style="color: #94a3b8;">Detect fraudulent emails and protect yourself from credential theft attacks.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Email Training", key="email_btn", use_container_width=True):
            st.session_state.page = 'email'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 48px;">💬</div>
            <h3>SMS Smishing</h3>
            <p style="color: #94a3b8;">Master SMS-based attack recognition and keep your devices secure.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start SMS Training", key="sms_btn", use_container_width=True):
            st.session_state.page = 'sms'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 48px;">📊</div>
            <h3>Statistics</h3>
            <p style="color: #94a3b8;">Track your progress and performance across all training scenarios.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View My Stats", key="stats_btn", use_container_width=True):
            st.session_state.page = 'stats'
            st.rerun()

# ============================================================================
# EMAIL SIMULATION PAGE (Gmail-like)
# ============================================================================
def show_email_page():
    st.markdown('<div class="gmail-header"><h2>📧 Email Client - Phishing Detection Training</h2></div>', unsafe_allow_html=True)
    
    # Fetch scenarios
    try:
        response = requests.get(f"{API_BASE_URL}/players/{PLAYER_ID}/scenarios")
        scenarios = response.json()
        
        # Transform to email format
        emails = []
        for scenario in scenarios:
            if scenario['scenario_type'] == 'email':
                content = scenario['content']
                emails.append({
                    'id': scenario['id'],
                    'sender': extract_sender(content),
                    'subject': extract_subject(content),
                    'snippet': extract_snippet(content),
                    'content': content,
                    'timestamp': scenario['created_at'],
                    'is_phishing': True,
                    'difficulty': scenario['difficulty_level']
                })
        
        if not emails:
            st.info("🎉 Inbox Zero! You've completed all scenarios. New ones will be added soon.")
            return
        
        # Layout: Inbox list (left) | Email detail (right)
        col_inbox, col_detail = st.columns([1, 2])
        
        with col_inbox:
            st.markdown("### 📥 Inbox")
            st.markdown(f"**{len(emails)} messages**")
            
            for email in emails:
                is_selected = st.session_state.selected_email and st.session_state.selected_email['id'] == email['id']
                
                card_class = "email-card"
                if is_selected:
                    card_class += " selected"
                
                if st.button(
                    f"**{email['sender']}**\n\n{email['subject']}\n\n{email['snippet'][:60]}...",
                    key=f"email_{email['id']}",
                    use_container_width=True
                ):
                    st.session_state.selected_email = email
                    st.rerun()
        
        with col_detail:
            if st.session_state.selected_email:
                email = st.session_state.selected_email
                
                st.markdown(f"### {email['subject']}")
                st.markdown(f"**From:** {email['sender']}")
                st.markdown(f"**Date:** {datetime.fromisoformat(email['timestamp'].replace('Z', '+00:00')).strftime('%B %d, %Y at %I:%M %p')}")
                st.markdown("---")
                
                # Email content
                st.markdown(email['content'], unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Action buttons
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.button("🚨 Report Phishing", key="report_phish", use_container_width=True, type="primary"):
                        handle_email_action(email['id'], 'reported_phish')
                        st.session_state.selected_email = None
                        st.rerun()
                
                with col2:
                    if st.button("✅ Mark Safe", key="mark_safe", use_container_width=True):
                        handle_email_action(email['id'], 'deleted_safe')
                        st.session_state.selected_email = None
                        st.rerun()
            else:
                st.info("👈 Select an email from the inbox to view details")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Please ensure it's running on http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"❌ Error loading emails: {str(e)}")

# ============================================================================
# SMS SIMULATION PAGE (WhatsApp-like)
# ============================================================================
def show_sms_page():
    st.markdown('<div class="whatsapp-header"><h2>💬 Messages - Smishing Detection Training</h2></div>', unsafe_allow_html=True)
    
    # Fetch SMS scenarios
    try:
        response = requests.get(f"{API_BASE_URL}/players/{PLAYER_ID}/scenarios")
        scenarios = response.json()
        
        # Filter SMS type scenarios
        sms_scenarios = [s for s in scenarios if s['scenario_type'] in ['sms', 'smishing']]
        
        if not sms_scenarios:
            st.info("🎉 No messages! You've completed all scenarios.")
            return
        
        # Layout: Conversations (left) | Chat (right)
        col_list, col_chat = st.columns([1, 2])
        
        with col_list:
            st.markdown("### 💬 Conversations")
            
            for sms in sms_scenarios:
                sender = extract_sender(sms['content'])
                snippet = extract_snippet(sms['content'])
                
                if st.button(
                    f"**{sender}**\n\n{snippet[:50]}...",
                    key=f"sms_{sms['id']}",
                    use_container_width=True
                ):
                    st.session_state.selected_sms = sms
                    st.rerun()
        
        with col_chat:
            if st.session_state.selected_sms:
                sms = st.session_state.selected_sms
                sender = extract_sender(sms['content'])
                
                # Chat header
                st.markdown(f"**👤 {sender}**")
                st.markdown("---")
                
                # Chat messages
                st.markdown(f"""
                <div class="sms-bubble received">
                    {sms['content']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Action buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🚨 Report as Scam", key="report_sms", use_container_width=True, type="primary"):
                        handle_email_action(sms['id'], 'reported_phish')
                        st.session_state.selected_sms = None
                        st.rerun()
                
                with col2:
                    if st.button("✅ Mark as Safe", key="safe_sms", use_container_width=True):
                        handle_email_action(sms['id'], 'deleted_safe')
                        st.session_state.selected_sms = None
                        st.rerun()
            else:
                st.info("👈 Select a conversation to view messages")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Please ensure it's running on http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"❌ Error loading messages: {str(e)}")

# ============================================================================
# STATISTICS PAGE
# ============================================================================
def show_stats_page():
    st.title("📊 Your Performance Statistics")
    
    try:
        response = requests.get(f"{API_BASE_URL}/players/{PLAYER_ID}/stats")
        stats = response.json()
        
        # Top metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{int(stats['current_skill_rating'])}</div>
                <div class="stat-label">Skill Rating</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{stats['accuracy_percentage']:.1f}%</div>
                <div class="stat-label">Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{stats['total_scenarios_resolved']}</div>
                <div class="stat-label">Scenarios Completed</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detailed stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Phishing Detection")
            
            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=['Correctly Identified', 'Missed Threats'],
                values=[stats['correctly_identified_phish'], stats['missed_phish']],
                marker=dict(colors=['#22c55e', '#ef4444']),
                hole=0.4
            )])
            fig.update_layout(
                showlegend=True,
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric("Correctly Identified", stats['correctly_identified_phish'])
            st.metric("Missed Threats", stats['missed_phish'])
        
        with col2:
            st.markdown("### ⚠️ Error Analysis")
            
            # Create bar chart
            fig = go.Figure(data=[
                go.Bar(
                    x=['False Positives'],
                    y=[stats['incorrectly_reported_safe']],
                    marker=dict(color='#eab308')
                )
            ])
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric("False Positives", stats['incorrectly_reported_safe'])
        
        st.markdown("---")
        
        # Insights
        st.markdown("### 💡 Performance Insights")
        
        if stats['current_skill_rating'] >= 600:
            st.success("🌟 Excellent! You're performing at an advanced level.")
        elif stats['current_skill_rating'] >= 500:
            st.info("📈 Good progress! Keep training to reach expert level.")
        else:
            st.warning("💪 You're learning! More practice will improve your skills.")
        
        if stats['accuracy_percentage'] >= 80:
            st.success("🎯 Outstanding accuracy! You're consistently making correct decisions.")
        elif stats['accuracy_percentage'] >= 60:
            st.info("👍 Solid performance. Focus on reducing mistakes for even better results.")
        else:
            st.warning("📚 Keep practicing! Review the training tips to improve your accuracy.")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Please ensure it's running on http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"❌ Error loading statistics: {str(e)}")

# ============================================================================
# AI GUARDIAN PAGE
# ============================================================================
def show_guardian_page():
    st.title("🤖 AI Guardian")
    st.markdown("### Your AI-Powered Cybersecurity Assistant")
    
    # Check AI provider status
    try:
        response = requests.get(f"{API_BASE_URL}/ai/provider")
        provider_info = response.json()
        
        if provider_info['status'] == 'active':
            rag_status = "✅ Enabled" if provider_info.get('rag_initialized') else "❌ Not Loaded"
            st.success(f"✅ AI Guardian is active\n\n**Provider:** {provider_info['provider']}\n\n**Model:** {provider_info.get('model_class', 'N/A')}\n\n**RAG System:** {rag_status}")
        else:
            st.warning("⚠️ AI Guardian is not configured")
    except Exception as e:
        st.warning(f"⚠️ Cannot connect to AI service: {str(e)}")
    
    st.markdown("---")
    
    # Query input
    query = st.text_area(
        "Ask a cybersecurity question:",
        placeholder="e.g., What are the red flags in phishing emails? How can I identify a smishing attack?",
        height=120
    )
    
    if st.button("🛡️ Ask Guardian", type="primary", use_container_width=True):
        if query.strip():
            with st.spinner("Guardian is thinking..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/guardian/query",
                        json={"query": query}
                    )
                    answer = response.json()
                    
                    st.markdown("### 📝 Answer")
                    st.markdown(answer['answer'])
                    
                    if answer.get('sources'):
                        st.markdown("---")
                        st.markdown("**📚 Knowledge Sources:**")
                        for source in answer['sources']:
                            st.markdown(f"- {source}")
                    
                    st.caption(f"Powered by {answer['provider']} • {datetime.fromisoformat(answer['timestamp'].replace('Z', '+00:00')).strftime('%B %d, %Y at %I:%M %p')}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend server")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter a question")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def extract_sender(content):
    """Extract sender from email content"""
    import re
    from_match = re.search(r'From:\s*(.+?)(?:\n|<br>)', content, re.IGNORECASE)
    if from_match:
        return from_match.group(1).strip()
    
    email_match = re.search(r'[\w.-]+@[\w.-]+\.\w+', content)
    if email_match:
        return email_match.group(0)
    
    return 'Unknown Sender'

def extract_subject(content):
    """Extract subject line from email content"""
    import re
    subject_match = re.search(r'Subject:\s*(.+?)(?:\n|<br>)', content, re.IGNORECASE)
    if subject_match:
        return subject_match.group(1).strip()
    
    # Fallback: use first line
    first_line = content.split('\n')[0].replace('<', '').replace('>', '').strip()
    return first_line[:50] + ('...' if len(first_line) > 50 else '')

def extract_snippet(content):
    """Extract preview snippet from email body"""
    import re
    # Remove HTML tags
    plain_text = re.sub(r'<[^>]*>', '', content).replace('\n', ' ').strip()
    
    # Skip header lines
    lines = [line for line in plain_text.split('.') if not re.match(r'^(From|To|Subject|Date):', line)]
    
    body_text = ' '.join(lines).strip()
    return body_text[:100] + ('...' if len(body_text) > 100 else '')

def handle_email_action(scenario_id, action):
    """Handle email/SMS action (Report/Delete)"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/scenarios/{scenario_id}/resolve",
            json={"action": action}
        )
        result = response.json()
        
        if result['correct']:
            st.success(f"✅ {result['message']}\n\nScore: +{result['score_change']} points | New Rating: {result['new_skill_rating']:.1f}")
        else:
            st.error(f"❌ {result['message']}\n\nScore: {result['score_change']} points | New Rating: {result['new_skill_rating']:.1f}")
    
    except Exception as e:
        st.error(f"Failed to process action: {str(e)}")

# ============================================================================
# MAIN APP ROUTING
# ============================================================================
def main():
    page = st.session_state.page
    
    if page == 'home':
        show_home_page()
    elif page == 'email':
        show_email_page()
    elif page == 'sms':
        show_sms_page()
    elif page == 'stats':
        show_stats_page()
    elif page == 'guardian':
        show_guardian_page()

if __name__ == "__main__":
    main()
