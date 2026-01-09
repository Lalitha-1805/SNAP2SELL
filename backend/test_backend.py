#!/usr/bin/env python3
"""
Backend Verification Script
Tests all critical APIs and components
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"
TIMEOUT = 5

def test_endpoint(method, endpoint, data=None, headers=None, label=""):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=TIMEOUT, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=TIMEOUT, headers=headers)
        
        status = "✓" if response.status_code < 400 else "✗"
        print(f"{status} [{response.status_code}] {label}")
        return response.status_code, response.json() if response.text else {}
    except Exception as e:
        print(f"✗ [ERROR] {label}: {str(e)}")
        return 0, {}

def run_tests():
    """Run comprehensive backend tests"""
    print("\n" + "="*60)
    print("AgriSmart Backend Verification Tests")
    print("="*60 + "\n")
    
    # 1. Health Check
    print("1. HEALTH & INFO ENDPOINTS")
    print("-" * 60)
    test_endpoint("GET", "/health", label="Health Check")
    test_endpoint("GET", "/info", label="API Info")
    test_endpoint("GET", "/database-info", label="Database Info")
    test_endpoint("GET", "/scheduler-status", label="Scheduler Status")
    
    # 2. Authentication
    print("\n2. AUTHENTICATION FLOW")
    print("-" * 60)
    
    # Signup
    signup_data = {
        "email": f"test_farmer_{int(time.time())}@test.com",
        "password": "testpass123",
        "name": "Test Farmer",
        "role": "farmer"
    }
    status, response = test_endpoint("POST", "/auth/signup", data=signup_data, label="Signup (Farmer)")
    
    access_token = None
    if status == 201 and "access_token" in response.get("data", {}):
        access_token = response["data"]["access_token"]
        print(f"  → Token received: {access_token[:20]}...")
    
    # Login
    login_data = {
        "email": "consumer@test.com",
        "password": "password123"
    }
    status, response = test_endpoint("POST", "/auth/login", data=login_data, label="Login (Existing Consumer)")
    
    if status == 200 and "access_token" in response.get("data", {}):
        access_token = response["data"]["access_token"]
        print(f"  → Token received: {access_token[:20]}...")
    
    # 3. Products API
    print("\n3. PRODUCTS API")
    print("-" * 60)
    test_endpoint("GET", "/products", label="Get All Products")
    test_endpoint("GET", "/products?page=1&limit=10", label="Get Products (Paginated)")
    test_endpoint("GET", "/products?category=Vegetables", label="Get Products (Filtered)")
    
    # Create product (with token)
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        create_product_data = {
            "name": "Test Tomato",
            "description": "Fresh organic tomatoes",
            "price": 50,
            "quantity": 100,
            "category": "Vegetables",
            "quality_grade": "A"
        }
        test_endpoint("POST", "/products", data=create_product_data, headers=headers, label="Create Product (Farmer)")
    
    # 4. ML Endpoints
    print("\n4. MACHINE LEARNING ENDPOINTS")
    print("-" * 60)
    
    # Crop Recommendation
    crop_data = {
        "soil_type": "loamy",
        "season": "kharif",
        "rainfall": 800,
        "temperature": 30,
        "humidity": 70
    }
    test_endpoint("POST", "/ml/crop-recommendation", data=crop_data, label="Crop Recommendation")
    
    # Price Prediction
    price_data = {
        "days_from_now": 7,
        "season": 0,
        "category": 0,
        "quantity": 100
    }
    test_endpoint("POST", "/ml/price-prediction", data=price_data, label="Price Prediction")
    
    # 5. Chatbot
    print("\n5. CHATBOT API")
    print("-" * 60)
    test_endpoint("GET", "/chatbot/suggestions", label="Get Suggestions")
    test_endpoint("GET", "/chatbot/kb-stats", label="Knowledge Base Stats")
    
    chatbot_data = {"question": "What crops should I grow in monsoon?"}
    test_endpoint("POST", "/chatbot/ask", data=chatbot_data, label="Ask Question")
    
    # 6. Orders
    print("\n6. ORDERS API")
    print("-" * 60)
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        test_endpoint("GET", "/orders", headers=headers, label="Get Orders")
    else:
        print("✗ [SKIP] Orders (No auth token)")
    
    # 7. Reviews
    print("\n7. REVIEWS API")
    print("-" * 60)
    test_endpoint("GET", "/reviews?product_id=test_id", label="Get Reviews")
    
    print("\n" + "="*60)
    print("Verification Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_tests()
