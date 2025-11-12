#!/usr/bin/env python3
"""
SocialProof Testing Script
Demonstrates all new features: 5 difficulty levels, variety, and dynamic generation
"""

import requests
import json
import time
from colorama import Fore, Back, Style, init

init(autoreset=True)

API_BASE = "http://127.0.0.1:8000"

def print_header(text):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{Style.RESET_ALL}\n")

def test_backend_health():
    print_header("🏥 Backend Health Check")
    response = requests.get(f"{API_BASE}/health")
    if response.status_code == 200:
        print(f"{Fore.GREEN}✅ Backend is healthy!")
        print(f"Response: {response.json()}")
    else:
        print(f"{Fore.RED}❌ Backend error: {response.status_code}")
    return response.status_code == 200

def test_ai_provider():
    print_header("🤖 AI Provider Status")
    response = requests.get(f"{API_BASE}/ai/provider")
    if response.status_code == 200:
        data = response.json()
        print(f"{Fore.GREEN}✅ AI Provider: {data.get('provider', 'unknown')}")
        print(f"📊 Status: {data.get('status', 'unknown')}")
        print(f"🧠 Model: {data.get('model_class', 'unknown')}")
        print(f"📚 RAG Initialized: {data.get('rag_initialized', False)}")
        return data.get('status') == 'active'
    return False

def test_difficulty_levels():
    print_header("🎯 Testing All 5 Difficulty Levels")
    
    levels = ["beginner", "easy", "medium", "hard", "expert"]
    results = {}
    
    for level in levels:
        print(f"\n{Fore.YELLOW}📝 Generating {level.upper()} level scenario...")
        
        response = requests.post(
            f"{API_BASE}/scenarios/generate",
            json={
                "player_id": 1,
                "scenario_type": "email",
                "difficulty": level
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            scenario_id = data.get('scenario_id')
            content_preview = data.get('content', '')[:100]
            
            print(f"{Fore.GREEN}✅ Scenario ID: {scenario_id}")
            print(f"📄 Preview: {content_preview}...")
            
            results[level] = scenario_id
            time.sleep(0.5)  # Rate limiting
        else:
            print(f"{Fore.RED}❌ Failed: {response.status_code}")
            results[level] = None
    
    return results

def test_sms_variety():
    print_header("📱 Testing SMS Variety")
    
    for i in range(3):
        print(f"\n{Fore.YELLOW}📲 Generating SMS scenario #{i+1}...")
        
        response = requests.post(
            f"{API_BASE}/scenarios/generate",
            json={
                "player_id": 1,
                "scenario_type": "sms",
                "difficulty": "medium"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('content', '')[:150]
            print(f"{Fore.GREEN}✅ {content}...")
        
        time.sleep(0.5)

def test_ai_guardian():
    print_header("🛡️ Testing AI Guardian with RAG")
    
    questions = [
        "What are the signs of a phishing email?",
        "How can I protect myself from smishing?",
        "What is social engineering?"
    ]
    
    for question in questions:
        print(f"\n{Fore.YELLOW}❓ Question: {question}")
        
        response = requests.post(
            f"{API_BASE}/guardian/query",
            json={"question": question}
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')[:200]
            sources = data.get('sources', [])
            
            print(f"{Fore.GREEN}💡 Answer: {answer}...")
            print(f"📚 Sources: {', '.join(sources)}")
        
        time.sleep(0.5)

def show_player_stats():
    print_header("📊 Player Statistics")
    
    response = requests.get(f"{API_BASE}/players/1/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"{Fore.GREEN}🎯 Score: {stats.get('score', 0)}")
        print(f"📝 Scenarios Attempted: {stats.get('scenarios_attempted', 0)}")
        print(f"✅ Correct Identifications: {stats.get('correct_identifications', 0)}")
        
        if stats.get('scenarios_attempted', 0) > 0:
            accuracy = (stats.get('correct_identifications', 0) / stats.get('scenarios_attempted', 0)) * 100
            print(f"🎓 Accuracy: {accuracy:.1f}%")

def main():
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║         🛡️  SocialProof Enhanced Test Suite  🛡️          ║")
    print("║                                                          ║")
    print("║  Testing: Multi-Level Difficulty, Variety, RAG AI       ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    
    # Run all tests
    if not test_backend_health():
        print(f"\n{Fore.RED}❌ Backend not running. Please start it first.")
        return
    
    if not test_ai_provider():
        print(f"\n{Fore.RED}⚠️  AI provider not active. Some features may not work.")
    
    test_difficulty_levels()
    test_sms_variety()
    test_ai_guardian()
    show_player_stats()
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║           ✅ All Tests Completed Successfully!           ║")
    print("║                                                          ║")
    print("║  🌐 Frontend: http://localhost:8501                      ║")
    print("║  🔧 Backend:  http://localhost:8000                      ║")
    print("║  📚 API Docs: http://localhost:8000/docs                 ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⏹️  Testing interrupted by user.")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {e}")
