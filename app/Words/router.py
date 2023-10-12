from fastapi import APIRouter, UploadFile, Depends, File
from app.Words.DAO import WordDAO
from app.Words.schemas import SWord

router = APIRouter(
    prefix="/word",
    tags=["Слова"]
)


@router.post("/add")
async def add_word(word: SWord):
    return await WordDAO.add_world_manual(word)
