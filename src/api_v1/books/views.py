import os
import io
from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, File, status, Form, Depends, Query
from loguru import logger
import pypandoc
from pdf2docx import Converter
from tempfile import TemporaryDirectory
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models import LiteratureEpub
from src.core.database import db_helper
from . import crud
from .schemas import SEpubResponse, SPatchRequest, ManyBookResponse
from . import dependencies

router = APIRouter(prefix="/books", tags=["Books"])


def ensure_pandoc():
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.download_pandoc()
        pypandoc.pandoc_path = pypandoc.get_pandoc_path()


def pdf_to_epub(pdf_path: str, epub_path: str, ignore_header_footer: bool = True):
    docx_path = pdf_path.rsplit('.', 1)[0] + ".docx"
    cv = Converter(pdf_path)
    try:
        cv.convert(docx_path, ignore_footer=ignore_header_footer, ignore_header=ignore_header_footer)
    finally:
        cv.close()

    ensure_pandoc()
    pypandoc.convert_file(docx_path, 'epub', outputfile=epub_path)


def docx_to_epub(docx_path: str, epub_path: str):
    ensure_pandoc()
    pypandoc.convert_file(docx_path, 'epub', outputfile=epub_path)


@router.post("",
    response_model=SEpubResponse,
    status_code=status.HTTP_201_CREATED)
async def add(
    file: UploadFile = File(...),
    filename: str = Form(...),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    """
    Endpoint for uploading ePub, FB2, DOCX, or PDF files.
    DOCX and PDF конвертируются в EPUB до сохранения.
    """
    exception = HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="This endpoint supports only .fb2, .epub, .docx, and .pdf files",
    )

    _, ext = os.path.splitext(file.filename or '')
    ext = ext.lower()

    if ext == ".epub":
        db_book = await crud.add_epub_book(db_session, file, filename)
    elif ext == ".fb2":
        db_book = await crud.add_fb2_book(db_session, file, filename)

    elif ext in {".pdf", ".docx"}:
        with TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, file.filename)
            epub_filename = os.path.splitext(file.filename)[0] + '.epub'
            output_path = os.path.join(tmpdir, epub_filename)

            content = await file.read()
            with open(input_path, 'wb') as f:
                f.write(content)

            if ext == ".pdf":
                pdf_to_epub(input_path, output_path)
            else:
                docx_to_epub(input_path, output_path)

            with open(output_path, 'rb') as f:
                epub_bytes = f.read()

            converted_upload = UploadFile(
                filename=epub_filename,
                file=io.BytesIO(epub_bytes)
            )

        db_book = await crud.add_epub_book(db_session, converted_upload, filename)

    else:
        raise exception

    return db_book


@router.get(
    "",
    response_model=ManyBookResponse,
    status_code=status.HTTP_200_OK,
)
async def get_many_books(
    literature_ids: list[int] = Query(default_factory=list, alias="id"),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    row_books = await crud.get_many_books(db_session, literature_ids)
    books = [SEpubResponse.model_validate(book, from_attributes=True) for book in row_books]
    return ManyBookResponse(books=books)


@router.get(
    "/{book_id}",
    response_model=SEpubResponse,
    status_code=status.HTTP_200_OK,
)
async def get(
    book: LiteratureEpub = Depends(dependencies.epub_book_dependency),
):
    return book


@router.patch(
    "/{book_id}",
    response_model=SEpubResponse,
    status_code=status.HTTP_200_OK,
)
async def patch(
    book_update: SPatchRequest,
    book: LiteratureEpub = Depends(dependencies.epub_book_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    book = await crud.update_partial_book(db_session, book, book_update)
    return book


@router.delete(
    "/{book_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    book: LiteratureEpub = Depends(dependencies.epub_book_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.delete_book(db_session, book)
