import re
from datetime import date
from enum import Enum
from pydantic import BaseModel
from app.persistance import Base, TimestampMixin
from sqlalchemy import event, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.persistance import Base, TimestampMixin


class CreateBusinessModel(BaseModel):
    name: str
    description: str


class UpdateBusinessModel(BaseModel):
    name: str | None = None
    description: str | None = None


class Business(Base, TimestampMixin):
    __tablename__ = "business"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    locations: Mapped[list["Location"]] = relationship(
        "Location", back_populates="business"
    )


class CreateLocationModel(BaseModel):
    name: str
    description: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    latitude: float
    longitude: float
    business_id: int


class Location(Base, TimestampMixin):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    business: Mapped["Business"] = relationship("Business", back_populates="locations")
    promotion_locations: Mapped[list["PromotionLocation"]] = relationship(
        "PromotionLocation", back_populates="location"
    )


class PromotionType(str, Enum):
    DISCOUNT = "discount"
    FREE_SHIPPING = "free_shipping"


def generate_slug(name: str, id: int | None = None) -> str:
    """Generate a URL-friendly slug from the name and id."""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", name.lower())
    slug = re.sub(r"\s+", "-", slug).strip("-")

    # Add id if available
    if id is not None:
        slug = f"{slug}-{id}"

    return slug


class CreatePromotionModel(BaseModel):
    """Model for creating a promotion."""

    name: str
    description: str | None = None
    promotion_type: PromotionType
    start_date: date
    end_date: date
    is_active: bool = True


class UpdatePromotionModel(BaseModel):
    """Model for updating a promotion."""

    name: str | None = None
    description: str | None = None
    promotion_type: PromotionType | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None


class Promotion(Base, TimestampMixin):
    __tablename__ = "promotion"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    promotion_type: Mapped[str] = mapped_column()
    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    slug: Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)
    promotion_locations: Mapped[list["PromotionLocation"]] = relationship(
        "PromotionLocation", back_populates="promotion"
    )


@event.listens_for(Promotion, "after_insert")
def update_slug_after_insert(mapper, connection, target):
    """Update the slug with the ID after the record has been inserted."""
    # Now we have the ID, update the slug
    target.slug = generate_slug(target.name, target.id)

    # Update the record in the database

    sql = text(f"UPDATE {target.__tablename__} SET slug = :slug WHERE id = :id")
    connection.execute(sql, {"slug": target.slug, "id": target.id})


@event.listens_for(Promotion, "after_update")
def update_slug_after_update(mapper, connection, target):
    """Update the slug with the ID after the record has been updated."""
    target.slug = generate_slug(target.name, target.id)

    sql = text(f"UPDATE {target.__tablename__} SET slug = :slug WHERE id = :id")
    connection.execute(sql, {"slug": target.slug, "id": target.id})


class PromotionLocation(Base, TimestampMixin):
    __tablename__ = "promotion_location"

    promotion_id: Mapped[int] = mapped_column(
        ForeignKey("promotion.id"), primary_key=True
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey("location.id"), primary_key=True
    )
    promotion: Mapped["Promotion"] = relationship(
        "Promotion", back_populates="promotion_locations"
    )
    location: Mapped["Location"] = relationship(
        "Location", back_populates="promotion_locations"
    )
