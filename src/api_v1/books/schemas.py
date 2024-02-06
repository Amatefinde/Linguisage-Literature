from datetime import datetime
from os.path import join

from src.core import settings
from pydantic import BaseModel, Field, field_serializer


class SEpubResponse(BaseModel):
    id: int
    title: str
    is_processed: bool
    cover: str | None = None
    original_file: str
    created_at: datetime
    last_opened_at: datetime | None = None
    last_read_position: int | None = None

    @field_serializer("cover")
    def serialize_cover_for_url(self, cover: str | None):
        if cover is None:
            return None
        return join(
            settings.base_url, settings.static_path, "epub_covers", cover
        ).replace("\\", "/")

    @field_serializer("original_file")
    def serialize_file_for_url(self, original_file: str):
        return join(
            settings.base_url, settings.static_path, "epubs", original_file
        ).replace("\\", "/")


class SPatchRequest(BaseModel):
    title: str


class ManyBookResponse(BaseModel):
    books: list[SEpubResponse] = Field(default_factory=list)
