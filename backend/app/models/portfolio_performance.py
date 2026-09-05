from sqlalchemy import (
    Column, Integer, Numeric, Date,
    DateTime, ForeignKey
)
from datetime import datetime

from app.db.database import Base


class PortfolioPerformance(Base):
    __tablename__ = "portfolio_performance"

    id = Column(Integer, primary_key=True, index=True)

    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id"),
        nullable=False,
        index=True
    )

    date = Column(Date, nullable=False, index=True)

    portfolio_return = Column(Numeric(12, 6), nullable=False)
    benchmark_return = Column(Numeric(12, 6))
    excess_return = Column(Numeric(12, 6))

    portfolio_value = Column(Numeric(18, 4), nullable=False)
    benchmark_value = Column(Numeric(18, 4))

    created_at = Column(DateTime, default=datetime.utcnow)