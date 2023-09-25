from typing import List
from .core import Base

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from .verification import VerificationKey


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    phone = Column(VARCHAR(11), nullable=False, unique=True)
    name = Column(VARCHAR(5), nullable=False)
    profile = Column(VARCHAR(100), nullable=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
    verifications: Mapped[List[VerificationKey]] = relationship(back_populates="user")


class UserSuspention(Base):
    __tablename__ = "user.suspentions"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user = relationship("User", foreign_keys="UserSuspention.user_id")
    reason = Column(VARCHAR(100), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
    expiry = Column(DATETIME, nullable=False)
