from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from app.database import Base
from app.Words.schemas import PrivacyType


class Word(Base):
    __tablename__ = "word"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String)

    meanings: Mapped[List["Meaning"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )


class Meaning(Base):
    __tablename__ = "meaning"
    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("word.id"))
    privacy: Mapped[PrivacyType] = mapped_column(String)
    definition: Mapped[str] = mapped_column(String)

    word: Mapped["Word"] = relationship(back_populates="meanings")
