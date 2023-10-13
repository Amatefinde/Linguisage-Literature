import os
import shutil
from datetime import datetime
from sqlalchemy import select, delete
from app.database import async_session_maker
import app.Words.models as models
from .schemas import SWord
from typing import List
from fastapi import UploadFile


class WordDAO:
    @classmethod
    async def add_world_manual(cls, word: SWord):
        async with async_session_maker() as session:
            db_word = models.Word(
                content=word.content
            )
            session.add(db_word)
            await session.commit()
            await session.refresh(db_word)

            if word.meanings:
                for meaning in word.meanings:
                    db_meaning = models.Meaning(
                        word_id=db_word.id,
                        privacy=meaning.privacy,
                        meaning=meaning.meaning,
                        short_meaning=meaning.short_meaning,
                    )
                    session.add(db_meaning)
                    await session.commit()
                    await session.refresh(db_meaning)

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
    async def add_test_collocation(cls, collocation):
        async with async_session_maker() as session:
            db_collocation = models.Collocation(
                content="_____".join(["dwdw", "hru-hru"]),
                title="oleg"
            )
            session.add(db_collocation)
            await session.commit()
            await session.refresh(db_collocation)
            return db_collocation




