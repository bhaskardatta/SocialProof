"""
Advanced AI Core for SocialProof - Enhanced with Variety & Multiple Levels
Generates diverse, dynamic scenarios across multiple categories and difficulty levels
"""

import os
import random
from typing import Dict, Any, List
from pathlib import Path

# Try to import LangChain components
try:
    from langchain_groq import ChatGroq
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

# Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Knowledge base
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent / "knowledge_base"
KNOWLEDGE_BASE = {"phishing": "", "smishing": "", "social_engineering": ""}

# Scenario categories for variety
SCENARIO_CATEGORIES = {
    "email": [
        "banking_alert", "package_delivery", "tax_notice", "prize_winner",
        "account_verification", "password_reset", "invoice_payment",
        "it_support", "executive_request", "charity_donation",
        "job_offer", "refund_notification", "subscription_renewal"
    ],
    "sms": [
        "delivery_update", "bank_alert", "verification_code", "prize_claim",
        "payment_due", "account_locked", "family_emergency", "job_opportunity",
        "package_held", "refund_pending", "subscription_confirm", "tax_refund"
    ]
}

# Difficulty configurations with specific attributes
DIFFICULTY_CONFIGS = {
    "beginner": {
        "red_flags": 5,
        "grammar_errors": 2,
        "urgency_level": "high",
        "suspicious_links": "obvious",
        "description": "Multiple obvious red flags, poor grammar, clear urgency tactics"
    },
    "easy": {
        "red_flags": 4,
        "grammar_errors": 1,
        "urgency_level": "high",
        "suspicious_links": "noticeable",
        "description": "Several red flags, some grammar issues, noticeable urgency"
    },
    "medium": {
        "red_flags": 3,
        "grammar_errors": 0,
        "urgency_level": "medium",
        "suspicious_links": "subtle",
        "description": "Few subtle red flags, proper grammar, moderate urgency"
    },
    "hard": {
        "red_flags": 2,
        "grammar_errors": 0,
        "urgency_level": "low",
        "suspicious_links": "very_subtle",
        "description": "Minimal red flags, professional tone, looks very legitimate"
    },
    "expert": {
        "red_flags": 1,
        "grammar_errors": 0,
        "urgency_level": "none",
        "suspicious_links": "almost_perfect",
        "description": "Nearly perfect mimicry, requires expert knowledge to detect"
    }
}

def load_knowledge_base():
    """Load knowledge base files"""
    global KNOWLEDGE_BASE
    try:
        for kb_type in ["phishing", "smishing", "social_engineering"]:
            file_path = KNOWLEDGE_BASE_PATH / f"{kb_type}.txt"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    KNOWLEDGE_BASE[kb_type] = f.read()
        return True
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return False

load_knowledge_base()

def get_llm_client(temperature: float = 0.7):
    """Get LLM client"""
    if not LANGCHAIN_AVAILABLE:
        raise ImportError("LangChain not available")
    
    if LLM_PROVIDER == "groq":
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
            temperature=temperature
        )
    return None

def generate_diverse_scenario(
    scenario_type: str,
    difficulty: str,
    category: str = None
) -> Dict[str, Any]:
    """
    Generate diverse scenarios with variety across categories and difficulties
    
    Args:
        scenario_type: 'email' or 'sms'
        difficulty: 'beginner', 'easy', 'medium', 'hard', 'expert'
        category: Specific category (auto-selected if None)
    
    Returns:
        Dict with scenario content and metadata
    """
    if not LANGCHAIN_AVAILABLE:
        return _generate_fallback_scenario(scenario_type, difficulty, category)
    
    # Auto-select category for variety
    if category is None:
        available_categories = SCENARIO_CATEGORIES.get(scenario_type, [])
        category = random.choice(available_categories) if available_categories else "general"
    
    llm = get_llm_client(temperature=0.8)  # Higher temp for variety
    
    difficulty_config = DIFFICULTY_CONFIGS.get(difficulty, DIFFICULTY_CONFIGS["medium"])
    
    # Build dynamic, varied prompts based on category
    if scenario_type == "email":
        system_prompt = _get_email_system_prompt(category, difficulty, difficulty_config)
    else:
        system_prompt = _get_sms_system_prompt(category, difficulty, difficulty_config)
    
    human_prompt = _get_human_prompt(scenario_type, category, difficulty, difficulty_config)
    
    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])
        
        return {
            "content": response.content,
            "scenario_type": scenario_type,
            "difficulty": difficulty,
            "category": category,
            "red_flags_count": difficulty_config["red_flags"],
            "is_phishing": True
        }
    except Exception as e:
        print(f"Error generating scenario: {e}")
        return _generate_fallback_scenario(scenario_type, difficulty, category)

