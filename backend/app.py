"""
AgriSmart Main Application
Flask application initialization and configuration
"""

# Load environment variables FIRST, before any other imports
from dotenv import load_dotenv
import os
load_dotenv()  # Load from .env file

from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from extensions import jwt, api, init_mongo, get_db, close_mongo
from models import create_indexes
from automation import automation_manager
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name='development'):
    """Application factory"""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config)
    
    # Initialize extensions
    jwt.init_app(app)
    api.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})
    
    # Initialize MongoDB
    with app.app_context():
        init_mongo(app)
        create_indexes()
    
    # Register blueprints
    from routes import auth_bp, products_bp, orders_bp, ml_bp, chatbot_bp, reviews_bp
    # Register core chatbot blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(ml_bp)
    app.register_blueprint(chatbot_bp)
    # Register error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'status': 'error', 'message': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'status': 'error', 'message': 'Forbidden'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            'status': 'running',
            'message': 'AgriSmart Backend is Live [OK]',
            'api_info': '/api/info',
            'health': '/api/health'
        }), 200
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'AgriSmart Backend'
        }), 200
    
    # API Info endpoint
    @app.route('/api/info', methods=['GET'])
    def api_info():
        return jsonify({
            'status': 'success',
            'data': {
                'name': 'AgriSmart - AI-Powered Agriculture E-Commerce Platform',
                'version': '1.0.0',
                'description': 'Complete agriculture e-commerce platform with ML and RAG',
                'endpoints': {
                    'auth': '/api/auth',
                    'products': '/api/products',
                    'orders': '/api/orders',
                    'ml': '/api/ml',
                    'chatbot': '/api/chatbot'
                }
            }
        }), 200
    
    # Database info endpoint
    @app.route('/api/database-info', methods=['GET'])
    def database_info():
        try:
            db = get_db()
            collections = db.list_collection_names()
            return jsonify({
                'status': 'success',
                'data': {
                    'database': db.name,
                    'collections': collections,
                    'collection_count': len(collections)
                }
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Database info failed: {str(e)}'
            }), 500
    
    # Scheduler status endpoint
    @app.route('/api/scheduler-status', methods=['GET'])
    def scheduler_status():
        status = automation_manager.get_job_status()
        return jsonify({
            'status': 'success',
            'data': status
        }), 200
    
    # Start automation scheduler
    automation_manager.start()
    
    logger.info("[OK] Flask application initialized successfully")
    
    return app


# Create app instance for WSGI servers (Waitress, Gunicorn)
app = create_app()


if __name__ == '__main__':
    print("""
    ===================================================================
      AgriSmart - AI-Powered Agriculture E-Commerce
      Backend Server Started
    ===================================================================
    """)
    
    print(f"[START] Server running on http://{config.SERVER_HOST}:{config.SERVER_PORT}")
    print(f"[API] Documentation: http://{config.SERVER_HOST}:{config.SERVER_PORT}/api/info")
    print(f"[DB] Database: {config.MONGODB_DB_NAME}")
    print(f"[JWT] JWT Enabled: Yes")
    print(f"[ML] ML Models: Crop Recommendation, Price Prediction, Product Recommendation")
    print(f"[AI] RAG Chatbot: Enabled")
    print(f"[AUTO] Automation: Enabled\n")
    
    app.run(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        debug=config.DEBUG
    )
