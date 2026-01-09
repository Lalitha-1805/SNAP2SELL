#!/usr/bin/env python
"""Quick test of production RAG chatbot"""

import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

# Test 1: Health
print('[TEST 1] Health Check')
try:
    r = requests.get(f'{BASE_URL}/api/health', timeout=5)
    print(f'✓ Status: {r.status_code}')
except Exception as e:
    print(f'✗ Error: {e}')

# Test 2: KB Stats  
print('\n[TEST 2] KB Stats')
try:
    r = requests.get(f'{BASE_URL}/api/chatbot/kb-stats', timeout=5)
    data = r.json().get('data', {})
    print(f'✓ Total Docs: {data.get("total_documents")}')
    print(f'✓ Gemini Available: {data.get("gemini_available")}')
    print(f'✓ Vector Store Ready: {data.get("vector_store_ready")}')
except Exception as e:
    print(f'✗ Error: {e}')

# Test 3: Query - Tomato Fertilizer
print('\n[TEST 3] Query - Tomato Fertilizer')
try:
    r = requests.post(f'{BASE_URL}/api/chatbot/query', 
        json={'question': 'Which fertilizer is best for tomatoes?'}, timeout=15)
    print(f'Status: {r.status_code}')
    resp = r.json()
    answer = resp.get('data', {}).get('answer', '')
    sources = resp.get('data', {}).get('sources', [])
    print(f'Answer: {answer[:150]}...')
    print(f'Sources Found: {len(sources)}')
    if sources:
        print(f'  - {sources[0]}')
except Exception as e:
    print(f'✗ Error: {e}')

# Test 4: Query - Non-existent crop (hallucination test)
print('\n[TEST 4] Query - Non-existent Crop (Hallucination Test)')
try:
    r = requests.post(f'{BASE_URL}/api/chatbot/query', 
        json={'question': 'How do I grow bananas?'}, timeout=15)
    print(f'Status: {r.status_code}')
    resp = r.json()
    answer = resp.get('data', {}).get('answer', '')
    print(f'Answer: {answer[:150]}...')
    if "don't have enough information" in answer.lower():
        print('✓ Correctly rejected (no hallucination)')
    else:
        print('⚠ May have hallucinated')
except Exception as e:
    print(f'✗ Error: {e}')

print('\n' + '='*60)
print('Test complete')
