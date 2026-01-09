#!/usr/bin/env python
"""Test Internal RAG Chatbot API"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("="*80)
print("TESTING AGRISMART RAG CHATBOT")
print("="*80)

# Test 1: Health check
print("\n[TEST 1] Health Check")
try:
    r = requests.get(f"{BASE_URL}/api/health", timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
except Exception as e:
    print(f"FAILED: {e}")

# Test 2: Get API info
print("\n[TEST 2] API Info")
try:
    r = requests.get(f"{BASE_URL}/api/info", timeout=5)
    print(f"Status: {r.status_code}")
    info = r.json()
    print(f"Available endpoints: {list(info.get('data', {}).get('endpoints', {}).keys())}")
except Exception as e:
    print(f"FAILED: {e}")

# Test 3: Chatbot /ask endpoint
print("\n[TEST 3] Chatbot /ask endpoint")
try:
    payload = {"question": "What crops should I grow in monsoon?"}
    r = requests.post(f"{BASE_URL}/api/chatbot/ask", json=payload, timeout=5)
    print(f"Status: {r.status_code}")
    resp = r.json()
    if resp.get('status') == 'success':
        print(f"Answer: {resp.get('data', {}).get('answer')[:200]}...")
        print(f"Sources: {resp.get('data', {}).get('sources')}")
    else:
        print(f"Error: {resp.get('message')}")
except Exception as e:
    print(f"FAILED: {e}")

# Test 4: NEW Chatbot /query endpoint (Internal RAG)
print("\n[TEST 4] Chatbot /query endpoint (Internal RAG)")
try:
    payload = {"question": "Which fertilizer is best for tomatoes?"}
    r = requests.post(f"{BASE_URL}/api/chatbot/query", json=payload, timeout=5)
    print(f"Status: {r.status_code}")
    resp = r.json()
    if resp.get('status') == 'success':
        data = resp.get('data', {})
        print(f"Question: {data.get('question')}")
        print(f"Answer: {data.get('answer')[:300]}...")
        print(f"Category: {data.get('category')}")
        print(f"Sources: {data.get('sources')}")
    else:
        print(f"Error: {resp.get('message')}")
except Exception as e:
    print(f"FAILED: {e}")

# Test 5: Chatbot suggestions
print("\n[TEST 5] Chatbot suggestions")
try:
    r = requests.get(f"{BASE_URL}/api/chatbot/suggestions", timeout=5)
    print(f"Status: {r.status_code}")
    resp = r.json()
    suggestions = resp.get('data', {}).get('suggestions', [])
    print(f"Suggestions: {suggestions[:3]}")
except Exception as e:
    print(f"FAILED: {e}")

# Test 6: KB stats
print("\n[TEST 6] Knowledge Base Stats")
try:
    r = requests.get(f"{BASE_URL}/api/chatbot/kb-stats", timeout=5)
    print(f"Status: {r.status_code}")
    resp = r.json()
    stats = resp.get('data', {})
    print(f"KB Entries: {stats.get('kb_entries')}")
    print(f"Chunks: {stats.get('chunks')}")
    print(f"Status: {stats.get('status')}")
except Exception as e:
    print(f"FAILED: {e}")

print("\n" + "="*80)
print("TEST COMPLETED")
print("="*80)
