#!/usr/bin/env python
"""
Detailed debugging of failed tests
"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'

print("=" * 60)
print("DEBUGGING FAILED TESTS")
print("=" * 60)

# Test 1: Login fails with missing email - should fail
print("\n[TEST 1] Login fails with missing email")
r = requests.post(f'{BASE_URL}/auth/login', json={'password': 'test'})
print(f"Status: {r.status_code}")
print(f"Response: {json.dumps(r.json(), indent=2)}")
if r.status_code != 400:
    print("❌ BUG: Login should return 400 for missing email")

# Test 2: Get orders list
print("\n[TEST 2] Get orders list without auth")
r = requests.get(f'{BASE_URL}/orders')
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:200]}")

# Authenticated
print("\n[TEST 2B] Get orders list with valid token")
# First login
login_r = requests.post(f'{BASE_URL}/auth/login', json={
    'email': 'test_consumer@example.com',
    'password': 'secret123'
})
if login_r.status_code == 200:
    token = login_r.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(f'{BASE_URL}/orders', headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
    if r.status_code != 200:
        print(f"❌ BUG: Should return 200, got {r.status_code}")

# Test 3: Invalid ID format
print("\n[TEST 3] Invalid ID format")
r = requests.get(f'{BASE_URL}/products/invalid_id')
print(f"Status: {r.status_code}")
print(f"Response: {json.dumps(r.json(), indent=2)}")
if r.status_code not in [400, 404]:
    print(f"❌ BUG: Invalid ID should return 400 or 404, got {r.status_code}")

