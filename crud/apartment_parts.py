from typing import Optional
import json

from sqlalchemy.orm import Session

from models import ApartmentPart, ApartmentRent, PartStatusEnum
from schemas.apartment_part import ApartmentPartCreate, ApartmentPartUpdate


def get_apartment_part(db: Session, part_id: int):
    return db.query(ApartmentPart).filter(ApartmentPart.id == part_id).first()


def get_apartment_parts(
    db: Session,
    apartment_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    status: Optional[PartStatusEnum] = None
):
    query = db.query(ApartmentPart)
    if apartment_id:
        query = query.filter(ApartmentPart.apartment_id == apartment_id)
    if status:
        query = query.filter(ApartmentPart.status == status)
    return query.offset(skip).limit(limit).all()


def create_apartment_part(db: Session, part: ApartmentPartCreate, admin_id: int, apartment_id: int, current_admin_role: str = None):
    from models import AdminRoleEnum
    # Get the apartment to inherit the floor
    apartment = db.query(ApartmentRent).filter(ApartmentRent.id == apartment_id).first()
    if not apartment:
        raise ValueError(f"Apartment with id {apartment_id} not found")
    
    # Check permissions: Master admin can create parts for any apartment,
    # regular admins can only create parts for apartments they created
    if current_admin_role != AdminRoleEnum.super_admin.value and apartment.listed_by_admin_id != admin_id:
        raise ValueError("Only the admin who created the apartment can create parts for it")
    
    # Create the apartment part with inherited floor
    part_data = part.dict()
    part_data['floor'] = apartment.floor  # Inherit floor from apartment
    
    # Convert photos_url list to JSON string
    if part_data.get('photos_url'):
        part_data['photos_url'] = json.dumps(part_data['photos_url'])
    
    db_part = ApartmentPart(
        apartment_id=apartment_id,
        **part_data,
        created_by_admin_id=admin_id
    )
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part


def update_apartment_part(db: Session, part_id: int, part: ApartmentPartUpdate, current_admin_id: int = None, current_admin_role: str = None):
    from models import AdminRoleEnum
    db_part = db.query(ApartmentPart).filter(ApartmentPart.id == part_id).first()
    if db_part:
        # Get the apartment to check ownership
        apartment = db.query(ApartmentRent).filter(ApartmentRent.id == db_part.apartment_id).first()
        
        # Check permissions: Master admin can update any part,
        # regular admins can only update parts for apartments they created
        if current_admin_role != AdminRoleEnum.super_admin.value and current_admin_id and apartment and apartment.listed_by_admin_id != current_admin_id:
            raise ValueError("Only the admin who created the apartment can update its parts")
        
        update_data = part.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'photos_url' and value is not None:
                setattr(db_part, field, json.dumps(value))
            else:
                setattr(db_part, field, value)
        db.commit()
        db.refresh(db_part)
    return db_part


def delete_apartment_part(db: Session, part_id: int, current_admin_id: int = None, current_admin_role: str = None):
    from models import AdminRoleEnum
    db_part = db.query(ApartmentPart).filter(ApartmentPart.id == part_id).first()
    if db_part:
        # Get the apartment to check ownership
        apartment = db.query(ApartmentRent).filter(ApartmentRent.id == db_part.apartment_id).first()
        
        # Check permissions: Master admin can delete any part,
        # regular admins can only delete parts for apartments they created
        if current_admin_role != AdminRoleEnum.super_admin.value and current_admin_id and apartment and apartment.listed_by_admin_id != current_admin_id:
            raise ValueError("Only the admin who created the apartment can delete its parts")
        
        db.delete(db_part)
        db.commit()
    return db_part



