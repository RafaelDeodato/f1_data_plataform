from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Circuit(Base):
    __tablename__ = "circuits"

    id = Column(Integer, primary_key=True, index=True)
    circuit_id = Column(String, unique=True, index=True, nullable=False)
    wikipedia_url = Column(String, nullable=True)
    name = Column(String, nullable=False)
    loc_latitude = Column(String, nullable=True)
    loc_longitude = Column(String, nullable=True)
    loc_locality = Column(String, nullable=True)
    loc_country = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())