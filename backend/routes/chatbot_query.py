from flask import Blueprint, request, jsonify
from rag.chatbot import rag_chatbot
from utils.errors import BadRequestError

chatbot_query_bp = Blueprint('chatbot_query', __name__, url_prefix='/api/chatbot')

@chatbot_query_bp.route('/query', methods=['POST'])
def query_chatbot():
    try:
        data = request.get_json() or {}
        question = data.get('question', '').strip()
        if not question:
            raise BadRequestError('Question cannot be empty')
        if len(question) > 2000:
            raise BadRequestError('Question too long')

        # Use the RAG chatbot's answer_query (compatible)
        result = rag_chatbot.answer_query(question)
        answer = result.get('answer')
        category = result.get('sources')[0] if result.get('sources') else result.get('category', 'general')

        return jsonify({'answer': answer, 'category': category}), 200
    except BadRequestError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Query failed'}), 500
