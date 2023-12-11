import logging
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.error import URLError, HTTPError
import ffmpeg
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

            self._logger.info(f"Downloading YouTube video: {youtube.title}")
            original_filename = video_stream.download(output_directory)
            new_filename = original_filename.replace(" ", "_")
            new_filepath = output_directory_path / new_filename
            Path(original_filename).replace(new_filepath)
            self._logger.info(f"Download Complete! File saved as: {new_filename}")

        except (URLError, HTTPError, PytubeError) as e:
            self._logger.error(f"An error occurred while downloading YouTube video: {e}")
            return None

        return new_filepath

    def split_video(self, video_path: Path) -> list[Path]:
        # splits the video into segments of 'segment time'
        try:
            video_title = video_path.stem
            output_directory = video_path.parent
            output_base_filename = video_title.replace(" ", "_")

            self._logger.info(f"Splitting video: {video_title}")

            (
                ffmpeg.input(str(video_path))
                .output(
                    str(output_directory / f"{output_base_filename}_%02d.mp4"),
                    codec='copy',
                    f='segment',
                    segment_time=90,
                    reset_timestamps=1,
                )
                .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
            )

            video_path.unlink()
            split_video_paths = sorted(output_directory.glob(f"{output_base_filename}_*.mp4"))
            self._logger.info(f"Video splitting complete!")
            return split_video_paths

        except ffmpeg.Error as e:
            self._logger.error(f"An error occurred while splitting the video: {e}")
            return []

    def download_and_split_video(self, url: str) -> list[Path] | None:
        # return the list of split video paths
        video_path = self.download_video(url)
        if video_path:
            return self.split_video(video_path)
        return None


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
