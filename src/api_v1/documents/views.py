import os
from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, status, Form

router = APIRouter(prefix="/document", tags=["Documents"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_document(
    file: UploadFile,
    filename: Annotated[bool, Form()] = None,
    use_ocr: Annotated[bool, Form()] = False,
):
    """Endpoint for PDF uploading"""
    _filename, file_extension = os.path.splitext(file.filename)
    if file_extension.lower() != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="this endpoint supporting only PDF files, for upload fb2 or epub use /book",
        )
    filename = filename or _filename
    # todo
    return filename
