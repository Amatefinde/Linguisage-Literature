from pydantic import BaseModel
from fastapi import UploadFile


class SLiterature(BaseModel):
    user_id: int
    title: str
