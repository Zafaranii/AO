# API Testing Guide

This guide provides comprehensive test data and examples for all API endpoints in the AO Apartment Management System.

## Quick Start

1. **Start the server:**
   ```bash
   source .venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Run the test script:**
   ```bash
   python test_api.py
   ```

3. **Or run curl tests:**
   ```bash
   ./test_curl.sh
   ```

## Test Data Files

- `api_test_bodies.json` - Complete JSON test data for all endpoints
- `test_api.py` - Python test script with examples
- `test_curl.sh` - Bash script with curl commands

## API Endpoints Overview

### Authentication
- `POST /api/v1/auth/login` - Login with email/phone and password
- `POST /api/v1/auth/register` - Register new admin (super admin only)
- `POST /api/v1/auth/create-master-admin` - Create master admin with special password (initial setup only)

### Admin Management
- `GET /api/v1/admins/` - List all admins (super admin only)
- `GET /api/v1/admins/me` - Get current admin info
- `POST /api/v1/admins/` - Create new admin (super admin only)
- `PUT /api/v1/admins/{id}` - Update admin (super admin only)
- `DELETE /api/v1/admins/{id}` - Delete admin (super admin only)

### Apartments Sale
- `GET /api/v1/apartments/sale` - List apartments for sale
- `GET /api/v1/apartments/sale/{id}` - Get apartment sale details
- `POST /api/v1/apartments/sale` - Create apartment for sale (admin only)
- `PUT /api/v1/apartments/sale/{id}` - Update apartment sale (admin only)
- `DELETE /api/v1/apartments/sale/{id}` - Delete apartment sale (super admin only)

### Apartments Rent
- `GET /api/v1/apartments/rent` - List apartments for rent
- `GET /api/v1/apartments/rent/{id}` - Get apartment rent details with parts
- `POST /api/v1/apartments/rent` - Create apartment for rent (admin only)
- `PUT /api/v1/apartments/rent/{id}` - Update apartment rent (admin only)
- `DELETE /api/v1/apartments/rent/{id}` - Delete apartment rent (super admin only)

### Apartment Parts
- `GET /api/v1/apartments/rent/{id}/parts` - Get apartment parts
- `POST /api/v1/apartments/rent/{id}/parts` - Create apartment part (admin only)
- `PUT /api/v1/apartments/rent/{id}/parts/{part_id}` - Update apartment part (admin only)
- `DELETE /api/v1/apartments/rent/{id}/parts/{part_id}` - Delete apartment part (super admin only)

### Rental Contracts
- `GET /api/v1/rental-contracts/` - List rental contracts (admin only)
- `POST /api/v1/rental-contracts/` - Create rental contract (admin only)
- `PUT /api/v1/rental-contracts/{id}` - Update rental contract (admin only)
- `DELETE /api/v1/rental-contracts/{id}` - Delete rental contract (super admin only)


## Sample Test Data

### Login
```json
{
  "username": "admin@example.com",
  "password": "admin123"
}
```

### Create Master Admin
```json
{
  "full_name": "Master Administrator",
  "email": "master@example.com",
  "phone": "+201111111111",
  "password": "masterpassword123",
  "master_password": "MASTER_ADMIN_SETUP_2024"
}
```

### Create Apartment Sale
```json
{
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
```

### Create Apartment Rent
```json
{
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
```

### Create Apartment Part
```json
{
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
```

### Create Rental Contract
```json
{
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
```

## Enum Values

### LocationEnum
- `maadi`
- `mokkattam`

### BathroomTypeEnum
- `shared`
- `private`

### FurnishedEnum
- `yes`
- `no`

### BalconyEnum
- `yes`
- `shared`
- `no`

### PartStatusEnum
- `available`
- `rented`
- `upcoming_end`

### AdminRoleEnum
- `super_admin`
- `studio_rental`
- `apartment_sale`

### CustomerSourceEnum
- `facebook`
- `instagram`
- `google`
- `referral`
- `walk_in`
- `other`


## Testing with curl

### 1. Create master admin (initial setup)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/create-master-admin" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Master Administrator",
    "email": "master@example.com",
    "phone": "+201111111111",
    "password": "masterpassword123",
    "master_password": "MASTER_ADMIN_SETUP_2024"
  }'
```

### 2. Login and get token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=master@example.com&password=masterpassword123"
```

### 3. Create apartment sale
```bash
curl -X POST "http://localhost:8000/api/v1/apartments/sale" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Test Apartment",
    "location": "maadi",
    "address": "Test Address",
    "area": 100.0,
    "number": "A-001",
    "price": 1000000.0,
    "bedrooms": 2,
    "bathrooms": "private",
    "photos_url": ["https://example.com/photo1.jpg"]
  }'
```

### 4. Get apartments
```bash
curl "http://localhost:8000/api/v1/apartments/sale"
curl "http://localhost:8000/api/v1/apartments/rent"
```

## Testing with Python

```python
import requests

# Create master admin (initial setup)
master_admin_data = {
    "full_name": "Master Administrator",
    "email": "master@example.com",
    "phone": "+201111111111",
    "password": "masterpassword123",
    "master_password": "MASTER_ADMIN_SETUP_2024"
}
response = requests.post("http://localhost:8000/api/v1/auth/create-master-admin", 
                        json=master_admin_data)

# Login
response = requests.post("http://localhost:8000/api/v1/auth/login", data={
    "username": "master@example.com",
    "password": "masterpassword123"
})
token = response.json()["access_token"]

# Create apartment
headers = {"Authorization": f"Bearer {token}"}
apartment_data = {
    "name": "Test Apartment",
    "location": "maadi",
    # ... other fields
}
response = requests.post("http://localhost:8000/api/v1/apartments/sale", 
                        json=apartment_data, headers=headers)
```

## Notes

- All endpoints that require authentication need the `Authorization: Bearer TOKEN` header
- The `photos_url` field accepts an array of strings (multiple URLs)
- Date fields should be in `YYYY-MM-DD` format
- Decimal fields should be numbers (not strings)
- Make sure to replace `YOUR_TOKEN` with the actual token from login
- The server must be running on `http://localhost:8000` for these tests to work
