"""
FastAPI Main Application Module for SocialProof Backend

This module serves as the entry point for the SocialProof cybersecurity simulation
game backend API. It defines all API routes, handles dependency injection for
database sessions, and configures the FastAPI application.
"""

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.database import async_engine, get_db

# Import AI core for Part 2 functionality
try:
    from app import ai_core_advanced as ai_core

    AI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  AI features not available: {e}")
    AI_AVAILABLE = False

# Initialize FastAPI application
app = FastAPI(
    title="SocialProof Backend API",
    description=(
        "Backend API for SocialProof - A sophisticated cybersecurity simulation game "
        "that helps users identify and defend against social engineering attacks."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ============================================================================
# Startup and Shutdown Events
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.

    This function is called when the FastAPI application starts. It initializes
    resources including the AI RAG pipeline for the Digital Guardian feature.

    Note: In production, use Alembic migrations instead of create_all().
    """
    print("🚀 Starting SocialProof Backend API...")

    # Initialize AI features if available
    if AI_AVAILABLE:
        try:
            print("🤖 Initializing AI systems...")
            status = ai_core.get_provider_status()
            if status["status"] == "active":
                print(
                    f"✅ AI systems ready! Provider: {status['provider']}, Model: {status.get('model', 'default')}"
                )
            else:
                print(f"⚠️  AI provider status: {status}")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize AI features: {e}")
            print("   The API will run but AI endpoints may not work correctly.")
    else:
        print("⚠️  AI features not available. Install AI dependencies to enable.")

    print("✅ SocialProof API startup complete!")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.

    This function is called when the FastAPI application is shutting down.
    It ensures proper cleanup of resources like database connections.
    """
    await async_engine.dispose()


# ============================================================================
# API Routes
# ============================================================================


@app.get(
    "/",
    summary="Welcome Endpoint",
    description="Returns a welcome message for the SocialProof API",
    tags=["Root"],
)
async def root():
    """
    Root endpoint that provides a welcome message.

    Returns:
        dict: Welcome message for the SocialProof API
    """
    return {
        "message": "Welcome to the SocialProof API",
        "version": "1.0.0",
        "documentation": "/docs",
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Check if the API is running and healthy",
    tags=["Health"],
)
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        dict: Status indicating the API is healthy
    """
    return {"status": "healthy"}


# ============================================================================
# Player Profile Endpoints
# ============================================================================


@app.post(
    "/players/",
    response_model=schemas.Player,
    status_code=status.HTTP_201_CREATED,
    summary="Create New Player",
    description="Register a new player profile in the SocialProof game",
    tags=["Players"],
)
async def create_player(
    player: schemas.PlayerCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new player profile.

    This endpoint registers a new player in the system. It validates that the
    email address is not already registered before creating the account.

    Args:
        player: PlayerCreate schema with username and email
        db: Database session (injected by FastAPI)

    Returns:
        Player: The newly created player profile with all fields

    Raises:
        HTTPException 400: If the email is already registered

    Example:
        POST /players/
        {
            "username": "cyber_defender",
            "email": "defender@example.com"
        }
    """
    # Check if email already exists
    db_player = await crud.get_player_by_email(db, email=player.email)
    if db_player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email address.",
        )

    # Check if username already exists
    db_player = await crud.get_player_by_username(db, username=player.username)
    if db_player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken. Please choose a different username.",
        )

    # Create the new player
    return await crud.create_player(db=db, player=player)


@app.get(
    "/players/",
    response_model=List[schemas.Player],
    summary="List All Players",
    description="Retrieve a paginated list of all registered players",
    tags=["Players"],
)
async def read_players(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a list of all players with pagination support.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100, max: 100)
        db: Database session (injected by FastAPI)

    Returns:
        List[Player]: List of player profiles

    Example:
        GET /players/?skip=0&limit=10
    """
    # Enforce maximum limit
    if limit > 100:
        limit = 100

    players = await crud.get_players(db, skip=skip, limit=limit)
    return players


@app.get(
    "/players/{player_id}",
    response_model=schemas.Player,
    summary="Get Player by ID",
    description="Retrieve a specific player profile by their unique ID",
    tags=["Players"],
)
async def read_player(player_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single player profile by ID.

    Args:
        player_id: Unique identifier of the player
        db: Database session (injected by FastAPI)

    Returns:
        Player: The requested player profile

    Raises:
        HTTPException 404: If the player is not found

    Example:
        GET /players/123
    """
    db_player = await crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found",
        )
    return db_player


