from typing import Optional

from sqlalchemy.orm import Session

from models import ApartmentPart, PartStatusEnum
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


def create_apartment_part(db: Session, part: ApartmentPartCreate, admin_id: int, apartment_id: int):
    db_part = ApartmentPart(
        apartment_id=apartment_id,
        **part.dict(),
        created_by_admin_id=admin_id
    )
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part


def update_apartment_part(db: Session, part_id: int, part: ApartmentPartUpdate):
    db_part = db.query(ApartmentPart).filter(ApartmentPart.id == part_id).first()
    if db_part:
        update_data = part.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_part, field, value)
        db.commit()
        db.refresh(db_part)
    return db_part


def delete_apartment_part(db: Session, part_id: int):
    db_part = db.query(ApartmentPart).filter(ApartmentPart.id == part_id).first()
    if db_part:
        db.delete(db_part)
        db.commit()
    return db_part



