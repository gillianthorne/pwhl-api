from sqlalchemy import Column, Date, ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship

from app.database import Base


class CurrentPlayers(Base):
    __tablename__ = "current_players"

    id = Column(Integer, ForeignKey("players.id"), primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    team_id = Column(Integer, ForeignKey("teams.id"))
    jersey_number = Column(Integer)
    position = Column(String)

    player = relationship("Player")
    team = relationship("Team")