# ============================================================================
# Game Scenario Endpoints
# ============================================================================


@app.post(
    "/scenarios/",
    response_model=schemas.Scenario,
    status_code=status.HTTP_201_CREATED,
    summary="Create New Scenario",
    description="Create a new game scenario for a player",
    tags=["Scenarios"],
)
async def create_scenario(
    player_id: int,
    scenario_type: str,
    content: str,
    difficulty_level: float,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new game scenario for a player.

    This endpoint will be expanded in Part 2 to include AI-generated content.
    For now, it accepts manual scenario data.

    Args:
        player_id: ID of the player receiving the scenario
        scenario_type: Type of scenario (e.g., 'EMAIL_PHISH', 'SMS_SCAM')
        content: The scenario content
        difficulty_level: Difficulty rating (1.0 to 10.0)
        db: Database session (injected by FastAPI)

    Returns:
        Scenario: The newly created scenario

    Raises:
        HTTPException 404: If the player is not found
    """
    # Verify player exists
    db_player = await crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found",
        )

    # Create scenario
    return await crud.create_player_scenario(
        db=db,
        player_id=player_id,
        scenario_type=scenario_type,
        content=content,
        difficulty_level=difficulty_level,
    )


@app.get(
    "/scenarios/{scenario_id}",
    response_model=schemas.Scenario,
    summary="Get Scenario by ID",
    description="Retrieve a specific game scenario by its unique ID",
    tags=["Scenarios"],
)
async def read_scenario(scenario_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single game scenario by ID.

    Args:
        scenario_id: Unique identifier of the scenario
        db: Database session (injected by FastAPI)

    Returns:
        Scenario: The requested scenario

    Raises:
        HTTPException 404: If the scenario is not found
    """
    db_scenario = await crud.get_scenario(db, scenario_id=scenario_id)
    if db_scenario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario with ID {scenario_id} not found",
        )
    return db_scenario


