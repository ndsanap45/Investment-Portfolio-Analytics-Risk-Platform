from sqlalchemy import (
    Column, Integer, Numeric, Date,
    DateTime, ForeignKey, UniqueConstraint
)
from datetime import datetime

from app.db.database import Base


class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id"),
        nullable=False,
        index=True
    )

    snapshot_date = Column(Date, nullable=False)

    total_value = Column(Numeric(18, 4), nullable=False)
    invested_amount = Column(Numeric(18, 4), nullable=False)
    cash_balance = Column(Numeric(18, 4), default=0)
    daily_pnl = Column(Numeric(18, 4), default=0)
    daily_return = Column(Numeric(12, 6), default=0)
    cumulative_return = Column(Numeric(12, 6), default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "portfolio_id",
            "snapshot_date",
            name="uq_snapshot_portfolio_date"
        ),
    )