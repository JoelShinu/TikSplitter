import logging
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.error import URLError, HTTPError

from pytube import YouTube
from pytube.exceptions import PytubeError


class Downloader(ABC):
    def __init__(self, output_path: Path):
        self.output_path = output_path

    @abstractmethod
    def download_video(self, url: str) -> Path | None:
        ...


class YouTubeDownloader(Downloader):
    def __init__(self, output_path: Path):
        super().__init__(output_path)

    def download_video(self, url: str) -> Path | None:
        try:
            output_directory = str(self.output_path)  # Convert Path to string
            output_directory_path = Path(output_directory)
            output_directory_path.mkdir(parents=True, exist_ok=True)

            youtube = YouTube(url)
            video_stream = youtube.streams.get_highest_resolution()

            logging.warning(f"Downloading YouTube video: {youtube.title}")
            original_filename = video_stream.download(output_directory)
            new_filename = original_filename.replace(" ", "_")
            new_filepath = output_directory_path / new_filename
            Path(original_filename).replace(new_filepath)
            logging.warning(f"Download Complete! File saved as: {new_filename}")

        except (URLError, HTTPError, PytubeError) as e:
            logging.error(f"An error occurred while downloading YouTube video: {e}")
            return None

        return new_filepath
