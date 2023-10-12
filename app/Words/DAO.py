import os
import shutil
from datetime import datetime
from sqlalchemy import select, delete
from app.database import async_session_maker
import app.Words.models as models
from .schemas import SWord
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
                        definition=meaning.definition
                    )
                session.add(db_meaning)

                await session.commit()
                await session.refresh(db_meaning)

            return word





