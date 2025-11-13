"""
AI Core Module for SocialProof Backend - Multi-Provider LLM System

This module implements a sophisticated, provider-agnostic AI system that powers
the SocialProof cybersecurity simulation game. It features:

1. Dynamic LLM Provider Switching: Factory pattern for runtime provider selection
2. RAG Pipeline: Retrieval-Augmented Generation for the Digital Guardian assistant
3. Scenario Generation: Dynamic, difficulty-adaptive social engineering scenarios
4. Extensibility: Easy to add new providers or modify existing configurations

Architecture Pattern: Factory Method + Singleton for RAG chain
"""

import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenRouter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq

# ============================================================================
# INITIALIZATION & CONFIGURATION
# ============================================================================

# Load environment variables
load_dotenv()

# Read provider configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google").lower()

# Global RAG chain instance (initialized once at startup)
_rag_chain: Optional[RetrievalQA] = None
_embeddings: Optional[GoogleGenerativeAIEmbeddings] = None


# ============================================================================
# LLM PROVIDER FACTORY (CORE ARCHITECTURE)
# ============================================================================


def get_llm_client(temperature: float = 0.3) -> BaseChatModel:
    """
    Factory function to instantiate the configured LLM client.

    This is the cornerstone of our multi-provider architecture. It decouples
    the application logic from specific LLM implementations, allowing seamless
    provider switching via environment configuration.

    Args:
        temperature: Controls randomness in responses (0.0 = deterministic, 1.0 = creative)
                    Default 0.3 provides balanced, slightly creative responses

    Returns:
        BaseChatModel: An initialized LangChain chat model for the configured provider

    Raises:
        ValueError: If the provider is not supported or API key is missing

    Supported Providers:
        - google: Google's Gemini Pro (balanced performance, multimodal capable)
        - groq: Llama 3 8B on Groq (ultra-fast inference, cost-effective)
        - openrouter: Access to multiple models (maximum flexibility)

    Example:
        llm = get_llm_client(temperature=0.5)
        response = llm.invoke("Explain phishing attacks")
    """
    if LLM_PROVIDER == "google":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not set in environment variables. "
                "Please add it to your .env file. Get your key at: "
                "https://makersuite.google.com/app/apikey"
            )
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # Updated to latest stable model
            google_api_key=api_key,
            temperature=temperature,
            convert_system_message_to_human=True,  # Better compatibility
        )

    elif LLM_PROVIDER == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set in environment variables. "
                "Please add it to your .env file. Get your key at: "
                "https://console.groq.com/keys"
            )
        return ChatGroq(
            temperature=temperature,
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile",  # Latest Llama 3.3 70B - fastest and best!
            max_tokens=4096,  # Increased for better responses
        )

    elif LLM_PROVIDER == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is not set in environment variables. "
                "Please add it to your .env file. Get your key at: "
                "https://openrouter.ai/keys"
            )
        return ChatOpenRouter(
            openrouter_api_key=api_key,
            model_name="meta-llama/llama-3.1-8b-instruct:free",  # Free tier model
            temperature=temperature,
            max_tokens=2048,
        )

    else:
        raise ValueError(
            f"Unsupported LLM provider: '{LLM_PROVIDER}'. "
            f"Supported providers are: 'google', 'groq', 'openrouter'. "
            f"Please update LLM_PROVIDER in your .env file."
        )


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """
    Get or create the embeddings model for vector database operations.

    Currently uses Google's embedding model as it provides excellent quality
    and is free to use. This could be extended to support other embedding
    providers in the future.

    Returns:
        GoogleGenerativeAIEmbeddings: Initialized embeddings model

    Raises:
        ValueError: If GOOGLE_API_KEY is not set (required for embeddings)
    """
    global _embeddings

    if _embeddings is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY is required for embeddings. "
                "Even if using a different LLM provider, embeddings currently use Google's model. "
                "Get your key at: https://makersuite.google.com/app/apikey"
            )
        _embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", google_api_key=api_key
        )

    return _embeddings


# ============================================================================
# RAG PIPELINE FOR DIGITAL GUARDIAN
# ============================================================================


