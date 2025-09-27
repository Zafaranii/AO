#!/usr/bin/env python3
"""
API Test Script for AO Apartment Management System
This script provides comprehensive test data and examples for all API endpoints.
"""

import requests
import json
from typing import Dict, Any

# Base URL for the API
BASE_URL = "http://localhost:8000"

class APITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
    
    def set_token(self, token: str):
        """Set authentication token for API calls"""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login and get authentication token"""
        url = f"{self.base_url}/auth/login"
        data = {
            "username": username,
            "password": password
        }
        response = self.session.post(url, data=data)
        response.raise_for_status()
        result = response.json()
        self.set_token(result["access_token"])
        return result
    
    def test_authentication(self):
        """Test authentication endpoints"""
        print("🔐 Testing Authentication...")
        
        # Test login
        login_data = {
            "username": "admin@example.com",
            "password": "admin123"
        }
        print(f"Login with: {login_data}")
        
        # Test create master admin (initial setup)
        master_admin_data = {
            "full_name": "Master Administrator",
            "email": "master@example.com",
            "phone": "+201111111111",
            "password": "masterpassword123",
            "master_password": "MASTER_ADMIN_SETUP_2024"
        }
        print(f"Create master admin: {master_admin_data}")
        
        # Test register (requires super admin token)
        register_data = {
            "full_name": "Test Admin",
            "email": "test@example.com",
            "phone": "+201234567890",
            "password": "testpass123",
            "role": "studio_rental"
        }
        print(f"Register data: {register_data}")
    
    def test_admin_management(self):
        """Test admin management endpoints"""
        print("\n👥 Testing Admin Management...")
        
        # Create admin
        create_admin_data = {
            "full_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "+201987654321",
            "password": "newpassword123",
            "role": "apartment_sale"
        }
        print(f"Create admin: {create_admin_data}")
        
        # Update admin
        update_admin_data = {
            "full_name": "Jane Smith Updated",
            "email": "jane.updated@example.com",
            "phone": "+201987654321",
            "role": "studio_rental"
        }
        print(f"Update admin: {update_admin_data}")
    
    def test_apartment_sale(self):
        """Test apartment sale endpoints"""
        print("\n🏠 Testing Apartment Sale...")
        
        # Create apartment sale
        apartment_sale_data = {
            "name": "Luxury Apartment in Maadi",
            "location": "maadi",
            "address": "123 Maadi Corniche, Cairo, Egypt",
            "area": 120.50,
            "number": "A-101",
            "price": 2500000.00,
            "bedrooms": 3,
            "bathrooms": "private",
            "description": "Beautiful luxury apartment with stunning Nile view",
            "photos_url": [
                "https://example.com/photos/living-room.jpg",
                "https://example.com/photos/kitchen.jpg",
                "https://example.com/photos/bedroom.jpg",
                "https://example.com/photos/bathroom.jpg",
                "https://example.com/photos/balcony.jpg"
            ],
            "location_on_map": "https://maps.google.com/example",
            "facilities_amenities": "Swimming pool, Gym, Security, Parking, Garden"
        }
        print(f"Create apartment sale: {json.dumps(apartment_sale_data, indent=2)}")
        
        # Update apartment sale
        update_sale_data = {
            "name": "Updated Luxury Apartment in Maadi",
            "price": 2600000.00,
            "description": "Updated description with more details",
            "photos_url": [
                "https://example.com/photos/new-living-room.jpg",
                "https://example.com/photos/new-kitchen.jpg"
            ]
        }
        print(f"Update apartment sale: {json.dumps(update_sale_data, indent=2)}")
    
    def test_apartment_rent(self):
        """Test apartment rent endpoints"""
        print("\n🏢 Testing Apartment Rent...")
        
        # Create apartment rent
        apartment_rent_data = {
            "name": "Modern Studio Apartment in Mokattam",
            "location": "mokkattam",
            "address": "456 Mokattam Hills, Cairo, Egypt",
            "area": 45.75,
            "number": "S-201",
            "price": 3500.00,
            "bedrooms": 1,
            "bathrooms": "private",
            "description": "Modern studio apartment perfect for young professionals",
            "photos_url": [
                "https://example.com/photos/studio-main.jpg",
                "https://example.com/photos/studio-kitchen.jpg",
                "https://example.com/photos/studio-bathroom.jpg"
            ],
            "location_on_map": "https://maps.google.com/example2",
            "facilities_amenities": "24/7 Security, Elevator, Balcony, Air Conditioning",
            "floor": 5,
            "total_parts": 3
        }
        print(f"Create apartment rent: {json.dumps(apartment_rent_data, indent=2)}")
    
    def test_apartment_parts(self):
        """Test apartment parts endpoints"""
        print("\n🏠 Testing Apartment Parts...")
        
        # Create apartment part
        apartment_part_data = {
            "status": "available",
            "title": "Studio A - Ground Floor",
            "area": 25.50,
            "monthly_price": 2500.00,
            "bedrooms": 1,
            "bathrooms": "shared",
            "furnished": "yes",
            "balcony": "no",
            "description": "Cozy ground floor studio with shared bathroom",
            "photos_url": [
                "https://example.com/photos/studio-a-main.jpg",
                "https://example.com/photos/studio-a-kitchen.jpg"
            ]
        }
        print(f"Create apartment part: {json.dumps(apartment_part_data, indent=2)}")
    
    def test_rental_contracts(self):
        """Test rental contracts endpoints"""
        print("\n📋 Testing Rental Contracts...")
        
        # Create rental contract
        rental_contract_data = {
            "apartment_part_id": 1,
            "customer_name": "Ahmed Mohamed",
            "customer_phone": "+201234567890",
            "customer_id_number": "12345678901234",
            "how_did_customer_find_us": "facebook",
            "paid_deposit": 5000.00,
            "warrant_amount": 2500.00,
            "rent_start_date": "2024-01-01",
            "rent_end_date": "2024-12-31",
            "rent_period": 12,
            "contract_url": "https://example.com/contracts/contract-001.pdf",
            "studio_number": "S-201-A",
            "customer_id_url": "https://example.com/documents/id-001.jpg",
            "commission": 500.00,
            "rent_price": 2500.00
        }
        print(f"Create rental contract: {json.dumps(rental_contract_data, indent=2)}")
    
    
    def run_all_tests(self):
        """Run all test examples"""
        print("🚀 Starting API Test Examples...")
        print("=" * 50)
        
        self.test_authentication()
        self.test_admin_management()
        self.test_apartment_sale()
        self.test_apartment_rent()
        self.test_apartment_parts()
        self.test_rental_contracts()
        
        print("\n✅ All test examples completed!")
        print("\n📝 Note: These are example data structures.")
        print("   To actually test the APIs, you need to:")
        print("   1. Start the server: uvicorn main:app --reload")
        print("   2. Login to get a token")
        print("   3. Use the token in Authorization header")
        print("   4. Make actual API calls with the provided data")

def main():
    """Main function to run the test examples"""
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()