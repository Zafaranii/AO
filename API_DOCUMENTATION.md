# AO Real Estate API Documentation

## Overview

This API provides endpoints for managing real estate properties, admin users, and rental contracts. The API is built with FastAPI and uses JWT authentication.

**Base URL:** `http://localhost:8000/api/v1`

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Response Format

All API responses follow this format:

### Success Response
```json
{
  "data": <response_data>,
  "message": "Success message (optional)"
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

## API Endpoints

### 1. Authentication

#### 1.1 Login
**POST** `/auth/login`

**Description:** Authenticate admin user and get access token

**Request Body:**
```json
{
  "username": "admin@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 1.2 Create Master Admin
**POST** `/auth/create-master-admin`

**Description:** Create initial master admin (one-time setup)

**Request Body:**
```json
{
  "full_name": "Master Administrator",
  "email": "master@example.com",
  "phone": "+201111111111",
  "password": "masterpassword123",
  "master_password": "MASTER_ADMIN_SETUP_2024"
}
```

**Response:**
```json
{
  "id": 1,
  "full_name": "Master Administrator",
  "email": "master@example.com",
  "phone": "+201111111111",
  "role": "super_admin",
  "created_at": "2025-09-05T19:51:52",
  "updated_at": null
}
```

### 2. Admin Management

#### 2.1 List All Admins
**GET** `/admins/`

**Description:** Get list of all admins (super admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "full_name": "Master Administrator",
    "email": "master@example.com",
    "phone": "+201111111111",
    "role": "super_admin",
    "created_at": "2025-09-05T19:51:52",
    "updated_at": null
  },
  {
    "id": 2,
    "full_name": "Test Admin",
    "email": "test@example.com",
    "phone": "+201234567890",
    "role": "studio_rental",
    "created_at": "2025-09-05T20:02:26",
    "updated_at": null
  }
]
```

#### 2.2 Get Current Admin Info
**GET** `/admins/me`

**Description:** Get current authenticated admin's information

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "full_name": "Master Administrator",
  "email": "master@example.com",
  "phone": "+201111111111",
  "role": "super_admin",
  "created_at": "2025-09-05T19:51:52",
  "updated_at": null
}
```

#### 2.3 Get Admin by ID
**GET** `/admins/{admin_id}`

**Description:** Get specific admin by ID (super admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 2,
  "full_name": "Test Admin",
  "email": "test@example.com",
  "phone": "+201234567890",
  "role": "studio_rental",
  "created_at": "2025-09-05T20:02:26",
  "updated_at": null
}
```

#### 2.4 Create New Admin
**POST** `/admins/`

**Description:** Create a new admin (super admin only)

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "New Admin",
  "email": "newadmin@example.com",
  "phone": "+201234567890",
  "password": "password123",
  "role": "apartment_sale"
}
```

**Response:**
```json
{
  "id": 3,
  "full_name": "New Admin",
  "email": "newadmin@example.com",
  "phone": "+201234567890",
  "role": "apartment_sale",
  "created_at": "2025-09-05T20:15:30",
  "updated_at": null
}
```

#### 2.5 Update Admin
**PUT** `/admins/{admin_id}`

**Description:** Update admin information (super admin only)

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "Updated Admin Name",
  "email": "updated@example.com",
  "phone": "+201234567890",
  "role": "studio_rental"
}
```

**Response:**
```json
{
  "id": 3,
  "full_name": "Updated Admin Name",
  "email": "updated@example.com",
  "phone": "+201234567890",
  "role": "studio_rental",
  "created_at": "2025-09-05T20:15:30",
  "updated_at": "2025-09-05T20:20:15"
}
```

#### 2.6 Delete Admin
**DELETE** `/admins/{admin_id}`

**Description:** Delete admin (super admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Admin deleted successfully"
}
```

### 3. Apartment Rent Management

#### 3.1 List Rent Apartments
**GET** `/apartments/rent`

