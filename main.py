from pathlib import Path

from download.downloader import YouTubeDownloader
from merge.merger import Merger

ROOT_DIR = Path.cwd()


def main():
    video_folder = ROOT_DIR / "videos"

    youtube_downloader = YouTubeDownloader(video_folder)

    youtube_video_url = "https://www.youtube.com/watch?v=AjnDIbKOO8w"

    youtube_downloader.download_video(youtube_video_url)


def main2():
    video_folder = ROOT_DIR / "videos"
    video_file = 'videos/Vikkstar Was Having None Of It.mp4.mp4'
    merger = Merger()
    merger.merge_videos(video_file)


if __name__ == "__main__":
    main2()
