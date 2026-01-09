#!/usr/bin/env python
"""
Comprehensive API Test Suite
Tests all critical endpoints: auth, products, orders, reviews, ML
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'
RESULTS = []

def log_test(name, status, details=""):
    """Log test result"""
    result = {"name": name, "status": status, "details": details, "time": datetime.now().isoformat()}
    RESULTS.append(result)
    icon = "✓" if status == "PASS" else "✗"
    print(f"{icon} {name}: {status} {details}")
    return status == "PASS"

def test_health():
    """Test: Backend health endpoint"""
    try:
        r = requests.get(f'{BASE_URL}/health', timeout=5)
        if r.status_code == 200:
            log_test("Health Check", "PASS", f"Status {r.status_code}")
            return True
        else:
            log_test("Health Check", "FAIL", f"Status {r.status_code}")
            return False
    except Exception as e:
        log_test("Health Check", "FAIL", str(e))
        return False

def test_signup(email, name, password, role):
    """Test: Signup endpoint"""
    try:
        data = {'email': email, 'name': name, 'password': password, 'role': role, 'phone': '9990001111', 'address': 'Test Address'}
        r = requests.post(f'{BASE_URL}/auth/signup', json=data, timeout=5)
        if r.status_code == 201:
            resp = r.json()
            if resp.get('access_token') and resp.get('user'):
                log_test(f"Signup ({role})", "PASS", f"{email}")
                return resp.get('access_token'), resp.get('user')
            else:
                log_test(f"Signup ({role})", "FAIL", "No token in response")
                return None, None
        else:
            log_test(f"Signup ({role})", "FAIL", f"Status {r.status_code}: {r.text[:100]}")
            return None, None
    except Exception as e:
        log_test(f"Signup ({role})", "FAIL", str(e))
        return None, None

def test_login(email, password):
    """Test: Login endpoint"""
    try:
        data = {'email': email, 'password': password}
        r = requests.post(f'{BASE_URL}/auth/login', json=data, timeout=5)
        if r.status_code == 200:
            resp = r.json()
            if resp.get('access_token'):
                log_test(f"Login ({email})", "PASS", "Token received")
                return resp.get('access_token'), resp.get('user')
            else:
                log_test(f"Login ({email})", "FAIL", "No token")
                return None, None
        else:
            log_test(f"Login ({email})", "FAIL", f"Status {r.status_code}")
            return None, None
    except Exception as e:
        log_test(f"Login ({email})", "FAIL", str(e))
        return None, None

def test_profile(token, role):
    """Test: Profile endpoint (JWT protected)"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.get(f'{BASE_URL}/auth/profile', headers=headers, timeout=5)
        if r.status_code == 200:
            resp = r.json()
            if resp.get('user'):
                log_test(f"Profile ({role})", "PASS", f"User: {resp['user'].get('name')}")
                return True
            else:
                log_test(f"Profile ({role})", "FAIL", "No user in response")
                return False
        else:
            log_test(f"Profile ({role})", "FAIL", f"Status {r.status_code}: {r.text[:100]}")
            return False
    except Exception as e:
        log_test(f"Profile ({role})", "FAIL", str(e))
        return False

