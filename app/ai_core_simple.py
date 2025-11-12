"""
Simplified AI Core Module for SocialProof
Uses Groq with Llama 3.3 70B for fast AI generation
Includes basic RAG using knowledge base files
"""

import os
from typing import Dict, Any
from pathlib import Path

# Try to import LangChain components
try:
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

# Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Knowledge base path
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent / "knowledge_base"

# Global knowledge base storage (simple RAG)
KNOWLEDGE_BASE = {
    "phishing": "",
    "smishing": "",
    "social_engineering": ""
}

def load_knowledge_base():
    """Load knowledge base files into memory (Simple RAG)"""
    global KNOWLEDGE_BASE
    
    try:
        # Load phishing knowledge
        phishing_file = KNOWLEDGE_BASE_PATH / "phishing.txt"
        if phishing_file.exists():
            with open(phishing_file, 'r') as f:
                KNOWLEDGE_BASE["phishing"] = f.read()
        
        # Load smishing knowledge
        smishing_file = KNOWLEDGE_BASE_PATH / "smishing.txt"
        if smishing_file.exists():
            with open(smishing_file, 'r') as f:
                KNOWLEDGE_BASE["smishing"] = f.read()
        
        # Load social engineering knowledge
        social_file = KNOWLEDGE_BASE_PATH / "social_engineering.txt"
        if social_file.exists():
            with open(social_file, 'r') as f:
                KNOWLEDGE_BASE["social_engineering"] = f.read()
        
        print("✅ Knowledge base loaded successfully!")
        return True
    except Exception as e:
        print(f"⚠️ Error loading knowledge base: {e}")
        return False

# Load knowledge base on module import
load_knowledge_base()

def get_relevant_context(query: str) -> str:
    """
    Simple RAG: Get relevant context from knowledge base
    Returns relevant knowledge snippets based on keywords
    """
    query_lower = query.lower()
    context_parts = []
    
    # Check for phishing-related queries
    if any(word in query_lower for word in ['phishing', 'email', 'suspicious email', 'fake email']):
        if KNOWLEDGE_BASE["phishing"]:
            context_parts.append("=== Phishing Knowledge ===\n" + KNOWLEDGE_BASE["phishing"])
    
    # Check for smishing-related queries
    if any(word in query_lower for word in ['smishing', 'sms', 'text message', 'text', 'message']):
        if KNOWLEDGE_BASE["smishing"]:
            context_parts.append("=== Smishing Knowledge ===\n" + KNOWLEDGE_BASE["smishing"])
    
    # Check for social engineering queries
    if any(word in query_lower for word in ['social engineering', 'manipulation', 'trick', 'scam', 'fraud']):
        if KNOWLEDGE_BASE["social_engineering"]:
            context_parts.append("=== Social Engineering Knowledge ===\n" + KNOWLEDGE_BASE["social_engineering"])
    
    # If no specific match, include all knowledge (fallback)
    if not context_parts:
        context_parts = [
            KNOWLEDGE_BASE["phishing"],
            KNOWLEDGE_BASE["smishing"],
            KNOWLEDGE_BASE["social_engineering"]
        ]
    
    return "\n\n".join(context_parts)

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

try:
    from langchain_groq import ChatGroq
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("⚠️  LangChain not available. AI features disabled.")


def get_llm_client(temperature: float = 0.7):
    """Get the configured LLM client"""
    if not LANGCHAIN_AVAILABLE:
        return None
    
    if LLM_PROVIDER == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        return ChatGroq(
            temperature=temperature,
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile",  # Latest fastest model!
        )
    
    elif LLM_PROVIDER == "google":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=temperature,
        )
    
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")


