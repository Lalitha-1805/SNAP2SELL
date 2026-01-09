"""
RAG package initialization
"""

# Use the simplified chatbot implementation
from .chatbot import SimpleRAGChatbot as RAGChatbot, rag_chatbot

__all__ = ['RAGChatbot', 'rag_chatbot']