def test_create_product(token, farmer_role):
    """Test: Create product (farmer-only)"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'name': f'Test Product {datetime.now().timestamp()}',
            'category': 'Vegetables',
            'description': 'Test description',
            'price': 100,
            'quantity': 50
        }
        r = requests.post(f'{BASE_URL}/products', json=data, headers=headers, timeout=5)
        if r.status_code == 201:
            resp = r.json()
            if resp.get('product_id'):
                log_test("Create Product (Farmer)", "PASS", f"Product ID: {resp['product_id'][:8]}")
                return resp.get('product_id')
            else:
                log_test("Create Product (Farmer)", "FAIL", "No product_id")
                return None
        else:
            log_test("Create Product (Farmer)", "FAIL", f"Status {r.status_code}: {r.text[:100]}")
            return None
    except Exception as e:
        log_test("Create Product (Farmer)", "FAIL", str(e))
        return None

def test_get_products():
    """Test: Get products (public)"""
    try:
        r = requests.get(f'{BASE_URL}/products', timeout=5)
        if r.status_code == 200:
            resp = r.json()
            count = len(resp.get('data', []))
            log_test("Get Products", "PASS", f"{count} products found")
            return resp.get('data', [])
        else:
            log_test("Get Products", "FAIL", f"Status {r.status_code}")
            return []
    except Exception as e:
        log_test("Get Products", "FAIL", str(e))
        return []

def test_create_order(token, product_ids):
    """Test: Create order (consumer-only)"""
    try:
        if not product_ids:
            log_test("Create Order", "SKIP", "No products available")
            return None
        
        headers = {'Authorization': f'Bearer {token}'}
        items = [{'product_id': pid, 'quantity': 1} for pid in product_ids[:1]]
        data = {'items': items, 'shipping_address': 'Test Address'}
        
        r = requests.post(f'{BASE_URL}/orders', json=data, headers=headers, timeout=5)
        if r.status_code == 201:
            resp = r.json()
            if resp.get('order_id'):
                log_test("Create Order", "PASS", f"Order ID: {resp['order_id'][:8]}")
                return resp.get('order_id')
            else:
                log_test("Create Order", "FAIL", "No order_id")
                return None
        else:
            log_test("Create Order", "FAIL", f"Status {r.status_code}: {r.text[:100]}")
            return None
    except Exception as e:
        log_test("Create Order", "FAIL", str(e))
        return None

def test_crop_recommendation():
    """Test: ML crop recommendation (public)"""
    try:
        data = {
            'soil_type': 'loamy',
            'season': 'monsoon',
            'rainfall': 800,
            'temperature': 25,
            'humidity': 70
        }
        r = requests.post(f'{BASE_URL}/ml/crop-recommendation', json=data, timeout=5)
        if r.status_code == 200:
            resp = r.json()
            if resp.get('data'):
                log_test("Crop Recommendation", "PASS", f"Got recommendations")
                return True
            else:
                log_test("Crop Recommendation", "FAIL", "No data")
                return False
        else:
            log_test("Crop Recommendation", "FAIL", f"Status {r.status_code}")
            return False
    except Exception as e:
        log_test("Crop Recommendation", "FAIL", str(e))
        return False

def test_price_prediction():
    """Test: ML price prediction (public)"""
    try:
        data = {
            'days_from_now': 7,
            'season': 1,
            'category': 0,
            'quantity': 100
        }
        r = requests.post(f'{BASE_URL}/ml/price-prediction', json=data, timeout=5)
        if r.status_code == 200:
            resp = r.json()
            if resp.get('data'):
                log_test("Price Prediction", "PASS", f"Got prediction")
                return True
            else:
                log_test("Price Prediction", "FAIL", "No data")
                return False
        else:
            log_test("Price Prediction", "FAIL", f"Status {r.status_code}")
            return False
    except Exception as e:
        log_test("Price Prediction", "FAIL", str(e))
        return False

def test_chatbot_ask():
    """Test: Chatbot ask (public)"""
    try:
        data = {'question': 'What crops should I grow in monsoon?'}
        r = requests.post(f'{BASE_URL}/chatbot/ask', json=data, timeout=5)
        if r.status_code == 200:
            resp = r.json()
            if resp.get('data'):
                log_test("Chatbot Ask", "PASS", f"Got answer")
                return True
            else:
                log_test("Chatbot Ask", "FAIL", "No data")
                return False
        else:
            log_test("Chatbot Ask", "FAIL", f"Status {r.status_code}")
            return False
    except Exception as e:
        log_test("Chatbot Ask", "FAIL", str(e))
        return False

def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passes = sum(1 for r in RESULTS if r['status'] == 'PASS')
    fails = sum(1 for r in RESULTS if r['status'] == 'FAIL')
    skips = sum(1 for r in RESULTS if r['status'] == 'SKIP')
    total = len(RESULTS)
    print(f"Total: {total} | Passed: {passes} | Failed: {fails} | Skipped: {skips}")
    print(f"Success Rate: {(passes/max(total-skips,1))*100:.1f}%")
    print("="*60)
    
    if fails > 0:
        print("\nFAILED TESTS:")
        for r in RESULTS:
            if r['status'] == 'FAIL':
                print(f"  - {r['name']}: {r['details']}")

# Run all tests
print("\n" + "="*60)
print("AGRISMART COMPREHENSIVE API TEST SUITE")
print("="*60 + "\n")

test_health()
farmer_token, farmer_user = test_signup('farmer_test@example.com', 'Test Farmer', 'secret123', 'farmer')
consumer_token, consumer_user = test_signup('consumer_test@example.com', 'Test Consumer', 'secret123', 'consumer')

if farmer_token:
    test_profile(farmer_token, 'farmer')
if consumer_token:
    test_profile(consumer_token, 'consumer')

if farmer_token:
    product_id = test_create_product(farmer_token, 'farmer')
    if product_id:
        products = [product_id]
    else:
        products = []
else:
    products = []

all_products = test_get_products()
if all_products:
    product_ids = [p['product_id'] for p in all_products[:3]]
else:
    product_ids = products

if consumer_token and product_ids:
    test_create_order(consumer_token, product_ids)

test_crop_recommendation()
test_price_prediction()
test_chatbot_ask()

print_summary()

# Exit with appropriate code
sys.exit(0 if sum(1 for r in RESULTS if r['status'] == 'FAIL') == 0 else 1)
