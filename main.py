import logging
from pathlib import Path

from config import ROOT_DIR
from tik_splitter.caption.auto_caption import AutoCaptioner
from tik_splitter.download.downloader import SampleVideoDownloader, VideoDownloader
from tik_splitter.entities.account import Account
from tik_splitter.merge.merger import Merger
from tik_splitter.post.tiktok_poster import Poster
from tik_splitter.utils.utils import get_env_details


def main():  # Download and Post Tester
    youtube_downloader = VideoDownloader()
    youtube_video_url = "https://www.youtube.com/watch?v=0ahOSXe1ow0"

    video = youtube_downloader.download_video(youtube_video_url)
    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP.value}_SESSION_ID"))
    poster.upload_videos(video)


def main2():  # Download, Merge and Post Tester
    downloader = VideoDownloader()
    videos = downloader.download_and_split_video(
        "https://www.youtube.com/watch?v=0ahOSXe1ow0", start_time="00:00", end_time="05:30", clip_size=90
    )

    merger = Merger()
    merged_vid = merger.merge_videos(videos[0], videos[1])

    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP.value}_SESSION_ID"))
    poster.upload_videos(merged_vid, videos[2], videos[3])


def main3():  # Auto-Caption Tester
    auto_caption = AutoCaptioner()
    auto_caption.get_and_save_captions("https://www.youtube.com/watch?v=0ahOSXe1ow0")


def main4():  # Sample Video Tester
    sample_file = Path("C:\\Users\\jenzy\\PycharmProjects\\TikSplitter\\data\\sample\\sample_video_data.json")
    sample = SampleVideoDownloader()
    sample.download_sample_video("subway_surfers1", sample_file)


def main5():  # Full Functionality Tester - Download, Split, Merge, Post
    downloader = VideoDownloader()
    sample = SampleVideoDownloader()
    merger = Merger()
    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP.value}_SESSION_ID"))
    sample_file = Path("C:\\Users\\jenzy\\PycharmProjects\\TikSplitter\\data\\sample\\sample_video_data.json")
    vid1 = downloader.download_and_split_video("https://www.youtube.com/watch?v=aNIQ0MUkOCs")
    vid2 = sample.download_sample_video("gta_2", sample_file)
    vid3 = merger.merge_videos(vid1[0], vid2)
    poster.upload_videos(vid3)


if __name__ == "__main__":
    main2()
