import logging
import sys
from app.Core.Config.settings import settings


logging.basicConfig(
    level=settings.LOG_LEVEL.upper(),
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)