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


def main2():  # Download and Merge Video Tester
    video_folder = ROOT_DIR / "data/videos"
    merge_folder = ROOT_DIR / "data/merged/output.mp4"
    youtube_downloader = YouTubeDownloader(video_folder)
    youtube_video_url = "https://www.youtube.com/watch?v=Yz6rC4K-Kng"
    videos = youtube_downloader.download_and_split_video(youtube_video_url)
    video1 = videos[0]
    video2 = videos[1]

    merger = Merger()
    merger.merge_videos(str(video1), str(video2), str(merge_folder))


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
    main2()

