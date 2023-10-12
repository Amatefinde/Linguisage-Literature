from fastapi import FastAPI

from app.Literature.router import router as literature_router
from app.Words.router import router as word_router

app = FastAPI()

app.include_router(literature_router)
app.include_router(word_router)
