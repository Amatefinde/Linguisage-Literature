from datetime import datetime

from pydantic import BaseModel, Field


class SEpubResponse(BaseModel):
    title: str
    last_opened_at: datetime | None = None
    cover: str | None = None
    original_file: str
    last_read_position: int | None = None
    created_at: datetime
    id: int


class SPatchRequest(BaseModel):
    title: str
