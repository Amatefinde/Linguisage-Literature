from contextlib import asynccontextmanager
from fastapi import FastAPI
from .linux_converter_permission import give_permission


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Do something before api start
    give_permission()
    yield
    # and after
