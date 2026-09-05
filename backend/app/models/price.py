from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Index
from app.db.database import Base


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False,
        index=True
    )

    price = Column(Numeric(18, 4), nullable=False)
    open_price = Column(Numeric(18, 4))
    high_price = Column(Numeric(18, 4))
    low_price = Column(Numeric(18, 4))
    close_price = Column(Numeric(18, 4))
    volume = Column(Numeric(20, 4))

    timestamp = Column(DateTime, nullable=False, index=True)

    __table_args__ = (
        Index("ix_prices_asset_timestamp", "asset_id", "timestamp"),
    )