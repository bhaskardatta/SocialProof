"""
Database Configuration Module for SocialProof Backend

This module handles all database connection setup, session management, and
provides the declarative base for SQLAlchemy ORM models. It uses asyncpg
for asynchronous PostgreSQL communication.
"""

import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate that DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please create a .env file based on .env.example with your database credentials."
    )

# Create the async SQLAlchemy engine
# echo=True enables SQL query logging for development debugging
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,  # Verify connections before using them
)

# Create an async session factory
# expire_on_commit=False prevents attributes from being expired after commit
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create the declarative base class for ORM models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that provides a database session.

    This function is designed to be used with FastAPI's dependency injection
    system. It creates a new database session for each request and ensures
    proper cleanup after the request is completed.

    Yields:
        AsyncSession: An async SQLAlchemy database session

    Example:
        @app.get("/items/")
        async def read_items(db: AsyncSession = Depends(get_db)):
            # Use db session here
            pass
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
