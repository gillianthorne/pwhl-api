from sqlalchemy import Column, Integer, String

from app.database import Base


class SeasonDescription(Base):
    __tablename__ = "season_descriptions"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30))