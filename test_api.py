#!/usr/bin/env python3
"""
Test script for Real Estate Platform API
Run this after setting up the application to verify functionality
"""

import requests
import json
from getpass import getpass

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_admin_login():
    """Test admin login"""
    print("\n🔐 Testing admin login...")
    email = input("Enter admin email: ")
    password = getpass("Enter admin password: ")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful")
            print(f"Admin: {data['admin']['name']} ({data['admin']['role']})")
            return data['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.json())
            return None
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return None

def test_apartments(token=None):
    """Test apartments endpoint"""
    print("\n🏢 Testing apartments endpoint...")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(f"{BASE_URL}/apartments", headers=headers)
        if response.status_code == 200:
            apartments = response.json()
            print(f"✅ Found {len(apartments)} apartments")
            return True
        else:
            print(f"❌ Apartments fetch failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Apartments fetch failed: {e}")
        return False

def test_create_apartment(token):
    """Test creating an apartment"""
    if not token:
        print("❌ Cannot test apartment creation without token")
        return False
    
    print("\n🏗️ Testing apartment creation...")
    
    apartment_data = {
        "title": "Test Apartment",
        "location": "Test Location",
        "type": "rent",
        "total_parts": 5,
        "description": "A test apartment for API testing",
        "rent_price": 1500.00
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(
            f"{BASE_URL}/apartments",
            json=apartment_data,
            headers=headers
        )
        
        if response.status_code == 201:
            apartment = response.json()
            print(f"✅ Apartment created with ID: {apartment['id']}")
            return apartment['id']
        else:
            print(f"❌ Apartment creation failed: {response.status_code}")
            print(response.json())
            return None
    except Exception as e:
        print(f"❌ Apartment creation failed: {e}")
        return None

def test_notifications(token):
    """Test notifications endpoint"""
    if not token:
        print("❌ Cannot test notifications without token")
        return False
    
    print("\n🔔 Testing notifications endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/notifications", headers=headers)
        if response.status_code == 200:
            notifications = response.json()
            print(f"✅ Found {len(notifications)} notifications")
            return True
        else:
            print(f"❌ Notifications fetch failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Notifications fetch failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Real Estate Platform API Test Suite")
    print("=====================================")
    
    # Test health
    if not test_health():
        print("❌ Application is not running. Please start with: uvicorn main:app --reload")
        return
    
    # Test public endpoints
    test_apartments()
    
    # Test admin endpoints
    token = test_admin_login()
    if token:
        test_create_apartment(token)
        test_notifications(token)
    else:
        print("⚠️ Skipping admin tests due to login failure")
    
    print("\n🎉 Test suite completed!")
    print("📖 Visit http://localhost:8000/docs for complete API documentation")

if __name__ == "__main__":
    main()
