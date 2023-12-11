import logging

from config import ROOT_DIR
from tik_splitter.caption.auto_caption import AutoCaptioner
from tik_splitter.download.downloader import VideoDownloader
from tik_splitter.merge.merger import Merger
from tik_splitter.post.account import Account
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
    vid1 = downloader.download_video("https://www.youtube.com/watch?v=yYXQkQAlMfU")
    vid2 = downloader.download_video("https://www.youtube.com/watch?v=yYXQkQAlMfU")
    merger = Merger()
    vid3 = merger.merge_videos(vid1, vid2)
    poster = Poster(get_env_details(f"{Account.CLIP_CHIMP.value}_SESSION_ID"))
    poster.upload_videos(vid3)


def main3():
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


if __name__ == "__main__":
    main2()
