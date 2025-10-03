#!/usr/bin/env python3
"""
Setup script for Real Estate Platform
This script creates the initial super admin user and sets up the database.
"""

import asyncio
import sys
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Admin, AdminRoleEnum
from dependencies import get_password_hash
from decouple import config

def create_database_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def create_super_admin():
    """Create the initial super admin user."""
    db = SessionLocal()
    try:
        # Check if super admin already exists
        existing_super_admin = db.query(Admin).filter(Admin.role == AdminRoleEnum.super_admin).first()
        if existing_super_admin:
            print(f"Super admin already exists: {existing_super_admin.email}")
            return existing_super_admin
        
        # Get admin details from environment variables or prompt
        admin_name = config("SUPER_ADMIN_NAME", default="Super Admin")
        admin_email = config("SUPER_ADMIN_EMAIL", default="")
        admin_phone = config("SUPER_ADMIN_PHONE", default="")
        admin_password = config("SUPER_ADMIN_PASSWORD", default="")
        
        if not admin_email:
            admin_email = input("Enter super admin email: ")
        if not admin_phone:
            admin_phone = input("Enter super admin phone: ")
        if not admin_password:
            admin_password = input("Enter super admin password: ")
        
        # Create super admin
        hashed_password = get_password_hash(admin_password)
        super_admin = Admin(
            name=admin_name,
            email=admin_email,
            phone=admin_phone,
            role=AdminRoleEnum.super_admin,
            password=hashed_password
        )
        
        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)
        
        print(f"Super admin created successfully!")
        print(f"Email: {super_admin.email}")
        print(f"Name: {super_admin.name}")
        print(f"Phone: {super_admin.phone}")
        
        return super_admin
        
    except Exception as e:
        print(f"Error creating super admin: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def setup_sample_data(super_admin: Admin):
    """Create some sample data for testing."""
    db = SessionLocal()
    try:
        from models import ApartmentRent, ApartmentSale
        from models.enums import LocationEnum, BathroomTypeEnum
        import json

        # Check if sample data already exists
        existing_apartment = db.query(ApartmentRent).first()
        if existing_apartment:
            print("Sample data already exists")
            return

        admin_id = super_admin.id
        admin_phone = super_admin.phone or "+201234567890"

        # Create sample rent apartments (match current model fields)
        sample_rent_apartments = [
            ApartmentRent(
                name="Luxury Studio in Maadi",
                location=LocationEnum.maadi,
                address="123 Maadi Corniche, Cairo, Egypt",
                area=50.0,
                number="S-301",
                price=4000.00,
                bedrooms=1,
                bathrooms=BathroomTypeEnum.private,
                description="Luxury studio with modern amenities",
                photos_url=json.dumps([
                    "https://example.com/photos/luxury-studio-1.jpg",
                    "https://example.com/photos/luxury-studio-2.jpg"
                ]),
                location_on_map="https://maps.google.com/example3",
                facilities_amenities="24/7 Security, Elevator, Balcony, Air Conditioning, Gym",
                floor=8,
                total_parts=2,
                listed_by_admin_id=admin_id,
                contact_number=admin_phone,
            ),
            ApartmentRent(
                name="Student Housing Complex",
                location=LocationEnum.mokkattam,
                address="45 University District, Cairo, Egypt",
                area=35.0,
                number="S-102",
                price=3800.00,
                bedrooms=1,
                bathrooms=BathroomTypeEnum.private,
                description="Affordable housing for students",
                photos_url=json.dumps([
                    "https://example.com/photos/student-1.jpg"
                ]),
                location_on_map="https://maps.google.com/example4",
                facilities_amenities="Elevator, Security",
                floor=5,
                total_parts=10,
                listed_by_admin_id=admin_id,
                contact_number=admin_phone,
            ),
        ]

        # Create sample sale apartments (match current model fields)
        sample_sale_apartments = [
            ApartmentSale(
                name="Family House for Sale",
                location=LocationEnum.mokkattam,
                address="789 Green Valley, Cairo, Egypt",
                area=120.5,
                number="V-101",
                price=465000.00,
                bedrooms=3,
                bathrooms=BathroomTypeEnum.private,
                description="Beautiful family house perfect for investment",
                photos_url=json.dumps([
                    "https://example.com/photos/villa-exterior.jpg",
                    "https://example.com/photos/villa-interior.jpg"
                ]),
                location_on_map="https://maps.google.com/example6",
                facilities_amenities="Garden, Parking, Security, Air Conditioning",
                listed_by_admin_id=admin_id,
                contact_number=admin_phone,
            )
        ]

        for apartment in sample_rent_apartments:
            db.add(apartment)

        for apartment in sample_sale_apartments:
            db.add(apartment)

        db.commit()
        print("Sample apartments created successfully!")

    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main setup function."""
    print("=" * 50)
    print("Real Estate Platform Setup")
    print("=" * 50)
    
    try:
        # Step 1: Create database tables
        create_database_tables()
        
        # Step 2: Create super admin
        super_admin = create_super_admin()
        if not super_admin:
            print("Failed to create super admin. Exiting...")
            sys.exit(1)
        
        # Step 3: Create sample data (optional)
        create_sample = input("Do you want to create sample data? (y/n): ").lower().strip()
        if create_sample in ['y', 'yes']:
            setup_sample_data(super_admin)
        
        print("\n" + "=" * 50)
        print("Setup completed successfully!")
        print("=" * 50)
        print("\nYou can now:")
        print("1. Start the application: python main.py")
        print("2. Access the API docs: http://localhost:8000/docs")
        print("3. Login with your super admin credentials")
        print("\nFor production deployment:")
        print("1. Update the .env file with your configuration")
        print("2. Use a proper WSGI server like Gunicorn")
        print("3. Set up a reverse proxy like Nginx")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
