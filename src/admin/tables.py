from typing import Any

from sqladmin import ModelView
from starlette.requests import Request

from src.api_v1.books.crud import get_book, delete_book
from src.core.database.models import LiteratureEpub
from src.core.database import db_helper


class AdminLiteratureEpub(ModelView, model=LiteratureEpub):
    column_list = [
        LiteratureEpub.id,
        LiteratureEpub.title,
        LiteratureEpub.is_processed,
        LiteratureEpub.created_at,
        LiteratureEpub.last_opened_at,
    ]

    async def delete_model(self, request: Request, pk: Any) -> None:
        async with db_helper.async_session_factory() as session:
            db_book = await get_book(session, int(pk))
            await delete_book(session, db_book)
