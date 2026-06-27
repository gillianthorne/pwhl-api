from sqlalchemy import Boolean, Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Time
from sqlalchemy.orm import relationship

from app.database import Base


class Shot(Base):
    __tablename__ = "shots"
    
    id = Column(Integer, primary_key=True)
    shooter_id = Column(Integer, ForeignKey("players.id"))
    goalie_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    period = Column(String(3))
    time = Column(Time)
    is_goal = Column(Boolean)
    x_location = Column(Integer)
    y_location = Column(Integer)
    type = Column(String(20))
    quality = Column(String(20))

    shooter = relationship("Player", foreign_keys=[shooter_id])
    goalie = relationship("Player", foreign_keys=[goalie_id])
    game = relationship("Game")
