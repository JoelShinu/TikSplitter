import logging
from pathlib import Path

from data.videos.tiktok_video import TikTokVideo
from tik_splitter.caption.auto_caption import AutoCaptioner
from tik_splitter.configs.utils import get_env_details
from tik_splitter.download.downloader import YouTubeDownloader, SampleVideoDownloader
from tik_splitter.merge.merger import Merger
from tik_splitter.post.account import Account
from tik_splitter.post.tiktok_poster import Poster
from data.sample.sample_video_data import sample_video_dict

ROOT_DIR = Path.cwd()


def main():  # YouTube Download and TikTok Post Tester
    video_folder = ROOT_DIR / "data/videos"
    youtube_downloader = YouTubeDownloader(video_folder)
    youtube_video_url = "https://www.youtube.com/watch?v=Yz6rC4K-Kng"
    path = youtube_downloader.download_and_split_video(youtube_video_url)

    video = TikTokVideo(str(path), "test")
    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP.value}_SESSION_ID"))
    poster.upload(video)


def main2():  # Merge Video Tester
    VIDEO1_PATH = ROOT_DIR.resolve() / "data/videos/Deji_Stitches_Up_Tobi.mp4"
    VIDEO2_PATH = ROOT_DIR / "data/videos/Callux_Gets_Violated.mp4"
    OUTPUT_PATH = ROOT_DIR.resolve() / "data/videos/merged_video.mp4"
    CAPTION_PATH = ROOT_DIR.resolve() / "data/captions/captions_output.srt"

    def add_subtitle_to_video(input_video_file, subtitles_file, output_video_with_subtitles_file):
        # Add subtitles to the input video
        ffmpeg.input(str(input_video_file)).output(
            str(output_video_with_subtitles_file), vf='subtitles=' + str(subtitles_file)
        ).run()

    add_subtitle_to_video(VIDEO1_PATH, CAPTION_PATH, OUTPUT_PATH)


def main3():  # AutoCaptioner Tester
    VIDEO_URL = "https://www.youtube.com/watch?v=yYXQkQAlMfU"
    VIDEO_OUTPUT_PATH = ROOT_DIR / "data/videos"
    CAPTION_OUTPUT_PATH = ROOT_DIR / "data/captions"

    downloader = YouTubeDownloader(VIDEO_OUTPUT_PATH)
    downloader.download_video(VIDEO_URL)

    auto_captioner = AutoCaptioner(CAPTION_OUTPUT_PATH)
    captions = auto_captioner.get_captions(VIDEO_URL)

    if captions is not None:
        auto_captioner.save_captions_as_srt(captions, "captions_output")
    else:
        logging.warning("No captions available")


def main4():  # Sample Video Tester
    sample_folder = ROOT_DIR / "data/sample"
    sample_downloader = SampleVideoDownloader(sample_folder)
    sample_downloader.download_sample_video("sample2", sample_video_dict)


if __name__ == "__main__":
    main()
