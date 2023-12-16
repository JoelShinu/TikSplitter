from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, urlparse

from pytube import Caption, YouTube
from youtube_transcript_api import YouTubeTranscriptApi

from config import CAPTION_PATH
from tik_splitter.utils.logging_config import configure_logging
from tik_splitter.utils.utils import clean_string


class AutoCaptioner:
    def __init__(self, output_path: Path = CAPTION_PATH):
        self._output_path = Path(output_path)
        self._logging = configure_logging("captioner")

    def get_and_save_captions(self, video_url: str):
        try:
            # Get video ID and captions
            video_id = self.extract_video_id(video_url)
            if video_id:
                captions = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])

                # Get video title and clean it
                video_title = self.get_video_title(video_url)
                formatted_title = clean_string(video_title)

                # Save captions as SRT with formatted video title
                self.save_captions_as_srt(captions, formatted_title)

            else:
                self._logging.error("Unable to extract video ID from the YouTube URL.")

        except Exception as e:
            self._logging.error("An error occurred while saving captions:")
            self._logging.exception(e)

    def get_captions(self, video_url: str) -> Iterable[Caption] | None:
        try:
            video_id = self.extract_video_id(video_url)
            if video_id:
                captions = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
                return captions
            else:
                self._logging.error("Unable to extract video ID from the YouTube URL.")
                return None

        except Exception as e:
            self._logging.error("An error occurred while fetching captions:")
            self._logging.exception(e)
            return None

    def extract_video_id(self, video_url: str) -> str | None:
        try:
            parsed_url = urlparse(video_url)
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]

            if not video_id and parsed_url.path.startswith("/v/"):
                # Handle case where video ID is in the path (e.g., /v/{video_id})
                video_id = parsed_url.path.split("/")[-1]

            return video_id
        except Exception as e:
            self._logging.error("An error occurred while extracting video ID:")
            self._logging.exception(e)
            return None

    def save_captions_as_srt(self, captions: Iterable[Caption], output_filename: str):
        try:
            output_file_path = self._output_path / (output_filename + ".srt")

            with open(output_file_path, "w", encoding="utf-8") as srt_file:
                for i, caption in enumerate(captions, start=1):
                    srt_file.write(f"{i}\n")
                    srt_file.write(f"{caption['start']} --> {caption['start'] + caption['duration']}\n")
                    srt_file.write(f"{caption['text']}\n\n")

            self._logging.info(f"Captions saved as SRT file: {output_file_path}")

        except Exception as e:
            self._logging.error("An error occurred while saving captions as SRT:")
            self._logging.exception(e)

    def get_video_title(self, video_url: str) -> str:
        try:
            video_info = YouTube(video_url)
            return video_info.title
        except Exception as e:
            self._logging.error("An error occurred while fetching video title:")
            self._logging.exception(e)
            return ""
