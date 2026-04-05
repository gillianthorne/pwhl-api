from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Venue(Base):
    __tablename__ = "arenas"

    venue_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    city = Column(String(20))
    province_state = Column(String(20))
    country = Column(String(20))
    capacity = Column(Integer)
    home_team_id = Column(Integer, ForeignKey("teams.id"))

    home_team = relationship("Team")