from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional, List
from enum import Enum


class PrivacyType(str, Enum):
    private = "private"
    public = "public"
    not_verified = "not_verified"


class Collocation(BaseModel):
    title: str
    body: List[str]


class SMeaning(BaseModel):
    privacy: PrivacyType
    short_meaning: Optional[str] = ""
    meaning: str
    examples: Optional[List[str]] = list()

    collocations: Optional[list[Collocation]] = list()

    class Config:
        from_attributes = True


class Idiom(BaseModel):
    content: str
    label: Optional[str] = ""
    explain: str
    examples: Optional[List[str]] = []


class SWord(BaseModel):
    content: str
    meanings: Optional[List[SMeaning]]
    idioms: Optional[List[Idiom]]

    class Config:
        from_attributes = True




