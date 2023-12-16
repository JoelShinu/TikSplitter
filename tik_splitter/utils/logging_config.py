import logging
import sys

from config import LOG_PATH


def configure_logging(name: str = "logger") -> logging.Logger:
    log_file_path = LOG_PATH / f"{name}.log"
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    handler1 = logging.FileHandler(log_file_path)
    handler1.setFormatter(formatter)
    handler2 = logging.StreamHandler(sys.stdout)
    handler2.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler1)
    logger.addHandler(handler2)

    return logger
