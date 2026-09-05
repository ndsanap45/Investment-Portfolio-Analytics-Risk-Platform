from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint
from datetime import datetime

from app.db.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(20), nullable=False)

    name = Column(String(150), nullable=False)

    asset_type = Column(String(50), nullable=False)

    exchange = Column(String(20), nullable=False)

    currency = Column(String(10), default="INR", nullable=False)

    sector = Column(String(100), nullable=True)

    country = Column(String(100), default="India")

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "symbol",
            "exchange",
            name="uq_asset_symbol_exchange"
        ),
    )