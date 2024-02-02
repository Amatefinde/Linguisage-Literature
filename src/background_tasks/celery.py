from celery import Celery


celery = Celery(
    "literature_tasks",
    broker="redis://127.0.0.1:6379",
    include=["src.background_tasks.tasks"],
)
celery.conf.task_default_queue = "lite_queue"
