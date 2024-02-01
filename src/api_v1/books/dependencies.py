from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from src.core.database import db_helper
from src.core.database.models import LiteratureEpub


async def epub_book_dependency(
    book_id: Annotated[int, Path(ge=1)],
    db_session: AsyncSession = Depends(db_helper.session_dependency),
) -> LiteratureEpub:
    db_book = await crud.get_book(session=db_session, book_id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return db_book
