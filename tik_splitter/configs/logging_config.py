import logging
from pathlib import Path


def configure_logging():
    # Get the directory of the script or module calling this function
    root_folder = Path(__file__).resolve().parent

    log_folder = root_folder / "logs"
    log_folder.mkdir(parents=True, exist_ok=True)

    log_file_path = log_folder / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
    )

    logger = logging.getLogger("TikSplitter")
    return logger
