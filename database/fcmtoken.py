from .user import User
from .core import Base

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME, ENUM
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from .verification import VerificationKey


class FCMToken(Base):
    __tablename__ = "fcmtokens"
    __table_args__ = {"mysql_charset": "utf8mb4"}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user = relationship("User", foreign_keys="FCMToken.user_id")
    token = Column(VARCHAR(300), nullable=False)
    platform = Column(ENUM("ANDROID", "IOS"), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
