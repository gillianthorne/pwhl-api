from sqlalchemy import Column, Integer, String

from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    nickname = Column(String(25))
    abbreviation = Column(String(3))
    logo = Column(String)
    division_id = Column(Integer)