def setup_rag_pipeline(knowledge_base_dir: str = "knowledge_base") -> None:
    """
    Initialize the Retrieval-Augmented Generation (RAG) pipeline.

    This function sets up the complete RAG system that powers the Digital Guardian
    feature. It loads cybersecurity knowledge documents, creates vector embeddings,
    and configures the question-answering chain.

    The RAG pipeline enables the Digital Guardian to provide accurate, contextual
    answers about cybersecurity topics by retrieving relevant information from
    the knowledge base before generating responses.

    Args:
        knowledge_base_dir: Path to directory containing knowledge base text files

    Raises:
        RuntimeError: If knowledge base directory doesn't exist or is empty
        ValueError: If required API keys are missing

    Architecture:
        1. Load documents from knowledge_base directory
        2. Create embeddings for each document chunk
        3. Store embeddings in ChromaDB vector database
        4. Create retrieval chain with custom prompt template
        5. Initialize question-answering system

    Called: Once at application startup (see main.py startup event)
    """
    global _rag_chain

    # Validate knowledge base directory
    if not os.path.exists(knowledge_base_dir):
        raise RuntimeError(
            f"Knowledge base directory '{knowledge_base_dir}' does not exist. "
            f"Please create it and add .txt files with cybersecurity information."
        )

    try:
        # Load all text files from knowledge base
        loader = DirectoryLoader(
            knowledge_base_dir, glob="*.txt", loader_cls=TextLoader, show_progress=True
        )
        documents = loader.load()

        if not documents:
            raise RuntimeError(
                f"No documents found in '{knowledge_base_dir}'. "
                f"Please add .txt files with cybersecurity knowledge."
            )

        print(f"📚 Loaded {len(documents)} documents from knowledge base")

        # Create embeddings and vector store
        embeddings = get_embeddings()
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            collection_name="socialproof_knowledge",
        )

        # Get configured LLM
        llm = get_llm_client(temperature=0.2)  # Lower temperature for factual responses

        # Define the Digital Guardian's personality and constraints
        prompt_template = """You are the "Digital Guardian," an expert AI cybersecurity assistant for the SocialProof training platform.

Your Role:
- Educate users about cybersecurity threats and best practices
- Provide clear, accurate information based on the knowledge base
- Help users understand social engineering tactics
- Encourage critical thinking without giving direct scenario answers

Guidelines:
- Use the provided context to answer questions accurately
- If the answer isn't in the context, acknowledge the limitation
- Be friendly, supportive, and encouraging
- Avoid technical jargon unless necessary; explain complex terms
- Never provide direct answers to active game scenarios
- Focus on general principles and red flags to watch for

Context from Knowledge Base:
{context}

User Question: {question}

Helpful Answer:"""

        QA_PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Create the RAG chain
        _rag_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # Stuff all retrieved docs into prompt
            retriever=vector_store.as_retriever(
                search_kwargs={"k": 3}  # Retrieve top 3 most relevant documents
            ),
            chain_type_kwargs={"prompt": QA_PROMPT},
            return_source_documents=True,  # Include sources for transparency
        )

        print(
            f"✅ RAG pipeline initialized successfully using '{LLM_PROVIDER}' provider"
        )
        print(f"   Model: {llm.__class__.__name__}")
        print(f"   Vector DB: ChromaDB with {len(documents)} documents")

    except Exception as e:
        raise RuntimeError(f"Failed to initialize RAG pipeline: {str(e)}")


def query_digital_guardian(query: str) -> Dict[str, Any]:
    """
    Process a user's question through the Digital Guardian RAG system.

    This function retrieves relevant cybersecurity knowledge and generates
    an informed, contextual response to the user's question.

    Args:
        query: User's cybersecurity question

    Returns:
        dict: Contains 'answer' (str) and 'sources' (list of str)

    Raises:
        RuntimeError: If RAG pipeline hasn't been initialized
        Exception: If query processing fails

    Example:
        result = query_digital_guardian("What is phishing?")
        print(result["answer"])
        print("Sources:", result["sources"])
    """
    if _rag_chain is None:
        raise RuntimeError(
            "RAG pipeline has not been initialized. "
            "Call setup_rag_pipeline() during application startup."
        )

    try:
        # Process query through RAG chain
        result = _rag_chain.invoke({"query": query})

        # Extract source documents for transparency
        sources = []
        if "source_documents" in result:
            sources = [
                doc.metadata.get("source", "Unknown")
                for doc in result["source_documents"]
            ]

        return {
            "answer": result["result"],
            "sources": sources,
            "provider": LLM_PROVIDER,
        }

    except Exception as e:
        raise Exception(f"Error processing Digital Guardian query: {str(e)}")