**Description:** Get list of all rent apartments

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Modern Studio Apartment in Mokattam",
    "location": "mokkattam",
    "address": "456 Mokattam Hills, Cairo, Egypt",
    "area": "45.75",
    "number": "S-201",
    "price": "3500.00",
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
    "total_parts": 3,
    "contact_number": "string",
    "listed_by_admin_id": 4,
    "created_at": "2025-09-05T20:10:47",
    "updated_at": null
  }
]
```

#### 3.2 Get Rent Apartment by ID
**GET** `/apartments/rent/{apartment_id}`

**Description:** Get specific rent apartment by ID

**Response:**
```json
{
  "id": 1,
  "name": "Modern Studio Apartment in Mokattam",
  "location": "mokkattam",
  "address": "456 Mokattam Hills, Cairo, Egypt",
  "area": "45.75",
  "number": "S-201",
  "price": "3500.00",
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
  "total_parts": 3,
  "contact_number": "string",
  "listed_by_admin_id": 4,
  "created_at": "2025-09-05T20:10:47",
  "updated_at": null
}
```

#### 3.3 Create Rent Apartment
**POST** `/apartments/rent`

**Description:** Create a new rent apartment (admin only)

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Luxury Studio in Maadi",
  "location": "maadi",
  "address": "123 Maadi Corniche, Cairo, Egypt",
  "area": "50.0",
  "number": "S-301",
  "price": "4000.00",
  "bedrooms": 1,
  "bathrooms": "private",
  "description": "Luxury studio with modern amenities",
  "photos_url": [
    "https://example.com/photos/luxury-studio-1.jpg",
    "https://example.com/photos/luxury-studio-2.jpg"
  ],
  "location_on_map": "https://maps.google.com/example3",
  "facilities_amenities": "24/7 Security, Elevator, Balcony, Air Conditioning, Gym",
  "floor": 8,
  "total_parts": 2,
  "contact_number": "+201234567890"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Luxury Studio in Maadi",
  "location": "maadi",
  "address": "123 Maadi Corniche, Cairo, Egypt",
  "area": "50.0",
  "number": "S-301",
  "price": "4000.00",
  "bedrooms": 1,
  "bathrooms": "private",
  "description": "Luxury studio with modern amenities",
  "photos_url": [
    "https://example.com/photos/luxury-studio-1.jpg",
    "https://example.com/photos/luxury-studio-2.jpg"
  ],
  "location_on_map": "https://maps.google.com/example3",
  "facilities_amenities": "24/7 Security, Elevator, Balcony, Air Conditioning, Gym",
  "floor": 8,
  "total_parts": 2,
  "contact_number": "+201234567890",
  "listed_by_admin_id": 1,
  "created_at": "2025-09-05T20:25:15",
  "updated_at": null
}
```

#### 3.4 Update Rent Apartment
**PUT** `/apartments/rent/{apartment_id}`

**Description:** Update rent apartment (admin only). Master admin can update any apartment, regular admins can only update apartments they created.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Updated Studio Name",
  "price": "4500.00",
  "description": "Updated description"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Updated Studio Name",
  "location": "maadi",
  "address": "123 Maadi Corniche, Cairo, Egypt",
  "area": "50.0",
  "number": "S-301",
  "price": "4500.00",
  "bedrooms": 1,
  "bathrooms": "private",
  "description": "Updated description",
  "photos_url": [
    "https://example.com/photos/luxury-studio-1.jpg",
    "https://example.com/photos/luxury-studio-2.jpg"
  ],
  "location_on_map": "https://maps.google.com/example3",
  "facilities_amenities": "24/7 Security, Elevator, Balcony, Air Conditioning, Gym",
  "floor": 8,
  "total_parts": 2,
  "contact_number": "+201234567890",
  "listed_by_admin_id": 1,
  "created_at": "2025-09-05T20:25:15",
  "updated_at": "2025-09-05T20:30:20"
}
```

#### 3.5 Delete Rent Apartment
**DELETE** `/apartments/rent/{apartment_id}`

**Description:** Delete rent apartment (admin only). Master admin can delete any apartment, regular admins can only delete apartments they created.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Apartment deleted successfully"
}
```

### 4. Apartment Sale Management

#### 4.1 List Sale Apartments
**GET** `/apartments/sale`

