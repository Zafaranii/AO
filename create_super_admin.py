#!/usr/bin/env python3
"""
Create Super Admin User Script
This script creates a super admin user for the Real Estate Platform.
"""

import sys
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Admin, AdminRoleEnum
from dependencies import get_password_hash
from decouple import config

def create_super_admin():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if super admin already exists
        existing_super_admin = db.query(Admin).filter(
            Admin.role == AdminRoleEnum.super_admin
        ).first()
        
        if existing_super_admin:
            print("❌ Super admin already exists!")
            print(f"Email: {existing_super_admin.email}")
            return
        
        print("🔧 Creating Super Admin")
        print("=====================")
        
        # Get admin details
        name = input("Enter admin name: ").strip()
        if not name:
            print("❌ Name cannot be empty")
            return
        
        email = input("Enter admin email: ").strip()
        if not email:
            print("❌ Email cannot be empty")
            return
        
        # Check if email already exists
        existing_admin = db.query(Admin).filter(Admin.email == email).first()
        if existing_admin:
            print("❌ Admin with this email already exists!")
            return
        
        phone = input("Enter admin phone: ").strip()
        if not phone:
            print("❌ Phone cannot be empty")
            return
        
        password = getpass("Enter admin password: ")
        if len(password) < 6:
            print("❌ Password must be at least 6 characters")
            return
        
        confirm_password = getpass("Confirm password: ")
        if password != confirm_password:
            print("❌ Passwords do not match")
            return
        
        # Create super admin
        hashed_password = get_password_hash(password)
        super_admin = Admin(
            name=name,
            email=email,
            phone=phone,
            role=AdminRoleEnum.super_admin,
            password=hashed_password
        )
        
        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)
        
        print("✅ Super admin created successfully!")
        print(f"ID: {super_admin.id}")
        print(f"Name: {super_admin.name}")
        print(f"Email: {super_admin.email}")
        print(f"Role: {super_admin.role.value}")
        
    except Exception as e:
        print(f"❌ Error creating super admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_super_admin()
