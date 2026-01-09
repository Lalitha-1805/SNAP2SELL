"""
Flask extensions initialization
Centralized management of Flask extensions
"""

from flask_jwt_extended import JWTManager
from flask_cors import CORS
from pymongo import MongoClient
from flask_restful import Api

# JWT Extension
jwt = JWTManager()

# CORS Extension
cors = CORS

# API Extension
api = Api()

# MongoDB Client
mongo_client = None
db = None


def init_mongo(app):
    """Initialize MongoDB connection"""
    global mongo_client, db
    
    from config import config
    
    mongo_uri = config.MONGODB_URI
    db_name = config.MONGODB_DB_NAME
    
    try:
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = mongo_client[db_name]
        
        # Verify connection
        mongo_client.admin.command('ismaster')
        print("[OK] MongoDB connected successfully")
    except Exception as e:
        print(f"[WARNING] MongoDB connection failed: {str(e)}")
        print("[WARNING] App will start without database (read-only mode)")
        mongo_client = None
        db = None


def get_db():
    """Get MongoDB database instance"""
    global db
    if db is None:
        return None  # Return None instead of raising, allowing graceful degradation
    return db


def close_mongo():
    """Close MongoDB connection"""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("[OK] MongoDB connection closed")
