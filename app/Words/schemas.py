from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional, List
from enum import Enum


class PrivacyType(str, Enum):
    private = "private"
    public = "public"
    not_verified = "not_verified"


class SMeaning(BaseModel):
    privacy: PrivacyType
    definition: str

    class Config:
        from_attributes = True


class SWord(BaseModel):
    content: str
    meanings: Optional[List[SMeaning]] = list()

    class Config:
        from_attributes = True




