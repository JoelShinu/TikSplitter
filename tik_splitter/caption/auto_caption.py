from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse, parse_qs

from pytube import Caption
from youtube_transcript_api import YouTubeTranscriptApi

from tik_splitter.configs.logging_config import configure_logging


class AutoCaptioner:
    def __init__(self, output_path: Path):
        self.output_path = Path(output_path)
        self._logging = configure_logging()

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
            self._logging.error(f"An error occurred while fetching captions: {e}")
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
            self._logging.error(f"An error occurred while extracting video ID: {e}")
            return None

    def save_captions_as_srt(self, captions: Iterable[Caption], output_filename: str):
        try:
            output_file_path = self.output_path / (output_filename + ".srt")

            with open(output_file_path, "w", encoding="utf-8") as srt_file:
                for i, caption in enumerate(captions, start=1):
                    srt_file.write(f"{i}\n")
                    srt_file.write(f"{caption['start']} --> {caption['start'] + caption['duration']}\n")
                    srt_file.write(f"{caption['text']}\n\n")

            self._logging.warning(f"Captions saved as SRT file: {output_file_path}")

        except Exception as e:
            self._logging.error(f"An error occurred while saving captions as SRT: {e}")

    def save_captions_as_txt(self, captions: Iterable[Caption], output_filename: str):
        try:
            output_file_path = self.output_path / (output_filename + ".txt")

            with open(output_file_path, 'w', encoding='utf-8') as txt_file:
                for i, caption in enumerate(captions, start=1):
                    txt_file.write(f"{i}. {caption['text']}\n")

            self._logging.warning(f"Captions saved as TXT file: {output_file_path}")

        except Exception as e:
            self._logging.error(f"An error occurred while saving captions as TXT: {e}")
