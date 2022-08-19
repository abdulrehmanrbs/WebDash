from sqlalchemy import Column, Float, String, Integer, Numeric
from .database import Base

class sepsis(Base):
    __tablename__ = "sepsis"
    authors = Column(String, unique=True, index=True)
    year = Column(Integer, primary_key=True, index=True)
    journal = Column(String)