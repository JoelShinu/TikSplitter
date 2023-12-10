import logging
from pathlib import Path
import os


def configure_logging():
    # Get the directory of the script or module calling this function
    root_folder = os.path.abspath(os.path.dirname(__file__))

    log_folder = os.path.join(root_folder, "logs")
    os.makedirs(log_folder, exist_ok=True)

    log_file_path = os.path.join(log_folder, "app.log")





    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
    )

    logger = logging.getLogger("TikSplitter")
    return logger
