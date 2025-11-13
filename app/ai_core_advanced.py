"""
Advanced AI Core for SocialProof - Enhanced with Variety & Multiple Levels
Generates diverse, dynamic scenarios across multiple categories and difficulty levels
"""

import os
import random
from pathlib import Path
from typing import Any, Dict

# Try to import LangChain components
try:
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_groq import ChatGroq

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

# Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Knowledge base
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent / "knowledge_base"
KNOWLEDGE_BASE = {"phishing": "", "smishing": "", "social_engineering": ""}

# Scenario categories for variety - INDIA SPECIFIC
SCENARIO_CATEGORIES = {
    "email": [
        "sbi_banking_alert",
        "hdfc_kyc_update",
        "icici_account_verification",
        "axis_bank_security",
        "blue_dart_delivery",
        "delhivery_package",
        "india_post_courier",
        "income_tax_notice",
        "gst_verification",
        "aadhaar_kyc_update",
        "pan_card_verification",
        "upi_refund_pending",
        "paytm_account_issue",
        "phonepe_payment_failed",
        "gpay_verification",
        "flipkart_prize_winner",
        "amazon_india_refund",
        "swiggy_order_issue",
        "zomato_delivery",
        "irctc_booking_confirm",
        "lic_policy_renewal",
        "epfo_pf_update",
        "mtnl_bsnl_bill",
        "reliance_jio_offer",
        "airtel_bill_due",
    ],
    "sms": [
        "upi_payment_failed",
        "bank_account_blocked",
        "aadhaar_expiry_alert",
        "pan_card_deactivate",
        "courier_delivery_fee",
        "otp_verification_scam",
        "lottery_winner_india",
        "electricity_bill_due",
        "gas_subsidy_claim",
        "income_tax_refund",
        "covid_vaccine_slot",
        "passport_appointment",
        "driving_license_renewal",
        "voter_id_update",
        "ration_card_kyc",
        "paytm_kyc_pending",
        "phonepe_account_limit",
        "gpay_cashback_claim",
        "jio_recharge_offer",
        "airtel_sim_block",
    ],
}

# Difficulty configurations with specific attributes
DIFFICULTY_CONFIGS = {
    "beginner": {
        "red_flags": 5,
        "grammar_errors": 2,
        "urgency_level": "high",
        "suspicious_links": "obvious",
        "description": "Multiple obvious red flags, poor grammar, clear urgency tactics",
    },
    "easy": {
        "red_flags": 4,
        "grammar_errors": 1,
        "urgency_level": "high",
        "suspicious_links": "noticeable",
        "description": "Several red flags, some grammar issues, noticeable urgency",
    },
    "medium": {
        "red_flags": 3,
        "grammar_errors": 0,
        "urgency_level": "medium",
        "suspicious_links": "subtle",
        "description": "Few subtle red flags, proper grammar, moderate urgency",
    },
    "hard": {
        "red_flags": 2,
        "grammar_errors": 0,
        "urgency_level": "low",
        "suspicious_links": "very_subtle",
        "description": "Minimal red flags, professional tone, looks very legitimate",
    },
    "expert": {
        "red_flags": 1,
        "grammar_errors": 0,
        "urgency_level": "none",
        "suspicious_links": "almost_perfect",
        "description": "Nearly perfect mimicry, requires expert knowledge to detect",
    },
}


def load_knowledge_base():
    """Load knowledge base files"""
    global KNOWLEDGE_BASE
    try:
        for kb_type in ["phishing", "smishing", "social_engineering"]:
            file_path = KNOWLEDGE_BASE_PATH / f"{kb_type}.txt"
            if file_path.exists():
                with open(file_path, "r") as f:
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
            temperature=temperature,
        )
    return None


