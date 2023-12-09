from pathlib import Path

from download.downloader import YouTubeDownloader

ROOT_DIR = Path.cwd()


def main():
    video_folder = ROOT_DIR / "videos"

    youtube_downloader = YouTubeDownloader(video_folder)

    youtube_video_url = "https://www.youtube.com/watch?v=AjnDIbKOO8w"

    youtube_downloader.download_video(youtube_video_url)


if __name__ == "__main__":
    main()
