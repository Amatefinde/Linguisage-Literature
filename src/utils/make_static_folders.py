from os import mkdir
from os.path import isdir, join

from loguru import logger

from src.core import settings


def make_static_folders() -> None:
    logger.debug("Making static folder")
    if not isdir(settings.abs_static_path):
        mkdir(settings.abs_static_path)

    if not isdir(settings.epub_dir):
        mkdir(settings.epub_dir)

    if not isdir(settings.epub_cover_dir):
        mkdir(settings.epub_cover_dir)

    if not isdir(settings.fb2_tmp):
        mkdir(settings.fb2_tmp)