def generate_diverse_scenario(
    scenario_type: str, difficulty: str, category: str = None
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
        category = (
            random.choice(available_categories) if available_categories else "general"
        )

    llm = get_llm_client(temperature=0.8)  # Higher temp for variety

    difficulty_config = DIFFICULTY_CONFIGS.get(difficulty, DIFFICULTY_CONFIGS["medium"])

    # Build dynamic, varied prompts based on category
    if scenario_type == "email":
        system_prompt = _get_email_system_prompt(
            category, difficulty, difficulty_config
        )
    else:
        system_prompt = _get_sms_system_prompt(category, difficulty, difficulty_config)

    human_prompt = _get_human_prompt(
        scenario_type, category, difficulty, difficulty_config
    )

    try:
        response = llm.invoke(
            [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
        )

        return {
            "content": response.content,
            "scenario_type": scenario_type,
            "difficulty": difficulty,
            "category": category,
            "red_flags_count": difficulty_config["red_flags"],
            "is_phishing": True,
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
        "subscription_renewal": "a subscription service (Netflix, Adobe, Microsoft)",
    }

    context = category_contexts.get(category, "a legitimate organization")

    return f"""You are creating realistic phishing email scenarios for cybersecurity training.

SCENARIO: Create a phishing email impersonating {context}.

DIFFICULTY: {difficulty.upper()} ({config["description"]})

CRITICAL INSTRUCTION: Return ONLY the email content (From, Subject, Body). DO NOT include any analysis, red flags, grammar errors, or educational notes in the output. The red flags should exist in the content but not be listed separately.

REQUIREMENTS FOR THE EMAIL CONTENT:
- Include {config["red_flags"]} suspicious elements naturally in the email
- Grammar errors: {config["grammar_errors"]}  
- Urgency level: {config["urgency_level"]}
- Link subtlety: {config["suspicious_links"]}

Use Indian context: Indian banks (SBI, HDFC, ICICI, Axis), Indian services (UPI, Paytm, PhonePe), Indian cities, rupee amounts (₹), +91 phone numbers, .in domains.

Make it REALISTIC - something an Indian person would actually receive.

OUTPUT FORMAT (ONLY THIS, NOTHING ELSE):
From: [sender name and email]
Subject: [subject line]

[Email body text]"""


def _get_sms_system_prompt(category: str, difficulty: str, config: Dict) -> str:
    """Generate SMS prompts - INDIA SPECIFIC"""
    category_contexts = {
        "upi_payment_failed": "UPI payment failure",
        "bank_account_blocked": "Indian bank account alert",
        "aadhaar_expiry_alert": "Aadhaar update notification",
        "pan_card_deactivate": "PAN card alert",
        "courier_delivery_fee": "courier delivery notification",
        "otp_verification_scam": "OTP verification message",
        "lottery_winner_india": "lottery/KBC winner alert",
        "electricity_bill_due": "electricity bill payment",
        "gas_subsidy_claim": "LPG subsidy notification",
        "income_tax_refund": "tax refund alert",
        "paytm_kyc_pending": "Paytm KYC alert",
        "phonepe_account_limit": "PhonePe notification",
        "gpay_cashback_claim": "Google Pay offer",
        "jio_recharge_offer": "Jio recharge offer",
        "airtel_sim_block": "Airtel SIM alert",
    }

    context = category_contexts.get(category, "a service notification")

    return f"""Create a realistic SMS phishing message targeting Indian users.

SCENARIO: {context}

DIFFICULTY: {difficulty.upper()} ({config["description"]})

CRITICAL INSTRUCTION: Return ONLY the SMS text message. DO NOT include any analysis, red flags list, or educational notes.

REQUIREMENTS FOR THE SMS:
- Red flags: {config["red_flags"]} (built into the message, not listed)
- Urgency: {config["urgency_level"]}
- Link type: {config["suspicious_links"]}

Use Indian context: +91 numbers, Indian banks, UPI, Aadhaar, PAN, Indian companies, rupees (Rs./₹), Indian sender IDs.

Keep it short (typical SMS length). Make it realistic to what Indians receive.

OUTPUT FORMAT (ONLY THE SMS TEXT, NOTHING ELSE):
[SMS message text]"""


def _get_human_prompt(
    scenario_type: str, category: str, difficulty: str, config: Dict
) -> str:
    """Generate human prompt for variety"""
    templates = [
        f"Create a {difficulty} difficulty {category} {scenario_type} phishing scenario targeting Indian users.",
        f"Generate a realistic {category} {scenario_type} scam at {difficulty} level for Indian audience.",
        f"Design a {difficulty} level phishing {scenario_type} for {category}. Include exactly {config['red_flags']} red flags.",
        f"Craft a {category} themed {scenario_type} phishing attack ({difficulty} difficulty). Make it different from typical examples.",
    ]

    return random.choice(templates)


def _generate_fallback_scenario(
    scenario_type: str, difficulty: str, category: str
) -> Dict[str, Any]:
    """Fallback scenarios when AI is unavailable"""
    fallbacks = {
        "email": {
            "beginner": "From: support@paypa1.com\nSubject: URGENT: Account Suspended!\n\nDear User,\n\nYour PayPal account has been LOCKED due to suspicious activity!!!\n\nClick here NOW to verify: http://paypal-verify.tk/login\n\nYou have 24 hours or account will be DELETED FOREVER!\n\nPayPal Security Team",
            "medium": "From: noreply@amazon-security.com\nSubject: Unusual Activity Detected\n\nHello,\n\nWe noticed a login from an unfamiliar device. If this wasn't you, please verify your account:\n\nhttps://amazon-verify.net/account\n\nThank you,\nAmazon Security",
        },
        "sms": {
            "beginner": "FEDEX: Package delivery failed. Reschedule now: http://bit.ly/fedex123 or package will be returned!",
            "medium": "Your Bank of America account was accessed from new device. Verify here: bofa-secure.net/verify",
        },
    }

    content = fallbacks.get(scenario_type, {}).get(
        difficulty, "Error: Scenario generation failed"
    )

    return {
        "content": content,
        "scenario_type": scenario_type,
        "difficulty": difficulty,
        "category": category or "fallback",
        "red_flags_count": 3,
        "is_phishing": True,
    }


def get_relevant_context(query: str) -> str:
    """Get relevant context from knowledge base for RAG"""
    query_lower = query.lower()
    context_parts = []

    if any(word in query_lower for word in ["phishing", "email"]):
        if KNOWLEDGE_BASE["phishing"]:
            context_parts.append(KNOWLEDGE_BASE["phishing"])

    if any(word in query_lower for word in ["smishing", "sms", "text"]):
        if KNOWLEDGE_BASE["smishing"]:
            context_parts.append(KNOWLEDGE_BASE["smishing"])

    if any(
        word in query_lower for word in ["social engineering", "manipulation", "scam"]
    ):
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
            "sources": [],
        }

    context = get_relevant_context(question)
    llm = get_llm_client(temperature=0.3)

    system_message = SystemMessage(
        content=f"""You are the Digital Guardian, an expert cybersecurity assistant.

KNOWLEDGE BASE:
{context}

Provide clear, actionable advice in 2-3 paragraphs using the knowledge base."""
    )

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
            "timestamp": "2025-11-12T00:00:00Z",
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "provider": LLM_PROVIDER,
            "sources": [],
            "timestamp": "2025-11-12T00:00:00Z",
        }


def generate_scenario_content(
    scenario_type: str, difficulty: str, category: str = None
) -> str:
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
            "error": "LangChain not installed",
        }

    try:
        _ = get_llm_client()
        rag_ready = any(KNOWLEDGE_BASE.values())

        return {
            "provider": LLM_PROVIDER,
            "status": "active",
            "model_class": "llama-3.3-70b-versatile",
            "rag_initialized": rag_ready,
            "error": None,
        }
    except Exception as e:
        return {
            "provider": LLM_PROVIDER,
            "status": "error",
            "model_class": None,
            "rag_initialized": False,
            "error": str(e),
        }
