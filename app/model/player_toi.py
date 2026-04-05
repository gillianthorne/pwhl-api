from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, Time
from sqlalchemy.orm import relationship

from app.database import Base


class PlayerTOI(Base):
    __tablename__ = "players_toi"

    player_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    time_on_ice = Column(Time)

    player = relationship("Player")
    game = relationship("Game")

    __table_args__ = (
        PrimaryKeyConstraint("player_id", "game_id")
    )