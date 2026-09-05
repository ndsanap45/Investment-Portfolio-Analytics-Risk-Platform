from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Text,
    DateTime,
    ForeignKey
)
from datetime import datetime

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

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

    transaction_type = Column(
        String(20),
        nullable=False
    )

    quantity = Column(
        Numeric(18, 6),
        nullable=False
    )

    price = Column(
        Numeric(18, 4),
        nullable=False
    )

    fees = Column(
        Numeric(18, 4),
        default=0
    )

    transaction_date = Column(
        DateTime,
        nullable=False
    )

    notes = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )