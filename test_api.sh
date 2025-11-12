#!/bin/bash

# Test script to verify the SocialProof backend is working correctly

echo "=========================================="
echo "  SocialProof Backend Test Suite"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="http://127.0.0.1:8000"

# Check if server is running
echo "1. Testing API connectivity..."
if curl -s -f "${BASE_URL}/" > /dev/null; then
    echo -e "${GREEN}✓ API is accessible${NC}"
else
    echo -e "${RED}✗ API is not accessible. Make sure the server is running with:${NC}"
    echo "  uvicorn app.main:app --reload"
    exit 1
fi

# Test root endpoint
echo ""
echo "2. Testing root endpoint..."
RESPONSE=$(curl -s "${BASE_URL}/")
if echo "$RESPONSE" | grep -q "Welcome to the SocialProof API"; then
    echo -e "${GREEN}✓ Root endpoint working${NC}"
    echo "   Response: $RESPONSE"
else
    echo -e "${RED}✗ Root endpoint failed${NC}"
fi

# Test health check
echo ""
echo "3. Testing health check..."
RESPONSE=$(curl -s "${BASE_URL}/health")
if echo "$RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
fi

# Create a test player
echo ""
echo "4. Creating a test player..."
TIMESTAMP=$(date +%s)
RESPONSE=$(curl -s -X POST "${BASE_URL}/players/" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"test_user_${TIMESTAMP}\",\"email\":\"test_${TIMESTAMP}@example.com\"}")

if echo "$RESPONSE" | grep -q "player_skill_rating"; then
    echo -e "${GREEN}✓ Player created successfully${NC}"
    PLAYER_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
    echo "   Player ID: $PLAYER_ID"
    echo "   Response: $RESPONSE"
else
    echo -e "${RED}✗ Player creation failed${NC}"
    echo "   Response: $RESPONSE"
    exit 1
fi

# Retrieve the player
echo ""
echo "5. Retrieving the created player..."
RESPONSE=$(curl -s "${BASE_URL}/players/${PLAYER_ID}")
if echo "$RESPONSE" | grep -q "test_user_${TIMESTAMP}"; then
    echo -e "${GREEN}✓ Player retrieved successfully${NC}"
else
    echo -e "${RED}✗ Player retrieval failed${NC}"
fi

# List all players
echo ""
echo "6. Listing all players..."
RESPONSE=$(curl -s "${BASE_URL}/players/")
if echo "$RESPONSE" | grep -q "\["; then
    echo -e "${GREEN}✓ Players list retrieved${NC}"
    PLAYER_COUNT=$(echo "$RESPONSE" | grep -o "\"id\":" | wc -l | tr -d ' ')
    echo "   Total players: $PLAYER_COUNT"
else
    echo -e "${RED}✗ Players list failed${NC}"
fi

# Test duplicate email
echo ""
echo "7. Testing duplicate email validation..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/players/" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"another_user\",\"email\":\"test_${TIMESTAMP}@example.com\"}")
HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
if [ "$HTTP_CODE" = "400" ]; then
    echo -e "${GREEN}✓ Duplicate email correctly rejected${NC}"
else
    echo -e "${RED}✗ Duplicate email validation failed (HTTP $HTTP_CODE)${NC}"
fi

# Test 404 for non-existent player
echo ""
echo "8. Testing 404 for non-existent player..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${BASE_URL}/players/99999")
HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
if [ "$HTTP_CODE" = "404" ]; then
    echo -e "${GREEN}✓ 404 error correctly returned${NC}"
else
    echo -e "${RED}✗ 404 test failed (HTTP $HTTP_CODE)${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "  All Tests Completed! ✨"
echo "==========================================${NC}"
echo ""
echo "API Documentation available at:"
echo "  - Swagger UI: ${BASE_URL}/docs"
echo "  - ReDoc: ${BASE_URL}/redoc"
echo ""
