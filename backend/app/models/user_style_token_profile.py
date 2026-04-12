from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from app.db import Base


class UserStyleTokenProfile(Base):
    __tablename__ = "user_style_token_profile"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "token_type",
            "token_value",
            name="uq_user_style_token_profile_user_token",
        ),
        Index("ix_user_style_token_profile_user_id", "user_id"),
        Index("ix_user_style_token_profile_user_type", "user_id", "token_type"),
        {"schema": "analytics"},
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("analytics.app_user.id", ondelete="CASCADE"),
        nullable=False,
    )
    token_type = Column(String, nullable=False)
    token_value = Column(String, nullable=False)
    token_count = Column(Integer, nullable=False, default=0)

    user = relationship("AppUser")
