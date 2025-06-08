import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from src.logs import get_logger
from src.database.db import db_create

from src.routers.auth_router import router as auth_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_create()
    logger.info(f"FastAPI({hash(app)}) application started up")
    yield
    logger.info(f"FastAPI({hash(app)}) application stopped")


app: FastAPI = FastAPI(
    default_response_class=ORJSONResponse, root_path="/backend", lifespan=lifespan
)


origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
