from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON

from app.database import Base


class Bookmark(Base):
    __tablename__ = "bookmark"

    book_mark_id = Column(Integer, primary_key=True)
    literature_id = Column(Integer, ForeignKey('literature.literature_id'), nullable=False)
    bookmark_title = Column(String, nullable=False)
    color = Column(String, nullable=True)
    place = Column(JSON, nullable=False)
    create_at = Column(TIMESTAMP, nullable=False)

    class Config:
        orm_mode = True
