from pathlib import Path

from caption import auto_caption
from download.downloader import YouTubeDownloader
from post.account import Account
from post.tiktok_poster import Poster
from utils import get_env_details
from videos.tiktok_video import TikTokVideo

ROOT_DIR = Path.cwd()


def main():
    video_folder = ROOT_DIR / "videos"
    youtube_downloader = YouTubeDownloader(video_folder)
    youtube_video_url = "https://www.youtube.com/watch?v=AjnDIbKOO8w"
    youtube_downloader.download_video(youtube_video_url)

    video = TikTokVideo("videos/Vikkstar Was Having None Of It.mp4", "test")
    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP}_SESSION_ID"))
    poster.upload(video)


def main2():
    auto_caption.transcribe_wav(
        "Vikkstar Was Having None Of It.wav", "transcription.txt"
    )


if __name__ == "__main__":
    main()
