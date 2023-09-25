from fastapi import APIRouter, UploadFile, Depends, File
from app.Literature.DAO import LiteratureDAO
from app.Literature.schemas import SLiterature

router = APIRouter(
    prefix="/literature",
    tags=["Литература"]
)


@router.get("/all")
async def get_all():
    result = LiteratureDAO.get_all()
    return await result


@router.get("user/{user_id}")
async def get_by_user_id(user_id: int):
    return await LiteratureDAO.get_by_user_id(user_id)


@router.get("/{literature_id}")
async def get_by_literature_id(literature_id: int):
    return await LiteratureDAO.get_by_literature_id(literature_id)


@router.delete("/{literature_id}")
async def delete_by_literature_id(literature_id: int):
    return await LiteratureDAO.delete_by_literature_id(literature_id)


@router.post("/")
async def add_one_literature(literature: SLiterature = Depends(), file: UploadFile = File(...)):
    return await LiteratureDAO.add_user_literature(literature, file)




