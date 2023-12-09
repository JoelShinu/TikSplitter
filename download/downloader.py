import logging
from abc import ABC, abstractmethod
from pathlib import Path

from pytube import YouTube


class Downloader(ABC):
    def __init__(self, output_path):
        self.output_path = output_path

    @abstractmethod
    def download_video(self, url):
        pass


class YouTubeDownloader(Downloader):
    def download_video(self, url):
        try:
            output_directory = str(self.output_path)  # Convert Path to string
            output_directory_path = Path(output_directory)
            output_directory_path.mkdir(parents=True, exist_ok=True)

            youtube = YouTube(url)
            video_stream = youtube.streams.get_highest_resolution()

            logging.warning(f"Downloading YouTube video: {youtube.title}")
            video_stream.download(output_directory)
            logging.warning("Download Complete!")

        except Exception as e:
            logging.error(f"An error occurred while downloading YouTube video: {e}")
