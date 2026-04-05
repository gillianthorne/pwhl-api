from sqlalchemy import Boolean, Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Time
from sqlalchemy.orm import relationship

from app.database import Base


class Faceoff(Base):
    __tablename__ = "faceoffs"

    home_player_id = Column(Integer, ForeignKey("players.id"))
    visiting_player_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    period = Column(String(3))
    time = Column(Time)
    x_location = Column(Integer)
    y_location = Column(Integer)
    home_win = Column(Boolean)
    id = Column(Integer, primary_key=True)

    home_player = relationship("Player", foreign_keys=[home_player_id])
    visiting_player = relationship("Player", foreign_keys=[visiting_player_id])
    game = relationship("Game")
