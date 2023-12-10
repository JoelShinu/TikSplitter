from pathlib import Path

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
    youtube_video_url = "https://www.youtube.com/shorts/e-G3YQaY8Ow"
    path = youtube_downloader.download_video(youtube_video_url)

    video = TikTokVideo(str(path), "test")
    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP.value}_SESSION_ID"))
    poster.upload(video)


def main2():
    VIDEO1_PATH = str(ROOT_DIR / "videos/Vikkstar_Was_Having_None_Of_It.mp4")
    VIDEO2_PATH = str(
        ROOT_DIR / "videos/POKE_MOMENTS_28_S4.mp4"
    )
    OUTPUT_PATH = str(ROOT_DIR / "merged_video.mp4")

    merger = Merger()
    merger.merge_videos(VIDEO1_PATH, VIDEO2_PATH, OUTPUT_PATH)


if __name__ == "__main__":
    main()
