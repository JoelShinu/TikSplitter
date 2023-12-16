import logging
import sys

from config import LOG_PATH


def configure_logging(name: str = "logger") -> logging.Logger:
    log_file_path = LOG_PATH / f"{name}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file_path), logging.StreamHandler(sys.stdout)],
    )

    logger = logging.getLogger(f"TikSplitter-{name}")
    return logger
