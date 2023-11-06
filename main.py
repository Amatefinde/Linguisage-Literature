from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.Literature.router import router as literature_router
from app.Words.router import router as word_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(literature_router)
app.include_router(word_router)
