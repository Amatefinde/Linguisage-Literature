import os

from PIL.Image import Image
from fastapi import UploadFile
from os.path import join
from uuid import uuid4

from src.core import settings
from src.core.database.models import LiteratureEpub
from src.utils import extract_cover_from_epub


def _save_book_to_disk(book: UploadFile) -> str:
    file_name = f"{str(uuid4())}.epub"
    file_path = join(settings.epub_dir, file_name)
    with open(file_path, "wb") as disk_file:
        disk_file.write(book.file.read())
    return file_name


def _save_book_cover_to_disk(book: UploadFile) -> str:
    cover: Image = extract_cover_from_epub(book.file)
    cover.thumbnail((512, 512))
    file_name = f"{str(uuid4())}.jpeg"
    file_path = join(settings.epub_cover_dir, file_name)
    cover.save(file_path, "JPEG", quality=95)
    return file_name


def _remove_book_cover(book: LiteratureEpub):
    if book.cover:
        book_cover_path = join(settings.epub_cover_dir, str(book.cover))
        os.remove(book_cover_path)


def _remove_book_from_disk(
    book: LiteratureEpub,
    remove_cover=True,
) -> None:
    book_path = join(settings.epub_dir, book.original_file)
    os.remove(book_path)
    if remove_cover:
        _remove_book_cover(book)
