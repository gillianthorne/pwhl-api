from sqlalchemy import Column, Float, ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship

from app.database import Base


class Salary(Base):
    __tablename__ = "salaries"

    player_id = Column(Integer, ForeignKey("players.id"))
    season = Column(String(8))
    salary = Column(Float)

    player = relationship("Player")

    __table_args__ = (
        PrimaryKeyConstraint("player_id", "season"),
    )