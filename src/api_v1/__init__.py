from fastapi import APIRouter
from src.api_v1.documents.views import router as documents_router
from src.api_v1.books.views import router as books_router
from src.core import settings

router = APIRouter(prefix=settings.api_v1_prefix)
router.include_router(books_router)
# router.include_router(documents_router)
