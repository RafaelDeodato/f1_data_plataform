from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Entrie(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, nullable=False, index=True)
    driver_id = Column(Integer, nullable=False, index=True)
    constructor_id = Column(Integer, nullable=False, index=True)
    car_number = Column(Integer, nullable=True)
    grid_position = Column(Integer, nullable=True)
    start_position = Column(Integer, nullable=True)
    finish_position = Column(Integer, nullable=True)
    status = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    laps_completed = Column(Integer, nullable=True)
    total_time = Column(String, nullable=True)