# ============================================================================
# DYNAMIC SCENARIO GENERATION
# ============================================================================


def calculate_difficulty_params(player_skill_rating: float) -> tuple[str, str, float]:
    """
    Determine scenario difficulty parameters based on player skill rating.

    This function implements an adaptive difficulty system that adjusts
    scenario complexity based on the player's demonstrated skill level.

    Args:
        player_skill_rating: Player's current skill rating (0-1000+)

    Returns:
        tuple: (difficulty_label, scenario_details, numerical_difficulty)

    Difficulty Tiers:
        - Beginner (< 600): Obvious red flags, spelling errors
        - Intermediate (600-850): Plausible pretexts, subtle indicators
        - Advanced (> 850): Highly convincing, personalized attacks
    """
    if player_skill_rating < 600:
        return (
            "Beginner",
            "include several obvious red flags such as spelling mistakes, grammatical errors, "
            "a generic greeting like 'Dear Customer', and an obviously suspicious sender address. "
            "The urgency should be exaggerated and unrealistic.",
            3.0,
        )
    elif 600 <= player_skill_rating < 850:
        return (
            "Intermediate",
            "be well-written with minor imperfections, use a plausible pretext that creates genuine concern, "
            "include a link that appears legitimate at first glance but has subtle discrepancies, "
            "and use moderate urgency that seems realistic but pressuring.",
            6.0,
        )
    else:
        return (
            "Advanced",
            "be highly convincing and professional, perfectly personalized with no grammatical errors, "
            "create a strong sense of urgency with logical reasoning, include sophisticated social engineering "
            "techniques, and use brand-accurate formatting and language. The message should be indistinguishable "
            "from legitimate communications at first glance.",
            9.0,
        )