@app.get(
    "/players/{player_id}/scenarios",
    response_model=List[schemas.Scenario],
    summary="Get Player's Scenarios",
    description="Retrieve all scenarios for a specific player",
    tags=["Scenarios"],
)
async def read_player_scenarios(
    player_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all scenarios for a specific player.

    Args:
        player_id: ID of the player
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100, max: 100)
        db: Database session (injected by FastAPI)

    Returns:
        List[Scenario]: List of scenarios for the player

    Raises:
        HTTPException 404: If the player is not found
    """
    # Verify player exists
    db_player = await crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found",
        )

    # Enforce maximum limit
    if limit > 100:
        limit = 100

    scenarios = await crud.get_player_scenarios(
        db, player_id=player_id, skip=skip, limit=limit
    )
    return scenarios


# ============================================================================
# AI-Powered Features - Part 2
# ============================================================================


@app.post(
    "/scenarios/generate",
    response_model=schemas.ScenarioGenerateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate AI-Powered Scenario",
    description="Generate a dynamic cybersecurity scenario using AI based on player skill level",
    tags=["AI Features"],
)
async def generate_scenario(
    request: schemas.ScenarioGenerateRequest, db: AsyncSession = Depends(get_db)
):
    """
    Generate a new cybersecurity scenario using AI.

    This endpoint uses the configured LLM provider to generate realistic
    social engineering attack simulations. The difficulty is automatically
    adjusted based on the player's skill rating.

    Args:
        request: Contains player_id and scenario_type
        db: Database session (injected by FastAPI)

    Returns:
        ScenarioGenerateResponse: Generated scenario with metadata

    Raises:
        HTTPException 404: If player not found
        HTTPException 503: If AI features are not available
        HTTPException 500: If scenario generation fails

    Example:
        POST /scenarios/generate
        {
            "player_id": 123,
            "scenario_type": "EMAIL_PHISH"
        }
    """
    if not AI_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI features are not available. Please install required dependencies.",
        )

    # Verify player exists and get their skill rating
    player = await crud.get_player(db, player_id=request.player_id)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {request.player_id} not found",
        )

    try:
        # Generate scenario using advanced AI with variety
        result = ai_core.generate_diverse_scenario(
            scenario_type=request.scenario_type,
            difficulty=request.difficulty,
            category=None,  # Auto-select for variety
        )

        # Map difficulty label to numerical level (now with 5 levels)
        difficulty_mapping = {
            "beginner": 1,
            "easy": 3,
            "medium": 5,
            "hard": 7,
            "expert": 9,
        }

        # Create AI result dict for database
        ai_result = {
            "content": result["content"],
            "difficulty_level": difficulty_mapping.get(request.difficulty.lower(), 5),
            "difficulty_label": request.difficulty,
            "provider": "groq",
            "scenario_type": request.scenario_type,
            "category": result.get("category", "general"),
            "red_flags_count": result.get("red_flags_count", 3),
        }

        # Save scenario to database
        db_scenario = await crud.create_ai_generated_scenario(
            db=db,
            player_id=request.player_id,
            scenario_type=request.scenario_type,
            ai_result=ai_result,
        )

        # Return response with all metadata
        return schemas.ScenarioGenerateResponse(
            scenario_id=db_scenario.id,
            content=db_scenario.content,
            difficulty_level=db_scenario.difficulty_level,
            difficulty_label=ai_result["difficulty_label"],
            scenario_type=db_scenario.scenario_type,
            player_id=db_scenario.player_id,
            provider=ai_result["provider"],
            created_at=db_scenario.created_at,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate scenario: {str(e)}",
        )


@app.post(
    "/guardian/query",
    response_model=schemas.DigitalGuardianResponse,
    summary="Query Digital Guardian",
    description="Ask the Digital Guardian AI assistant about cybersecurity topics",
    tags=["AI Features"],
)
async def query_guardian(query_request: schemas.DigitalGuardianQuery):
    """
    Query the Digital Guardian AI assistant.

    The Digital Guardian uses RAG (Retrieval-Augmented Generation) to provide
    accurate, contextual answers about cybersecurity topics based on the
    knowledge base.

    Args:
        query_request: Contains the user's question

    Returns:
        DigitalGuardianResponse: AI-generated answer with sources

    Raises:
        HTTPException 503: If AI features are not available
        HTTPException 500: If query processing fails

    Example:
        POST /guardian/query
        {
            "query": "What is phishing and how can I protect myself?"
        }
    """
    if not AI_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI features are not available. Please install required dependencies.",
        )

    try:
        # Process query through RAG system
        result = ai_core.digital_guardian_query(query_request.query)

        # Return formatted response
        return schemas.DigitalGuardianResponse(
            answer=result["answer"],
            sources=result["sources"],
            provider=result["provider"],
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}",
        )


@app.get(
    "/ai/provider",
    response_model=schemas.AIProviderInfo,
    summary="Get AI Provider Info",
    description="Check which LLM provider is currently active and its status",
    tags=["AI Features"],
)
async def get_provider_info():
    """
    Get information about the current AI configuration.

    This endpoint provides details about which LLM provider is active,
    whether the RAG system is initialized, and the overall AI system status.

    Returns:
        AIProviderInfo: Current provider and status information

    Example:
        GET /ai/provider
    """
    if not AI_AVAILABLE:
        return schemas.AIProviderInfo(
            provider="none",
            status="unavailable",
            model_class=None,
            rag_initialized=False,
            error="AI dependencies not installed",
        )

    try:
        info = ai_core.get_provider_info()
        return schemas.AIProviderInfo(**info)
    except Exception as e:
        return schemas.AIProviderInfo(
            provider="unknown",
            status="error",
            model_class=None,
            rag_initialized=False,
            error=str(e),
        )


@app.get(
    "/ai/validate",
    summary="Validate AI Configuration",
    description="Comprehensive validation of AI system configuration",
    tags=["AI Features"],
)
async def validate_ai():
    """
    Perform comprehensive AI system validation.

    This endpoint checks all aspects of the AI configuration including:
    - LLM provider setup
    - API key availability
    - RAG pipeline status
    - Knowledge base integrity

    Returns:
        dict: Detailed validation results

    Example:
        GET /ai/validate
    """
    if not AI_AVAILABLE:
        return {
            "valid": False,
            "errors": ["AI dependencies not installed"],
            "warnings": [],
            "provider": "none",
            "rag_ready": False,
        }

    try:
        validation = ai_core.validate_ai_configuration()
        return validation
    except Exception as e:
        return {
            "valid": False,
            "errors": [str(e)],
            "warnings": [],
            "provider": "unknown",
            "rag_ready": False,
        }


# ============================================================================
# Scenario Resolution Endpoints - Interactive Gameplay
# ============================================================================


@app.post(
    "/scenarios/{scenario_id}/resolve",
    response_model=schemas.ScenarioResolutionResponse,
    summary="Resolve Scenario Action",
    description="Process player action on a scenario and update their score",
    tags=["Scenarios"],
)
async def resolve_scenario(
    scenario_id: int,
    resolution: schemas.ScenarioResolutionRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Resolve a scenario based on player action.

    This endpoint evaluates whether the player's action was correct,
    updates their skill rating accordingly, and provides instant feedback.

    The scoring logic:
    - Correctly reporting phishing: +25 points
    - Incorrectly reporting legitimate email: -15 points
    - Correctly deleting safe email: +10 points (future)
    - Incorrectly deleting phishing: -20 points (future)

    Args:
        scenario_id: ID of the scenario being resolved
        resolution: Contains the action taken by the player
        db: Database session (injected by FastAPI)

    Returns:
        ScenarioResolutionResponse: Feedback and updated score

    Raises:
        HTTPException 404: If scenario not found

    Example:
        POST /scenarios/123/resolve
        {
            "action": "reported_phish"
        }
    """
    # Fetch the scenario
    scenario = await crud.get_scenario(db, scenario_id=scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario with ID {scenario_id} not found",
        )

    # Determine if this is actually a phishing email
    # Look for common phishing indicators in the content
    content_lower = scenario.content.lower()
    phishing_keywords = [
        "urgent",
        "password",
        "account",
        "verify",
        "confirm",
        "suspended",
        "click here",
        "act now",
        "limited time",
        "security alert",
        "unusual activity",
        "verify your identity",
        "confirm your account",
        "update your information",
        "prize",
        "winner",
        "claim",
        "refund",
        "tax",
        "irs",
        "bank",
    ]

    is_phishing = any(keyword in content_lower for keyword in phishing_keywords)

    # Also check scenario type if available
    if scenario.scenario_type in ["phishing", "EMAIL_PHISH", "email_phishing"]:
        is_phishing = True

    # Evaluate the action
    action_correct = False
    score_change = 0.0
    message = ""

    if resolution.action == "reported_phish":
        if is_phishing:
            action_correct = True
            score_change = 25.0
            message = "🎉 Correct! This was a phishing attempt. You've successfully identified the threat!"
        else:
            action_correct = False
            score_change = -15.0
            message = "❌ Incorrect. This was a legitimate email. Be more careful before reporting!"

    elif resolution.action == "deleted_safe":
        if not is_phishing:
            action_correct = True
            score_change = 10.0
            message = (
                "✅ Correct! This was a safe email and you handled it appropriately."
            )
        else:
            action_correct = False
            score_change = -20.0
            message = (
                "⚠️ Incorrect! This was a phishing email. You should have reported it!"
            )

    elif resolution.action == "ignored":
        # Neutral action - no score change but provide feedback
        if is_phishing:
            score_change = -5.0
            message = "⚠️ You ignored a phishing email. It's safer to report suspicious messages!"
        else:
            score_change = 0.0
            message = "Neutral action. The email was safe, but consider deleting unwanted emails."

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action: {resolution.action}. Valid actions: reported_phish, deleted_safe, ignored",
        )

    # Update player's skill rating
    updated_player = await crud.adjust_player_skill_rating(
        db, player_id=scenario.player_id, score_change=score_change
    )

    # Mark scenario as completed
    await crud.update_scenario_result(
        db, scenario_id=scenario_id, is_successful=action_correct
    )

    return schemas.ScenarioResolutionResponse(
        correct=action_correct,
        message=message,
        new_skill_rating=updated_player.player_skill_rating,
        score_change=score_change,
    )


# ============================================================================
# Player Statistics Endpoints - Performance Tracking
# ============================================================================


@app.get(
    "/players/{player_id}/stats",
    response_model=schemas.PlayerStats,
    summary="Get Player Statistics",
    description="Retrieve comprehensive performance statistics for a player",
    tags=["Players"],
)
async def get_player_statistics(player_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get comprehensive statistics for a player.

    This endpoint calculates and returns detailed performance metrics including:
    - Total scenarios resolved
    - Correctly identified phishing attacks
    - Missed phishing attacks
    - False positives (incorrectly reported safe messages)
    - Overall accuracy percentage
    - Current skill rating

    Args:
        player_id: ID of the player
        db: Database session (injected by FastAPI)

    Returns:
        PlayerStats: Comprehensive player statistics

    Raises:
        HTTPException 404: If player not found

    Example:
        GET /players/1/stats
    """
    player = await crud.get_player(db, player_id=player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found",
        )

    stats = await crud.get_player_stats(db, player_id=player_id)
    return stats
