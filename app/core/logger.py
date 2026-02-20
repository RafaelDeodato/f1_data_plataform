import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.settings import settings

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"

def setup_logger() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if settings.ENV == "development":
        os.makedirs("logs", exist_ok=True)

        file_handler = RotatingFileHandler("logs/app.log", maxBytes=5*1024*1024, backupCount=4)

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)