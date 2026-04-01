from sqlalchemy import Column, Date, Integer, ForeignKey, String, Time, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    scorer_id = Column(Integer, ForeignKey("players.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    period = Column(String(3))
    time = Column(Time)
    is_powerplay = Column(Boolean)
    is_shorthanded = Column(Boolean)
    is_emptynet = Column(Boolean)
    is_insurancegoal = Column(Boolean)
    is_gamewinninggoal = Column(Boolean)
    x_location = Column(Integer)
    y_location = Column(Integer)

    scorer = relationship("Player")
    game = relationship("Game")