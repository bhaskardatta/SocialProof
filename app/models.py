"""
SQLAlchemy ORM Models for SocialProof Backend

This module defines all database table schemas using SQLAlchemy's declarative ORM.
Each model class represents a table in the PostgreSQL database and defines the
structure, relationships, and constraints for that table.
"""

from typing import List

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, relationship

from app.database import Base


class PlayerProfile(Base):
    """
    PlayerProfile ORM Model

    Represents a player's profile in the SocialProof cybersecurity simulation game.
    Each player has a unique username and email, along with a skill rating that
    tracks their performance across scenarios.

    Attributes:
        id: Unique identifier for the player
        username: Unique username chosen by the player
        email: Unique email address for the player
        player_skill_rating: Numerical rating representing the player's skill level
        created_at: Timestamp of when the profile was created
        scenarios: Relationship to all game scenarios associated with this player
    """

    __tablename__ = "player_profiles"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Player identification fields
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)

    # Player metrics
    player_skill_rating = Column(Float, nullable=False, default=500.0)

    # Timestamp
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationships
    scenarios: Mapped[List["GameScenario"]] = relationship(
        "GameScenario", back_populates="player", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of PlayerProfile for debugging."""
        return (
            f"<PlayerProfile(id={self.id}, username='{self.username}', "
            f"email='{self.email}', skill_rating={self.player_skill_rating})>"
        )


class GameScenario(Base):
    """
    GameScenario ORM Model

    Represents a single cybersecurity scenario presented to a player in the
    SocialProof game. Each scenario contains AI-generated content that simulates
    a real-world security threat (e.g., phishing emails, social engineering attempts).

    Attributes:
        id: Unique identifier for the scenario
        player_id: Foreign key reference to the PlayerProfile
        scenario_type: Type of security scenario (e.g., 'EMAIL_PHISH', 'SMS_SCAM')
        content: The actual AI-generated content of the scenario
        difficulty_level: Numerical difficulty rating for the scenario
        is_successful: Whether the player successfully identified/handled the threat
        created_at: Timestamp of when the scenario was created
        player: Relationship back to the PlayerProfile who received this scenario
    """

    __tablename__ = "game_scenarios"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to player
    player_id = Column(
        Integer,
        ForeignKey("player_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Scenario details
    scenario_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    difficulty_level = Column(Float, nullable=False)
    is_successful = Column(Boolean, nullable=False, default=False)

    # Timestamp
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationships
    player: Mapped["PlayerProfile"] = relationship(
        "PlayerProfile", back_populates="scenarios"
    )

    def __repr__(self) -> str:
        """String representation of GameScenario for debugging."""
        return (
            f"<GameScenario(id={self.id}, player_id={self.player_id}, "
            f"type='{self.scenario_type}', difficulty={self.difficulty_level}, "
            f"successful={self.is_successful})>"
        )
