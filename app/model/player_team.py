from sqlalchemy import Column, Date, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class PlayerTeam(Base):
    __tablename__ = "player_teams"

    player_id = Column(Integer, ForeignKey("players.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    start_date = Column(Date)
    end_date = Column(Date)

    player = relationship("Player")
    team = relationship("Team")

    __table_args__ = (
        PrimaryKeyConstraint("player_id", "team_id", "start_date")
    )