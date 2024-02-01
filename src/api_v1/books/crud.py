from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import SPatchRequest
from .utils import _save_book_to_disk, _save_book_cover_to_disk, _remove_book_from_disk
from src.core.database.models import LiteratureEpub


async def add_book(
    session: AsyncSession,
    book: UploadFile,
    filename: str,
):
    disk_file_name = _save_book_to_disk(book)
    disk_file_cover_name = _save_book_cover_to_disk(book)

    db_epub = LiteratureEpub(
        title=filename,
        original_file=disk_file_name,
        cover=disk_file_cover_name,
    )

    session.add(db_epub)
    await session.commit()
    await session.refresh(db_epub)
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
