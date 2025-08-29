from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.types import Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class ApartmentRent(Base):
    __tablename__ = "apartment_rents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    location = Column(String(255), nullable=False)
    total_parts = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    rent_price = Column(Numeric(10, 2), nullable=False)
    listed_by_admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    apartment_parts = relationship("ApartmentPart", back_populates="apartment", cascade="all, delete-orphan")
    listed_by_admin = relationship("Admin")


