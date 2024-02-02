import asyncio
import os
from os.path import join

from PIL.Image import Image
from loguru import logger

from .celery import celery
from src.utils.fb2_converter import save_fb2_as_epub
from src.core import settings
from src.core.database import db_helper
from src.utils import extract_cover_from_epub
from src.core.database.models import LiteratureEpub

loop = asyncio.get_event_loop()


async def update_epub_db(
    cover_name: str,
    book_id: int,
):
    logger.debug("асинхронно вошли")
    async with db_helper.async_session_factory() as db_session:
        db_book = await db_session.get_one(LiteratureEpub, book_id)
        db_book.cover = cover_name
        db_book.is_processed = True
        await db_session.commit()


@celery.task(ignore_result=True)
def handle_fb2(filename_without_ext: str, book_id: int):
    fb2_filepath = str(join(settings.fb2_tmp, f"{filename_without_ext}.fb2"))
    save_fb2_as_epub(fb2_filepath, settings.epub_dir)
    logger.debug(f"converted epub saved to {settings.epub_dir}")
    os.remove(fb2_filepath)

    epub_filename = f"{filename_without_ext}.epub"
    epub_filepath = str(join(settings.epub_dir, epub_filename))
    cover_image: Image = extract_cover_from_epub(epub_filepath)
    cover_filename = f"{filename_without_ext}.jpeg"
    cover_image_path = join(settings.epub_cover_dir, cover_filename)
    cover_image.save(cover_image_path, format="JPEG", quality=95)

    loop.run_until_complete(update_epub_db(cover_filename, book_id))
