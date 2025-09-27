from sqlalchemy.orm import Session
import json

from models import ApartmentRent
from schemas.apartment_rent import ApartmentRentCreate, ApartmentRentUpdate


def get_apartment_rent(db: Session, apartment_id: int):
    return db.query(ApartmentRent).filter(ApartmentRent.id == apartment_id).first()


def get_apartments_rent(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ApartmentRent).offset(skip).limit(limit).all()


def get_apartments_rent_by_admin(db: Session, admin_id: int, skip: int = 0, limit: int = 100):
    """Get apartments created by a specific admin."""
    return db.query(ApartmentRent).filter(ApartmentRent.listed_by_admin_id == admin_id).offset(skip).limit(limit).all()


def get_apartments_with_parts_by_admin(db: Session, admin_id: int, admin_role: str = None, skip: int = 0, limit: int = 100):
    """Get apartments with their parts created by a specific admin. If admin is super_admin, return all apartments."""
    from models import ApartmentPart, AdminRoleEnum
    
    # If admin is super_admin, get all apartments, otherwise get only admin's apartments
    if admin_role == AdminRoleEnum.super_admin.value:
        apartments = db.query(ApartmentRent).offset(skip).limit(limit).all()
    else:
        apartments = db.query(ApartmentRent).filter(ApartmentRent.listed_by_admin_id == admin_id).offset(skip).limit(limit).all()
    
    # For each apartment, get its parts
    result = []
    for apartment in apartments:
        apartment_dict = {
            "id": apartment.id,
            "name": apartment.name,
            "location": apartment.location,
            "address": apartment.address,
            "area": apartment.area,
            "number": apartment.number,
            "price": apartment.price,
            "bedrooms": apartment.bedrooms,
            "bathrooms": apartment.bathrooms,
            "description": apartment.description,
            "photos_url": apartment.photos_url,
            "location_on_map": apartment.location_on_map,
            "facilities_amenities": apartment.facilities_amenities,
            "floor": apartment.floor,
            "total_parts": apartment.total_parts,
            "contact_number": apartment.contact_number,
            "listed_by_admin_id": apartment.listed_by_admin_id,
            "created_at": apartment.created_at,
            "updated_at": apartment.updated_at,
            "apartment_parts": []
        }
        
        # Get parts for this apartment
        parts = db.query(ApartmentPart).filter(ApartmentPart.apartment_id == apartment.id).all()
        for part in parts:
            part_dict = {
                "id": part.id,
                "apartment_id": part.apartment_id,
                "status": part.status,
                "title": part.title,
                "area": part.area,
                "floor": part.floor,
                "monthly_price": part.monthly_price,
                "bedrooms": part.bedrooms,
                "bathrooms": part.bathrooms,
                "furnished": part.furnished,
                "balcony": part.balcony,
                "description": part.description,
                "photos_url": part.photos_url,
                "created_by_admin_id": part.created_by_admin_id,
                "created_at": part.created_at,
                "updated_at": part.updated_at
            }
            apartment_dict["apartment_parts"].append(part_dict)
        
        result.append(apartment_dict)
    
    return result


def create_apartment_rent(db: Session, apartment: ApartmentRentCreate, listed_by_admin_id: int, admin_phone: str):
    apartment_data = apartment.dict()
    apartment_data['listed_by_admin_id'] = listed_by_admin_id
    apartment_data['contact_number'] = admin_phone
    
    # Convert photos_url list to JSON string
    if apartment_data.get('photos_url'):
        apartment_data['photos_url'] = json.dumps(apartment_data['photos_url'])
    
    db_apartment = ApartmentRent(**apartment_data)
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment


def update_apartment_rent(db: Session, apartment_id: int, apartment: ApartmentRentUpdate, current_admin_id: int = None, current_admin_role: str = None):
    from models import AdminRoleEnum
    db_apartment = db.query(ApartmentRent).filter(ApartmentRent.id == apartment_id).first()
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


def delete_apartment_rent(db: Session, apartment_id: int, current_admin_id: int = None, current_admin_role: str = None):
    from models import AdminRoleEnum
    db_apartment = db.query(ApartmentRent).filter(ApartmentRent.id == apartment_id).first()
    if db_apartment:
        # Check permissions: Master admin can delete any apartment,
        # regular admins can only delete apartments they created
        if current_admin_role != AdminRoleEnum.super_admin.value and current_admin_id and db_apartment.listed_by_admin_id != current_admin_id:
            raise ValueError("Only the admin who created the apartment can delete it")
        
        db.delete(db_apartment)
        db.commit()
    return db_apartment


