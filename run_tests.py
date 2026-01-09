#!/usr/bin/env python
"""
Simplified Test Suite for AgriSmart - Windows Compatible
Tests all core functionality without Unicode issues
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'
TEST_RESULTS = {'passed': 0, 'failed': 0}

def test(name, condition, details=""):
    """Test and log result"""
    status = "PASS" if condition else "FAIL"
    symbol = "[OK]" if condition else "[FAIL]"
    print(f"{symbol} {name}")
    if details:
        print(f"    {details}")
    if condition:
        TEST_RESULTS['passed'] += 1
    else:
        TEST_RESULTS['failed'] += 1
    return condition

print("\n" + "="*60)
print("  AgriSmart Testing Suite")
print("  Started: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print("="*60 + "\n")

# PHASE 1: HEALTH CHECK
print("PHASE 1: HEALTH CHECK")
print("-" * 60)
try:
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    test("Health endpoint responds", r.status_code == 200)
except Exception as e:
    test("Health endpoint responds", False, str(e))

# PHASE 2: AUTHENTICATION
print("\nPHASE 2: AUTHENTICATION TESTING")
print("-" * 60)

# Signup with validation
r = requests.post(f"{BASE_URL}/auth/signup", json={"email": "", "password": "test"}, timeout=5)
test("Signup rejects empty email", r.status_code in [400, 422])

# Valid signup - Consumer
consumer_data = {
    "email": f"consumer_{datetime.now().timestamp()}@test.com",
    "password": "Test@1234",
    "role": "consumer"
}
r = requests.post(f"{BASE_URL}/auth/signup", json=consumer_data, timeout=5)
test("Consumer signup succeeds", r.status_code == 201 or r.status_code == 200)
consumer_token = r.json().get('access_token') if r.status_code in [200, 201] else None

# Valid signup - Farmer
farmer_data = {
    "email": f"farmer_{datetime.now().timestamp()}@test.com",
    "password": "Test@1234",
    "role": "farmer"
}
r = requests.post(f"{BASE_URL}/auth/signup", json=farmer_data, timeout=5)
test("Farmer signup succeeds", r.status_code == 201 or r.status_code == 200)
farmer_token = r.json().get('access_token') if r.status_code in [200, 201] else None

# Login
r = requests.post(f"{BASE_URL}/auth/login", json={"email": consumer_data['email'], "password": consumer_data['password']}, timeout=5)
test("Login succeeds with valid credentials", r.status_code == 200)
if r.status_code == 200:
    consumer_token = r.json().get('access_token')
    test("Access token returned", consumer_token is not None)

# Login with missing email
r = requests.post(f"{BASE_URL}/auth/login", json={"email": "", "password": "test"}, timeout=5)
test("Login rejects missing email (400 status)", r.status_code == 400)

# PHASE 3: PRODUCTS
print("\nPHASE 3: PRODUCTS TESTING")
print("-" * 60)

if farmer_token:
    # Create product
    product_data = {
        "name": f"Test Crop {datetime.now().timestamp()}",
        "category": "Vegetables",
        "price": 100.0,
        "stock": 50,
        "description": "Test product"
    }
    headers = {"Authorization": f"Bearer {farmer_token}"}
    r = requests.post(f"{BASE_URL}/products", json=product_data, headers=headers, timeout=5)
    test("Farmer can create product", r.status_code in [200, 201])
    
    if r.status_code in [200, 201]:
        product_id = r.json().get('_id') or r.json().get('id')
        
        # Get product details
        r = requests.get(f"{BASE_URL}/products/{product_id}", timeout=5)
        test("Get product details succeeds", r.status_code == 200)
        
        # Invalid ID handling - BUG FIX VERIFICATION
        r = requests.get(f"{BASE_URL}/products/invalid_id_format_xyz", timeout=5)
        test("Invalid product ID returns 404 (not 500)", r.status_code == 404)

# Get all products
r = requests.get(f"{BASE_URL}/products", timeout=5)
test("Get products list succeeds", r.status_code == 200)

# PHASE 4: ORDERS
print("\nPHASE 4: ORDERS TESTING")
print("-" * 60)

if consumer_token and farmer_token:
    # Get orders - BUG FIX VERIFICATION (Consumer role now accepted)
    headers = {"Authorization": f"Bearer {consumer_token}"}
    r = requests.get(f"{BASE_URL}/orders", headers=headers, timeout=5)
    test("Consumer can access GET /orders (Bug Fix #3)", r.status_code == 200)
    
    # Create order
    if farmer_token:
        # First create a product
        product_data = {
            "name": f"Test Product for Order {datetime.now().timestamp()}",
            "category": "Fruits",
            "price": 50.0,
            "stock": 100,
            "description": "Product for order test"
        }
        headers_farmer = {"Authorization": f"Bearer {farmer_token}"}
        r = requests.post(f"{BASE_URL}/products", json=product_data, headers=headers_farmer, timeout=5)
        
        if r.status_code in [200, 201]:
            product_id = r.json().get('_id') or r.json().get('id')
            
            # Create order with consumer token
            order_data = {
                "items": [{"product_id": product_id, "quantity": 2}],
                "total_price": 100.0
            }
            headers_consumer = {"Authorization": f"Bearer {consumer_token}"}
            r = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers_consumer, timeout=5)
            test("Consumer can create order (Bug Fix #3)", r.status_code in [200, 201])

# PHASE 5: ERROR HANDLING
print("\nPHASE 5: ERROR HANDLING")
print("-" * 60)

# Missing Authorization header
r = requests.get(f"{BASE_URL}/orders", timeout=5)
test("Missing auth header returns 401", r.status_code == 401)

# Invalid JSON
r = requests.post(f"{BASE_URL}/auth/signup", data="invalid", headers={"Content-Type": "application/json"}, timeout=5)
test("Invalid JSON handled gracefully", r.status_code in [400, 422, 500])

# PHASE 6: SYSTEM STATUS
print("\nPHASE 6: SYSTEM COMPONENTS")
print("-" * 60)

# Check ML models
r = requests.get(f"{BASE_URL}/health", timeout=5)
if r.status_code == 200:
    health = r.json()
    test("ML Models loaded", health.get('ml_models_loaded', False))
    test("MongoDB connected", health.get('database_connected', False))
    test("JWT enabled", health.get('jwt_enabled', False))

# RESULTS
print("\n" + "="*60)
print("TEST RESULTS")
print("="*60)
total = TEST_RESULTS['passed'] + TEST_RESULTS['failed']
percentage = (TEST_RESULTS['passed'] / total * 100) if total > 0 else 0
print(f"Passed: {TEST_RESULTS['passed']}/{total} ({percentage:.1f}%)")
print(f"Failed: {TEST_RESULTS['failed']}/{total}")
print("="*60 + "\n")

# Exit with appropriate code
exit(0 if TEST_RESULTS['failed'] == 0 else 1)
