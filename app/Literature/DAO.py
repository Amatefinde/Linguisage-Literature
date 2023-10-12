import os
import shutil
from datetime import datetime
from sqlalchemy import select, delete
from app.database import async_session_maker
from app.Literature.models import Literature
from .schemas import SLiterature
from fastapi import UploadFile


class LiteratureDAO:
    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            queue = select(Literature)
            result = await session.execute(queue)
            return result.mappings().all()

    @classmethod
    async def get_by_user_id(cls, user_id):
        async with async_session_maker() as session:
            query = select(Literature).where(Literature.user_id == user_id)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add_user_literature(cls, literature: SLiterature, file: UploadFile):
        file_extension = os.path.splitext(file.filename)[-1]
        file_name = os.path.splitext(file.filename)[-2]
        print("file_extension", file_extension)
        print("file_name", file_name)
        if file_extension != "pdf":
            return {"error": "Only pdf files support now"}

        literature_data = literature.model_dump()
        literature_data["add_date"] = datetime.utcnow()
        literature_data["last_use_date"] = None
        literature_data["parsed_literature_object"] = ""  # todo
        literature_data["original_literature_path"] = f"app/static/{file.filename}"

        with open(f"app/static/{file.filename}", "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        async with async_session_maker() as session:
            new_literature = Literature(**literature_data)
            session.add(new_literature)
            await session.commit()

        return {"message": "Литература успешно добавлена"}

    @classmethod
    async def get_by_literature_id(cls, literature_id):
        async with async_session_maker() as session:
            queue = select(Literature).where(Literature.literature_id == literature_id)
            result = await session.execute(queue)
            literature = result.scalars().one_or_none()

            if literature:
                literature.last_use_date = datetime.utcnow()
                await session.commit()
        print(literature)
        return literature

    @classmethod
    async def delete_by_literature_id(cls, literature_id):
        async with async_session_maker() as session:
            literature = await session.get(Literature, literature_id)

            if literature:
                session.delete(literature)
                await session.commit()
                return {"message": "Литература удалена успешно"}
            else:
                return {"message": "Что то пошло не так. Запрашиваемые объект не существует"}


