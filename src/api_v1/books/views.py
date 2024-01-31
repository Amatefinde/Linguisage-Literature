import os
from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, status, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/")
async def add(
    file: UploadFile,
    filename: Annotated[str, Form()],
    use_ocr: Annotated[bool, Form()] = False,
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Endpoint for ePub and fb2 uploading"""
    exception = HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="this endpoint supporting only fb2 and ePub files, for upload PDF use /document",
    )
    if type(file.filename) is str:
        _, file_extension = os.path.splitext(file.filename)
    else:
        raise exception
    if not file_extension or file_extension.lower() not in (".epub", ".fb2"):
        raise exception
    # todo
    return filename
