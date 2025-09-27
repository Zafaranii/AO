from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.types import Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from .enums import LocationEnum, BathroomTypeEnum


class ApartmentSale(Base):
    __tablename__ = "apartment_sales"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    location = Column(Enum(LocationEnum), nullable=False)
    address = Column(String(500), nullable=False)
    area = Column(Numeric(8, 2), nullable=False)  # Area in square meters
    number = Column(String(50), nullable=False)  # Apartment number
    price = Column(Numeric(12, 2), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Enum(BathroomTypeEnum), nullable=False)
    description = Column(Text, nullable=True)
    contact_number = Column(String(20), nullable=False)  # Auto-filled from admin
    photos_url = Column(Text, nullable=True)  # JSON string of photo URLs
    location_on_map = Column(String(500), nullable=True)  # Google Maps or similar link
    facilities_amenities = Column(Text, nullable=True)  # Facilities and amenities
    listed_by_admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    listed_by_admin = relationship("Admin")


