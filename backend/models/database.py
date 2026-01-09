"""
Database Models using PyMongo
Define MongoDB collection schemas and operations
"""

from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from extensions import get_db
import hashlib


class BaseModel:
    """Base model for common operations"""
    
    collection_name = None
    
    @classmethod
    def get_collection(cls):
        """Get MongoDB collection"""
        if cls.collection_name is None:
            raise NotImplementedError("collection_name must be defined")
        return get_db()[cls.collection_name]
    
    @classmethod
    def create(cls, data):
        """Create a new document"""
        doc = {
            **data,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = cls.get_collection().insert_one(doc)
        return result.inserted_id
    
    @classmethod
    def find_by_id(cls, doc_id):
        """Find document by ID"""
        try:
            if isinstance(doc_id, str):
                doc_id = ObjectId(doc_id)
            return cls.get_collection().find_one({'_id': doc_id})
        except (InvalidId, ValueError) as e:
            # Invalid ObjectId format
            return None
    
    @classmethod
    def find_one(cls, query):
        """Find single document"""
        return cls.get_collection().find_one(query)
    
    @classmethod
    def find_many(cls, query, limit=None, skip=None):
        """Find multiple documents"""
        cursor = cls.get_collection().find(query)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    
    @classmethod
    def update(cls, doc_id, data):
        """Update document"""
        if isinstance(doc_id, str):
            doc_id = ObjectId(doc_id)
        
        update_data = {
            **data,
            'updated_at': datetime.utcnow()
        }
        
        result = cls.get_collection().update_one(
            {'_id': doc_id},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @classmethod
    def delete(cls, doc_id):
        """Delete document"""
        if isinstance(doc_id, str):
            doc_id = ObjectId(doc_id)
        result = cls.get_collection().delete_one({'_id': doc_id})
        return result.deleted_count > 0
    
    @classmethod
    def delete_many(cls, query):
        """Delete multiple documents"""
        result = cls.get_collection().delete_many(query)
        return result.deleted_count
    
    @classmethod
    def count(cls, query=None):
        """Count documents"""
        if query is None:
            query = {}
        return cls.get_collection().count_documents(query)


class User(BaseModel):
    """User model for farmers, buyers, and admins"""
    collection_name = 'users'
    
    # Accept both 'buyer' and 'consumer' to be compatible with frontend
    ROLES = ['farmer', 'buyer', 'consumer', 'admin']
    
    @classmethod
    def create_user(cls, email, password, name, role='buyer', phone=None, address=None):
        """Create a new user with hashed password"""
        
        # Check if user already exists
        if cls.find_one({'email': email}):
            raise ValueError(f"User with email {email} already exists")
        
        if role not in cls.ROLES:
            raise ValueError(f"Invalid role. Must be one of {cls.ROLES}")
        
        # Hash password
        password_hash = cls._hash_password(password)
        
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'name': name,
            'role': role,
            'phone': phone,
            'address': address,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        return cls.create(user_data)
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        return cls.find_one({'email': email})
    
    @classmethod
    def verify_password(cls, user, password):
        """Verify password"""
        if not user:
            return False
        password_hash = cls._hash_password(password)
        return user.get('password_hash') == password_hash
    
    @staticmethod
    def _hash_password(password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()


class Product(BaseModel):
    """Product model for crops and agricultural items"""
    collection_name = 'products'
    
    # Include categories used by frontend (Vegetables, Grains, Fruits, Spices)
    CATEGORIES = [
        'crops', 'seeds', 'fertilizers', 'tools', 'equipment',
        'Vegetables', 'Grains', 'Fruits', 'Spices'
    ]
    
    @classmethod
    def create_product(cls, farmer_id, name, category, description, price, quantity, 
                      soil_type=None, season=None, quality_grade=None, image_url=None):
        """Create a new product"""
        
        if category not in cls.CATEGORIES:
            raise ValueError(f"Invalid category. Must be one of {cls.CATEGORIES}")
        
        product_data = {
            'farmer_id': ObjectId(farmer_id) if isinstance(farmer_id, str) else farmer_id,
            'name': name,
            'category': category,
            'description': description,
            'price': price,
            'quantity': quantity,
            'soil_type': soil_type,
            'season': season,
            'quality_grade': quality_grade,
            'image_url': image_url,
            'rating': 0,
            'review_count': 0,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        return cls.create(product_data)
    
    @classmethod
    def find_by_category(cls, category, limit=None, skip=None):
        """Find products by category"""
        return cls.find_many({'category': category, 'is_active': True}, limit=limit, skip=skip)
    
    @classmethod
    def find_by_farmer(cls, farmer_id, limit=None, skip=None):
        """Find products by farmer"""
        if isinstance(farmer_id, str):
            farmer_id = ObjectId(farmer_id)
        return cls.find_many({'farmer_id': farmer_id, 'is_active': True}, limit=limit, skip=skip)


class Order(BaseModel):
    """Order model for purchases"""
    collection_name = 'orders'
    
    STATUSES = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    
    @classmethod
    def create_order(cls, buyer_id, items, total_price, shipping_address):
        """Create a new order"""
        
        order_data = {
            'buyer_id': ObjectId(buyer_id) if isinstance(buyer_id, str) else buyer_id,
            'items': items,  # List of {product_id, quantity, price}
            'total_price': total_price,
            'status': 'pending',
            'shipping_address': shipping_address,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        return cls.create(order_data)
    
    @classmethod
    def find_by_buyer(cls, buyer_id, limit=None, skip=None):
        """Find orders by buyer"""
        if isinstance(buyer_id, str):
            buyer_id = ObjectId(buyer_id)
        return cls.find_many({'buyer_id': buyer_id}, limit=limit, skip=skip)
    
    @classmethod
    def update_status(cls, order_id, new_status):
        """Update order status"""
        if new_status not in cls.STATUSES:
            raise ValueError(f"Invalid status. Must be one of {cls.STATUSES}")
        return cls.update(order_id, {'status': new_status})


class Review(BaseModel):
    """Review model for product ratings"""
    collection_name = 'reviews'
    
    @classmethod
    def create_review(cls, product_id, buyer_id, rating, comment=None):
        """Create a new review"""
        
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        review_data = {
            'product_id': ObjectId(product_id) if isinstance(product_id, str) else product_id,
            'buyer_id': ObjectId(buyer_id) if isinstance(buyer_id, str) else buyer_id,
            'rating': rating,
            'comment': comment,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        return cls.create(review_data)
    
    @classmethod
    def find_by_product(cls, product_id, limit=None, skip=None):
        """Find reviews by product"""
        if isinstance(product_id, str):
            product_id = ObjectId(product_id)
        return cls.find_many({'product_id': product_id}, limit=limit, skip=skip)


class PriceHistory(BaseModel):
    """Price history for market trends"""
    collection_name = 'price_history'
    
    @classmethod
    def record_price(cls, product_id, price, market_price=None):
        """Record product price"""
        
        history_data = {
            'product_id': ObjectId(product_id) if isinstance(product_id, str) else product_id,
            'price': price,
            'market_price': market_price,
            'timestamp': datetime.utcnow()
        }
        
        return cls.create(history_data)
    
    @classmethod
    def get_price_trend(cls, product_id, days=30):
        """Get price trend for a product"""
        if isinstance(product_id, str):
            product_id = ObjectId(product_id)
        
        from datetime import timedelta
        start_date = datetime.utcnow() - timedelta(days=days)
        
        return cls.find_many({
            'product_id': product_id,
            'timestamp': {'$gte': start_date}
        })


class RAGDocument(BaseModel):
    """RAG documents for chatbot knowledge base"""
    collection_name = 'rag_documents'
    
    @classmethod
    def add_document(cls, content, title, category, source_file=None):
        """Add a document to RAG knowledge base"""
        
        doc_data = {
            'content': content,
            'title': title,
            'category': category,
            'source_file': source_file,
            'is_indexed': False,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        return cls.create(doc_data)
    
    @classmethod
    def find_by_category(cls, category):
        """Find documents by category"""
        return cls.find_many({'category': category, 'is_indexed': True})


def create_indexes():
    """Create MongoDB indexes for better query performance"""
    
    # User indexes
    User.get_collection().create_index('email', unique=True)
    
    # Product indexes
    Product.get_collection().create_index('farmer_id')
    Product.get_collection().create_index('category')
    Product.get_collection().create_index([('name', 'text'), ('description', 'text')])
    
    # Order indexes
    Order.get_collection().create_index('buyer_id')
    Order.get_collection().create_index('status')
    
    # Review indexes
    Review.get_collection().create_index('product_id')
    Review.get_collection().create_index('buyer_id')
    
    # Price history indexes
    PriceHistory.get_collection().create_index('product_id')
    PriceHistory.get_collection().create_index('timestamp')
    
    # RAG document indexes
    RAGDocument.get_collection().create_index('category')
    
    print("[OK] All MongoDB indexes created successfully")
