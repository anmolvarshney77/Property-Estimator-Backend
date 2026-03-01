"""SQLAlchemy ORM models."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Estimate(Base):
    __tablename__ = "estimates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    square_footage: Mapped[float] = mapped_column(Float, nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    bathrooms: Mapped[float] = mapped_column(Float, nullable=False)
    year_built: Mapped[int] = mapped_column(Integer, nullable=False)
    lot_size: Mapped[float] = mapped_column(Float, nullable=False)
    distance_to_city_center: Mapped[float] = mapped_column(Float, nullable=False)
    school_rating: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
