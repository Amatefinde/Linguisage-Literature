from fastapi import APIRouter, UploadFile, Depends, File, HTTPException, status
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
    db_world_info = await WordDAO.get_word(word)
    if db_world_info:
        return db_world_info
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found info about word \"{word}\" in db ")


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


@router.get("/meaning_by_id")
async def get_meaning_by_id(meaning_id: int):
    meaning_db = await WordDAO.get_meaning_by_id(meaning_id)
    if meaning_db:
        return meaning_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meaning with this id is not found")


@router.get("/get_word_meaning_by_id")
async def get_word_meaning_by_id(meaning_id: int):
    meaning_db = await WordDAO.get_word_meaning_by_id(meaning_id)
    if meaning_db:
        return meaning_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meaning with this id is not found")


@router.get('/image')
async def get_image_by_id(image_id: int) -> str:
    image_db = await WordDAO.get_image_by_id(image_id)
    if image_db:
        return image_db.content
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image with this id is not found")