**Description:** Get list of all sale apartments

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "name": "3BR Villa in Green Valley",
    "location": "mokkattam",
    "address": "789 Green Valley, Cairo, Egypt",
    "area": "120.5",
    "number": "V-101",
    "price": "465000.00",
    "bedrooms": 3,
    "bathrooms": "private",
    "description": "Beautiful 3-bedroom villa with garden",
    "photos_url": [
      "https://example.com/photos/villa-exterior.jpg",
      "https://example.com/photos/villa-interior.jpg"
    ],
    "location_on_map": "https://maps.google.com/example4",
    "facilities_amenities": "Garden, Parking, Security, Air Conditioning",
    "floor": 1,
    "total_parts": 1,
    "contact_number": "+201234567890",
    "listed_by_admin_id": 1,
    "created_at": "2025-09-05T20:35:10",
    "updated_at": null
  }
]
```

#### 4.2 Get Sale Apartment by ID
**GET** `/apartments/sale/{apartment_id}`

**Description:** Get specific sale apartment by ID

**Response:**
```json
{
  "id": 1,
  "name": "3BR Villa in Green Valley",
  "location": "mokkattam",
  "address": "789 Green Valley, Cairo, Egypt",
  "area": "120.5",
  "number": "V-101",
  "price": "465000.00",
  "bedrooms": 3,
  "bathrooms": "private",
  "description": "Beautiful 3-bedroom villa with garden",
  "photos_url": [
    "https://example.com/photos/villa-exterior.jpg",
    "https://example.com/photos/villa-interior.jpg"
  ],
  "location_on_map": "https://maps.google.com/example4",
  "facilities_amenities": "Garden, Parking, Security, Air Conditioning",
  "floor": 1,
  "total_parts": 1,
  "contact_number": "+201234567890",
  "listed_by_admin_id": 1,
  "created_at": "2025-09-05T20:35:10",
  "updated_at": null
}
```

#### 4.3 Create Sale Apartment
**POST** `/apartments/sale`

**Description:** Create a new sale apartment (admin only)

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "2BR Apartment in Maadi",
  "location": "maadi",
  "address": "456 Maadi Street, Cairo, Egypt",
  "area": "85.0",
  "number": "A-201",
  "price": "250000.00",
  "bedrooms": 2,
  "bathrooms": "private",
  "description": "Modern 2-bedroom apartment",
  "photos_url": [
    "https://example.com/photos/apartment-1.jpg",
    "https://example.com/photos/apartment-2.jpg"
  ],
  "location_on_map": "https://maps.google.com/example5",
  "facilities_amenities": "Elevator, Security, Air Conditioning",
  "floor": 3,
  "total_parts": 1,
  "contact_number": "+201234567890"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "2BR Apartment in Maadi",
  "location": "maadi",
  "address": "456 Maadi Street, Cairo, Egypt",
  "area": "85.0",
  "number": "A-201",
  "price": "250000.00",
  "bedrooms": 2,
  "bathrooms": "private",
  "description": "Modern 2-bedroom apartment",
  "photos_url": [
    "https://example.com/photos/apartment-1.jpg",
    "https://example.com/photos/apartment-2.jpg"
  ],
  "location_on_map": "https://maps.google.com/example5",
  "facilities_amenities": "Elevator, Security, Air Conditioning",
  "floor": 3,
  "total_parts": 1,
  "contact_number": "+201234567890",
  "listed_by_admin_id": 1,
  "created_at": "2025-09-05T20:40:25",
  "updated_at": null
}
```

#### 4.4 Update Sale Apartment
**PUT** `/apartments/sale/{apartment_id}`

