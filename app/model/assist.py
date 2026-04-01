from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Assist(Base):
    __tablename__ = "assists"

    goal_id = Column(Integer, ForeignKey("goals.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    primary_secondary = Column(Integer)

    goal = relationship("Goal")
    player = relationship("Player")

    __table_args__ = (
        PrimaryKeyConstraint("goal_id", "player_id")
    )