from sqlalchemy import (
    Column, Integer, String,
    Text, DateTime, ForeignKey
)
from datetime import datetime

from app.db.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    action = Column(
        String(100),
        nullable=False
    )

    entity_type = Column(
        String(50),
        nullable=False
    )

    entity_id = Column(Integer, nullable=True)

    old_value = Column(Text, nullable=True)

    new_value = Column(Text, nullable=True)

    ip_address = Column(String(45), nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )