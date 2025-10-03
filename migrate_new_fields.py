#!/usr/bin/env python3
"""
Migration script to clean up unwanted fields.
This script removes redundant and unnecessary fields from database tables.
"""

import sys
from sqlalchemy import text
from database import engine, SessionLocal

def migrate_database():
    """Remove unwanted fields from database tables."""
    db = SessionLocal()
    try:
        print("Starting database cleanup migration...")
        
        # Remove unwanted fields from apartment_sales table
        print("Removing unwanted fields from apartment_sales table...")
        
        # Remove floor column if it exists
        try:
            db.execute(text("ALTER TABLE apartment_sales DROP COLUMN floor"))
            print("✓ Removed 'floor' column from apartment_sales")
        except Exception as e:
            if "doesn't exist" in str(e) or "Unknown column" in str(e):
                print("✓ 'floor' column doesn't exist in apartment_sales")
            else:
                print(f"⚠ Warning removing 'floor' column: {e}")
        
        # Remove total_parts column if it exists
        try:
            db.execute(text("ALTER TABLE apartment_sales DROP COLUMN total_parts"))
            print("✓ Removed 'total_parts' column from apartment_sales")
        except Exception as e:
            if "doesn't exist" in str(e) or "Unknown column" in str(e):
                print("✓ 'total_parts' column doesn't exist in apartment_sales")
            else:
                print(f"⚠ Warning removing 'total_parts' column: {e}")
        
        # Remove unwanted fields from apartment_parts table
        print("Removing unwanted fields from apartment_parts table...")
        
        # Remove studio_number column if it exists
        try:
            db.execute(text("ALTER TABLE apartment_parts DROP COLUMN studio_number"))
            print("✓ Removed 'studio_number' column from apartment_parts")
        except Exception as e:
            if "doesn't exist" in str(e) or "Unknown column" in str(e):
                print("✓ 'studio_number' column doesn't exist in apartment_parts")
            else:
                print(f"⚠ Warning removing 'studio_number' column: {e}")
        
        # Remove rent_value column if it exists
        try:
            db.execute(text("ALTER TABLE apartment_parts DROP COLUMN rent_value"))
            print("✓ Removed 'rent_value' column from apartment_parts")
        except Exception as e:
            if "doesn't exist" in str(e) or "Unknown column" in str(e):
                print("✓ 'rent_value' column doesn't exist in apartment_parts")
            else:
                print(f"⚠ Warning removing 'rent_value' column: {e}")
        
        # Remove unwanted fields from rental_contracts table
        print("Removing unwanted fields from rental_contracts table...")
        
        # Remove studio_number column if it exists
        try:
            db.execute(text("ALTER TABLE rental_contracts DROP COLUMN studio_number"))
            print("✓ Removed 'studio_number' column from rental_contracts")
        except Exception as e:
            if "doesn't exist" in str(e) or "Unknown column" in str(e):
                print("✓ 'studio_number' column doesn't exist in rental_contracts")
            else:
                print(f"⚠ Warning removing 'studio_number' column: {e}")
        
        # Commit all changes
        db.commit()
        print("\n✅ Database cleanup completed successfully!")
        print("\nRemoved fields:")
        print("- apartment_sales: floor, total_parts")
        print("- apartment_parts: studio_number, rent_value")
        print("- rental_contracts: studio_number")
        print("\nAll existing data has been preserved.")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    migrate_database()
