from sqlalchemy import Column, Date, ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship

from app.database import Base


class PlayerHistory(Base):
    __tablename__ = "player_history"

    id = Column(Integer, ForeignKey("players.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    team_id = Column(Integer, ForeignKey("teams.id"))
    jersey_number = Column(Integer)
    position = Column(String)

    player = relationship("Player")
    team = relationship("Team")

    __table_args__ = (
        PrimaryKeyConstraint("id", "start_date"),
    )