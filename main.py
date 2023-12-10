import logging
from pathlib import Path

from caption.auto_caption import AutoCaptioner
from download.downloader import YouTubeDownloader
from merge.merger import Merger
from post.account import Account
from post.tiktok_poster import Poster
from utils import get_env_details
from videos.tiktok_video import TikTokVideo

ROOT_DIR = Path.cwd()


def main():
    video_folder = ROOT_DIR / "videos"
    youtube_downloader = YouTubeDownloader(video_folder)
    youtube_video_url = "https://www.youtube.com/watch?v=yYXQkQAlMfU"
    youtube_downloader.download_video(youtube_video_url)

    video = TikTokVideo("videos/Vikkstar_Was_Having_None_Of_It.mp4", "test")
    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP}_SESSION_ID"))
    poster.upload(video)


def main2():
    VIDEO1_PATH = str(ROOT_DIR / "videos/Deji_Stitches_Up_Tobi.mp4")
    VIDEO2_PATH = str(ROOT_DIR / "videos/Callux_Gets_Violated.mp4")
    OUTPUT_PATH = str(ROOT_DIR / "merged_video.mp4")

    merger = Merger()
    merger.merge_videos(VIDEO1_PATH, VIDEO2_PATH, OUTPUT_PATH)


def main3():
    VIDEO_URL = "https://www.youtube.com/watch?v=yYXQkQAlMfU"
    OUTPUT_PATH = str(ROOT_DIR / "caption")

    downloader = YouTubeDownloader(OUTPUT_PATH)
    downloader.download_video(VIDEO_URL)

    auto_captioner = AutoCaptioner(OUTPUT_PATH)
    captions = auto_captioner.get_captions(VIDEO_URL)

    if captions is not None:
        auto_captioner.save_captions_as_srt(captions, "captions_output")
    else:
        logging.warning("No captions availal")


if __name__ == "__main__":
    main3()
