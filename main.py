from pathlib import Path

from download.downloader import YouTubeDownloader
from post.account import Account
from post.tiktok_poster import Poster
from utils import get_env_details
from videos.tiktok_video import TikTokVideo
from merge.merger import Merger

ROOT_DIR = Path.cwd()


def main():
    video_folder = ROOT_DIR / "videos"
    youtube_downloader = YouTubeDownloader(video_folder)
    youtube_video_url = "https://www.youtube.com/watch?v=AjnDIbKOO8w"
    youtube_downloader.download_video(youtube_video_url)

    video = TikTokVideo("videos/Vikkstar_Was_Having_None_Of_It.mp4", "test")
    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP}_SESSION_ID"))
    poster.upload(video)


def main2():
    VIDEO1_PATH = str(ROOT_DIR / "videos/Vikkstar_Was_Having_None_Of_It.mp4")
    VIDEO2_PATH = str(
        ROOT_DIR / "videos/CHUNKZ_Reveals_The_TRUTH_About_His_WEIGHT_LOSS_Journey!.mp4"
    )
    OUTPUT_PATH = str(ROOT_DIR / "merged_video.mp4")

    merger = Merger()
    merger.merge_videos(VIDEO1_PATH, VIDEO2_PATH, OUTPUT_PATH)


if __name__ == "__main__":
    main()
