from pathlib import Path

from tik_splitter.download.downloader import YouTubeDownloader
from tik_splitter.merge.merger import Merger

ROOT_DIR = Path.cwd()


def main():
    video_folder = ROOT_DIR / "data/videos"

    youtube_downloader = YouTubeDownloader(video_folder)

    youtube_video_url = "https://www.youtube.com/watch?v=AjnDIbKOO8w"

    youtube_downloader.download_video(youtube_video_url)


def main2():
    VIDEO1_PATH = str(ROOT_DIR / "data/videos/Vikkstar_Was_Having_None_Of_It.mp4")
    VIDEO2_PATH = str(ROOT_DIR / "data/videos/CHUNKZ_Reveals_The_TRUTH_About_His_WEIGHT_LOSS_Journey!.mp4")
    OUTPUT_PATH = str(ROOT_DIR / "data/videos/merged_video.mp4")

    merger = Merger()
    merger.merge_videos(VIDEO1_PATH, VIDEO2_PATH, OUTPUT_PATH)


if __name__ == "__main__":
    main2()
