import uvicorn
from elasticsearch_dsl import connections
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.routers.es import router as es_router
from app.routers.search import router as search_router
from app.routers.filter import router as filter_router
from app.routers.read import router as read_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize elasticsearch
    connections.create_connection(
        hosts=[settings.ELASTICSEARCH_HOST],
        http_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD)
        if (settings.ELASTICSEARCH_USER and settings.ELASTICSEARCH_PASSWORD)
        else None,
    )
    yield
    connections.remove_connection(alias="default")


app = FastAPI(lifespan=lifespan)
app.include_router(es_router)
app.include_router(search_router)
app.include_router(filter_router)
app.include_router(read_router)


@app.get("/")
async def root():
    return "AHA-BIBLE"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