def generate_advanced_scenario(scenario_type: str, difficulty: str, category: str = None) -> Dict[str, Any]:
    """
    Generate a realistic phishing email scenario using AI
    
    Args:
        difficulty: easy, medium, or hard
    
    Returns:
        Dict with scenario content and metadata
    """
    if not LANGCHAIN_AVAILABLE:
        # Fallback to hardcoded scenarios
        return {
            "content": """From: support@paypa1-secure.com
Subject: Urgent: Your PayPal Account Has Been Limited

Dear Valued Customer,

We have detected unusual activity on your PayPal account. For your security, we have temporarily limited your account access.

To restore full access, please verify your identity immediately by clicking the link below:

https://paypa1-secure-verify.com/account/restore

If you do not verify within 24 hours, your account will be permanently suspended.

Thank you for your prompt attention.

PayPal Security Team""",
            "scenario_type": "phishing",
            "difficulty_level": difficulty,
            "is_phishing": True,
            "hints": ["Check sender email domain", "Urgency tactic", "Suspicious link"]
        }
    
    llm = get_llm_client(temperature=0.8)
    
    difficulty_instructions = {
        "easy": "Make it obvious with spelling errors, suspicious links, and urgent language.",
        "medium": "Make it moderately suspicious with subtle red flags in the email domain and request.",
        "hard": "Make it very convincing, mimicking legitimate company communication closely with only subtle indicators."
    }
    
    system_message = SystemMessage(content="""You are an expert cybersecurity trainer creating realistic phishing email scenarios for educational purposes. 
Your emails should look authentic but contain red flags that trained users can identify.
Always include: From, Subject, and email body with a suspicious link or request.""")
    
    human_message = HumanMessage(content=f"""Create a realistic {difficulty} difficulty phishing email scenario.

Difficulty level: {difficulty_instructions.get(difficulty, difficulty_instructions['medium'])}

Format your response as an email with:
- From: [email address]
- Subject: [subject line]
- [Email body with realistic content]

Make it educational - include red flags but make them appropriately subtle for the difficulty level.""")
    
    try:
        response = llm.invoke([system_message, human_message])
        content = response.content
        
        return {
            "content": content,
            "scenario_type": "phishing",
            "difficulty_level": difficulty,
            "is_phishing": True
        }
    except Exception as e:
        print(f"Error generating scenario: {e}")
        # Fallback
        return {
            "content": f"Error: {str(e)}",
            "scenario_type": "phishing",
            "difficulty_level": difficulty,
            "is_phishing": True
        }


def digital_guardian_query(question: str) -> Dict[str, Any]:
    """
    Digital Guardian - AI-powered cybersecurity assistant with RAG
    Uses knowledge base to provide contextual answers
    
    Args:
        question: User's cybersecurity question
    
    Returns:
        Dict with answer and metadata
    """
    if not LANGCHAIN_AVAILABLE:
        return {
            "answer": "AI features are not available. Please install LangChain dependencies.",
            "provider": "none",
            "sources": []
        }
    
    # RAG: Get relevant context from knowledge base
    context = get_relevant_context(question)
    
    llm = get_llm_client(temperature=0.3)
    
    # Enhanced system message with RAG context
    system_message = SystemMessage(content=f"""You are the Digital Guardian, an expert cybersecurity assistant specializing in:
- Phishing detection and prevention
- Smishing (SMS phishing) awareness
- Social engineering tactics
- Email security best practices
- Online safety and privacy

You have access to the following knowledge base to provide accurate answers:

{context}

Use this knowledge base to provide clear, accurate, and actionable advice in 2-3 paragraphs. 
Be educational and helpful. When relevant, reference specific techniques or red flags from the knowledge base.""")
    
    human_message = HumanMessage(content=question)
    
    try:
        response = llm.invoke([system_message, human_message])
        
        # Determine which sources were used
        sources = []
        if "phishing" in context.lower():
            sources.append("Phishing Knowledge Base")
        if "smishing" in context.lower():
            sources.append("Smishing Knowledge Base")
        if "social engineering" in context.lower():
            sources.append("Social Engineering Knowledge Base")
        
        return {
            "answer": response.content,
            "provider": f"{LLM_PROVIDER} (with RAG)",
            "sources": sources if sources else ["General Knowledge"],
            "timestamp": "2025-11-12T00:00:00Z"
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "provider": LLM_PROVIDER,
            "sources": [],
            "timestamp": "2025-11-11T19:30:00Z"
        }


def generate_scenario_content(scenario_type: str, difficulty: str) -> str:
    """
    Generate scenario content (wrapper for compatibility)
    
    Args:
        scenario_type: Type of scenario (phishing, smishing, etc.)
        difficulty: Difficulty level
    
    Returns:
        Generated content string
    """
    if scenario_type == "phishing":
        result = generate_phishing_scenario(difficulty)
        return result["content"]
    else:
        # Fallback for other types
        return generate_phishing_scenario(difficulty)["content"]


def get_provider_info() -> Dict[str, Any]:
    """Get current AI provider status with RAG info"""
    if not LANGCHAIN_AVAILABLE:
        return {
            "provider": "none",
            "status": "unavailable",
            "model_class": None,
            "rag_initialized": False,
            "error": "LangChain dependencies not installed"
        }
    
    try:
        # Test if we can create a client
        _ = get_llm_client()
        
        # Check if knowledge base is loaded
        rag_ready = any(KNOWLEDGE_BASE.values())
        
        return {
            "provider": LLM_PROVIDER,
            "status": "active",
            "model_class": "llama-3.3-70b-versatile" if LLM_PROVIDER == "groq" else "gemini-1.5-flash",
            "rag_initialized": rag_ready,
            "error": None
        }
    except Exception as e:
        return {
            "provider": LLM_PROVIDER,
            "status": "error",
            "model_class": None,
            "rag_initialized": False,
            "error": str(e)
        }
