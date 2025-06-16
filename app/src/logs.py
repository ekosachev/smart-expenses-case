import logging
from src.params.config import config


def get_logger(name: str, level: int = logging.INFO, tags: dict | None = None):
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


