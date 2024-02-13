from celery import Celery
from src.core import settings

celery = Celery(
    "literature_tasks",
    broker=f"redis://{settings.REDIS_HOST}:6379",
    include=["src.background_tasks.tasks"],
)
celery.conf.task_default_queue = "lite_queue"
