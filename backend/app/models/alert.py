from sqlalchemy import (
    Column, Integer, Numeric,
    String, Text, Boolean,
    DateTime, ForeignKey
)
from datetime import datetime

from app.db.database import Base


class Alert(Base):
    __tablename__ = "alerts"

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
        nullable=True,
        index=True
    )

    alert_type = Column(
        String(50),
        nullable=False
    )

    severity = Column(
        String(20),
        nullable=False
    )

    message = Column(Text, nullable=False)

    threshold = Column(Numeric(18, 4))

    actual_value = Column(Numeric(18, 4))

    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    resolved_at = Column(DateTime, nullable=True)