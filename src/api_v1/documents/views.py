import os
from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, status, Form

router = APIRouter(prefix="/document", tags=["Documents"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_document(
    file: UploadFile,
    filename: Annotated[str, Form()],
    use_ocr: Annotated[bool, Form()] = False,
):
    """Endpoint for PDF uploading"""

    exception = HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="this endpoint supporting only PDF files, for upload fb2 or epub use /book",
    )
    if type(file.filename) is str:
        _, file_extension = os.path.splitext(file.filename)
    else:
        raise exception
    if not file_extension or file_extension.lower() not in (".epub", ".fb2"):
        raise exception
    # todo
    return filename
