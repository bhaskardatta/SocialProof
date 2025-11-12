"""
Initialize database tables directly
"""
import asyncio
from app.database import async_engine
from app.models import Base

async def create_tables():
    """Create all database tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
