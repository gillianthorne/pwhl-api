from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, Time
from sqlalchemy.orm import relationship

from app.database import Base


class Hit(Base):
    __tablename__ = "hits"

    player_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    period = Column(Integer)
    time = Column(Time)
    x_location = Column(Integer)
    y_location = Column(Integer)
    on_player_id = Column(Integer, ForeignKey("players.id"))

    player = relationship("Player", foreign_keys=[player_id])
    game = relationship("Game")
    on_player = relationship("Player", foreign_keys=[on_player_id])

    __table_args__ = (
        PrimaryKeyConstraint("player_id", "game_id", "period", "time")
    )
