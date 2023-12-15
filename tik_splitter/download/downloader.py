from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from urllib.error import HTTPError, URLError
import ffmpeg
import subprocess
import json
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
from pytube.cli import on_progress
from pytube.exceptions import PytubeError
from config import SAMPLE_PATH, VIDEO_PATH
from tik_splitter.entities.video import Video
from tik_splitter.utils.logging_config import configure_logging
from tik_splitter.utils.utils import clean_string, get_sec


class Downloader(ABC):
    def __init__(self, output_path: Path):
        self._output_path = output_path
        self._logger = configure_logging()

    @abstractmethod
    def download_video(self, url: str) -> Video | None:
        ...


class VideoDownloader(Downloader):
    def __init__(self, output_path: Path = VIDEO_PATH):
        super().__init__(output_path)

    def download_video(self, url: str, start_time: str = None, end_time: str = None) -> Video | None:
        if (start_time is None and end_time is not None) or (start_time is not None and end_time is None):
            raise ValueError("If either start time or end time is provided, both must be provided")
        try:
            output_path = self._output_path
            output_directory = str(self._output_path)  # Convert Path to string

            youtube = YouTube(url)
            video_title = clean_string(youtube.title)  # regex video name
            video_length = youtube.length
            video_stream = youtube.streams.get_highest_resolution()

            self._logger.info(f"Downloading YouTube video: {youtube.title}")
            video_download = video_stream.download(output_directory)
            new_filename = video_title + ".mp4"
            video_filepath = output_path / new_filename

            if start_time and end_time:  # TODO: if start_ or end_time:
                start = get_sec(start_time)  # TODO: if start_time else 0
                end = get_sec(end_time)  # TODO: if end_time else video_length
                video = VideoFileClip(str(video_download)).subclip(start, end)
                video.write_videofile(str(video_filepath))
                video.close()

                Path(video_download).unlink()
                video_duration = int(end - start)
            else:
                Path(video_download).rename(video_filepath)
                video_duration = int(youtube.length)

            self._logger.info(f"Download Complete! File saved as: {new_filename}")

        except (URLError, HTTPError, PytubeError, subprocess.CalledProcessError) as e:
            self._logger.error(f"An error occurred while downloading YouTube video: {e}")
            return None

        tags = youtube.keywords
        desc = "#fyp " + " ".join(list(map(lambda tag: "#" + str(tag).strip(), tags)))
        duration = video_duration
        return Video(video_filepath, youtube.title, desc, duration)

    def split_video(self, video: Video, clip_size: int = 90) -> List[Video]:
        # splits the video into segments of 'segment time'
        try:
            video_filepath = video.get_filename()
            video_title = video_filepath.stem
            output_directory = video_filepath.parent

            self._logger.info(f"Splitting video: {video_title}")

            duration = int(video.get_duration())
            number_of_clips = duration // clip_size

            combined_clips = []

            for i in range(number_of_clips - 1):
                start_time = i * clip_size
                end_time = (i + 1) * clip_size
                self.process_clip(video, output_directory, video_title, start_time, end_time, i + 1, combined_clips)

            # Process the last clip separately
            start_time_last_clip = (number_of_clips - 1) * clip_size
            end_time_last_clip = duration
            self.process_clip(
                video,
                output_directory,
                video_title,
                start_time_last_clip,
                end_time_last_clip,
                number_of_clips,
                combined_clips,
            )

            self._logger.info(f"Video splitting complete!")

            video_filepath.unlink()

            return combined_clips

        except ffmpeg.Error as e:
            self._logger.error(f"An error occurred while splitting the video: {e}")
            return []

    def download_and_split_video(
        self, url: str, start_time: str = None, end_time: str = None, clip_size: int = None
    ) -> List[Video] | None:
        # return the list of split video paths
        video = self.download_video(url, start_time, end_time)
        if video:
            return self.split_video(video, clip_size)
        return None

    def process_clip(
        self,
        video: Video,
        output_directory: Path,
        video_title: str,
        start_time: int,
        end_time: int,
        clip_number: int,
        combined_clips: List[Video],
    ):
        output_filepath = str(output_directory / f"{video_title}_{clip_number}.mp4")

        (
            ffmpeg.input(video.get_filename_as_string(), ss=start_time, to=end_time)
            .output(
                output_filepath,
                codec='copy',
            )
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )

        video_clip = Video(
            Path(output_filepath), video.get_title(), video.get_raw_description(), int(end_time - start_time)
        )
        combined_clips.append(video_clip)


class SampleVideoDownloader(VideoDownloader):
    def __init__(self, output_path: Path = SAMPLE_PATH):
        super().__init__(output_path)

    def download_video(self, url: str) -> Video | None:
        ...

    def download_sample_video(self, video_name: str, json_file_path: Path) -> Video | None:
        # TODO: should the json_file_path in the method be Path = SAMPLE_PATH?
        with open(json_file_path, 'r') as file:
            video_dict = json.load(file)

        if video_name in video_dict:
            url = video_dict[video_name]
            video = super().download_video(url)

            if video:
                self._logger.info("Sample videos successfully downloaded!")
            else:
                self._logger.error(f"Error downloading: {video_name}")

            return video
        else:
            self._logger.info(f"No URL found for the video name: {video_name}")
