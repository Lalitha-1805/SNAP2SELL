"""
Routes package initialization
"""

from routes.auth import auth_bp
from routes.products import products_bp
from routes.orders import orders_bp
from routes.reviews import reviews_bp
from routes.ml import ml_bp
from routes.chatbot import chatbot_bp

__all__ = [
    'auth_bp', 'products_bp', 'orders_bp', 'reviews_bp', 'ml_bp', 'chatbot_bp'
]
