from typing import Sequence, Iterable

from fastapi import UploadFile
from sqlalchemy import select

from src.background_tasks import handle_fb2
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import SPatchRequest
from src.api_v1.books.book_storage import (
    _save_epub_to_disk,
    _save_book_cover_to_disk,
    _remove_book_from_disk,
    _save_fb2_in_tmp,
)
from src.core.database.models import LiteratureEpub


async def add_epub_book(
    session: AsyncSession,
    book: UploadFile,
    filename: str,
):

    disk_file_name = _save_epub_to_disk(book)
    disk_file_cover_name = _save_book_cover_to_disk(book)

    db_epub = LiteratureEpub(
        title=filename,
        original_file=disk_file_name,
        cover=disk_file_cover_name,
        is_processed=True,
    )

    session.add(db_epub)
    await session.commit()
    await session.refresh(db_epub)
    return db_epub


async def add_fb2_book(
    session: AsyncSession,
    book: UploadFile,
    user_chosen_filename: str,
):
    filename_without_extension = _save_fb2_in_tmp(book)

    db_epub = LiteratureEpub(
        title=user_chosen_filename,
        original_file=f"{filename_without_extension}.epub",
        is_processed=False,
    )

    session.add(db_epub)
    await session.commit()
    await session.refresh(db_epub)

    handle_fb2.delay(filename_without_extension, db_epub.id)

    return db_epub


async def get_book(session: AsyncSession, book_id: int) -> LiteratureEpub | None:
    return await session.get(LiteratureEpub, book_id)


async def update_partial_book(
    session: AsyncSession,
    book: LiteratureEpub,
    new_fields: SPatchRequest,
) -> LiteratureEpub:
    for field_name, value in new_fields.model_dump(exclude_none=True).items():
        setattr(book, field_name, value)

    await session.commit()
    await session.refresh(book)

    return book


async def delete_book(session: AsyncSession, book: LiteratureEpub) -> None:
    _remove_book_from_disk(book)
    await session.delete(book)
    await session.commit()


async def get_many_books(
    session: AsyncSession, book_ids: list[int]
) -> Iterable[LiteratureEpub]:
    stmt = select(LiteratureEpub).where(LiteratureEpub.id.in_(book_ids))
    return await session.scalars(stmt)
