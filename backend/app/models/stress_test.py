from sqlalchemy import (
    Column, Integer, Numeric,
    String, DateTime, ForeignKey
)
from datetime import datetime

from app.db.database import Base


class StressTest(Base):
    __tablename__ = "stress_tests"

    id = Column(Integer, primary_key=True, index=True)

    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id"),
        nullable=False,
        index=True
    )

    scenario_name = Column(String(100), nullable=False)

    market_shock_percent = Column(
        Numeric(8, 4),
        nullable=False
    )

    estimated_loss = Column(Numeric(18, 4))

    estimated_loss_percent = Column(Numeric(12, 6))

    created_at = Column(DateTime, default=datetime.utcnow)

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )