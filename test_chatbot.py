#!/usr/bin/env python
"""
Test script to verify chatbot is working with intelligent responses
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000/api"

# Test questions covering different agricultural topics
test_questions = [
    "How to grow crops",
    "soil health tips",
    "water management for farming",
    "pest control in agriculture",
    "best fertilizer recommendations",
    "current crop prices",
    "how to cook potatoes",  # Should still give farming advice
    "weather forecast"
]

print("=" * 60)
print("AgriSmart Chatbot Test - Intelligent Fallback Responses")
print("=" * 60)

for question in test_questions:
    print(f"\n[Q] {question}")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/chatbot/ask",
            json={"question": question},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('data', {}).get('answer', 'No answer')
            sources = data.get('data', {}).get('sources', [])
            
            # Truncate long answers for readability
            answer_display = answer[:200] + "..." if len(answer) > 200 else answer
            print(f"[A] {answer_display}")
            
            if sources:
                print(f"[Sources] {', '.join(sources)}")
            print(f"[Status] ✓ Success")
        else:
            print(f"[Error] HTTP {response.status_code}: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("[Error] Cannot connect to backend. Is the server running?")
        break
    except Exception as e:
        print(f"[Error] {type(e).__name__}: {str(e)}")
    
    time.sleep(0.5)

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
