from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from app.database import Base


class Penalty(Base):
    __tablename__ = "penalties"

    penalty_id = Column(Integer, primary_key=True)
    taken_by_id = Column(Integer, ForeignKey("players.id"))
    served_by_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    description = Column(String(20))
    period = Column(Integer)
    time = Column(Time)
    length = Column(Integer)
    is_powerplay = Column(Boolean)
    is_bench = Column(Boolean)

    taken_by = relationship("Player", foreign_keys=[taken_by_id])
    served_by = relationship("Player", foreign_keys=[served_by_id])
    game = relationship("Game")