from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  full_name = Column(String, nullable=True)
  phone_number = Column(
      String, unique=True, index=True, nullable=True
  )
  is_active = Column(
      Boolean, default=True
  )
  is_admin = Column(
      Boolean, default=False
  )
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(
      DateTime,
      default=lambda: datetime.now(timezone.utc),
      onupdate=lambda: datetime.now(timezone.utc),
  )
