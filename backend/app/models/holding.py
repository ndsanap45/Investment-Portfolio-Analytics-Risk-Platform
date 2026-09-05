from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from datetime import datetime

from app.db.database import Base


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)

    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id"),
        nullable=False,
        index=True
    )

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False,
        index=True
    )

    quantity = Column(
        Numeric(18, 6),
        nullable=False,
        default=0
    )

    average_cost = Column(
        Numeric(18, 4),
        nullable=False,
        default=0
    )

    current_price = Column(
        Numeric(18, 4),
        nullable=True
    )

    market_value = Column(
        Numeric(18, 4),
        nullable=True
    )

    unrealized_pnl = Column(
        Numeric(18, 4),
        nullable=True
    )

    unrealized_pnl_percent = Column(
        Numeric(10, 4),
        nullable=True
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )