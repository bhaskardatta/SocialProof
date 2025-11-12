#!/bin/bash

# SocialProof Backend Quick Setup Script
# This script automates the initial setup process

set -e  # Exit on any error

echo "=========================================="
echo "  SocialProof Backend Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created. Please edit it with your database credentials.${NC}"
    echo -e "${YELLOW}⚠️  Opening .env file for editing...${NC}"
    echo ""
    echo "Please update the DATABASE_URL with your PostgreSQL credentials:"
    echo "DATABASE_URL=\"postgresql+asyncpg://YOUR_USER:YOUR_PASSWORD@localhost:5432/YOUR_DATABASE\""
    echo ""
    read -p "Press Enter after you've updated the .env file..."
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Check if alembic is initialized
if [ ! -d alembic ]; then
    echo ""
    echo -e "${YELLOW}Initializing Alembic for database migrations...${NC}"
    alembic init alembic
    echo -e "${GREEN}✓ Alembic initialized${NC}"
    
    echo ""
    echo -e "${YELLOW}⚠️  You need to configure Alembic manually:${NC}"
    echo ""
    echo "1. Edit alembic/env.py and add the following imports at the top:"
    echo "   import os"
    echo "   import sys"
    echo "   from dotenv import load_dotenv"
    echo "   sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))"
    echo "   from app.database import Base"
    echo "   from app import models"
    echo ""
    echo "2. In the same file, after the Alembic config, add:"
    echo "   load_dotenv()"
    echo "   config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))"
    echo ""
    echo "3. Replace 'target_metadata = None' with:"
    echo "   target_metadata = Base.metadata"
    echo ""
    echo "4. In alembic.ini, comment out or remove the sqlalchemy.url line"
    echo ""
    read -p "Press Enter after you've made these changes..."
    
    echo ""
    echo -e "${YELLOW}Creating initial database migration...${NC}"
    alembic revision --autogenerate -m "Initial database schema"
    echo -e "${GREEN}✓ Migration created${NC}"
    
    echo ""
    echo -e "${YELLOW}Applying migrations to database...${NC}"
    alembic upgrade head
    echo -e "${GREEN}✓ Database tables created${NC}"
else
    echo -e "${GREEN}✓ Alembic already initialized${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "  Setup Complete! 🎉"
echo "==========================================${NC}"
echo ""
echo "To start the development server, run:"
echo -e "${YELLOW}uvicorn app.main:app --reload${NC}"
echo ""
echo "Then visit:"
echo "  - API: http://127.0.0.1:8000"
echo "  - Docs: http://127.0.0.1:8000/docs"
echo "  - ReDoc: http://127.0.0.1:8000/redoc"
echo ""
