import logging
import os


def configure_logging(root_folder):
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