def generate_scenario_content(
    player_skill_rating: float, scenario_type: str
) -> Dict[str, Any]:
    """
    Generate dynamic, AI-powered social engineering scenario content.

    This function creates realistic cybersecurity attack simulations tailored
    to the player's skill level. It uses the configured LLM provider to generate
    authentic-looking phishing emails, smishing messages, or other social
    engineering attacks.

    Args:
        player_skill_rating: Player's current skill rating (determines difficulty)
        scenario_type: Type of attack (e.g., "EMAIL_PHISH", "SMS_SCAM", "VOICE_PHISH")

    Returns:
        dict: Contains 'content' (generated message), 'difficulty_level' (float),
              'difficulty_label' (str), and 'provider' (str)

    Raises:
        ValueError: If scenario_type is invalid or API keys are missing
        Exception: If content generation fails

    Example:
        scenario = generate_scenario_content(650, "EMAIL_PHISH")
        print(scenario["content"])
        print(f"Difficulty: {scenario['difficulty_label']}")
    """
    try:
        # Get LLM with slightly higher temperature for creative variation
        llm = get_llm_client(temperature=0.4)

        # Calculate difficulty parameters
        difficulty_label, scenario_details, difficulty_level = (
            calculate_difficulty_params(player_skill_rating)
        )

        # Map scenario types to human-readable formats
        scenario_type_map = {
            "EMAIL_PHISH": "phishing email",
            "SMS_SCAM": "smishing (SMS phishing) text message",
            "VOICE_PHISH": "vishing (voice phishing) phone call script",
            "SOCIAL_ENGINEERING": "social engineering attempt",
            "PRETEXTING": "pretexting scenario",
        }

        readable_type = scenario_type_map.get(
            scenario_type.upper(), scenario_type.lower().replace("_", " ")
        )

        # Construct the generation prompt
        prompt_template = """You are a cybersecurity training simulation engine creating realistic attack scenarios.

Task: Generate a {scenario_type} for cybersecurity training purposes.

Difficulty Level: {difficulty_label}
Requirements: The message should {scenario_details}

CRITICAL INSTRUCTIONS:
- Generate ONLY the message content itself (email body, SMS text, etc.)
- Do NOT include any explanatory text, preamble, or meta-commentary
- Do NOT include subject lines or headers (unless specifically for email format)
- Make it realistic enough for training but clearly a simulation
- The content should test the user's ability to identify social engineering tactics

Generate the {scenario_type} now:"""

        prompt = PromptTemplate.from_template(prompt_template)

        # Generate the scenario
        chain = prompt | llm
        response = chain.invoke(
            {
                "scenario_type": readable_type,
                "difficulty_label": difficulty_label,
                "scenario_details": scenario_details,
            }
        )

        # Extract and clean the content
        content = response.content.strip()

        # Remove common AI preambles if present
        unwanted_prefixes = [
            "Here is",
            "Here's",
            "Subject:",
            "Message:",
            "The message",
            "This is",
        ]
        for prefix in unwanted_prefixes:
            if content.startswith(prefix):
                # Find first newline and start from there
                first_newline = content.find("\n")
                if first_newline > 0:
                    content = content[first_newline:].strip()

        return {
            "content": content,
            "difficulty_level": difficulty_level,
            "difficulty_label": difficulty_label,
            "provider": LLM_PROVIDER,
            "scenario_type": scenario_type,
        }

    except Exception as e:
        raise Exception(f"Error generating scenario content: {str(e)}")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def get_provider_info() -> Dict[str, Any]:
    """
    Get information about the currently configured LLM provider.

    Returns:
        dict: Provider name, status, and configuration details

    Example:
        info = get_provider_info()
        print(f"Using provider: {info['provider']}")
        print(f"Status: {info['status']}")
    """
    try:
        llm = get_llm_client()
        return {
            "provider": LLM_PROVIDER,
            "status": "active",
            "model_class": llm.__class__.__name__,
            "rag_initialized": _rag_chain is not None,
        }
    except ValueError as e:
        return {
            "provider": LLM_PROVIDER,
            "status": "error",
            "error": str(e),
            "rag_initialized": False,
        }


def validate_ai_configuration() -> Dict[str, Any]:
    """
    Validate that AI system is properly configured.

    This function performs comprehensive checks on the AI configuration,
    including provider settings, API keys, and RAG pipeline status.

    Returns:
        dict: Validation results with status and any error messages

    Example:
        validation = validate_ai_configuration()
        if validation["valid"]:
            print("AI system ready!")
        else:
            print("Errors:", validation["errors"])
    """
    errors = []
    warnings = []

    # Check LLM provider
    if not LLM_PROVIDER:
        errors.append("LLM_PROVIDER not set in environment")
    elif LLM_PROVIDER not in ["google", "groq", "openrouter"]:
        errors.append(f"Invalid LLM_PROVIDER: {LLM_PROVIDER}")

    # Check API keys
    try:
        llm = get_llm_client()
    except ValueError as e:
        errors.append(str(e))

    # Check embeddings (requires Google API key)
    try:
        embeddings = get_embeddings()
    except ValueError as e:
        warnings.append(f"Embeddings unavailable: {str(e)}")

    # Check RAG pipeline
    if _rag_chain is None:
        warnings.append("RAG pipeline not initialized")

    # Check knowledge base
    if not os.path.exists("knowledge_base"):
        warnings.append("Knowledge base directory not found")
    elif not os.listdir("knowledge_base"):
        warnings.append("Knowledge base directory is empty")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "provider": LLM_PROVIDER,
        "rag_ready": _rag_chain is not None,
    }


# ============================================================================
# MODULE INITIALIZATION CHECK
# ============================================================================

# Perform basic validation on module import
try:
    _provider_check = get_provider_info()
    if _provider_check["status"] == "error":
        print(f"⚠️  Warning: AI provider '{LLM_PROVIDER}' not properly configured")
        print(f"   Error: {_provider_check['error']}")
    else:
        print("✅ AI Core module loaded successfully")
        print(f"   Provider: {LLM_PROVIDER}")
        print(f"   Model: {_provider_check['model_class']}")
except Exception as e:
    print(f"⚠️  Warning: AI Core module loaded with errors: {str(e)}")
