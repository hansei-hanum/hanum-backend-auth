from .core import Base

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME, ENUM, TINYINT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class VerificationKey(Base):
    __tablename__ = "verification.keys"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    key = Column(VARCHAR(6), nullable=False, primary_key=True, unique=True)
    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    user = relationship("User", foreign_keys="VerificationKey.user_id")
    type = Column(ENUM("STUDENT", "TEACHER"), nullable=False)
    department = Column(
        ENUM(
            "CLOUD_SECURITY",
            "NETWORK_SECURITY",
            "HACKING_SECURITY",
            "METAVERSE_GAME",
            "GAME",
            "INTELLIGENT_SOFTWARE",
        ),
        nullable=True,
    )
    grade = Column(
        TINYINT(unsigned=True),
        nullable=True,
    )
    classroom = Column(
        TINYINT(unsigned=True),
        nullable=True,
    )
    number = Column(
        TINYINT(unsigned=True),
        nullable=True,
    )
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
    valid_until = Column(DATETIME, nullable=True)
    used_at = Column(DATETIME, nullable=True, server_default=None, onupdate=func.now())