def _get_email_system_prompt(category: str, difficulty: str, config: Dict) -> str:
    """Generate varied email system prompts"""
    category_contexts = {
        "banking_alert": "a major bank (Chase, Bank of America, Wells Fargo)",
        "package_delivery": "a shipping company (FedEx, UPS, Amazon, DHL)",
        "tax_notice": "the IRS or tax authority",
        "prize_winner": "a lottery, sweepstakes, or prize organization",
        "account_verification": "a popular online service (PayPal, Amazon, Microsoft)",
        "password_reset": "a tech company (Google, Apple, Microsoft, Facebook)",
        "invoice_payment": "a vendor or service provider",
        "it_support": "internal IT support or tech support",
        "executive_request": "a company executive (CEO, CFO, Manager)",
        "charity_donation": "a charitable organization",
        "job_offer": "a recruiting firm or company HR",
        "refund_notification": "a retailer or service provider",
        "subscription_renewal": "a subscription service (Netflix, Adobe, Microsoft)"
    }
    
    context = category_contexts.get(category, "a legitimate organization")
    
    return f"""You are an expert cybersecurity trainer creating REALISTIC phishing email scenarios for education.

SCENARIO CONTEXT: Create a phishing email impersonating {context}.

DIFFICULTY: {difficulty.upper()} ({config['description']})

REQUIREMENTS:
- Red flags to include: {config['red_flags']}
- Grammar errors: {config['grammar_errors']}
- Urgency level: {config['urgency_level']}
- Link subtlety: {config['suspicious_links']}

CREATIVE VARIETY:
- Use different sender names, email formats, and writing styles
- Vary the hook (fear, urgency, curiosity, greed)
- Change up the call-to-action
- Make each scenario UNIQUE and REALISTIC

Format as actual email with From, Subject, and Body."""

def _get_sms_system_prompt(category: str, difficulty: str, config: Dict) -> str:
    """Generate varied SMS system prompts"""
    category_contexts = {
        "delivery_update": "FedEx, UPS, USPS, or Amazon delivery",
        "bank_alert": "Bank of America, Chase, Wells Fargo, or credit union",
        "verification_code": "Google, Apple, Microsoft, or PayPal verification",
        "prize_claim": "lottery, sweepstakes, or contest winnings",
        "payment_due": "utility company, credit card, or subscription",
        "account_locked": "bank, email provider, or online service",
        "family_emergency": "family member in trouble needing money",
        "job_opportunity": "recruiter or hiring manager",
        "package_held": "customs or delivery service",
        "refund_pending": "IRS, retailer, or insurance company",
        "subscription_confirm": "Netflix, Spotify, or other subscription",
        "tax_refund": "IRS or tax refund service"
    }
    
    context = category_contexts.get(category, "a legitimate service")
    
    return f"""Create a realistic SMISHING (SMS phishing) message for education.

SCENARIO: {context} notification

DIFFICULTY: {difficulty.upper()} ({config['description']})

REQUIREMENTS:
- Red flags: {config['red_flags']}
- Urgency: {config['urgency_level']}
- Link type: {config['suspicious_links']}
- Keep SMS format (short, under 160 chars for basic, up to 300 for complex)

VARIETY ELEMENTS:
- Different phone number formats
- Various URL shorteners or suspicious domains
- Diverse messaging styles
- Unique scenarios each time

Format as SMS text message."""

def _get_human_prompt(scenario_type: str, category: str, difficulty: str, config: Dict) -> str:
    """Generate human prompt for variety"""
    templates = [
        f"Create a {difficulty} difficulty {category} {scenario_type} phishing scenario. Make it unique and educational.",
        f"Generate a realistic {category} {scenario_type} scam at {difficulty} level. Focus on making it believable but detectable.",
        f"Design a {difficulty} level phishing {scenario_type} for {category}. Include exactly {config['red_flags']} red flags.",
        f"Craft a {category} themed {scenario_type} phishing attack ({difficulty} difficulty). Make it different from typical examples."
    ]
    
    return random.choice(templates)

