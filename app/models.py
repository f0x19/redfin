from __future__ import annotations

from datetime import datetime
from typing import Dict, Any, List

from sqlalchemy import Index, String, Integer, Float, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db


class Property(db.Model):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    address_line: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    state: Mapped[str] = mapped_column(String(20), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(20), nullable=False)

    price: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bathrooms: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    property_type: Mapped[str] = mapped_column(String(50), nullable=False, default="house")

    square_feet: Mapped[int] = mapped_column(Integer, nullable=True)
    lot_size_sqft: Mapped[int] = mapped_column(Integer, nullable=True)

    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    year_built: Mapped[int] = mapped_column(Integer, nullable=True)

    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="for_sale")

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    images: Mapped[List["PropertyImage"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    __table_args__ = (
        Index("idx_properties_city_state", "city", "state"),
        Index("idx_properties_created_at", "created_at"),
    )

    def to_dict(self, include_images: bool = False) -> Dict[str, Any]:
        primary_image = next((img for img in self.images if img.is_primary), None)
        cover_url = (
            primary_image.url
            if primary_image
            else (self.images[0].url if self.images else None)
        )
        data: Dict[str, Any] = {
            "id": self.id,
            "title": self.title,
            "address_line": self.address_line,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "price": self.price,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "property_type": self.property_type,
            "square_feet": self.square_feet,
            "lot_size_sqft": self.lot_size_sqft,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "year_built": self.year_built,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "cover_image_url": cover_url,
        }
        if include_images:
            data["images"] = [img.to_dict() for img in self.images]
        return data


class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    property: Mapped[Property] = relationship(back_populates="images")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "property_id": self.property_id,
            "url": self.url,
            "is_primary": self.is_primary,
            "created_at": self.created_at.isoformat(),
        }
