from datetime import datetime
from sqlalchemy import select, delete, insert
from app.database import async_session_maker
import app.Literature.models as models
from .schemas import SLiterature
from fastapi import HTTPException
from config import static_path as static_path_default


def save_pdf_to_disk(pdf_example, output_file_path):
    with open(output_file_path, 'wb') as output_file:
        output_file.write(pdf_example.read())


class LiteratureDAO:
    @classmethod
    async def add_original_literature(cls, file):
        async with async_session_maker() as session:
            query = select(models.Literature)
            result = await session.execute(query)
            file_id = len(result.all()) + 1

            path_for_original_file = static_path_default + "literature_original" + "/" + str(file_id) + ".pdf"
            try:
                save_pdf_to_disk(file, path_for_original_file)
                session.add(models.Literature(original_literature_path=path_for_original_file))
                await session.commit()
                return file_id
            except Exception as Ex:
                print(Ex)
                return HTTPException(500, "Что то пошло не так при сохранении файла")

    @classmethod
    async def add_page_for_literature(cls, word_data: dict, literature_number, number_page, image_path):
        async with async_session_maker() as session:
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
                    "img": i.image_path,
                })

            return pages

