import os
from datetime import datetime
from sqlalchemy import select, delete, insert, func
from app.database import async_session_maker
import app.Literature.models as models
from .schemas import SLiterature
from fastapi import HTTPException
from config import static_path as static_path_default, static_access_http_path
from os import path


def save_pdf_to_disk(pdf_example, output_file_path):
    with open(output_file_path, 'wb') as output_file:
        output_file.write(pdf_example.read())


class LiteratureDAO:
    @classmethod
    async def add_original_literature(cls, file):
        async with async_session_maker() as session:
            db_literature = models.Literature()
            session.add(db_literature)
            await session.commit()
            await session.refresh(db_literature)
            path_for_original_file = path.join(static_path_default, "literature_original", str(db_literature.id) + ".pdf")
            try:
                print("Путь ADD (DAO) ", path_for_original_file)
                save_pdf_to_disk(file, path_for_original_file)
                db_literature.original_literature_path = path_for_original_file
                session.add(db_literature)
                await session.commit()
                return db_literature.id
            except Exception as Ex:
                print(Ex)
                raise HTTPException(500, "Что то пошло не так при сохранении файла")

    @classmethod
    async def add_page_for_literature(cls, word_data: dict, literature_number, number_page, image_path):
        async with async_session_maker() as session:
            print(literature_number)
            db_literature = await session.get(models.Literature, int(literature_number))

            db_parsed_page = models.ParsedPage(
                literature_id=db_literature.id,
                number_page=int(number_page),
                object=word_data,
                image_path=image_path
            )
            session.add(db_parsed_page)
            await session.commit()
            return 200

    @classmethod
    async def get_pages_for_literature(cls, literature_id: int, start: int, end: int):
        pages = []
        async with async_session_maker() as session:
            db_literature = await session.get(models.Literature, int(literature_id))
            if not db_literature:
                raise HTTPException(status_code=404, detail=f"Файл с id {literature_id} не найден")
            if end == 0:
                query = select(models.ParsedPage).where(
                    models.ParsedPage.literature_id == literature_id
                ).where(models.ParsedPage.number_page >= start)
            else:
                query = select(models.ParsedPage).where(
                    models.ParsedPage.literature_id == literature_id
                ).where(models.ParsedPage.number_page >= start).where(end >= models.ParsedPage.number_page)

            response = await session.execute(query)
            data = response.scalars().all()
            for i in data:
                pages.append({
                    "text_info": i.object,
                    "number_page": i.number_page,
                    "img": path.join(static_access_http_path, i.image_path)
                })

            return pages

    @classmethod
    async def delete_literature(cls, literature_id: int):
        async with async_session_maker() as session:
            selected_literature = await session.get(models.Literature, literature_id)
            print("selected literature: ", selected_literature)
            if not selected_literature:
                raise HTTPException(status_code=404, detail="Literature not found")
            try:
                query = select(models.ParsedPage).where(models.ParsedPage.literature_id == literature_id)
                response = await session.execute(query)
                data = response.scalars().all()

                # Удаляем оригинальный пдф
                if os.path.exists(selected_literature.original_literature_path):
                    os.remove(selected_literature.original_literature_path)

                # Удаляем все изображения страниц
                for i in data:
                    os.remove(path.join("app", i.image_path))

                # Удаляем запись из таблицы литератур, ссылающиеся на ней записи из таблицы страниц дропнутся каскадом
                await session.delete(selected_literature)
                await session.commit()
            except Exception as Ex:
                print(Ex)
                raise Exception("Что то пошло не так при удалении файла")

            return selected_literature.id
