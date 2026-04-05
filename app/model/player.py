from sqlalchemy import Column, Date, Integer, String

from app.database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    shoots = Column(String(1))
    catches = Column(String(1))
    jersey_number = Column(Integer)
    position = Column(String(2))
    birthdate = Column(Date)
    hometown = Column(String(75))