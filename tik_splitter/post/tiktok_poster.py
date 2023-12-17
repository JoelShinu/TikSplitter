from datetime import datetime as dt
from datetime import timedelta as td
from typing import List

from selenium.webdriver.chrome.options import Options
from tiktok_uploader.upload import upload_video

from tik_splitter.entities.video import Video
from tik_splitter.utils.logging_config import configure_logging


class Poster:
    def __init__(self, session_id: str, headless: bool = True, last_uploaded: dt = None):
        self._session_id = session_id
        self._headless = headless
        self._options = Options()
        self._options.add_argument("start-maximized")
        self._last_uploaded = last_uploaded
        self._logger = configure_logging("poster")

    def get_last_uploaded(self) -> dt:
        return self._last_uploaded

    def upload_videos(self, *videos: Video) -> List[Video]:
        failed_uploads = []

        for video in videos:
            if len(failed_uploads) != 0:
                failed_uploads.append(video)
                continue

            success = self.upload(video)
            if not success:  # retry once if failed upload
                self._logger.warning(f"Failed to post: [{video.get_title()}], retrying...")

                success = self.upload(video)
                if not success:
                    failed_uploads.append(video)
                    self._logger.error(f"Failed to post: [{video.get_title()}] again. Quitting...")
                    continue

            self._logger.info(f"Successfully posted: [{video.get_title()}]")

        return failed_uploads

    def upload(self, video: Video) -> bool:
        now = dt.utcnow()
        upload_time = None

        if self._last_uploaded is not None:
            # if last post happened over 10 minutes ago then post now, otherwise schedule for 25 minutes from now
            if self._last_uploaded < now:
                diff = now - self._last_uploaded
                diff_minutes = int(diff.total_seconds() / 60)
                upload_time = None if diff_minutes > 10 else now + td(minutes=25)
            # if videos are already scheduled to be posted later, then schedule for 25 minutes later than the last video
            else:
                upload_time = self._last_uploaded + td(minutes=25)

        failed_uploads = upload_video(
            filename=video.get_filename_as_string(),
            description=video.get_optimised_description(),
            sessionid=self._session_id,
            headless=self._headless,
            options=self._options if self._headless is False else None,
            schedule=upload_time,
        )

        success = len(failed_uploads) == 0
        if success:
            self._last_uploaded = now if upload_time is None else upload_time

        return success
