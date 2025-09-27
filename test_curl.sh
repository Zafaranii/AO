#!/bin/bash

# API Test Script using curl
# Make sure the server is running: uvicorn main:app --reload

BASE_URL="http://localhost:8000"
TOKEN=""

echo "🚀 Starting API Tests with curl..."
echo "=================================="

# Function to create master admin
create_master_admin() {
    echo "👑 Creating master admin..."
    curl -X POST "$BASE_URL/api/v1/auth/create-master-admin" \
        -H "Content-Type: application/json" \
        -d '{
            "full_name": "Master Administrator",
            "email": "master@example.com",
            "phone": "+201111111111",
            "password": "masterpassword123",
            "master_password": "MASTER_ADMIN_SETUP_2024"
        }' | jq '.'
    echo ""
}

# Function to get token
get_token() {
    echo "🔐 Getting authentication token..."
    RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=master@example.com&password=masterpassword123")
    
    TOKEN=$(echo $RESPONSE | jq -r '.access_token')
    echo "Token: $TOKEN"
    echo ""
}

# Function to test apartment sale creation
test_create_apartment_sale() {
    echo "🏠 Testing apartment sale creation..."
    curl -X POST "$BASE_URL/api/v1/apartments/sale" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{
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
        }' | jq '.'
    echo ""
}

# Function to test apartment rent creation
test_create_apartment_rent() {
    echo "🏢 Testing apartment rent creation..."
    curl -X POST "$BASE_URL/api/v1/apartments/rent" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{
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
        }' | jq '.'
    echo ""
}

# Function to test apartment part creation
test_create_apartment_part() {
    echo "🏠 Testing apartment part creation..."
    curl -X POST "$BASE_URL/api/v1/apartments/rent/1/parts" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{
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
        }' | jq '.'
    echo ""
}

# Function to test rental contract creation
test_create_rental_contract() {
    echo "📋 Testing rental contract creation..."
    curl -X POST "$BASE_URL/api/v1/rental-contracts/" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{
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
        }' | jq '.'
    echo ""
}

# Function to test getting apartments
test_get_apartments() {
    echo "📋 Testing get apartments..."
    echo "Getting sale apartments:"
    curl -s "$BASE_URL/api/v1/apartments/sale" | jq '.'
    echo ""
    
    echo "Getting rent apartments:"
    curl -s "$BASE_URL/api/v1/apartments/rent" | jq '.'
    echo ""
}

# Function to test WhatsApp contact
test_whatsapp_contact() {
    echo "📱 Testing WhatsApp contact..."
    curl -s "$BASE_URL/api/v1/apartments/rent/1/whatsapp" | jq '.'
    echo ""
}

# Main execution
main() {
    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        echo "❌ jq is not installed. Please install jq to run this script."
        echo "   On macOS: brew install jq"
        echo "   On Ubuntu: sudo apt-get install jq"
        exit 1
    fi
    
    # Create master admin first (if needed)
    create_master_admin
    
    # Get authentication token
    get_token
    
    if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
        echo "❌ Failed to get authentication token. Please check your credentials."
        exit 1
    fi
    
    # Run tests
    test_create_apartment_sale
    test_create_apartment_rent
    test_create_apartment_part
    test_create_rental_contract
    test_get_apartments
    test_whatsapp_contact
    
    echo "✅ All tests completed!"
}

# Run main function
main
