"""
Seed database with sample agricultural products
"""

import sys
sys.path.insert(0, '/root')

from models import User, Product
from extensions import init_mongo, get_db
from flask import Flask
from config import config

app = Flask(__name__)
app.config.from_object(config)

# Initialize MongoDB
init_mongo(app)

def seed_products():
    """Add sample products to database"""
    
    try:
        # Get database
        db = get_db()
        if not db:
            print("ERROR: Could not connect to database")
            return
        
        # First, create a sample farmer if doesn't exist
        farmer_email = "farmer@agrismart.com"
        farmer = User.find_by_email(farmer_email)
        
        if not farmer:
            print("Creating sample farmer...")
            farmer_id = User.create_user(
                email=farmer_email,
                password="farmer123",
                name="John Farmer",
                role="farmer",
                phone="9876543210",
                address="Punjab, India"
            )
            farmer = User.find_by_id(farmer_id)
            print(f"[OK] Farmer created: {farmer_email}")
        else:
            print(f"[OK] Farmer already exists: {farmer_email}")
            farmer_id = farmer['_id']
        
        # Sample products
        sample_products = [
            {
                "name": "Fresh Tomatoes",
                "category": "Vegetables",
                "description": "Locally grown, pesticide-free tomatoes. Perfect for cooking and salads.",
                "price": 45,
                "quantity": 500,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Tomatoes",
                "quality_rating": 4.5,
                "is_active": True
            },
            {
                "name": "Organic Carrots",
                "category": "Vegetables",
                "description": "Fresh orange carrots packed with nutrients. Grown using organic methods.",
                "price": 35,
                "quantity": 300,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Carrots",
                "quality_rating": 4.7,
                "is_active": True
            },
            {
                "name": "Premium Basmati Rice",
                "category": "Grains",
                "description": "Long grain basmati rice with aromatic flavor. 1 kg packs.",
                "price": 120,
                "quantity": 1000,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Basmati+Rice",
                "quality_rating": 4.8,
                "is_active": True
            },
            {
                "name": "Wheat Grains",
                "category": "Grains",
                "description": "High-quality wheat for grinding and bread making. Direct from farm.",
                "price": 55,
                "quantity": 2000,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Wheat",
                "quality_rating": 4.6,
                "is_active": True
            },
            {
                "name": "Fresh Apples",
                "category": "Fruits",
                "description": "Crispy red apples. Fresh from the orchard. 2kg box.",
                "price": 150,
                "quantity": 200,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Apples",
                "quality_rating": 4.9,
                "is_active": True
            },
            {
                "name": "Organic Turmeric Powder",
                "category": "Spices",
                "description": "Pure turmeric powder with high curcumin content. 500g pack.",
                "price": 250,
                "quantity": 100,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Turmeric",
                "quality_rating": 4.7,
                "is_active": True
            },
            {
                "name": "Fresh Onions",
                "category": "Vegetables",
                "description": "Sweet golden onions. Perfect for cooking. 5kg bag.",
                "price": 80,
                "quantity": 800,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Onions",
                "quality_rating": 4.5,
                "is_active": True
            },
            {
                "name": "Organic Potatoes",
                "category": "Vegetables",
                "description": "Starchy potatoes. Great for curries and fries. 10kg bag.",
                "price": 200,
                "quantity": 500,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Potatoes",
                "quality_rating": 4.6,
                "is_active": True
            },
            {
                "name": "Fresh Spinach",
                "category": "Vegetables",
                "description": "Leafy green spinach. Rich in iron and nutrients. 500g bundles.",
                "price": 30,
                "quantity": 200,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Spinach",
                "quality_rating": 4.4,
                "is_active": True
            },
            {
                "name": "Sweet Corn",
                "category": "Vegetables",
                "description": "Fresh sweet corn. Locally grown. 6 pieces per pack.",
                "price": 60,
                "quantity": 150,
                "farmer_id": farmer_id,
                "image_url": "https://via.placeholder.com/300x200?text=Corn",
                "quality_rating": 4.7,
                "is_active": True
            }
        ]
        
        # Add products to database
        count = 0
        for product_data in sample_products:
            # Check if product already exists
            existing = Product.find_one({
                "name": product_data["name"],
                "farmer_id": farmer_id
            })
            
            if not existing:
                Product.create(product_data)
                count += 1
                print(f"[OK] Added: {product_data['name']} - {product_data['price']}")
            else:
                print(f"[SKIP] Already exists: {product_data['name']}")
        
        print(f"\n[OK] Database seeded successfully! Added {count} new products.")
        print(f"[OK] Total products now: {Product.get_collection().count_documents({})}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    with app.app_context():
        seed_products()
