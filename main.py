from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from fastapi.middleware.cors import CORSMiddleware
from src.api_v1 import router as api_v1_router
from src.core import settings
from src.core.database import db_helper
from src.utils import lifespan, make_static_folders
from src.admin import AdminLiteratureEpub

make_static_folders()

app = FastAPI(lifespan=lifespan)
app.title = "Literature"
app.summary = (
    "One of Linguisage microservices that have response for literature management"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://linguisage.ru",
]

headers = [
    "Authorization",
    "Content-Type",
    "Set-Cookie",
    "Accept",
    "Content-Length",
    "User-Agent",
    "Proxy-Authorization",
    "Proxy-Connection",
    "User-Agent",
    "Access-Control-Allow-Headers",
    "Access-Control-Request-Method",
    "Access-Control-Allow-Origin",
]

app.mount(
    "/static",
    StaticFiles(directory=settings.static_path),
    name="static_files",
)
app.include_router(api_v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=headers,
)


@app.get("/get_error")
async def get_error():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test error")


admin = Admin(app, engine=db_helper.engine)
admin.add_view(AdminLiteratureEpub)
