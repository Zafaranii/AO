from sqlalchemy.orm import Session

from models import ApartmentSale
from schemas.apartment_sale import ApartmentSaleCreate, ApartmentSaleUpdate


def get_apartment_sale(db: Session, apartment_id: int):
    return db.query(ApartmentSale).filter(ApartmentSale.id == apartment_id).first()


def get_apartments_sale(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ApartmentSale).offset(skip).limit(limit).all()


def create_apartment_sale(db: Session, apartment: ApartmentSaleCreate):
    db_apartment = ApartmentSale(**apartment.dict())
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment


def update_apartment_sale(db: Session, apartment_id: int, apartment: ApartmentSaleUpdate):
    db_apartment = db.query(ApartmentSale).filter(ApartmentSale.id == apartment_id).first()
    if db_apartment:
        update_data = apartment.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_apartment, field, value)
        db.commit()
        db.refresh(db_apartment)
    return db_apartment


def delete_apartment_sale(db: Session, apartment_id: int):
    db_apartment = db.query(ApartmentSale).filter(ApartmentSale.id == apartment_id).first()
    if db_apartment:
        db.delete(db_apartment)
        db.commit()
    return db_apartment


