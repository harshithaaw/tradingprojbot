import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = os.path.join(LOG_DIR, f"bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
#creates a logfile with date and time so each gets a unique name


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers: #Prevents adding handlers multiple times
        return logger

    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # writes to log file
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    # prints to terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) #handles info and abov
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger