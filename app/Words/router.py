from fastapi import APIRouter, UploadFile, Depends, File
from app.Words.DAO import WordDAO
from app.Words.schemas import SWord

router = APIRouter(
    prefix="/word",
    tags=["Слова"]
)


@router.post("/add")
async def add_word(word: SWord):
    """If 'word' already exist, but current 'meaning' or 'idioms' is new, then for 'word' will be added new 'meanings' or 'idioms'.
    If 'word', 'meaning' and 'idioms' already exists - will be nothing"""
    return await WordDAO.add_word_manual(word)


@router.get("/get")
async def add_word(word: str):
    """Return data for requested word"""
    return await WordDAO.get_word(word)


@router.get("/get_word_id")
async def add_word(word: str):
    """For developers"""
    return await WordDAO.get_word_id(word)


@router.get("/get_word_meaning_id")
async def add_word(word: str, meaning: str):
    """For developers"""
    return await WordDAO.get_word_meaning_id(word, meaning)


@router.get("/get_word_idiom_id")
async def add_word(word: str, idiom_content: str):
    """For developers"""
    return await WordDAO.get_word_meaning_id(word, idiom_content)

