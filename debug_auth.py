#!/usr/bin/env python3
"""
Debug authentication issues
"""
import requests
import json
from jose import jwt

BASE_URL = "http://localhost:8000"
SECRET_KEY = "saba7"

def test_auth_flow():
    print("🔍 Testing authentication flow...")
    
    # 1. Login
    print("\n1. Logging in...")
    login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", data={
        "username": "master@example.com",
        "password": "masterpassword123"
    })
    
    print(f"Login status: {login_response.status_code}")
    print(f"Login response: {login_response.text}")
    
    if login_response.status_code != 200:
        return
    
    token_data = login_response.json()
    token = token_data["access_token"]
    print(f"Token: {token}")
    
    # 2. Decode token
    print("\n2. Decoding token...")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print(f"Admin ID: {payload.get('sub')} (type: {type(payload.get('sub'))})")
    except Exception as e:
        print(f"Error decoding token: {e}")
        return
    
    # 3. Test admin creation
    print("\n3. Testing admin creation...")
    headers = {"Authorization": f"Bearer {token}"}
    admin_data = {
        "full_name": "Test Admin",
        "email": "test@example.com",
        "phone": "+201234567890",
        "password": "testpass123",
        "role": "studio_rental"
    }
    
    create_response = requests.post(
        f"{BASE_URL}/api/v1/admins/",
        json=admin_data,
        headers=headers
    )
    
    print(f"Create admin status: {create_response.status_code}")
    print(f"Create admin response: {create_response.text}")

if __name__ == "__main__":
    test_auth_flow()
