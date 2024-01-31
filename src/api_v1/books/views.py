import os
from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, status, Form


router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/")
async def add(
    file: UploadFile,
    filename: Annotated[bool, Form()] = None,
    use_ocr: Annotated[bool, Form()] = False,
):
    """Endpoint for ePub and fb2 uploading"""
    _filename, file_extension = os.path.splitext(file.filename)
    if file_extension.lower() not in (".epub", ".fb2"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="this endpoint supporting only fb2 and ePub files, for upload PDF use /document",
        )
    filename = filename or _filename
    # todo
    return filename
