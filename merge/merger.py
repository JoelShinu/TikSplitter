from pathlib import Path
from moviepy.editor import VideoFileClip, clips_array


class Merger:
    def __init__(self, root_folder="root", output_file="merged_video.mp4"):
        self.root_folder = Path(root_folder)
        self.videos_folder = self.root_folder / "videos"
        self.samples_folder = self.root_folder / "sample"
        self.output_file = self.root_folder / output_file

    def merge_videos(self):
        video_files = sorted(self.videos_folder.glob("*.mp4"))
        sample_files = sorted(self.samples_folder.glob("*.mp4"))

        video_clips = [VideoFileClip(file) for file in video_files]
        sample_clips = [VideoFileClip(file) for file in sample_files]

        # Resize sample videos to match the height of video clips
        # TODO: resize method not currently working properly
        sample_clips_resized = [
            clip.resize(height=video_clips[0].h) for clip in sample_clips
        ]

        # Combine video clips and sample clips horizontally
        clips = clips_array(
            [
                [video_clip, sample_clip]
                for video_clip, sample_clip in zip(video_clips, sample_clips_resized)
            ],
            bg_color=(0, 0, 0),
        )

        # Resize the final video to 1080x1920 - TikTok video sizing (I think)
        final_clip = clips.resize(width=1080)

        # Write the final video to the output file
        final_clip.write_videofile(
            str(self.output_file), codec="libx264", audio_codec="aac"
        )
