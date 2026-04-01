from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Time
from sqlalchemy.orm import relationship

from app.database import Base


class BlockedShot(Base):
    __tablename__ = "blocked_shots"

    shooter_id = Column(Integer, ForeignKey("players.id"))
    blocker_id = Column(Integer, ForeignKey("players.id"))
    goalie_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    period = Column(String(3))
    time = Column(Time)
    x_location = Column(Integer)
    y_location = Column(Integer)
    quality = String(20)
    shot_type = String(20)

    shooter = relationship("Player", foreign_keys=[shooter_id])
    blocker = relationship("Player", foreign_keys=[blocker_id])
    goalie = relationship("Player", foreign_keys=[goalie_id])
    game = relationship("Game")

    __table_args__ = (
        PrimaryKeyConstraint("game_id", "period", "time")
    )