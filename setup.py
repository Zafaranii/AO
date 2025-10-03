#!/usr/bin/env python3
"""
Setup script for Real Estate Platform
This script creates the initial super admin user and sets up the database.
"""

import asyncio
import sys
import os
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
            full_name=admin_name,
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
        from models import ApartmentRent, ApartmentSale, ApartmentPart, RentalContract
        from models.enums import LocationEnum, BathroomTypeEnum, FurnishedEnum, BalconyEnum, PartStatusEnum, CustomerSourceEnum
        import json
        from datetime import date, timedelta

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

        # Refresh to get IDs
        for apartment in sample_rent_apartments:
            db.refresh(apartment)

        # Create apartment parts for the first rent apartment
        primary_rent_apartment = sample_rent_apartments[0]
        parts = [
            ApartmentPart(
                apartment_id=primary_rent_apartment.id,
                status=PartStatusEnum.available,
                title="Studio S-301-A",
                area=30.0,
                floor=primary_rent_apartment.floor,
                monthly_price=3500.00,
                bedrooms=1,
                bathrooms=BathroomTypeEnum.private,
                furnished=FurnishedEnum.yes,
                balcony=BalconyEnum.yes,
                description="Cozy studio with balcony and AC",
                photos_url=json.dumps([
                    "https://example.com/photos/studio-a1.jpg"
                ]),
                created_by_admin_id=admin_id,
            ),
            ApartmentPart(
                apartment_id=primary_rent_apartment.id,
                status=PartStatusEnum.rented,
                title="Studio S-301-B",
                area=28.0,
                floor=primary_rent_apartment.floor,
                monthly_price=3400.00,
                bedrooms=1,
                bathrooms=BathroomTypeEnum.private,
                furnished=FurnishedEnum.no,
                balcony=BalconyEnum.no,
                description="Bright studio, great value",
                photos_url=json.dumps([
                    "https://example.com/photos/studio-b1.jpg"
                ]),
                created_by_admin_id=admin_id,
            ),
        ]

        for part in parts:
            db.add(part)
        db.commit()
        for part in parts:
            db.refresh(part)

        # Create a rental contract for the rented part (second part)
        rented_part = parts[1]
        start_date = date.today().replace(day=1)
        end_date = start_date + timedelta(days=365)

        contract = RentalContract(
            apartment_part_id=rented_part.id,
            customer_name="John Doe",
            customer_phone="+201234567890",
            customer_id_number="12345678901234",
            how_did_customer_find_us=CustomerSourceEnum.facebook,
            paid_deposit=3400.00,
            warrant_amount=3400.00,
            rent_start_date=start_date,
            rent_end_date=end_date,
            rent_period=12,
            contract_url="https://example.com/contracts/sample1.pdf",
            customer_id_url="https://example.com/documents/id1.jpg",
            commission=340.00,
            rent_price=3400.00,
            is_active=True,
            created_by_admin_id=admin_id,
        )

        db.add(contract)
        db.commit()

        print("Sample apartments, parts, and rental contract created successfully!")

    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def setup_sample_parts_for_existing(super_admin: Admin, force: bool = False):
    """Create sample apartment parts (and a rental contract) for an existing rent apartment.
    If force=True, parts are created even if parts already exist for the chosen apartment.
    """
    db = SessionLocal()
    try:
        from models import ApartmentRent, ApartmentPart, RentalContract
        from models.enums import BathroomTypeEnum, FurnishedEnum, BalconyEnum, PartStatusEnum, CustomerSourceEnum
        import json
        from datetime import date, timedelta

        rent_apartment = db.query(ApartmentRent).order_by(ApartmentRent.id.asc()).first()
        if not rent_apartment:
            print("No rent apartments found. Please create rent apartments first.")
            return

        existing_parts = db.query(ApartmentPart).filter(ApartmentPart.apartment_id == rent_apartment.id).count()
        if existing_parts > 0 and not force:
            print(f"Apartment parts already exist for rent apartment id={rent_apartment.id}; skipping part seeding. Use --force to override.")
            return

        admin_id = super_admin.id

        parts = [
            ApartmentPart(
                apartment_id=rent_apartment.id,
                status=PartStatusEnum.available,
                title="Studio A",
                area=30.0,
                floor=rent_apartment.floor,
                monthly_price=3500.00,
                bedrooms=1,
                bathrooms=BathroomTypeEnum.private,
                furnished=FurnishedEnum.yes,
                balcony=BalconyEnum.yes,
                description="Cozy studio with balcony and AC",
                photos_url=json.dumps(["https://example.com/photos/studio-a1.jpg"]),
                created_by_admin_id=admin_id,
            ),
            ApartmentPart(
                apartment_id=rent_apartment.id,
                status=PartStatusEnum.rented,
                title="Studio B",
                area=28.0,
                floor=rent_apartment.floor,
                monthly_price=3400.00,
                bedrooms=1,
                bathrooms=BathroomTypeEnum.private,
                furnished=FurnishedEnum.no,
                balcony=BalconyEnum.no,
                description="Bright studio, great value",
                photos_url=json.dumps(["https://example.com/photos/studio-b1.jpg"]),
                created_by_admin_id=admin_id,
            ),
        ]

        # If forcing, delete existing parts for that apartment first
        if existing_parts > 0 and force:
            # Delete rental contracts referencing existing parts, then delete parts
            existing_part_ids = [pid for (pid,) in db.query(ApartmentPart.id).filter(
                ApartmentPart.apartment_id == rent_apartment.id
            ).all()]
            if existing_part_ids:
                db.query(RentalContract).filter(
                    RentalContract.apartment_part_id.in_(existing_part_ids)
                ).delete(synchronize_session=False)
                db.commit()
                db.query(ApartmentPart).filter(
                    ApartmentPart.id.in_(existing_part_ids)
                ).delete(synchronize_session=False)
                db.commit()

        for part in parts:
            db.add(part)
        db.commit()
        for part in parts:
            db.refresh(part)

        rented_part = parts[1]
        start_date = date.today().replace(day=1)
        end_date = start_date + timedelta(days=365)

        # Remove existing contracts for that part when forcing
        if force:
            db.query(RentalContract).filter(RentalContract.apartment_part_id == rented_part.id).delete()
            db.commit()

        contract = RentalContract(
            apartment_part_id=rented_part.id,
            customer_name="John Doe",
            customer_phone="+201234567890",
            customer_id_number="12345678901234",
            how_did_customer_find_us=CustomerSourceEnum.facebook,
            paid_deposit=3400.00,
            warrant_amount=3400.00,
            rent_start_date=start_date,
            rent_end_date=end_date,
            rent_period=12,
            contract_url="https://example.com/contracts/sample1.pdf",
            customer_id_url="https://example.com/documents/id1.jpg",
            commission=340.00,
            rent_price=3400.00,
            is_active=True,
            created_by_admin_id=admin_id,
        )
        db.add(contract)
        db.commit()

        print(f"Created 2 apartment parts and 1 rental contract for rent apartment id={rent_apartment.id}.")

    except Exception as e:
        print(f"Error creating sample parts/contracts: {e}")
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
        auto_create = (
            "--create-sample" in sys.argv or
            "-y" in sys.argv or
            os.getenv("CREATE_SAMPLE_DATA", "").lower() in ["1", "true", "yes", "y"]
        )
        create_parts_only = (
            "--create-parts" in sys.argv or
            os.getenv("CREATE_SAMPLE_PARTS", "").lower() in ["1", "true", "yes", "y"]
        )
        force = ("--force" in sys.argv or os.getenv("FORCE_SAMPLE", "").lower() in ["1", "true", "yes", "y"]) 
        if auto_create:
            setup_sample_data(super_admin)
        elif create_parts_only:
            setup_sample_parts_for_existing(super_admin, force=force)
        else:
            try:
                create_sample = input("Do you want to create sample data? (y/n): ").lower().strip()
                if create_sample in ['y', 'yes']:
                    setup_sample_data(super_admin)
                else:
                    create_parts = input("Only create parts and a contract for existing rent apartment? (y/n): ").lower().strip()
                    if create_parts in ['y', 'yes']:
                        setup_sample_parts_for_existing(super_admin, force=False)
            except EOFError:
                print("Non-interactive session detected; skipping sample data. Use --create-sample or --create-parts, optionally with --force.")
        
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
