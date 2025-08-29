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

def setup_sample_data():
    """Create some sample data for testing."""
    db = SessionLocal()
    try:
        from models import ApartmentRent, ApartmentSale
        
        # Check if sample data already exists
        existing_apartment = db.query(ApartmentRent).first()
        if existing_apartment:
            print("Sample data already exists")
            return
        
        # Create sample rent apartments
        sample_rent_apartments = [
            ApartmentRent(
                title="Luxury Apartment Downtown",
                location="Downtown, City Center",
                total_parts=4,
                description="Modern luxury apartment with 4 studios available for rent",
                rent_price=1200.00,
                listed_by_admin_id=1  # Assuming super admin ID is 1
            ),
            ApartmentRent(
                title="Student Housing Complex",
                location="University District",
                total_parts=10,
                description="Affordable housing for students with 10 individual studios",
                rent_price=800.00,
                listed_by_admin_id=1  # Assuming super admin ID is 1
            )
        ]
        
        # Create sample sale apartments
        sample_sale_apartments = [
            ApartmentSale(
                title="Family House for Sale",
                location="Suburban Area, Green Valley",
                description="Beautiful family house perfect for investment",
                price=350000.00
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
            setup_sample_data()
        
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