**Description:** Update sale apartment (admin only). Master admin can update any apartment, regular admins can only update apartments they created.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Updated Apartment Name",
  "price": "275000.00",
  "description": "Updated description"
}
```

**Response:**
```json
{
  "id": 2,
  "name": "Updated Apartment Name",
  "location": "maadi",
  "address": "456 Maadi Street, Cairo, Egypt",
  "area": "85.0",
  "number": "A-201",
  "price": "275000.00",
  "bedrooms": 2,
  "bathrooms": "private",
  "description": "Updated description",
  "photos_url": [
    "https://example.com/photos/apartment-1.jpg",
    "https://example.com/photos/apartment-2.jpg"
  ],
  "location_on_map": "https://maps.google.com/example5",
  "facilities_amenities": "Elevator, Security, Air Conditioning",
  "floor": 3,
  "total_parts": 1,
  "contact_number": "+201234567890",
  "listed_by_admin_id": 1,
  "created_at": "2025-09-05T20:40:25",
  "updated_at": "2025-09-05T20:45:30"
}
```

#### 4.5 Delete Sale Apartment
**DELETE** `/apartments/sale/{apartment_id}`

**Description:** Delete sale apartment (admin only). Master admin can delete any apartment, regular admins can only delete apartments they created.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Apartment deleted successfully"
}
```

### 5. Apartment Parts Management

#### 5.1 List All Apartment Parts
**GET** `/apartments/parts`

**Description:** Get list of all apartment parts

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "apartment_id": 1,
    "studio_number": "S-101",
    "rent_value": "3500.00",
    "status": "available",
    "floor": 5,
    "created_by_admin_id": 1,
    "created_at": "2025-09-05T20:50:15",
    "updated_at": null
  }
]
```

#### 5.2 Get Apartment Part by ID
**GET** `/apartments/parts/{part_id}`

**Description:** Get specific apartment part by ID

**Response:**
```json
{
  "id": 1,
  "apartment_id": 1,
  "studio_number": "S-101",
  "rent_value": "3500.00",
  "status": "available",
  "floor": 5,
  "created_by_admin_id": 1,
  "created_at": "2025-09-05T20:50:15",
  "updated_at": null
}
```

#### 5.3 Create Apartment Part
**POST** `/apartments/rent/{apartment_id}/parts`

**Description:** Create a new apartment part for rent apartment (admin only). Master admin can create parts for any apartment, regular admins can only create parts for apartments they created.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "studio_number": "S-102",
  "rent_value": "3800.00",
  "floor": 6
}
```

**Response:**
```json
{
  "id": 2,
  "apartment_id": 1,
  "studio_number": "S-102",
  "rent_value": "3800.00",
  "status": "available",
  "floor": 6,
  "created_by_admin_id": 1,
  "created_at": "2025-09-05T20:55:20",
  "updated_at": null
}
```

#### 5.4 Update Apartment Part
**PUT** `/apartments/parts/{part_id}`

**Description:** Update apartment part (admin only). Master admin can update parts for any apartment, regular admins can only update parts for apartments they created.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "studio_number": "S-102A",
  "rent_value": "4000.00",
  "status": "rented"
}
```

**Response:**
```json
{
  "id": 2,
  "apartment_id": 1,
  "studio_number": "S-102A",
  "rent_value": "4000.00",
  "status": "rented",
  "floor": 6,
  "created_by_admin_id": 1,
  "created_at": "2025-09-05T20:55:20",
  "updated_at": "2025-09-05T21:00:25"
}
```

#### 5.5 Delete Apartment Part
**DELETE** `/apartments/parts/{part_id}`

**Description:** Delete apartment part (admin only). Master admin can delete parts for any apartment, regular admins can only delete parts for apartments they created.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Apartment part deleted successfully"
}
```

#### 5.6 Get Admin's Own Content
**GET** `/apartments/my-content`

