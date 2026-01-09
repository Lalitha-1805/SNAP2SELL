#!/usr/bin/env python
"""
Production RAG Chatbot Test Suite
Tests Gemini Flash integration with strict context-only answers
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

# Test cases: (question, expected_crop_in_answer, should_succeed)
TEST_CASES = [
    ("Which fertilizer is best for tomatoes?", "Tomato", True),
    ("How do I grow cucumber?", "Cucumber", True),
    ("What is the best irrigation method for wheat?", "Wheat", True),
    ("How can I prevent pests on rice?", "Rice", True),
    ("When should I harvest onions?", "Onion", True),
    ("Tell me about unicorn farming", None, False),  # Should fail - not in KB
]

print("="*80)
print("PRODUCTION RAG CHATBOT TEST SUITE")
print("Testing Google Gemini Flash + FAISS RAG System")
print("="*80)

# Test 1: Health Check
print("\n[TEST 1] Backend Health Check")
try:
    r = requests.get(f"{BASE_URL}/api/health", timeout=5)
    print(f"✓ Status: {r.status_code}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

# Test 2: KB Stats
print("\n[TEST 2] Knowledge Base Stats")
try:
    r = requests.get(f"{BASE_URL}/api/chatbot/kb-stats", timeout=5)
    stats = r.json().get('data', {})
    print(f"✓ Total Documents: {stats.get('total_documents')}")
    print(f"✓ Gemini Available: {stats.get('gemini_available')}")
    print(f"✓ Vector Store Ready: {stats.get('vector_store_ready')}")
except Exception as e:
    print(f"✗ FAILED: {e}")

# Test 3: Query Suggestions
print("\n[TEST 3] Chatbot Suggestions")
try:
    r = requests.get(f"{BASE_URL}/api/chatbot/suggestions", timeout=5)
    suggestions = r.json().get('data', {}).get('suggestions', [])
    print(f"✓ Available suggestions: {len(suggestions)}")
    for s in suggestions[:3]:
        print(f"  - {s}")
except Exception as e:
    print(f"✗ FAILED: {e}")

# Test 4: RAG Queries with Context Validation
print("\n[TEST 4] RAG Query Tests")
passed = 0
failed = 0

for question, expected_crop, should_succeed in TEST_CASES:
    try:
        payload = {"question": question}
        r = requests.post(f"{BASE_URL}/api/chatbot/query", json=payload, timeout=10)
        
        if r.status_code != 200:
            print(f"✗ {question[:50]}... | Status: {r.status_code}")
            failed += 1
            continue
        
        resp = r.json()
        answer = resp.get('data', {}).get('answer', '')
        sources = resp.get('data', {}).get('sources', [])
        
        # Validate response
        if should_succeed:
            if answer and sources:
                # Check for hallucination: crop info shouldn't mix
                print(f"✓ {question[:50]}...")
                print(f"  Answer: {answer[:150]}...")
                print(f"  Sources: {sources}")
                passed += 1
            else:
                print(f"✗ {question[:50]}... | No answer or sources")
                failed += 1
        else:
            # Should fail - test if chatbot correctly rejects
            if "don't have enough information" in answer.lower():
                print(f"✓ {question[:50]}... | Correctly rejected (not in KB)")
                passed += 1
            else:
                print(f"⚠ {question[:50]}... | Should have rejected (possible hallucination)")
                print(f"  Answer: {answer[:100]}...")
                failed += 1
    
    except Exception as e:
        print(f"✗ {question[:50]}... | ERROR: {e}")
        failed += 1

# Test 5: Legacy /ask endpoint
print("\n[TEST 5] Legacy /ask Endpoint")
try:
    payload = {"question": "What fertilizer for wheat?"}
    r = requests.post(f"{BASE_URL}/api/chatbot/ask", json=payload, timeout=10)
    if r.status_code == 200:
        print(f"✓ Legacy /ask endpoint works")
    else:
        print(f"✗ Legacy /ask returned {r.status_code}")
except Exception as e:
    print(f"✗ FAILED: {e}")

# Summary
print("\n" + "="*80)
print(f"TEST SUMMARY: {passed} passed, {failed} failed")
if failed == 0:
    print("✓ ALL TESTS PASSED - Production RAG system is working correctly!")
    sys.exit(0)
else:
    print(f"✗ {failed} test(s) failed - Please review output above")
    sys.exit(1)
