from pathlib import Path
from typing import Union

from moviepy.audio.fx.all import audio_fadein
from moviepy.editor import VideoFileClip, clips_array
from moviepy.video.fx.all import resize
from numpy import random

from config import MERGED_PATH
from tik_splitter.entities.video import Video
from tik_splitter.utils.logging_config import configure_logging


class Merger:
    def __init__(self):
        self._logger = configure_logging()

    def merge_videos(self, video1: Video, video2: Video) -> Video | None:
        try:
            # Load the videos
            vid1 = VideoFileClip(video1.get_filename_as_string())
            vid2 = VideoFileClip(video2.get_filename_as_string())

            # Duration of videos
            video1_duration = vid1.duration
            video2_duration = vid2.duration

            # Trim the beginning of video2 randomly if it's longer than video1
            if video2_duration > video1_duration:
                start_time = random.uniform(0, video2_duration - video1_duration)
                trimmed_video2 = vid2.subclip(start_time, start_time + video1_duration)
            else:
                trimmed_video2 = vid2

            # Resize both videos to 1920x1080
            resized_video1 = vid1.fx(resize, width=1920, height=1080)
            resized_video2 = trimmed_video2.fx(resize, width=1920, height=1080)

            # Mute video2
            muted_video2 = resized_video2.fx(audio_fadein, 0.01)
            muted_video2 = muted_video2.volumex(0)

            # Concatenate the videos vertically
            final_video = clips_array([[resized_video1], [muted_video2]])

            # Write the final video to the output path
            merged_title = video1.get_title() + " " + video2.get_title()
            merged_filename = (merged_title + " " + "merged.mp4").replace(" ", "_")
            file_location = MERGED_PATH / merged_filename
            final_video.write_videofile(str(file_location), codec="libx264", audio_codec="aac")

            self._logger.info(f"Videos successfully merged and saved at {file_location}")

        except Exception as e:
            self._logger.error(f"An error occurred: {e}")
            return None

        return Video(
            file_location,
            merged_title,
            video1.get_raw_description() + " " + video2.get_raw_description(),
            vid1.duration + vid2.duration,
        )