**Description:** Get apartments and studios created by the requesting admin. Master admin sees all apartments from all admins, regular admins see only their own apartments (admin only).

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**
```json
{
  "rent_apartments": [
    {
      "id": 1,
      "name": "Test Apartment",
      "location": "maadi",
      "address": "123 Test Street, Cairo, Egypt",
      "area": "50.00",
      "number": "T-101",
      "price": "3000.00",
      "bedrooms": 1,
      "bathrooms": "private",
      "description": "Test apartment description",
      "photos_url": ["https://example.com/test1.jpg"],
      "location_on_map": "https://maps.google.com/test",
      "facilities_amenities": "Test amenities",
      "floor": 1,
      "total_parts": 1,
      "contact_number": "+201111111111",
      "listed_by_admin_id": 1,
      "created_at": "2025-09-05T21:01:51",
      "updated_at": null,
      "apartment_parts": [
        {
          "id": 1,
          "apartment_id": 1,
          "status": "available",
          "title": "Studio T-101A",
          "area": "30.00",
          "floor": 1,
          "monthly_price": "3000.00",
          "bedrooms": 1,
          "bathrooms": "private",
          "furnished": "yes",
          "balcony": "yes",
          "description": "Test studio description",
          "photos_url": ["https://example.com/studio1.jpg"],
          "created_by_admin_id": 1,
          "created_at": "2025-09-05T21:02:05",
          "updated_at": null
        }
      ]
    }
  ],
  "sale_apartments": [
    {
      "id": 1,
      "name": "Sale Apartment",
      "location": "mokkattam",
      "address": "456 Sale Street, Cairo, Egypt",
      "area": "85.0",
      "number": "A-201",
      "price": "250000.00",
      "bedrooms": 2,
      "bathrooms": "private",
      "description": "Sale apartment description",
      "photos_url": ["https://example.com/sale1.jpg"],
      "location_on_map": "https://maps.google.com/sale",
      "facilities_amenities": "Elevator, Security, Air Conditioning",
      "floor": 3,
      "total_parts": 1,
      "contact_number": "+201234567890",
      "listed_by_admin_id": 1,
      "created_at": "2025-09-05T20:40:25",
      "updated_at": null
    }
  ],
  "total_rent_apartments": 1,
  "total_sale_apartments": 1,
  "total_studios": 1
}
```

### 6. Rental Contracts Management

#### 6.1 List Rental Contracts
**GET** `/rental-contracts/`

**Description:** Get list of all rental contracts (admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)
- `apartment_id` (optional): Filter by apartment ID
- `is_active` (optional): Filter by active status (true/false)

**Response:**
```json
[
  {
    "id": 1,
    "apartment_part_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "+201234567890",
    "customer_id_number": "12345678901234",
    "how_did_customer_find_us": "facebook",
    "paid_deposit": "3500.00",
    "warrant_amount": "3500.00",
    "rent_start_date": "2025-09-01",
    "rent_end_date": "2026-08-31",
    "rent_period": 12,
    "contract_url": "https://example.com/contracts/contract1.pdf",
    "studio_number": "S-101",
    "customer_id_url": "https://example.com/documents/id1.jpg",
    "commission": "350.00",
    "rent_price": "3500.00",
    "is_active": true,
    "created_by_admin_id": 1,
    "created_at": "2025-09-05T21:05:30",
    "updated_at": null
  }
]
```

#### 6.2 List Rental Contracts by Studio (Ordered)
**GET** `/rental-contracts/by-studio`

**Description:** Get list of rental contracts ordered by studio number (latest first) (admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)
- `apartment_id` (optional): Filter by apartment ID
- `is_active` (optional): Filter by active status (true/false)

