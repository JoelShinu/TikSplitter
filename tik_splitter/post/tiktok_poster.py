from datetime import datetime as dt, timedelta as td

from tiktok_uploader.upload import upload_video

from tik_splitter.entities.tiktok_video import TikTokVideo


class Poster:
    def __init__(self, sessionId: str):
        self._sessionId = sessionId
        self._lastUploaded: dt | None = None

    def upload_videos(self, *videos: TikTokVideo):
        for video in videos:
            success = self.upload(video)
            if not success:  # retry once if failed upload
                self.upload(video)

    def upload(self, video: TikTokVideo) -> bool:
        now = dt.utcnow()
        uploadTime = None

        if self._lastUploaded is not None:
            # if last post happened over 10 minutes ago then post now, otherwise schedule for 25 minutes from now
            if self._lastUploaded < now:
                diff = now - self._lastUploaded
                diffMinutes = int(diff.total_seconds() / 60)
                uploadTime = None if diffMinutes > 10 else now + td(minutes=25)
            # if videos are already scheduled to be posted later, then schedule for 25 minutes later than the last video
            else:
                uploadTime = self._lastUploaded + td(minutes=25)

        failedUploads = upload_video(
            filename=video.getFilename(),
            description=video.getDescription(),
            sessionid=self._sessionId,
            headless=True,
            schedule=uploadTime
        )

        self._lastUploaded = now if uploadTime is None else uploadTime
        return len(failedUploads) == 0
