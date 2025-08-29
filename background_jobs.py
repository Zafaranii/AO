import asyncio
from datetime import date, timedelta
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from decouple import config

from database import SessionLocal
from models import Admin, AdminRoleEnum, NotificationStatusEnum
from schemas.notification import NotificationCreate
from crud import get_expiring_contracts, create_notification, get_admins

# Configuration
NOTIFICATION_DAYS_AHEAD = config("NOTIFICATION_DAYS_AHEAD", default=30, cast=int)
UNPAID_RENT_CHECK_DAYS = config("UNPAID_RENT_CHECK_DAYS", default=5, cast=int)

scheduler = AsyncIOScheduler()

async def check_contract_expirations():
    """Background job to check for contract expirations and create notifications."""
    db = SessionLocal()
    try:
        # Get contracts expiring within the specified days
        expiring_contracts = get_expiring_contracts(db, days_ahead=NOTIFICATION_DAYS_AHEAD)
        
        # Get all admins to notify (you can modify this logic)
        admins = get_admins(db)
        admin_to_notify = None
        
        # Prefer super admin for notifications
        for admin in admins:
            if admin.role == AdminRoleEnum.super_admin:
                admin_to_notify = admin
                break
        
        # If no super admin, use first admin
        if not admin_to_notify and admins:
            admin_to_notify = admins[0]
        
        if not admin_to_notify:
            print("No admin found to send notifications")
            return
        
        notifications_created = 0
        for contract in expiring_contracts:
            # Calculate days until expiration
            days_until_expiry = (contract.contract_end_date - date.today()).days
            
            description = (
                f"Contract for {contract.tenant_name} in apartment {contract.apartment_part.apartment.title} "
                f"(Studio {contract.apartment_part.studio_number}) expires in {days_until_expiry} days "
                f"on {contract.contract_end_date.strftime('%Y-%m-%d')}"
            )
            
            notification = NotificationCreate(
                rental_contract_id=contract.id,
                status=NotificationStatusEnum.upcoming_end,
                notify_admin_id=admin_to_notify.id,
                description=description
            )
            
            created_notification = create_notification(db, notification)
            if created_notification:
                notifications_created += 1
        
        print(f"Contract expiration check completed. Created {notifications_created} notifications.")
        
    except Exception as e:
        print(f"Error in contract expiration check: {e}")
    finally:
        db.close()

async def check_unpaid_rent():
    """Background job to check for unpaid rent and create notifications."""
    db = SessionLocal()
    try:
        # This is a placeholder - in a real implementation, you'd need to track
        # rent payment dates and check for overdue payments
        # For now, we'll just demonstrate the structure
        
        # You could add a payment tracking table and check for unpaid rent here
        print("Unpaid rent check completed (placeholder implementation)")
        
    except Exception as e:
        print(f"Error in unpaid rent check: {e}")
    finally:
        db.close()

def start_scheduler():
    """Start the background job scheduler."""
    # Schedule contract expiration check daily at 9:00 AM
    scheduler.add_job(
        check_contract_expirations,
        CronTrigger(hour=9, minute=0),
        id="contract_expiration_check",
        name="Check contract expirations",
        replace_existing=True
    )
    
    # Schedule unpaid rent check daily at 10:00 AM
    scheduler.add_job(
        check_unpaid_rent,
        CronTrigger(hour=10, minute=0),
        id="unpaid_rent_check",
        name="Check unpaid rent",
        replace_existing=True
    )
    
    scheduler.start()
    print("Background job scheduler started")

def stop_scheduler():
    """Stop the background job scheduler."""
    scheduler.shutdown()
    print("Background job scheduler stopped")

# For manual testing
async def run_manual_checks():
    """Run all checks manually for testing."""
    print("Running manual contract expiration check...")
    await check_contract_expirations()
    
    print("Running manual unpaid rent check...")
    await check_unpaid_rent()

if __name__ == "__main__":
    # For testing the background jobs manually
    asyncio.run(run_manual_checks())
