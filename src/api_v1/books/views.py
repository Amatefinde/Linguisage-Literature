import os
from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, status, Form, Depends, Query
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models import LiteratureEpub
from src.core.database import db_helper
from . import crud
from .schemas import SEpubResponse, SPatchRequest, ManyBookResponse
from . import dependencies

router = APIRouter(prefix="/books", tags=["Books"])


@router.post(
    "",
    response_model=SEpubResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add(
    file: UploadFile,
    filename: Annotated[str, Form()],
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Endpoint for ePub and fb2 uploading"""
    exception = HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="this endpoint supporting only fb2 and ePub files, for upload PDF use /document",
    )
    if type(file.filename) is str:
        _, file_extension = os.path.splitext(file.filename)
    else:
        raise exception

    if file_extension == ".epub":
        db_book = await crud.add_epub_book(db_session, file, filename)
    elif file_extension == ".fb2":
        db_book = await crud.add_fb2_book(db_session, file, filename)
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
    books = []
    for book in row_books:
        model_book = SEpubResponse.model_validate(book, from_attributes=True)
        books.append(model_book)
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
