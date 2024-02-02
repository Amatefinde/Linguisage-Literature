from os import mkdir
from os.path import isdir, join
from loguru import logger

from src.core import settings


def make_static_folders() -> None:
    if not isdir(settings.abs_static_path):
        mkdir(settings.abs_static_path)
        logger.info("static dir created")

    if not isdir(settings.epub_dir):
        mkdir(settings.epub_dir)
        logger.info("epub dir created")

    if not isdir(settings.epub_cover_dir):
        mkdir(settings.epub_cover_dir)
        logger.info("epub_cover dir created")

    if not isdir(settings.fb2_tmp):
        mkdir(settings.fb2_tmp)
        logger.info("fb2_tmp dir created")
