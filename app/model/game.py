from sqlalchemy import Column, Integer, ForeignKey, Date, String, Time
from sqlalchemy.orm import relationship
from app.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    home_goals = Column(Integer)
    visiting_team_id = Column(Integer, ForeignKey("teams.id"))
    visiting_goals = Column(Integer)
    win_type = Column(String)
    season = Column(Integer, ForeignKey("seasons.id"))
    venue = Column(Integer, ForeignKey("arenas.venue_id"))
    attendance = Column(Integer)
    start_time = Column(Time)
    end_time = Column(Time)
    duration = Column(Time)

    home_team = relationship("Team", foreign_keys=[home_team_id])
    visiting_team = relationship("Team", foreign_keys=[visiting_team_id])
    game_season = relationship("Season")
    game_venue = relationship("Venue")
    