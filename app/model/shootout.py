from sqlalchemy import Boolean, Column, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Shootout(Base):
    __tablename__ = "shootouts"

    shooter_id = Column(Integer, ForeignKey("players.id"))
    goalie_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    is_goal = Column(Boolean)
    is_gamewinninggoal = Column(Boolean)
    shootout_attempt = Column(Integer)
    id = Column(Integer, primary_key=True)

    shooter = relationship("Player", foreign_keys=[shooter_id])
    goalie = relationship("Player", foreign_keys=[goalie_id])
    game = relationship("Game")
