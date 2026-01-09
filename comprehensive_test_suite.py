#!/usr/bin/env python
"""
Comprehensive Testing Suite for AgriSmart Platform
Tests all endpoints, validations, edge cases, and integration flows
"""

import requests
import json
import time
from datetime import datetime
import sys

# Configuration
BASE_URL = 'http://localhost:5000/api'
TIMEOUT = 10

# Test Results Storage
TEST_RESULTS = {
    'passed': 0,
    'failed': 0,
    'bugs_found': [],
    'warnings': []
}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log_test(name, result, message=""):
    """Log test result"""
    icon = f"{Colors.GREEN}[OK]{Colors.END}" if result else f"{Colors.RED}[FAIL]{Colors.END}"
    status = "PASS" if result else "FAIL"
    print(f"{icon} [{status}] {name}")
    if message:
        print(f"   → {message}")
    if result:
        TEST_RESULTS['passed'] += 1
    else:
        TEST_RESULTS['failed'] += 1

def log_bug(title, description, severity="HIGH"):
    """Log a found bug"""
    bug = {
        'title': title,
        'description': description,
        'severity': severity,
        'timestamp': datetime.now().isoformat()
    }
    TEST_RESULTS['bugs_found'].append(bug)
    print(f"{Colors.RED}[BUG FOUND]{Colors.END} {title}")
    print(f"   Severity: {severity}")
    print(f"   Description: {description}")

def request_get(endpoint, headers=None, params=None):
    """Make GET request"""
    try:
        url = BASE_URL + endpoint
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        return response
    except Exception as e:
        return None

def request_post(endpoint, data, headers=None):
    """Make POST request"""
    try:
        url = BASE_URL + endpoint
        response = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
        return response
    except Exception as e:
        return None

def request_put(endpoint, data, headers=None):
    """Make PUT request"""
    try:
        url = BASE_URL + endpoint
        response = requests.put(url, json=data, headers=headers, timeout=TIMEOUT)
        return response
    except Exception as e:
        return None

