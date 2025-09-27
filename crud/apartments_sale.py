from sqlalchemy.orm import Session
import json

from models import ApartmentSale
from schemas.apartment_sale import ApartmentSaleCreate, ApartmentSaleUpdate


def get_apartment_sale(db: Session, apartment_id: int):
    return db.query(ApartmentSale).filter(ApartmentSale.id == apartment_id).first()


def get_apartments_sale(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ApartmentSale).offset(skip).limit(limit).all()


def get_apartments_sale_by_admin(db: Session, admin_id: int, admin_role: str = None, skip: int = 0, limit: int = 100):
    """Get sale apartments created by a specific admin. If admin is super_admin, return all apartments."""
    from models import AdminRoleEnum
    
    # If admin is super_admin, get all apartments, otherwise get only admin's apartments
    if admin_role == AdminRoleEnum.super_admin.value:
        return db.query(ApartmentSale).offset(skip).limit(limit).all()
    else:
        return db.query(ApartmentSale).filter(ApartmentSale.listed_by_admin_id == admin_id).offset(skip).limit(limit).all()


def create_apartment_sale(db: Session, apartment: ApartmentSaleCreate, admin_id: int, admin_phone: str):
    apartment_data = apartment.dict()
    apartment_data['listed_by_admin_id'] = admin_id
    apartment_data['contact_number'] = admin_phone
    
    # Convert photos_url list to JSON string
    if apartment_data.get('photos_url'):
        apartment_data['photos_url'] = json.dumps(apartment_data['photos_url'])
    
    db_apartment = ApartmentSale(**apartment_data)
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment


def update_apartment_sale(db: Session, apartment_id: int, apartment: ApartmentSaleUpdate, current_admin_id: int = None, current_admin_role: str = None):
    from models import AdminRoleEnum
    db_apartment = db.query(ApartmentSale).filter(ApartmentSale.id == apartment_id).first()
    if db_apartment:
        # Check permissions: Master admin can update any apartment,
        # regular admins can only update apartments they created
        if current_admin_role != AdminRoleEnum.super_admin.value and current_admin_id and db_apartment.listed_by_admin_id != current_admin_id:
            raise ValueError("Only the admin who created the apartment can update it")
        
        update_data = apartment.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'photos_url' and value is not None:
                setattr(db_apartment, field, json.dumps(value))
            else:
                setattr(db_apartment, field, value)
        db.commit()
        db.refresh(db_apartment)
    return db_apartment


def delete_apartment_sale(db: Session, apartment_id: int, current_admin_id: int = None, current_admin_role: str = None):
    from models import AdminRoleEnum
    db_apartment = db.query(ApartmentSale).filter(ApartmentSale.id == apartment_id).first()
    if db_apartment:
        # Check permissions: Master admin can delete any apartment,
        # regular admins can only delete apartments they created
        if current_admin_role != AdminRoleEnum.super_admin.value and current_admin_id and db_apartment.listed_by_admin_id != current_admin_id:
            raise ValueError("Only the admin who created the apartment can delete it")
        
        db.delete(db_apartment)
        db.commit()
    return db_apartment