def _generate_fallback_scenario(scenario_type: str, difficulty: str, category: str) -> Dict[str, Any]:
    """Fallback scenarios when AI is unavailable"""
    fallbacks = {
        "email": {
            "beginner": "From: support@paypa1.com\nSubject: URGENT: Account Suspended!\n\nDear User,\n\nYour PayPal account has been LOCKED due to suspicious activity!!!\n\nClick here NOW to verify: http://paypal-verify.tk/login\n\nYou have 24 hours or account will be DELETED FOREVER!\n\nPayPal Security Team",
            "medium": "From: noreply@amazon-security.com\nSubject: Unusual Activity Detected\n\nHello,\n\nWe noticed a login from an unfamiliar device. If this wasn't you, please verify your account:\n\nhttps://amazon-verify.net/account\n\nThank you,\nAmazon Security"
        },
        "sms": {
            "beginner": "FEDEX: Package delivery failed. Reschedule now: http://bit.ly/fedex123 or package will be returned!",
            "medium": "Your Bank of America account was accessed from new device. Verify here: bofa-secure.net/verify"
        }
    }
    
    content = fallbacks.get(scenario_type, {}).get(difficulty, "Error: Scenario generation failed")
    
    return {
        "content": content,
        "scenario_type": scenario_type,
        "difficulty": difficulty,
        "category": category or "fallback",
        "red_flags_count": 3,
        "is_phishing": True
    }

def get_relevant_context(query: str) -> str:
    """Get relevant context from knowledge base for RAG"""
    query_lower = query.lower()
    context_parts = []
    
    if any(word in query_lower for word in ['phishing', 'email']):
        if KNOWLEDGE_BASE["phishing"]:
            context_parts.append(KNOWLEDGE_BASE["phishing"])
    
    if any(word in query_lower for word in ['smishing', 'sms', 'text']):
        if KNOWLEDGE_BASE["smishing"]:
            context_parts.append(KNOWLEDGE_BASE["smishing"])
    
    if any(word in query_lower for word in ['social engineering', 'manipulation', 'scam']):
        if KNOWLEDGE_BASE["social_engineering"]:
            context_parts.append(KNOWLEDGE_BASE["social_engineering"])
    
    if not context_parts:
        context_parts = list(KNOWLEDGE_BASE.values())
    
    return "\n\n".join(filter(None, context_parts))

def digital_guardian_query(question: str) -> Dict[str, Any]:
    """AI Guardian with RAG"""
    if not LANGCHAIN_AVAILABLE:
        return {
            "answer": "AI features unavailable. Please install LangChain.",
            "provider": "none",
            "sources": []
        }
    
    context = get_relevant_context(question)
    llm = get_llm_client(temperature=0.3)
    
    system_message = SystemMessage(content=f"""You are the Digital Guardian, an expert cybersecurity assistant.

KNOWLEDGE BASE:
{context}

Provide clear, actionable advice in 2-3 paragraphs using the knowledge base.""")
    
    human_message = HumanMessage(content=question)
    
    try:
        response = llm.invoke([system_message, human_message])
        
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
            "sources": sources or ["General Knowledge"],
            "timestamp": "2025-11-12T00:00:00Z"
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "provider": LLM_PROVIDER,
            "sources": [],
            "timestamp": "2025-11-12T00:00:00Z"
        }

def generate_scenario_content(scenario_type: str, difficulty: str, category: str = None) -> str:
    """Wrapper for scenario generation - returns content string"""
    result = generate_diverse_scenario(scenario_type, difficulty, category)
    return result["content"]

def get_provider_info() -> Dict[str, Any]:
    """Get AI provider status"""
    if not LANGCHAIN_AVAILABLE:
        return {
            "provider": "none",
            "status": "unavailable",
            "model_class": None,
            "rag_initialized": False,
            "error": "LangChain not installed"
        }
    
    try:
        _ = get_llm_client()
        rag_ready = any(KNOWLEDGE_BASE.values())
        
        return {
            "provider": LLM_PROVIDER,
            "status": "active",
            "model_class": "llama-3.3-70b-versatile",
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
