from datetime import datetime as dt
from datetime import timedelta as td

from tiktok_uploader.upload import upload_video

from tik_splitter.entities.video import Video


class Poster:
    def __init__(self, session_id: str, headless: bool = True):
        self._session_id = session_id
        self._headless = headless
        self._last_uploaded: dt | None = None

    def upload_videos(self, *videos: Video):
        for video in videos:
            success = self.upload(video)
            if not success:  # retry once if failed upload
                self.upload(video)

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
            schedule=upload_time,
        )

        self._last_uploaded = now if upload_time is None else upload_time
        return len(failed_uploads) == 0
