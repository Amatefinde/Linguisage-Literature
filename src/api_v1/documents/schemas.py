from pydantic import BaseModel
from fastapi import UploadFile


class SLiterature(BaseModel):
    file: UploadFile
    use_ocr: bool
