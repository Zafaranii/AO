from sqlalchemy.orm import Session

from models import ApartmentRent
from schemas.apartment_rent import ApartmentRentCreate, ApartmentRentUpdate


def get_apartment_rent(db: Session, apartment_id: int):
    return db.query(ApartmentRent).filter(ApartmentRent.id == apartment_id).first()


def get_apartments_rent(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ApartmentRent).offset(skip).limit(limit).all()


def create_apartment_rent(db: Session, apartment: ApartmentRentCreate, listed_by_admin_id: int):
    db_apartment = ApartmentRent(**apartment.dict(), listed_by_admin_id=listed_by_admin_id)
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment


def update_apartment_rent(db: Session, apartment_id: int, apartment: ApartmentRentUpdate):
    db_apartment = db.query(ApartmentRent).filter(ApartmentRent.id == apartment_id).first()
    if db_apartment:
        update_data = apartment.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_apartment, field, value)
        db.commit()
        db.refresh(db_apartment)
    return db_apartment


def delete_apartment_rent(db: Session, apartment_id: int):
    db_apartment = db.query(ApartmentRent).filter(ApartmentRent.id == apartment_id).first()
    if db_apartment:
        db.delete(db_apartment)
        db.commit()
    return db_apartment


