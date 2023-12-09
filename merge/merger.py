import glob
import logging
import os
from typing import List

from moviepy.editor import VideoFileClip, clips_array
from moviepy.video.fx.all import resize

from configs.logging_config import configure_logging


class Merger:
    def __init__(self, root_folder="root", output_file="merged_video.mp4"):
        self.root_folder = os.path.abspath(root_folder)
        self.videos_folder = os.path.join(self.root_folder, "videos")
        self.samples_folder = os.path.join(os.path.dirname(self.root_folder), "sample")
        self.output_file = os.path.join(self.root_folder, output_file)
        self.logger = configure_logging(self.root_folder)

    def get_next_output_file(self):
        base_name, extension = os.path.splitext(self.output_file)
        index = 1
        while os.path.exists(f"{base_name}_{index}{extension}"):
            index += 1
        return f"{base_name}_{index}{extension}"

    def merge_videos(self, video_file: str):
        sample_files = sorted(
            glob.glob(os.path.join(self.samples_folder, "sample_video*.mp4"))
        )
        output_file = self.get_next_output_file()

        video_number = int(
            os.path.splitext(os.path.basename(video_file))[0].replace("video", "")
        )
        sample_file = next(
            (
                file
                for file in sample_files
                if f"sample_video{video_number}" in os.path.basename(file)
            ),
            None,
        )

        if sample_file is not None:
            video_clip = VideoFileClip(video_file)
            sample_clip = VideoFileClip(sample_file)

            # Resize sample video to match the height of the video clip
            sample_clip_resized = resize(sample_clip, height=video_clip.h)

            # Combine video clip and sample clip horizontally
            clips = clips_array(
                [[video_clip, sample_clip_resized]], bg_color=(0, 0, 0)
            )

            # Resize the final video to 1080x1920 - TikTok video sizing (I think)
            final_clip = clips.resize(height=1920)

            # Write the final video to the output file
            final_clip.write_videofile(
                output_file, codec="libx264", audio_codec="aac"
            )

            self.logger.info(
                f"Merged {os.path.basename(video_file)} with {os.path.basename(sample_file)}. Saved as {os.path.basename(output_file)}"
            )
        else:
            self.logger.warning(
                f"No corresponding sample video found for {os.path.basename(video_file)}"
            )