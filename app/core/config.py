import os
import sys
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

REDIS_URL = os.getenv("REDIS_URL")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Set up the logger with Loguru
logger.remove()
logger.add(
    "app_logs.log",  # Log file
    rotation="500 MB",  # Rotate logs after they reach 500 MB
    retention="7 days",  # Keep logs for 7 days
    compression="zip",  # Compress old log files
    level=LOG_LEVEL,  # Log level from environment variable (e.g., INFO, DEBUG)
)
logger.add(
    sys.stderr,  # Log to console as well
    level=LOG_LEVEL,
)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

API_PREFIX = os.getenv("API_PREFIX", "/api")
