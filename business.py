from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from persistance import Base, TimestampMixin


class CreateBusinessModel(BaseModel):
    name: str
    description: str


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
