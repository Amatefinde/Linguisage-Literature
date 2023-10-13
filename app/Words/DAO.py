import os
import shutil
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from app.database import async_session_maker
import app.Words.models as models
from .schemas import SWord
from typing import List
from fastapi import UploadFile


class WordDAO:
    @classmethod
    async def get_word_id(cls, word: str):
        async with async_session_maker() as session:
            existing_word = await session.execute(models.Word.__table__.select().where(models.Word.content == word))
            answer = existing_word.scalar()
            return int(answer) if answer else None

    @classmethod
    async def get_word_meaning_id(cls, word: str, meaning: str):
        async with async_session_maker() as session:
            word_id = await cls.get_word_id(word)
            existing_meaning = await session.execute(models.Meaning.__table__.select().where(
                models.Meaning.meaning == meaning and models.Meaning.word_id == word_id))
            answer = existing_meaning.scalar()
            return answer

    @classmethod
    async def get_word_idiom_id(cls, word: str, idiom: str):
        async with async_session_maker() as session:
            word_id = await cls.get_word_id(word)
            existing_idiom = await session.execute(models.Idiom.__table__.select().where(
                models.Idiom.content == idiom and models.Idiom.word_id == word_id))
            answer = existing_idiom.scalar()
            print(answer)
            return answer

    @classmethod
    async def add_word_manual(cls, word: SWord):
        async with async_session_maker() as session:
            word_id = await cls.get_word_id(word.content)
            if word_id:
                db_word = await session.get(models.Word, word_id)
            else:
                db_word = models.Word(
                    content=word.content
                )
                session.add(db_word)
                await session.commit()
                await session.refresh(db_word)

            if word.meanings:
                for meaning in word.meanings:
                    meaning_id = await cls.get_word_meaning_id(word.content, meaning.meaning)
                    if meaning_id:
                        db_meaning = await session.get(models.Meaning, meaning_id)
                    else:
                        db_meaning = models.Meaning(
                            word_id=db_word.id,
                            privacy=meaning.privacy,
                            meaning=meaning.meaning,
                            short_meaning=meaning.short_meaning,
                        )
                        session.add(db_meaning)
                        await session.commit()
                        await session.refresh(db_meaning)

                        # Выдвинуть на один уровень, что бы сделать в независимости от уже существования значения
                        if meaning.examples:
                            for example in meaning.examples:
                                db_example = models.Example(
                                    meaning_id=db_meaning.id,
                                    content=example
                                )
                                session.add(db_example)
                                await session.commit()
                                await session.refresh(db_example)

                        if meaning.collocations:
                            for collocation in meaning.collocations:
                                db_collocation = models.Collocation(
                                    meaning_id=db_meaning.id,
                                    title=collocation.title,
                                    content="_____".join(collocation.body)
                                )
                                session.add(db_collocation)
                                await session.commit()
                                await session.refresh(db_collocation)

            if word.idioms:
                for idiom in word.idioms:
                    idiom_id = await cls.get_word_idiom_id(word.content, idiom.content)
                    if idiom_id:
                        db_idiom = await session.get(models.Idiom, idiom_id)
                    else:
                        db_idiom = models.Idiom(
                            word_id=db_word.id,
                            content=idiom.content,
                            label=idiom.label,
                            explain=idiom.explain,
                            examples="_____".join(idiom.examples)
                        )

                        session.add(db_idiom)
                        await session.commit()
                        await session.refresh(db_idiom)
            return word

    @classmethod
    async def get_word(cls, word: str):
        async with async_session_maker() as session:
            word_data = await session.execute(
                select(models.Word)
                .options(joinedload(models.Word.meanings).joinedload(models.Meaning.examples))
                .options(joinedload(models.Word.meanings).joinedload(models.Meaning.collocations))
                .options(joinedload(models.Word.idioms))
                .filter(models.Word.content == word)
            )
            word = word_data.mappings().first()['Word']  # type: models.Word

            return word
