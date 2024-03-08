from typing import List
from .core import Base

from sqlalchemy import Column, BOOLEAN
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from .verification import VerificationKey


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )


    is_announcement = Column(BOOLEAN, nullable=False, default=False)
    title = Column(VARCHAR(1000), nullable=True)
    body = Column(VARCHAR(1000), nullable=True)
    link = Column(VARCHAR(1000), nullable=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())