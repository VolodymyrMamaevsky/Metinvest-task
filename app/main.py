from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import endpoints
from app.models.database import create_db
from app.core.config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application is starting...")
    try:
        create_db()
        logger.info("Database successfully created.")
    except Exception as e:
        logger.error(f"Error while creating the database: {e}")
    yield


app = FastAPI(lifespan=lifespan)

# Include routes (endpoints) from endpoints.py
app.include_router(endpoints.router)


@app.get("/")
def read_root():
    logger.info("Request to the homepage.")
    return {"message": "Metinvest test task"}
