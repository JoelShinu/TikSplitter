import random
from datetime import datetime as dt

from tik_splitter.caption.auto_caption import AutoCaptioner
from tik_splitter.download.downloader import SampleVideoDownloader, VideoDownloader
from tik_splitter.entities.account import Account
from tik_splitter.entities.username import Username
from tik_splitter.merge.merger import Merger
from tik_splitter.post.tiktok_poster import Poster
from tik_splitter.utils.utils import get_env_details


def main():  # Download and Post Tester
    youtube_downloader = VideoDownloader()
    youtube_video_url = "https://www.youtube.com/watch?v=0ahOSXe1ow0"

    video = youtube_downloader.download_video(youtube_video_url)
    poster = Poster(get_env_details(f"{Username.CLIP_CHIMP.value}_SESSION_ID"))
    poster.upload_videos(video)


def main2():  # Download, Merge and Post Tester
    downloader = VideoDownloader()
    videos = downloader.download_and_split_video(
        "https://www.youtube.com/watch?v=0ahOSXe1ow0", start_time="00:00", end_time="05:30", clip_size=90
    )

    merger = Merger()
    merged_vid = merger.merge_videos(videos[0], videos[1])

    poster = Poster(get_env_details(f"{Username.CLIP_CHIMP.value}_SESSION_ID"))
    poster.upload_videos(merged_vid, videos[2], videos[3])


def main3():  # Auto-Caption Tester
    auto_caption = AutoCaptioner()
    auto_caption.get_and_save_captions("https://www.youtube.com/watch?v=0ahOSXe1ow0")


def main4():  # Sample Video Tester
    sample = SampleVideoDownloader()
    sample.download_sample_video("subway_surfers1")


def main5():  # Full Functionality Tester - Download, Split, Merge, Post
    downloader = VideoDownloader()
    sampler = SampleVideoDownloader()
    merger = Merger()
    account = Account(Username.CLIP_CHIMP)
    poster = Poster(account.get_session_id(), last_uploaded=dt(2023, 12, 18, 0, 0))
    videos = downloader.download_and_split_video("https://www.youtube.com/watch?v=9RhWXPcKBI8", clip_size=180)
    sample1 = sampler.download_sample_video("subway_surfers1")
    sample2 = sampler.download_sample_video("minecraft1")
    merged = []
    for vid in videos:
        merged.append(merger.merge_videos(vid, random.choice([sample1, sample2])))

    failed = poster.upload_videos(*merged)
    if len(failed) != 0:
        last_uploaded = poster.get_last_uploaded()
        poster = Poster(account.get_session_id(), False, last_uploaded)
        poster.upload_videos(*failed)


if __name__ == "__main__":
    main5()
