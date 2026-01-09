#!/usr/bin/env python3
"""
Comprehensive API test - Full workflow validation
Tests all major features: Auth, Products, Orders, Reviews, ML, Admin
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'

class TestClient:
    def __init__(self):
        self.consumer_token = None
        self.farmer_token = None
        self.admin_token = None
        self.product_id = None
        self.order_id = None
        
    def log(self, title, result):
        status = "✅ PASS" if result.get('success') else "❌ FAIL"
        print(f"\n{status} | {title}")
        if result.get('error'):
            print(f"   Error: {result['error']}")
        if result.get('data'):
            print(f"   Data: {json.dumps(result['data'], indent=2, default=str)[:200]}")
    
    def test_signup(self):
        """Test user signup"""
        print("\n" + "="*60)
        print("TEST PHASE 1: AUTHENTICATION")
        print("="*60)
        
        # Consumer signup
        response = requests.post(f'{BASE_URL}/auth/signup', json={
            'email': 'test_consumer_v2@example.com',
            'password': 'Test@123456',
            'full_name': 'Test Consumer',
            'phone': '9876543210',
            'role': 'consumer'
        })
        
        result = response.json() if response.status_code in [200, 201] else {'error': response.text}
        if response.status_code in [200, 201]:
            self.consumer_token = result.get('access_token')
            result['success'] = True
        else:
            result['success'] = False
        
        self.log("Consumer Signup", result)
        
        # Farmer signup
        response = requests.post(f'{BASE_URL}/auth/signup', json={
            'email': 'test_farmer_v2@example.com',
            'password': 'Test@123456',
            'full_name': 'Test Farmer',
            'phone': '9876543211',
            'role': 'farmer',
            'state': 'Maharashtra',
            'district': 'Pune'
        })
        
        result = response.json() if response.status_code in [200, 201] else {'error': response.text}
        if response.status_code in [200, 201]:
            self.farmer_token = result.get('access_token')
            result['success'] = True
        else:
            result['success'] = False
        
        self.log("Farmer Signup", result)
        
    def test_login(self):
        """Test user login"""
        response = requests.post(f'{BASE_URL}/auth/login', json={
            'email': 'test_consumer_v2@example.com',
            'password': 'Test@123456'
        })
        
        result = response.json() if response.status_code == 200 else {'error': response.text}
        if response.status_code == 200:
            result['success'] = True
            if not self.consumer_token:
                self.consumer_token = result.get('access_token')
        else:
            result['success'] = False
        
        self.log("Consumer Login", result)
    
    def test_profile(self):
        """Test profile endpoint"""
        response = requests.get(
            f'{BASE_URL}/auth/profile',
            headers={'Authorization': f'Bearer {self.consumer_token}'}
        )
        
        result = response.json() if response.status_code == 200 else {'error': response.text}
        result['success'] = response.status_code == 200
        self.log("Get Profile", result)
    
    def test_create_product(self):
        """Test product creation"""
        print("\n" + "="*60)
        print("TEST PHASE 2: PRODUCT MANAGEMENT")
        print("="*60)
        
        response = requests.post(
            f'{BASE_URL}/products',
            headers={'Authorization': f'Bearer {self.farmer_token}'},
            json={
                'name': 'Premium Tomatoes',
                'category': 'Vegetables',
                'description': 'Fresh red tomatoes from our farm',
                'price': 45.50,
                'quantity': 100,
                'quality_grade': 'A',
                'season': 'Summer'
            }
        )
        
        result = response.json() if response.status_code in [200, 201] else {'error': response.text}
        if response.status_code in [200, 201]:
            self.product_id = result.get('product_id')
            result['success'] = True
        else:
            result['success'] = False
        
        self.log("Create Product", result)
        return self.product_id
    
    def test_list_products(self):
        """Test product listing"""
        response = requests.get(f'{BASE_URL}/products')
        
        result = response.json() if response.status_code == 200 else {'error': response.text}
        result['success'] = response.status_code == 200
        if result['success']:
            result['data'] = {'count': len(result.get('data', []))}
        self.log("List Products", result)
    
    def test_update_product(self):
        """Test product update"""
        if not self.product_id:
            print("⏭️  Skipping Update Product (no product created)")
            return
        
        response = requests.put(
            f'{BASE_URL}/products/{self.product_id}',
            headers={'Authorization': f'Bearer {self.farmer_token}'},
            json={'price': 50.00, 'quantity': 150}
        )
        
        result = response.json() if response.status_code == 200 else {'error': response.text}
        result['success'] = response.status_code == 200
        self.log("Update Product", result)
    
    def test_create_order(self):
        """Test order creation"""
        print("\n" + "="*60)
        print("TEST PHASE 3: ORDER MANAGEMENT")
        print("="*60)
        
        if not self.product_id:
            print("⏭️  Skipping Create Order (no product available)")
            return
        
        response = requests.post(
            f'{BASE_URL}/orders',
            headers={'Authorization': f'Bearer {self.consumer_token}'},
            json={
                'items': [{'product_id': self.product_id, 'quantity': 5}],
                'shipping_address': '123 Main St, Pune, 411001'
            }
        )
        
        result = response.json() if response.status_code in [200, 201] else {'error': response.text}
        if response.status_code in [200, 201]:
            self.order_id = result.get('order_id')
            result['success'] = True
        else:
            result['success'] = False
        
        self.log("Create Order", result)
    
    def test_get_orders(self):
        """Test get user orders"""
        response = requests.get(
            f'{BASE_URL}/orders',
            headers={'Authorization': f'Bearer {self.consumer_token}'}
        )
        
        result = response.json() if response.status_code == 200 else {'error': response.text}
        result['success'] = response.status_code == 200
        if result['success']:
            result['data'] = {'count': len(result.get('data', []))}
        self.log("Get Orders", result)
    
    def test_get_order_detail(self):
        """Test get order detail"""
        if not self.order_id:
            print("⏭️  Skipping Get Order Detail (no order created)")
            return
        
        response = requests.get(
            f'{BASE_URL}/orders/{self.order_id}',
            headers={'Authorization': f'Bearer {self.consumer_token}'}
        )
        
        result = response.json() if response.status_code == 200 else {'error': response.text}
        result['success'] = response.status_code == 200
        self.log("Get Order Detail", result)
    
    def test_create_review(self):
        """Test review creation"""
        print("\n" + "="*60)
        print("TEST PHASE 4: REVIEW MANAGEMENT")
        print("="*60)
        
        if not self.product_id:
            print("⏭️  Skipping Create Review (no product available)")
            return
        
        response = requests.post(
            f'{BASE_URL}/reviews',
            headers={'Authorization': f'Bearer {self.consumer_token}'},
            json={
                'product_id': self.product_id,
                'rating': 5,
                'comment': 'Excellent quality tomatoes! Highly recommended.'
            }
        )
        
        result = response.json() if response.status_code in [200, 201] else {'error': response.text}
        result['success'] = response.status_code in [200, 201]
        self.log("Create Review", result)
    
    def test_ml_recommendations(self):
        """Test ML crop recommendation"""
        print("\n" + "="*60)
        print("TEST PHASE 5: ML MODELS")
        print("="*60)
        
        response = requests.post(
            f'{BASE_URL}/ml/crop-recommendation',
            headers={'Authorization': f'Bearer {self.consumer_token}'},
            json={'climate': 'tropical', 'soil_type': 'loam', 'rainfall': 2500}
        )
        
        result = response.json() if response.status_code == 200 else {'error': response.text}
        result['success'] = response.status_code == 200
        self.log("ML Crop Recommendation", result)
    
    def test_product_recommendation(self):
        """Test product recommendation"""
        response = requests.post(
            f'{BASE_URL}/ml/product-recommendation',
            headers={'Authorization': f'Bearer {self.consumer_token}'},
            json={'user_preference': 'organic'}
        )
        
        result = response.json() if response.status_code == 200 else {'error': response.text}
        result['success'] = response.status_code == 200
        self.log("ML Product Recommendation", result)
    
    def test_price_prediction(self):
        """Test price prediction"""
        response = requests.post(
            f'{BASE_URL}/ml/price-prediction',
            json={
                'product_category': 'Vegetables',
                'quantity': 100,
                'quality': 'A'
            }
        )
        
        result = response.json() if response.status_code == 200 else {'error': response.text}
        result['success'] = response.status_code == 200
        self.log("ML Price Prediction", result)
    
    def run_all(self):
        """Run all tests"""
        print("\n" + "🚀 "*10)
        print("COMPREHENSIVE AGRI E-COMMERCE API TEST SUITE")
        print("🚀 "*10)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Base URL: {BASE_URL}")
        
        try:
            # Phase 1: Auth
            self.test_signup()
            self.test_login()
            self.test_profile()
            
            # Phase 2: Products
            self.test_list_products()
            self.test_create_product()
            self.test_update_product()
            
            # Phase 3: Orders
            self.test_create_order()
            self.test_get_orders()
            self.test_get_order_detail()
            
            # Phase 4: Reviews
            self.test_create_review()
            
            # Phase 5: ML
            self.test_ml_recommendations()
            self.test_product_recommendation()
            self.test_price_prediction()
            
        except Exception as e:
            print(f"\n❌ TEST SUITE ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*60)
        print("TEST SUITE COMPLETE")
        print("="*60)

if __name__ == '__main__':
    client = TestClient()
    client.run_all()