**Response:**
```json
[
  {
    "id": 3,
    "apartment_part_id": 3,
    "customer_name": "Alice Johnson",
    "customer_phone": "+201111111111",
    "customer_id_number": "11111111111111",
    "how_did_customer_find_us": "instagram",
    "paid_deposit": "4000.00",
    "warrant_amount": "4000.00",
    "rent_start_date": "2025-10-01",
    "rent_end_date": "2026-09-30",
    "rent_period": 12,
    "contract_url": "https://example.com/contracts/contract3.pdf",
    "studio_number": "S-103",
    "customer_id_url": "https://example.com/documents/id3.jpg",
    "commission": "400.00",
    "rent_price": "4000.00",
    "is_active": true,
    "created_by_admin_id": 1,
    "created_at": "2025-09-05T21:15:45",
    "updated_at": null
  },
  {
    "id": 2,
    "apartment_part_id": 2,
    "customer_name": "Jane Smith",
    "customer_phone": "+201987654321",
    "customer_id_number": "98765432109876",
    "how_did_customer_find_us": "google",
    "paid_deposit": "3800.00",
    "warrant_amount": "3800.00",
    "rent_start_date": "2025-09-15",
    "rent_end_date": "2026-09-14",
    "rent_period": 12,
    "contract_url": "https://example.com/contracts/contract2.pdf",
    "studio_number": "S-102",
    "customer_id_url": "https://example.com/documents/id2.jpg",
    "commission": "380.00",
    "rent_price": "3800.00",
    "is_active": true,
    "created_by_admin_id": 1,
    "created_at": "2025-09-05T21:10:30",
    "updated_at": null
  },
  {
    "id": 1,
    "apartment_part_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "+201234567890",
    "customer_id_number": "12345678901234",
    "how_did_customer_find_us": "facebook",
    "paid_deposit": "3500.00",
    "warrant_amount": "3500.00",
    "rent_start_date": "2025-09-01",
    "rent_end_date": "2026-08-31",
    "rent_period": 12,
    "contract_url": "https://example.com/contracts/contract1.pdf",
    "studio_number": "S-101",
    "customer_id_url": "https://example.com/documents/id1.jpg",
    "commission": "350.00",
    "rent_price": "3500.00",
    "is_active": true,
    "created_by_admin_id": 1,
    "created_at": "2025-09-05T21:05:30",
    "updated_at": null
  }
]
```

#### 6.3 Get Rental Contract by ID
**GET** `/rental-contracts/{contract_id}`

**Description:** Get specific rental contract by ID (admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "apartment_part_id": 1,
  "customer_name": "John Doe",
  "customer_phone": "+201234567890",
  "customer_id_number": "12345678901234",
  "how_did_customer_find_us": "facebook",
  "paid_deposit": "3500.00",
  "warrant_amount": "3500.00",
  "rent_start_date": "2025-09-01",
  "rent_end_date": "2026-08-31",
  "rent_period": 12,
  "contract_url": "https://example.com/contracts/contract1.pdf",
  "studio_number": "S-101",
  "customer_id_url": "https://example.com/documents/id1.jpg",
  "commission": "350.00",
  "rent_price": "3500.00",
  "is_active": true,
  "created_by_admin_id": 1,
  "created_at": "2025-09-05T21:05:30",
  "updated_at": null
}
```

#### 6.4 Create Rental Contract
**POST** `/rental-contracts/`

**Description:** Create a new rental contract (admin only). Master admin can create contracts for any apartment, regular admins can only create contracts for apartments they created.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "apartment_part_id": 1,
  "customer_name": "Jane Smith",
  "customer_phone": "+201987654321",
  "customer_id_number": "98765432109876",
  "how_did_customer_find_us": "instagram",
  "paid_deposit": "3800.00",
  "warrant_amount": "3800.00",
  "rent_start_date": "2025-10-01",
  "rent_end_date": "2026-09-30",
  "rent_period": 12,
  "contract_url": "https://example.com/contracts/contract2.pdf",
  "studio_number": "S-102",
  "customer_id_url": "https://example.com/documents/id2.jpg",
  "commission": "380.00",
  "rent_price": "3800.00"
}
```

**Response:**
```json
{
  "id": 2,
  "apartment_part_id": 1,
  "customer_name": "Jane Smith",
  "customer_phone": "+201987654321",
  "customer_id_number": "98765432109876",
  "how_did_customer_find_us": "instagram",
  "paid_deposit": "3800.00",
  "warrant_amount": "3800.00",
  "rent_start_date": "2025-10-01",
  "rent_end_date": "2026-09-30",
  "rent_period": 12,
  "contract_url": "https://example.com/contracts/contract2.pdf",
  "studio_number": "S-102",
  "customer_id_url": "https://example.com/documents/id2.jpg",
  "commission": "380.00",
  "rent_price": "3800.00",
  "is_active": true,
  "created_by_admin_id": 1,
  "created_at": "2025-09-05T21:10:45",
  "updated_at": null
}
```

#### 6.5 Update Rental Contract
**PUT** `/rental-contracts/{contract_id}`

