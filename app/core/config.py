import os
import sys
from loguru import logger
from dotenv import load_dotenv
from celery import Celery

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logger.remove()
logger.add(
    "app_logs.log",  # Log file storage
    rotation="500 MB",  # Limit log file size
    retention="7 days",  # Keep logs for 7 days
    compression="zip",  # Compress old logs
    level=LOG_LEVEL,
)
logger.add(
    sys.stderr,  # Output logs to console
    level=LOG_LEVEL,
)

# FastAPI server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Celery settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery.conf.update(
    broker_connection_retry_on_startup=True
)
