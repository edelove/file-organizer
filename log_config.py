import logging
from logging.handlers import RotatingFileHandler
from constants import LOG_BACKUP_COUNT,LOG_FILENAME,LOG_MAX_BYTES

def setup_logging():

    open(LOG_FILENAME, "w").close()
    
    file_handler = RotatingFileHandler(
        LOG_FILENAME,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            file_handler,
            logging.StreamHandler()
        ]
    )