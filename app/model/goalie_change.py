from sqlalchemy import Boolean, Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Time
from sqlalchemy.orm import relationship

from app.database import Base


class GoalieChange(Base):
    __tablename__ = "goalie_changes"

    player_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    period = Column(String(3))
    time = Column(Time)
    entering = Column(Boolean)

    player = relationship("Player")
    game = relationship("Game")

    __table_args__ = (
        PrimaryKeyConstraint("player_id", "game_id", "period", "time")
    )