"""
Seed initial data for testing
"""
import asyncio
from app.database import AsyncSessionLocal
from app import models

async def seed_data():
    """Create initial test player"""
    async with AsyncSessionLocal() as db:
        # Create a test player
        player = models.PlayerProfile(
            username="testplayer",
            email="test@socialproof.com",
            player_skill_rating=500.0
        )
        db.add(player)
        await db.commit()
        print(f"✅ Created test player (ID: {player.id})")
        print(f"   Username: {player.username}")
        print(f"   Skill Rating: {player.player_skill_rating}")

if __name__ == "__main__":
    asyncio.run(seed_data())
