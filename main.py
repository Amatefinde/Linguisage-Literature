from fastapi import FastAPI

from app.Literature.router import router as literature_router

app = FastAPI()

app.include_router(literature_router)
