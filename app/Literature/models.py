from typing import List

from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base


class Literature(Base):
    __tablename__ = "literature"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_literature_path: Mapped[str] = mapped_column(String, nullable=True)

    parsed_pages: Mapped[List["ParsedPage"]] = relationship(back_populates="literature", cascade="all, delete-orphan")


class ParsedPage(Base):
    __tablename__ = "parsed_page"

    id: Mapped[int] = mapped_column(primary_key=True)
    number_page: Mapped[int] = mapped_column(Integer)
    object: Mapped[JSON] = mapped_column(JSON)
    image_path: Mapped[str] = mapped_column(String)
    literature_id: Mapped[int] = mapped_column(ForeignKey("literature.id"))

    literature: Mapped["Literature"] = relationship(back_populates="parsed_pages")
