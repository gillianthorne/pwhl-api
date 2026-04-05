from sqlalchemy import Boolean, Column, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class PlusMinus(Base):
    __tablename__ = "plus_minus"
    
    goal_id = Column(Integer, ForeignKey("goals.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    is_plus = Column(Boolean)

    goal = relationship("Goal")
    player = relationship("Player")

    __table_args__ = (
        PrimaryKeyConstraint("goal_id", "player_id"),
    )