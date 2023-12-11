from pathlib import Path
from typing import Union

from moviepy.audio.fx.all import audio_fadein
from moviepy.editor import VideoFileClip, clips_array
from moviepy.video.fx.all import resize

from tik_splitter.utils.logging_config import configure_logging


class Merger:
    def __init__(self):
        self._logger = configure_logging()

    def merge_videos(self, video1_path: Union[Path, str], video2_path: Union[Path, str], output_path: str) -> Path:
        try:
            # Change the Paths to strings
            video1_str = str(video1_path)
            video2_str = str(video2_path)

            # Load the videos
            video1 = VideoFileClip(video1_str)
            video2 = VideoFileClip(video2_str)

            # Resize both videos to 540x960
            resized_video1 = video1.fx(resize, width=540, height=960)

            trimmed_video2 = video2.subclip(0, resized_video1.duration)
            resized_video2 = trimmed_video2.fx(resize, width=540, height=960)

            # Mute video2
            muted_video2 = resized_video2.fx(audio_fadein, 0.01)
            muted_video2 = muted_video2.volumex(0)

            # Concatenate the videos vertically
            final_video = clips_array([[resized_video1], [muted_video2]])

            # Write the final video to the output path
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

            self._logger.info(f"Videos successfully merged and saved at {output_path}")

            return Path(output_path)

        except Exception as e:
            self._logger.error(f"An error occurred: {str(e)}")