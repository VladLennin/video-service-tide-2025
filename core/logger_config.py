import os
import logging
from logging.handlers import RotatingFileHandler

from core.config import settings

# Define base logs directory
LOG_BASE_DIR = settings.logs.base_dir
# Define logs format
LOG_FORMAT = settings.logs.format
# Define logs file size
LOG_FILE_SIZE = settings.logs.file_size
# Define logs backup count
LOG_BACKUP_COUNT = settings.logs.backup_count

os.makedirs(LOG_BASE_DIR, exist_ok=True)


def get_logger(module_name: str):
    """
    Creates a logger for a specific module with file rotation.

    Each module gets its own directory inside "logs/".
    """
    # Define module-specific log directory
    module_log_dir = os.path.join(LOG_BASE_DIR, module_name)
    os.makedirs(module_log_dir, exist_ok=True)  # Create module-specific log dir

    # Define module log file path
    log_file_path = os.path.join(module_log_dir, f"{module_name}.log")

    # Create rotating file handler (5MB per file, keep 3 backups)
    file_handler = RotatingFileHandler(log_file_path, maxBytes=LOG_FILE_SIZE, backupCount=LOG_BACKUP_COUNT)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Create logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(logging.StreamHandler())  # Also log to console

    return logger
