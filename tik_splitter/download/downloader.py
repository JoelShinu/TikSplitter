import logging
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.error import URLError, HTTPError

from pytube import YouTube
from pytube.exceptions import PytubeError
from tik_splitter.configs.logging_config import configure_logging


class Downloader(ABC):
    def __init__(self, output_path: Path):
        self.output_path = output_path
        self._logger = configure_logging()

    @abstractmethod
    def download_video(self, url: str) -> Path | None:
        ...


class YouTubeDownloader(Downloader):
    def __init__(self, output_path: Path):
        super().__init__(output_path)

    def download_video(self, url: str) -> Path | None:
        try:
            output_directory = str(self.output_path)
            output_directory_path = Path(output_directory)
            output_directory_path.mkdir(parents=True, exist_ok=True)

            youtube = YouTube(url)
            video_stream = youtube.streams.get_highest_resolution()

            self._logger.warning(f"Downloading YouTube video: {youtube.title}")
            original_filename = video_stream.download(output_directory)
            new_filename = original_filename.replace(" ", "_")
            new_filepath = output_directory_path / new_filename
            Path(original_filename).replace(new_filepath)
            self._logger.warning(f"Download Complete! File saved as: {new_filename}")

        except (URLError, HTTPError, PytubeError) as e:
            self._logger.error(f"An error occurred while downloading YouTube video: {e}")
            return None

        return new_filepath


class SampleVideoDownloader(YouTubeDownloader):
    def __init__(self, output_path: Path):
        super().__init__(output_path)

    def download_sample_video(self, video_name: str, video_dict: dict) -> Path | None:
        if video_name in video_dict:
            url = video_dict[video_name]
            self._logger.info("Sample videos successfully downloaded!")
            return self.download_video(url)
        else:
            self._logger.error(f"No URL found for video name: {video_name}")
            return None
