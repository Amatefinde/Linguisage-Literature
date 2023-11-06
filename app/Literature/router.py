from fastapi import APIRouter, UploadFile, Depends, File, Path, Query
from app.Literature.DAO import LiteratureDAO
from app.Literature.schemas import SLiterature
from app.Literature.LiteratureProcessing import TextExtraction
import io
from typing import Annotated

router = APIRouter(
    prefix="/literature",
    tags=["Литература"]
)


@router.post("/add")
async def add(file: UploadFile, use_ocr: bool):
    """Позволяет загружать PDF литературу. Возможно сразу же применять OCR
    (OCR работает медленно, манга наруты на 200 страниц - 15 минут).
    Возвращает id литературы, по которму можно будет получить к ней доступ в дальнейшем."""
    loaded_file = file.file.read()
    pdf_example = io.BytesIO(loaded_file)

    # Сохранение оригинальной литературы в формате PDF
    id_literature = await LiteratureDAO.add_original_literature(pdf_example)

    await TextExtraction.parse_pfd(pdf_example, literature_number=id_literature, use_ocr=use_ocr)
    return id_literature


@router.get("/get_pages")
async def get_pages(
        literature_id: Annotated[int, Query(title="The ID of the literature to get", ge=1)],
        start_page: Annotated[int, Query(title="The number of first page", ge=1)] = 1,
        end_page: Annotated[int, Query(title="The number of last page (0 - return until the end)", ge=0)] = 0):
    """Возвращает список обьектов.
    Обьект состоит из данных о словах на странице, номера страницы и ссылки на изображение страницы.\n
    Parameters:\n
                    literature_id (int): уникальный идентификационный номер литературы, выдается при добавлении\n
                    start_page (int): определяет начиная с какой страницы вернуться\n
                    end_page (int): определяет до какой страницы вернуться обьекты, значение 0 вернет страницы до конца документа\n

    То есть при запросе literature_id=2, start_page=5, end_page=10 - вернуться все страницы начиная с пятой и заканчивая
    десятой включительно, второго документа
    """
    data = await LiteratureDAO.get_pages_for_literature(literature_id, start_page, end_page)
    return data


@router.delete("/delete")
async def delete_literature(literature_id: int):
    """Позволяет удалять литературу по id"""

    response = await LiteratureDAO.delete_literature(literature_id)
    return response
