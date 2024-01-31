import asyncio

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from src.core import settings


class DatabaseHelper:
    def __init__(self, db_url: str, echo: bool = False):
        self.engine = create_async_engine(db_url, echo=echo)

        self.async_session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_scoped_session(self):
        async_session = async_scoped_session(
            session_factory=self.async_session_factory,
            scopefunc=asyncio.current_task,
        )
        return async_session

    async def session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.remove()


db_helper = DatabaseHelper(db_url=settings.db_url, echo=settings.db_echo)
