from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    season_type = Column(Integer, ForeignKey("season_descriptions.id"))
    season_year = Column(String(8))

    s_type = relationship("SeasonDescription")
