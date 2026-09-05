from sqlalchemy import (
    Column, Integer, Numeric, Date,
    DateTime, ForeignKey
)
from datetime import datetime

from app.db.database import Base


class RiskMetric(Base):
    __tablename__ = "risk_metrics"

    id = Column(Integer, primary_key=True, index=True)

    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id"),
        nullable=False,
        index=True
    )

    calculation_date = Column(Date, nullable=False, index=True)

    volatility = Column(Numeric(12, 6))
    sharpe_ratio = Column(Numeric(12, 6))
    sortino_ratio = Column(Numeric(12, 6))
    beta = Column(Numeric(12, 6))
    alpha = Column(Numeric(12, 6))
    max_drawdown = Column(Numeric(12, 6))

    var_95 = Column(Numeric(18, 4))
    var_99 = Column(Numeric(18, 4))
    expected_shortfall = Column(Numeric(18, 4))

    risk_score = Column(Numeric(8, 4))

    created_at = Column(DateTime, default=datetime.utcnow)