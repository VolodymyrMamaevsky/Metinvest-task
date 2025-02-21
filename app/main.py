from fastapi import FastAPI
from app.api import endpoints
from app.models.database import create_db
from app.core.config import logger

app = FastAPI()


@app.on_event("startup")
def on_startup():
    logger.info("Application is starting...")
    try:
        create_db()
        logger.info("Database successfully created.")
    except Exception as e:
        logger.error(f"Error while creating the database: {e}")


# Include routes (endpoints) from the endpoints.py file
app.include_router(endpoints.router)


@app.get("/")
def read_root():
    logger.info("Request to the homepage.")
    return {"message": "Metinvest test task"}
