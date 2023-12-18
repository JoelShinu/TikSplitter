from moviepy.audio.fx.all import audio_fadein
from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip, clips_array
from moviepy.video.fx.all import crop, resize
from numpy import random
from moviepy.config import change_settings

from config import MERGED_PATH
from tik_splitter.entities.video import SplitVideo, Video
from tik_splitter.utils.logging_config import configure_logging


class Merger:
    def __init__(self):
        self._logger = configure_logging("merger")

    def merge_videos(self, video: Video, sample: Video) -> Video | None:
        try:
            change_settings(
                {"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"}
            )  # replace filepath to imagemagick binary
            # Load the videos
            vid1 = VideoFileClip(video.get_filename_as_string())
            vid2 = VideoFileClip(sample.get_filename_as_string())

            # Duration of videos
            video1_duration = vid1.duration
            video2_duration = vid2.duration

            # Trim the beginning of video2 randomly if it's longer than video1
            if video2_duration > video1_duration:
                start_time = random.uniform(0, video2_duration - video1_duration)
                trimmed_video2 = vid2.subclip(start_time, start_time + video1_duration)
            else:
                trimmed_video2 = vid2

            # Resize videos
            resized_video1 = vid1.fx(resize, width=1080, height=606)
            resized_video2 = trimmed_video2.fx(resize, width=2366, height=1314)
            # Calculate the crop parameters to keep the middle section
            target_width, target_height = 1080, 1314
            crop_x_center = resized_video2.size[0] / 2
            crop_y_center = resized_video2.size[1] / 2
            # Crop the video from the center
            cropped_video2 = resized_video2.fx(
                crop, x_center=crop_x_center, y_center=crop_y_center, width=target_width, height=target_height
            )
            # Mute video2
            muted_video2 = cropped_video2.fx(audio_fadein, 0.01)
            muted_video2 = muted_video2.volumex(0)

            if isinstance(video, SplitVideo):
                # Create a TextClip with the caption for one frame
                caption_text = f'{video.get_title()} part {video.get_part()}'
                # Calculate appropriate fontsize for one-line caption
                fontsize = min(resized_video1.size[1], resized_video2.size[1]) // 8

                caption_clip = TextClip(caption_text, fontsize=fontsize, color='white', font='Komika')
                caption_clip = caption_clip.set_duration(1)  # Display for 1 second
                caption_clip = caption_clip.set_pos('center', 606)

            # Position video1 in the top half, and video2 in the bottom half
            final_video = CompositeVideoClip(
                [resized_video1.set_position((0, 0)), muted_video2.set_position((0, 606))], size=(1080, 1920)
            )
            final_video = CompositeVideoClip([final_video, caption_clip], size=(1080, 1920))

            # Write the final video to the output path
            merged_title = video.get_title() + " " + sample.get_title()
            merged_filename = video.get_filename().stem + "_" + sample.get_filename().stem + "_merged.mp4"
            file_location = MERGED_PATH / merged_filename
            final_video.write_videofile(str(file_location), codec="libx264", audio_codec="aac")

            self._logger.info(f"Videos successfully merged and saved at {file_location}")

        except Exception as e:
            self._logger.error("Merge failed:")
            self._logger.exception(e)
            return None

        if isinstance(video, SplitVideo):
            return SplitVideo(
                file_location, merged_title, video.get_raw_description(), video1_duration, video.get_part()
            )

        return Video(
            file_location,
            merged_title,
            video.get_raw_description(),
            video1_duration,
        )
