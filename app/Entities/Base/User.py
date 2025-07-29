from sqlalchemy import Boolean, Column, String
from app.Entities.BaseEntity import BaseEntity


class User(BaseEntity):
    __tablename__ = "users"
    __table_args__ = {"schema": "users"}

    user_name = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)