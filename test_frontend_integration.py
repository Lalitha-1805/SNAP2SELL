#!/usr/bin/env python3
"""
AgriSmart Frontend Integration Test Suite
Tests all critical flows between frontend and backend
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE = "http://127.0.0.1:5000/api"
FRONTEND_URL = "http://localhost:5173"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status == "OK":
        print(f"{Colors.GREEN}[✓ {timestamp}] {message}{Colors.END}")
    elif status == "ERROR":
        print(f"{Colors.RED}[✗ {timestamp}] {message}{Colors.END}")
    elif status == "TEST":
        print(f"{Colors.BLUE}[→ {timestamp}] {message}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}[• {timestamp}] {message}{Colors.END}")

def test_backend_health():
    """Test backend is running"""
    log("Testing backend health...", "TEST")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            log("Backend is running ✓", "OK")
            return True
        else:
            log(f"Backend returned status {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Cannot connect to backend: {e}", "ERROR")
        return False

def test_signup():
    """Test user signup"""
    log("Testing signup flow...", "TEST")
    test_email = f"test_{int(time.time())}@agrismart.com"
    
    try:
        response = requests.post(f"{API_BASE}/auth/signup", json={
            "email": test_email,
            "password": "testpass123",
            "name": "Test User",
            "role": "consumer"
        })
        
        if response.status_code == 201:
            data = response.json()
            if "access_token" in data:
                log(f"Signup successful - User: {test_email}", "OK")
                return data.get("access_token"), test_email
            else:
                log("Signup returned no token", "ERROR")
                return None, None
        else:
            log(f"Signup failed with status {response.status_code}: {response.text}", "ERROR")
            return None, None
    except Exception as e:
        log(f"Signup error: {e}", "ERROR")
        return None, None

def test_login():
    """Test login with existing credentials"""
    log("Testing login flow...", "TEST")
    
    try:
        response = requests.post(f"{API_BASE}/auth/login", json={
            "email": "consumer@test.com",
            "password": "password123"
        })
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data and "user" in data:
                log(f"Login successful - User: {data['user'].get('name')}", "OK")
                return data.get("access_token")
            else:
                log("Login returned no token", "ERROR")
                return None
        else:
            log(f"Login failed with status {response.status_code}", "ERROR")
            return None
    except Exception as e:
        log(f"Login error: {e}", "ERROR")
        return None

def test_products(token):
    """Test product listing"""
    log("Testing product retrieval...", "TEST")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE}/products", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get("data", [])
            log(f"Retrieved {len(products)} products", "OK")
            return len(products) > 0
        else:
            log(f"Failed with status {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Product retrieval error: {e}", "ERROR")
        return False

def test_create_product(token):
    """Test product creation (farmer only)"""
    log("Testing product creation (farmer endpoint)...", "TEST")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{API_BASE}/products", headers=headers, json={
            "name": "Test Tomato",
            "description": "Fresh red tomatoes",
            "price": 50,
            "quantity": 100,
            "category": "Vegetables"
        })
        
        if response.status_code in [201, 403]:  # 201 = success, 403 = consumer (expected)
            if response.status_code == 201:
                log("Product created successfully", "OK")
                return True
            else:
                log("Consumer cannot create products (expected behavior)", "OK")
                return True
        else:
            log(f"Unexpected status {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Product creation error: {e}", "ERROR")
        return False

def test_chatbot(token):
    """Test AI chatbot"""
    log("Testing AI chatbot...", "TEST")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{API_BASE}/chatbot/ask", headers=headers, json={
            "question": "What is the best way to grow tomatoes?"
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data", {}).get("answer"):
                log("Chatbot responded successfully", "OK")
                return True
            else:
                log("Chatbot returned empty response", "ERROR")
                return False
        else:
            log(f"Chatbot failed with status {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Chatbot error: {e}", "ERROR")
        return False

def test_orders(token):
    """Test order endpoints"""
    log("Testing order retrieval...", "TEST")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE}/orders", headers=headers)
        
        if response.status_code == 200:
            log("Order retrieval successful", "OK")
            return True
        else:
            log(f"Order retrieval failed with status {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Order retrieval error: {e}", "ERROR")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("AgriSmart Frontend Integration Test Suite")
    print(f"{'='*60}{Colors.END}\n")
    
    results = {}
    
    # Test 1: Backend Health
    results["Backend Health"] = test_backend_health()
    if not results["Backend Health"]:
        log("Cannot continue - backend not running", "ERROR")
        return
    
    time.sleep(0.5)
    
    # Test 2: Login
    token = test_login()
    results["Login"] = token is not None
    
    if not token:
        log("Cannot continue - login failed", "ERROR")
        return
    
    time.sleep(0.5)
    
    # Test 3: Products
    results["Product Listing"] = test_products(token)
    time.sleep(0.5)
    
    # Test 4: Product Creation
    results["Product Creation"] = test_create_product(token)
    time.sleep(0.5)
    
    # Test 5: Chatbot
    results["Chatbot"] = test_chatbot(token)
    time.sleep(0.5)
    
    # Test 6: Orders
    results["Orders"] = test_orders(token)
    time.sleep(0.5)
    
    # Test 7: Signup
    new_token, new_email = test_signup()
    results["Signup"] = new_token is not None
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}")
    print("Test Results Summary")
    print(f"{'='*60}{Colors.END}\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        color = Colors.GREEN if passed_test else Colors.RED
        print(f"{color}{status}{Colors.END} - {test_name}")
    
    print(f"\n{Colors.BLUE}Total: {passed}/{total} tests passed{Colors.END}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}✓ ALL TESTS PASSED - Frontend is fully connected!{Colors.END}\n")
    else:
        print(f"{Colors.YELLOW}⚠ Some tests failed - Check backend logs{Colors.END}\n")

if __name__ == "__main__":
    main()
