"""
Pydantic Schemas for SocialProof Backend

This module defines all Pydantic models used for data validation, serialization,
and API request/response schemas. These schemas ensure type safety and automatic
validation of incoming and outgoing data in the FastAPI application.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# ============================================================================
# PlayerProfile Schemas
# ============================================================================


class PlayerBase(BaseModel):
    """
    Base schema for PlayerProfile containing common fields.

    This schema defines the fundamental attributes that are shared across
    different player-related operations.
    """

    username: str = Field(
        ..., min_length=3, max_length=50, description="Unique username for the player"
    )
    email: EmailStr = Field(..., description="Valid email address for the player")


class PlayerCreate(PlayerBase):
    """
    Schema for creating a new player profile.

    This schema inherits all fields from PlayerBase and is used when
    accepting player registration data from API requests.
    """

    pass


class Player(PlayerBase):
    """
    Complete player schema for API responses.

    This schema includes all player data including system-generated fields
    like ID, skill rating, and creation timestamp. It is used when returning
    player data to API clients.
    """

    id: int = Field(..., description="Unique identifier for the player")
    player_skill_rating: float = Field(..., description="Player's current skill rating")
    created_at: datetime = Field(
        ..., description="Timestamp when the player profile was created"
    )

    class Config:
        """Pydantic configuration for ORM compatibility."""

        from_attributes = True  # Replaces orm_mode in Pydantic v2


# ============================================================================
# GameScenario Schemas
# ============================================================================


class ScenarioBase(BaseModel):
    """
    Base schema for GameScenario containing common fields.

    This schema defines the fundamental attributes required when creating
    or working with game scenarios.
    """

    scenario_type: str = Field(
        ..., description="Type of scenario (e.g., 'EMAIL_PHISH', 'SMS_SCAM')"
    )
    player_id: int = Field(..., description="ID of the player receiving this scenario")


class ScenarioCreate(ScenarioBase):
    """
    Schema for creating a new game scenario.

    This schema is used when generating new scenarios through the API.
    Additional fields like content, difficulty, and success status will
    be populated by the backend logic.
    """

    pass


class Scenario(ScenarioBase):
    """
    Complete scenario schema for API responses.

    This schema includes all scenario data including the AI-generated content,
    difficulty level, success status, and timestamps. It is used when returning
    scenario data to API clients.
    """

    id: int = Field(..., description="Unique identifier for the scenario")
    content: str = Field(..., description="AI-generated content of the scenario")
    difficulty_level: float = Field(
        ..., description="Difficulty rating of the scenario"
    )
    is_successful: bool = Field(
        ..., description="Whether the player successfully handled the scenario"
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the scenario was created"
    )

    class Config:
        """Pydantic configuration for ORM compatibility."""

        from_attributes = True  # Replaces orm_mode in Pydantic v2


# ============================================================================
# AI-Powered Features Schemas - Part 2
# ============================================================================


class ScenarioGenerateRequest(BaseModel):
    """
    Schema for requesting AI-generated scenario content.

    This schema is used when a player requests a new cybersecurity simulation
    scenario. The system uses the player's skill rating to adjust difficulty.
    """

    player_id: int = Field(..., description="ID of the player requesting the scenario")
    scenario_type: str = Field(
        ...,
        description="Type of scenario to generate (e.g., 'phishing', 'smishing')",
    )
    difficulty: str = Field(
        default="medium", description="Difficulty level: easy, medium, or hard"
    )


class ScenarioGenerateResponse(BaseModel):
    """
    Schema for AI-generated scenario response.

    This schema includes the generated scenario content along with metadata
    about difficulty level and generation details.
    """

    scenario_id: int = Field(..., description="ID of the created scenario")
    content: str = Field(..., description="AI-generated scenario content")
    difficulty_level: float = Field(
        ..., description="Numerical difficulty rating (0-10)"
    )
    difficulty_label: str = Field(
        ..., description="Human-readable difficulty (Beginner/Intermediate/Advanced)"
    )
    scenario_type: str = Field(..., description="Type of scenario generated")
    player_id: int = Field(
        ..., description="ID of the player who received this scenario"
    )
    provider: str = Field(..., description="LLM provider used for generation")
    created_at: datetime = Field(..., description="Timestamp when scenario was created")


class DigitalGuardianQuery(BaseModel):
    """
    Schema for querying the Digital Guardian AI assistant.

    The Digital Guardian uses RAG (Retrieval-Augmented Generation) to provide
    accurate, contextual answers about cybersecurity topics.
    """

    query: str = Field(
        ...,
        min_length=5,
        max_length=3000,
        description="User's cybersecurity question",
        examples=["What is phishing?", "How can I identify a smishing attack?"],
    )


class DigitalGuardianResponse(BaseModel):
    """
    Schema for Digital Guardian response.

    This schema includes the AI-generated answer along with source documents
    for transparency and verification.
    """

    answer: str = Field(..., description="Digital Guardian's response to the query")
    sources: list[str] = Field(
        default=[], description="Source documents used to generate the answer"
    )
    provider: str = Field(..., description="LLM provider used for response generation")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="When the response was generated"
    )


class AIProviderInfo(BaseModel):
    """
    Schema for AI provider configuration information.

    Used to check which LLM provider is currently active and its status.
    """

    provider: str = Field(..., description="Currently active LLM provider")
    status: str = Field(..., description="Provider status (active/error)")
    model_class: Optional[str] = Field(
        default=None, description="LangChain model class in use"
    )
    rag_initialized: bool = Field(..., description="Whether RAG pipeline is ready")
    error: Optional[str] = Field(
        default=None, description="Error message if status is error"
    )


# ============================================================================
# Scenario Resolution Schemas - Interactive Gameplay
# ============================================================================


class ScenarioResolutionRequest(BaseModel):
    """
    Schema for resolving a scenario when a player takes action.

    This schema is used when a player interacts with a simulation (e.g., reporting
    an email as phishing or deleting it). The backend evaluates the action and
    updates the player's score accordingly.
    """

    action: str = Field(
        ...,
        description="Action taken by the player (e.g., 'reported_phish', 'deleted_safe', 'ignored')",
        examples=["reported_phish", "deleted_safe"],
    )


class ScenarioResolutionResponse(BaseModel):
    """
    Schema for scenario resolution response.

    This schema provides feedback to the player about their action, including
    whether it was correct, a message, and their updated skill rating.
    """

    correct: bool = Field(..., description="Whether the player's action was correct")
    message: str = Field(..., description="Feedback message for the player")
    new_skill_rating: float = Field(..., description="Player's updated skill rating")
    score_change: float = Field(..., description="Points gained or lost")


# ============================================================================
# Player Statistics Schemas - Performance Tracking
# ============================================================================


class PlayerStats(BaseModel):
    """
    Schema for player performance statistics.

    This schema provides a comprehensive overview of a player's performance
    across all scenarios, including accuracy metrics and skill rating.
    """

    total_scenarios_resolved: int = Field(
        ..., description="Total number of scenarios completed"
    )
    correctly_identified_phish: int = Field(
        ..., description="Number of phishing attacks correctly identified"
    )
    missed_phish: int = Field(..., description="Number of phishing attacks missed")
    incorrectly_reported_safe: int = Field(
        ..., description="Number of safe messages incorrectly reported"
    )
    accuracy_percentage: float = Field(..., description="Overall accuracy percentage")
    current_skill_rating: float = Field(
        ..., description="Player's current skill rating"
    )
