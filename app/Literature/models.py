from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON

from app.database import Base


class Literature(Base):
    __tablename__ = "literature"

    literature_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    add_date = Column(TIMESTAMP, nullable=True)
    last_use_date = Column(TIMESTAMP, nullable=True)
    original_literature_path = Column(String, nullable=False)
    parsed_literature_object = Column(String, nullable=False)

    class Config:
        orm_mode = True