**Description:** Update rental contract (admin only)

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "customer_name": "Jane Smith Updated",
  "rent_price": "4000.00",
  "is_active": false
}
```

**Response:**
```json
{
  "id": 2,
  "apartment_part_id": 1,
  "customer_name": "Jane Smith Updated",
  "customer_phone": "+201987654321",
  "customer_id_number": "98765432109876",
  "how_did_customer_find_us": "instagram",
  "paid_deposit": "3800.00",
  "warrant_amount": "3800.00",
  "rent_start_date": "2025-10-01",
  "rent_end_date": "2026-09-30",
  "rent_period": 12,
  "contract_url": "https://example.com/contracts/contract2.pdf",
  "studio_number": "S-102",
  "customer_id_url": "https://example.com/documents/id2.jpg",
  "commission": "380.00",
  "rent_price": "4000.00",
  "is_active": false,
  "created_by_admin_id": 1,
  "created_at": "2025-09-05T21:10:45",
  "updated_at": "2025-09-05T21:15:50"
}
```

#### 6.6 Delete Rental Contract
**DELETE** `/rental-contracts/{contract_id}`

**Description:** Delete rental contract (super admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Rental contract deleted successfully"
}
```

## Data Types and Enums

### Admin Roles
- `super_admin`: Full system access
- `studio_rental`: Can manage studio rentals
- `apartment_sale`: Can manage apartment sales

### Apartment Types
- `rent`: For rental properties
- `purchase`: For sale properties

### Part Status
- `available`: Available for rent
- `rented`: Currently rented
- `upcoming_end`: Contract ending soon

### Bathroom Types
- `shared`: Shared bathroom
- `private`: Private bathroom

### Furnished Status
- `yes`: Furnished
- `no`: Unfurnished

### Balcony Types
- `yes`: Has balcony
- `shared`: Shared balcony
- `no`: No balcony

### Locations
- `maadi`: Maadi area
- `mokkattam`: Mokattam area

### Customer Sources
- `facebook`: Found through Facebook
- `instagram`: Found through Instagram
- `google`: Found through Google
- `referral`: Referred by someone
- `walk_in`: Walk-in customer
- `other`: Other source

## Error Codes

### HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

### Common Error Messages
- `"Could not validate credentials"`: Invalid or expired token
- `"Not authenticated"`: Missing or invalid authentication
- `"Insufficient permissions"`: User doesn't have required role
- `"Email already registered"`: Email already exists
- `"Phone number already registered"`: Phone number already exists
- `"Apartment not found"`: Apartment doesn't exist
- `"Admin not found"`: Admin doesn't exist
- `"Rental contract not found"`: Contract doesn't exist
- `"Only the admin who created the apartment can create contracts for its studios"`: Authorization error when trying to create a contract for an apartment created by another admin
- `"Only the admin who created the apartment can update it"`: Authorization error when trying to update an apartment created by another admin
- `"Only the admin who created the apartment can delete it"`: Authorization error when trying to delete an apartment created by another admin
- `"Only the admin who created the apartment can create parts for it"`: Authorization error when trying to create apartment parts for an apartment created by another admin
- `"Only the admin who created the apartment can update its parts"`: Authorization error when trying to update apartment parts for an apartment created by another admin
- `"Only the admin who created the apartment can delete its parts"`: Authorization error when trying to delete apartment parts for an apartment created by another admin

## Rate Limiting

Currently, there are no rate limits implemented. However, it's recommended to implement reasonable request limits in production.

## Pagination

Most list endpoints support pagination using `skip` and `limit` parameters:

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

Example:
```
GET /apartments/rent?skip=20&limit=10
```

## File Uploads

Currently, file uploads are handled via URL strings in the request body. The API expects URLs to uploaded files rather than direct file uploads.

## Webhooks

Currently, no webhooks are implemented.

## SDKs and Libraries

No official SDKs are provided. Use any HTTP client library in your preferred language to interact with the API.

## Support

For API support and questions, please contact the development team.

## Changelog

### Version 1.0.0
- Initial API release
- Authentication system
- Admin management
- Apartment management (rent and sale)
- Apartment parts management
- Rental contracts management
- Notification system removed
