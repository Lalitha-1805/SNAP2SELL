"""
Chatbot Routes
API endpoints for RAG chatbot functionality
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.chatbot_service import ChatbotService
from utils.errors import BadRequestError
import os
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Initialize chatbot service
chatbot_service = ChatbotService()



@chatbot_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get common agricultural question suggestions"""
    suggestions = [
        "Which fertilizer is best for tomatoes?",
        "How do I grow cucumber?",
        "What is the best irrigation method for wheat?",
        "How can I prevent pests on rice?",
        "When should I harvest onions?",
        "What fertilizer for cotton?",
        "How to grow potatoes?",
        "When to plant wheat?"
    ]
    
    return jsonify({
        'status': 'success',
        'data': {
            'suggestions': suggestions
        }
    }), 200


@chatbot_bp.route('/ask', methods=['POST'])
def ask_question():
    """Legacy endpoint - use /query instead"""
    return query_internal_rag()


@chatbot_bp.route('/add-document', methods=['POST'])
@jwt_required()
def add_knowledge_document():
    """Add a new document to the knowledge base (admin only) - Not supported in production RAG"""
    return jsonify({'status': 'error', 'message': 'Document addition not supported. KB is pre-built.'}), 403


@chatbot_bp.route('/ask-image', methods=['POST'])
def ask_image():
    """Accept an image and optional question for disease diagnosis (future feature)"""
    return jsonify({'status': 'error', 'message': 'Image analysis coming soon'}), 501


@chatbot_bp.route('/query', methods=['POST'])
def query_internal_rag():
    """Query internal self-contained agriculture RAG knowledge base with Gemini Flash"""
    try:
        data = request.get_json() or {}
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'status': 'error', 'message': 'Question cannot be empty'}), 400
        
        if len(question) > 2000:
            return jsonify({'status': 'error', 'message': 'Question too long (max 2000 characters)'}), 400
        
        # Use production RAG chatbot service
        result = chatbot_service.query(question)
        
        return jsonify({
            'status': result.get('status'),
            'data': {
                'question': question,
                'answer': result.get('answer'),
                'sources': result.get('sources', [])
            }
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Query failed: {str(e)}'}), 500


@chatbot_bp.route('/kb-stats', methods=['GET'])
def get_knowledge_base_stats():
    """Get knowledge base and system statistics"""
    try:
        stats = chatbot_service.get_stats()
        return jsonify({
            'status': 'success',
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@chatbot_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Get user's chat history (placeholder)"""
    return jsonify({
        'status': 'success',
        'data': {
            'message': 'Chat history feature coming soon'
        }
    }), 200
