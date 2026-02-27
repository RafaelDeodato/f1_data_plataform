from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    date = Column(String, nullable=True)
    time = Column(String, nullable=True)
    session_key_openf1 = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())