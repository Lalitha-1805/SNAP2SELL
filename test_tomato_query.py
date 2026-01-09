#!/usr/bin/env python
"""Quick test of enhanced chatbot for tomato fertilizer queries"""

import sys
sys.path.insert(0, r'C:\Users\HP\Desktop\agri e commerce\agri-smart\backend')

from rag.chatbot import rag_chatbot

queries = [
    'what fertilizer used for tomatoes',
    'tomato fertilizer NPK dosage',
    'how to apply DAP for tomato crop',
]

for q in queries:
    print(f"\n{'='*80}")
    print(f"QUERY: {q}")
    print(f"{'='*80}")
    result = rag_chatbot.answer_query(q)
    print(result['answer'])
    print(f"\nSources: {result.get('sources', [])}")
    print(f"Confidence: {'high' if result.get('context_count', 0) > 0 else 'low'}")