def print_section(title):
    """Print section header"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.END}\n")

# =====================================================
# PHASE 1: HEALTH CHECK
# =====================================================

def test_health_check():
    """Test API health endpoint"""
    print_section("PHASE 1: HEALTH CHECK")
    
    r = request_get('/health')
    log_test("Health endpoint responds", r is not None and r.status_code == 200)
    if r:
        data = r.json()
        log_test("Health response has status", 'status' in data and data['status'] == 'healthy')

# =====================================================
# PHASE 2: AUTHENTICATION TESTS
# =====================================================

def test_authentication():
    """Test authentication endpoints"""
    print_section("PHASE 2: AUTHENTICATION TESTING")
    
    test_data = {
        'consumer': {
            'email': f'consumer_test_{int(time.time())}@test.com',
            'password': 'TestPassword123',
            'name': 'Test Consumer',
            'role': 'consumer',
            'phone': '9876543210',
            'address': 'Test Address'
        },
        'farmer': {
            'email': f'farmer_test_{int(time.time())}@test.com',
            'password': 'TestPassword123',
            'name': 'Test Farmer',
            'role': 'farmer',
            'phone': '9876543210',
            'address': 'Farm Address'
        }
    }
    
    # Test 1: Signup validation - missing email
    print(f"\n{Colors.BLUE}→ Testing signup validation{Colors.END}")
    r = request_post('/auth/signup', {'password': 'test', 'name': 'Test'})
    log_test("Signup fails with missing email", r is not None and r.status_code == 400, 
             r.json().get('message', '') if r else "No response")
    
    # Test 2: Signup validation - weak password
    r = request_post('/auth/signup', {
        'email': 'test@test.com',
        'password': '123',  # Too short
        'name': 'Test'
    })
    log_test("Signup rejects weak password", r is not None and r.status_code == 400)
    
    # Test 3: Signup validation - invalid email
    r = request_post('/auth/signup', {
        'email': 'not-an-email',
        'password': 'ValidPassword123',
        'name': 'Test'
    })
    log_test("Signup rejects invalid email", r is not None and r.status_code == 400)
    if r and r.status_code != 400:
        log_bug("Invalid email not rejected", 
                f"Email 'not-an-email' was accepted but should be rejected",
                "MEDIUM")
    
    # Test 4: Successful signup - Consumer
    print(f"\n{Colors.BLUE}→ Testing successful signup{Colors.END}")
    consumer_data = test_data['consumer']
    r = request_post('/auth/signup', consumer_data)
    log_test("Consumer signup succeeds", r is not None and r.status_code == 201, 
             r.json().get('message', '') if r else "No response")
    consumer_signup_response = r.json() if r else None
    
    # Test 5: Successful signup - Farmer
    farmer_data = test_data['farmer']
    r = request_post('/auth/signup', farmer_data)
    log_test("Farmer signup succeeds", r is not None and r.status_code == 201)
    farmer_signup_response = r.json() if r else None
    
    # Test 6: Duplicate email prevention
    print(f"\n{Colors.BLUE}→ Testing duplicate email prevention{Colors.END}")
    r = request_post('/auth/signup', consumer_data)
    log_test("Duplicate email is rejected", r is not None and r.status_code == 400)
    if r and r.status_code != 400:
        log_bug("Duplicate email not prevented", 
                f"Email {consumer_data['email']} was allowed twice",
                "CRITICAL")
    
    # Test 7: Login validation - missing email
    print(f"\n{Colors.BLUE}→ Testing login validation{Colors.END}")
    r = request_post('/auth/login', {'password': 'test'})
    log_test("Login fails with missing email", r is not None and r.status_code == 400)
    
    # Test 8: Login validation - wrong password
    r = request_post('/auth/login', {
        'email': consumer_data['email'],
        'password': 'WrongPassword'
    })
    log_test("Login fails with wrong password", r is not None and r.status_code == 401, 
             r.json().get('message', '') if r else "No response")
    
    # Test 9: Successful login
    print(f"\n{Colors.BLUE}→ Testing successful login{Colors.END}")
    r = request_post('/auth/login', {
        'email': consumer_data['email'],
        'password': consumer_data['password']
    })
    log_test("Consumer login succeeds", r is not None and r.status_code == 200)
    consumer_login = r.json() if r else None
    
    r = request_post('/auth/login', {
        'email': farmer_data['email'],
        'password': farmer_data['password']
    })
    log_test("Farmer login succeeds", r is not None and r.status_code == 200)
    farmer_login = r.json() if r else None
    
    # Test 10: JWT token validation
    print(f"\n{Colors.BLUE}→ Testing JWT tokens{Colors.END}")
    if consumer_login and 'access_token' in consumer_login:
        log_test("Access token returned", True)
        token = consumer_login['access_token']
        
        # Test with token
        headers = {'Authorization': f'Bearer {token}'}
        r = request_get('/auth/profile', headers=headers)
        log_test("Profile endpoint works with valid token", r is not None and r.status_code == 200)
    else:
        log_test("Access token returned", False)
    
    # Test 11: Invalid token rejection
    headers = {'Authorization': 'Bearer invalid_token_xyz'}
    r = request_get('/auth/profile', headers=headers)
    log_test("Invalid token is rejected", r is not None and r.status_code != 200)
    
    return {
        'consumer_token': consumer_login['access_token'] if consumer_login else None,
        'consumer_id': consumer_login['user']['user_id'] if consumer_login else None,
        'farmer_token': farmer_login['access_token'] if farmer_login else None,
        'farmer_id': farmer_login['user']['user_id'] if farmer_login else None,
        'consumer_email': consumer_data['email'],
        'farmer_email': farmer_data['email']
    }

# =====================================================
# PHASE 3: PRODUCT TESTING
# =====================================================

def test_products(tokens):
    """Test product endpoints"""
    print_section("PHASE 3: PRODUCT TESTING")
    
    if not tokens['farmer_token']:
        print(f"{Colors.RED}Skipping product tests - no farmer token{Colors.END}")
        return {}
    
    farmer_headers = {'Authorization': f"Bearer {tokens['farmer_token']}"}
    consumer_headers = {'Authorization': f"Bearer {tokens['consumer_token']}"}
    
    # Test 1: Get all products
    print(f"\n{Colors.BLUE}→ Testing product retrieval{Colors.END}")
    r = request_get('/products')
    log_test("Get products works without auth", r is not None and r.status_code == 200)
    if r:
        data = r.json()
        log_test("Products response has correct structure", 'data' in data or 'products' in data)
    
    # Test 2: Create product - validation
    print(f"\n{Colors.BLUE}→ Testing product creation validation{Colors.END}")
    r = request_post('/products', {'name': 'Test'}, headers=farmer_headers)
    log_test("Create product with missing fields fails", r is not None and r.status_code != 201)
    
    # Test 3: Create valid product
    print(f"\n{Colors.BLUE}→ Testing valid product creation{Colors.END}")
    product_data = {
        'name': f'Test Tomato {int(time.time())}',
        'category': 'Vegetables',
        'description': 'Fresh red tomatoes',
        'price': 50,
        'quantity': 100,
        'soil_type': 'Loam',
        'season': 'Summer'
    }
    r = request_post('/products', product_data, headers=farmer_headers)
    log_test("Farmer can create product", r is not None and r.status_code == 201, 
             r.json().get('message', '') if r else "No response")
    product_id = r.json().get('product_id') if r else None
    
    # Test 4: Consumer cannot create product
    print(f"\n{Colors.BLUE}→ Testing role-based access control{Colors.END}")
    r = request_post('/products', product_data, headers=consumer_headers)
    log_test("Consumer cannot create product", r is not None and r.status_code != 201)
    if r and r.status_code == 201:
        log_bug("Role-based access control broken", 
                "Consumer was able to create product when only farmers should",
                "CRITICAL")
    
    # Test 5: Get single product
    if product_id:
        print(f"\n{Colors.BLUE}→ Testing product details{Colors.END}")
        r = request_get(f'/products/{product_id}')
        log_test("Get product details works", r is not None and r.status_code == 200)
    
    # Test 6: Filter by category
    print(f"\n{Colors.BLUE}→ Testing product filters{Colors.END}")
    r = request_get('/products', params={'category': 'Vegetables'})
    log_test("Filter by category works", r is not None and r.status_code == 200)
    
    # Test 7: Pagination
    r = request_get('/products', params={'page': 1, 'limit': 10})
    log_test("Pagination works", r is not None and r.status_code == 200)
    
    return {
        'product_id': product_id,
        'product_data': product_data
    }

# =====================================================
# PHASE 4: ORDER TESTING
# =====================================================

def test_orders(tokens, products):
    """Test order endpoints"""
    print_section("PHASE 4: ORDER TESTING")
    
    if not tokens['consumer_token'] or not products.get('product_id'):
        print(f"{Colors.RED}Skipping order tests - missing prerequisites{Colors.END}")
        return {}
    
    consumer_headers = {'Authorization': f"Bearer {tokens['consumer_token']}"}
    
    # Test 1: Create order validation
    print(f"\n{Colors.BLUE}→ Testing order creation validation{Colors.END}")
    r = request_post('/orders', {'items': []}, headers=consumer_headers)
    log_test("Order with no items fails", r is not None and r.status_code != 201)
    
    # Test 2: Create valid order
    print(f"\n{Colors.BLUE}→ Testing valid order creation{Colors.END}")
    order_data = {
        'items': [
            {'product_id': products['product_id'], 'quantity': 2}
        ],
        'shipping_address': 'Test Address, City, Country'
    }
    r = request_post('/orders', order_data, headers=consumer_headers)
    log_test("Consumer can create order", r is not None and r.status_code == 201, 
             r.json().get('message', '') if r else "No response")
    order_id = r.json().get('order_id') if r else None
    
    # Test 3: Get orders
    print(f"\n{Colors.BLUE}→ Testing order retrieval{Colors.END}")
    if order_id:
        r = request_get(f'/orders/{order_id}', headers=consumer_headers)
        log_test("Get order details works", r is not None and r.status_code == 200)
    
    r = request_get('/orders', headers=consumer_headers)
    log_test("Get orders list works", r is not None and r.status_code == 200)
    
    return {'order_id': order_id}

# =====================================================
# PHASE 5: REVIEW TESTING
# =====================================================

def test_reviews(tokens, products):
    """Test review endpoints"""
    print_section("PHASE 5: REVIEW TESTING")
    
    if not tokens['consumer_token'] or not products.get('product_id'):
        print(f"{Colors.RED}Skipping review tests - missing prerequisites{Colors.END}")
        return
    
    consumer_headers = {'Authorization': f"Bearer {tokens['consumer_token']}"}
    product_id = products['product_id']
    
    # Test 1: Create review validation
    print(f"\n{Colors.BLUE}→ Testing review validation{Colors.END}")
    r = request_post('/reviews', {'product_id': product_id, 'rating': 0}, headers=consumer_headers)
    log_test("Review with invalid rating fails", r is not None and r.status_code != 201)
    
    r = request_post('/reviews', {'product_id': product_id, 'rating': 6}, headers=consumer_headers)
    log_test("Review with rating > 5 fails", r is not None and r.status_code != 201)
    
    # Test 2: Create valid review
    print(f"\n{Colors.BLUE}→ Testing valid review creation{Colors.END}")
    review_data = {
        'product_id': product_id,
        'rating': 5,
        'comment': 'Excellent product! Very fresh and high quality.'
    }
    r = request_post('/reviews', review_data, headers=consumer_headers)
    log_test("Consumer can create review", r is not None and r.status_code == 201, 
             r.json().get('message', '') if r else "No response")
    
    # Test 3: Get reviews for product
    print(f"\n{Colors.BLUE}→ Testing review retrieval{Colors.END}")
    r = request_get(f'/reviews?product_id={product_id}')
    log_test("Get reviews works", r is not None and r.status_code == 200)

# =====================================================
# PHASE 6: EDGE CASE & ERROR HANDLING
# =====================================================

def test_edge_cases(tokens):
    """Test edge cases and error handling"""
    print_section("PHASE 6: EDGE CASE & ERROR HANDLING TESTING")
    
    # Test 1: Non-existent product
    print(f"\n{Colors.BLUE}→ Testing not found errors{Colors.END}")
    r = request_get('/products/000000000000000000000000')
    log_test("Non-existent product returns 404", r is not None and r.status_code == 404)
    
    # Test 2: Invalid ObjectID format
    r = request_get('/products/invalid_id')
    log_test("Invalid ID format handled gracefully", r is not None and r.status_code in [400, 404])
    if r and r.status_code not in [400, 404]:
        log_bug("Invalid ID format not handled", 
                f"Invalid ObjectID 'invalid_id' returned status {r.status_code}",
                "MEDIUM")
    
    # Test 3: Missing authorization header
    print(f"\n{Colors.BLUE}→ Testing authorization enforcement{Colors.END}")
    farmer_headers = {}  # No auth
    r = request_post('/products', {'name': 'Test'}, headers=farmer_headers)
    log_test("Unauthorized requests rejected", r is not None and r.status_code in [401, 403])
    
    # Test 4: Empty request body
    print(f"\n{Colors.BLUE}→ Testing input validation{Colors.END}")
    r = request_post('/auth/signup', {})
    log_test("Empty signup rejected", r is not None and r.status_code == 400)
    
    # Test 5: Large payload
    large_data = {
        'name': 'Test',
        'email': 'test@test.com',
        'password': 'password',
        'large_field': 'x' * 10000000  # Very large string
    }
    r = request_post('/auth/signup', large_data)
    log_test("Large payload handled", r is not None)  # Should not crash
    
    # Test 6: SQL Injection in email
    print(f"\n{Colors.BLUE}→ Testing security validations{Colors.END}")
    r = request_post('/auth/login', {
        'email': "' OR '1'='1",
        'password': 'test'
    })
    log_test("SQL injection attempt rejected", r is not None and r.status_code != 200)
    if r and r.status_code == 200:
        log_bug("SQL injection vulnerability", 
                "SQL injection string was accepted",
                "CRITICAL")

# =====================================================
# MAIN EXECUTION
# =====================================================

def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  AgriSmart Comprehensive Testing Suite")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}{Colors.END}\n")
    
    try:
        test_health_check()
        tokens = test_authentication()
        products = test_products(tokens)
        orders = test_orders(tokens, products)
        test_reviews(tokens, products)
        test_edge_cases(tokens)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Test execution error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
    
    # Print summary
    print_section("TEST SUMMARY")
    print(f"{Colors.GREEN}Passed: {TEST_RESULTS['passed']}{Colors.END}")
    print(f"{Colors.RED}Failed: {TEST_RESULTS['failed']}{Colors.END}")
    print(f"Total: {TEST_RESULTS['passed'] + TEST_RESULTS['failed']}")
    print(f"Success Rate: {100 * TEST_RESULTS['passed'] / (TEST_RESULTS['passed'] + TEST_RESULTS['failed'] or 1):.1f}%\n")
    
    if TEST_RESULTS['bugs_found']:
        print_section(f"BUGS FOUND ({len(TEST_RESULTS['bugs_found'])})")
        for i, bug in enumerate(TEST_RESULTS['bugs_found'], 1):
            print(f"{i}. {bug['title']} [{bug['severity']}]")
            print(f"   {bug['description']}\n")
    else:
        print(f"{Colors.GREEN}No bugs found!{Colors.END}\n")

if __name__ == '__main__':
    main()

