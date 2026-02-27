from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(String, index=True, nullable=False)
    code = Column(String, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_birth = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    headshot_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())