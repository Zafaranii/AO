from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, Text
from sqlalchemy.types import Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from .enums import PartStatusEnum, BathroomTypeEnum, FurnishedEnum, BalconyEnum


class ApartmentPart(Base):
    __tablename__ = "apartment_parts"

    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("apartment_rents.id"), nullable=False)
    status = Column(Enum(PartStatusEnum), nullable=False, default=PartStatusEnum.available)
    title = Column(String(200), nullable=False)
    area = Column(Numeric(8, 2), nullable=False)  # Area in square meters
    floor = Column(Integer, nullable=False)
    monthly_price = Column(Numeric(10, 2), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Enum(BathroomTypeEnum), nullable=False)
    furnished = Column(Enum(FurnishedEnum), nullable=False)
    balcony = Column(Enum(BalconyEnum), nullable=False)
    description = Column(Text, nullable=True)
    photos_url = Column(Text, nullable=True)  # JSON string of photo URLs
    created_by_admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    apartment = relationship("ApartmentRent", back_populates="apartment_parts")
    created_by_admin = relationship("Admin", back_populates="created_apartment_parts")
    rental_contract = relationship("RentalContract", back_populates="apartment_part", uselist=False)


