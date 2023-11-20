from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from app.database import Base
from app.Words.schemas import PrivacyType


class Word(Base):
    __tablename__ = "word"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String)

    meanings: Mapped[List["Meaning"]] = relationship(back_populates="word", cascade="all, delete-orphan")
    idioms: Mapped[List["Idiom"]] = relationship(back_populates="word", cascade="all, delete-orphan")


class Meaning(Base):
    __tablename__ = "meaning"
    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("word.id"))
    privacy: Mapped[PrivacyType] = mapped_column(String)
    meaning: Mapped[str] = mapped_column(String)
    short_meaning: Mapped[str] = mapped_column(String)

    word: Mapped["Word"] = relationship(back_populates="meanings")
    examples: Mapped[List["Example"]] = relationship(back_populates="meaning", cascade="all, delete-orphan")
    collocations: Mapped[List["Collocation"]] = relationship(back_populates="meaning", cascade="all, delete-orphan")
    images: Mapped[List["Image"]] = relationship(back_populates="meaning", cascade="all, delete-orphan")



class Example(Base):
    __tablename__ = "example"
    id: Mapped[int] = mapped_column(primary_key=True)
    meaning_id: Mapped[int] = mapped_column(ForeignKey("meaning.id"))
    content: Mapped[str] = mapped_column(String)

    meaning: Mapped["Meaning"] = relationship(back_populates="examples")


class Collocation(Base):
    __tablename__ = "collocation"
    id: Mapped[int] = mapped_column(primary_key=True)
    meaning_id: Mapped[int] = mapped_column(ForeignKey("meaning.id"))
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)

    meaning: Mapped["Meaning"] = relationship(back_populates="collocations")


class Idiom(Base):
    __tablename__ = "idiom"
    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("word.id"))
    content: Mapped[str] = mapped_column(String)
    label: Mapped[str] = mapped_column(String)
    explain: Mapped[str] = mapped_column(String)
    examples: Mapped[str] = mapped_column(String)

    word: Mapped["Word"] = relationship(back_populates="idioms")


class Image(Base):
    __tablename__ = "image"
    content: Mapped[str]
    privacy: Mapped[str]
    meaning_id: Mapped[int] = mapped_column(ForeignKey("meaning.id"))

    meaning: Mapped["Meaning"] = relationship(back_populates="images")


