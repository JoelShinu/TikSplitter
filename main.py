import logging

from config import ROOT_DIR
from data.sample.sample_video_data import sample_video_dict
from tik_splitter.caption.auto_caption import AutoCaptioner
from tik_splitter.download.downloader import SampleVideoDownloader, VideoDownloader
from tik_splitter.entities.account import Account
from tik_splitter.merge.merger import Merger
from tik_splitter.post.tiktok_poster import Poster
from tik_splitter.utils.utils import get_env_details


def main():
    video_folder = ROOT_DIR / "data/videos"
    youtube_downloader = VideoDownloader(video_folder)
    youtube_video_url = "https://www.youtube.com/watch?v=yYXQkQAlMfU"

    video = youtube_downloader.download_video(youtube_video_url)
    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP.value}_SESSION_ID"))
    poster.upload_videos(video)


def main2():
    downloader = VideoDownloader()
    videos = downloader.download_and_split_video("https://www.youtube.com/watch?v=YDp3Np4suO4")

    merger = Merger()
    merged_vid = merger.merge_videos(videos[0], videos[1])

    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP.value}_SESSION_ID"))
    poster.upload_videos(merged_vid, videos[2], videos[3])


def main3():  # AutoCaptioner Tester
    VIDEO_URL = "https://www.youtube.com/watch?v=yYXQkQAlMfU"
    VIDEO_OUTPUT_PATH = ROOT_DIR / "data/videos"
    CAPTION_OUTPUT_PATH = ROOT_DIR / "data/captions"

    downloader = VideoDownloader(VIDEO_OUTPUT_PATH)
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
