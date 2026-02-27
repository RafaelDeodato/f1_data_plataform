from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    wikipedia_url = Column(String, nullable=True)
    name = Column(String, nullable=False)
    official_name = Column(String, nullable=True)
    circuit_id = Column(String, nullable=False)
    date = Column(String, nullable=True)
    time = Column(String, nullable=True)
    meeting_key_openf1 = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
