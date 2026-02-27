from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Constructor(Base):
    __tablename__ = "constructors"

    id = Column(Integer, primary_key=True, index=True)
    constructor_id = Column(String, nullable=False)
    wikipedia_url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    colour = Column(String, nullable=True)