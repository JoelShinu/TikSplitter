# Python script for posting the final video to TikTok.
from tiktok_uploader.upload import upload_video

from videos.tiktok_video import TikTokVideo


class Poster:
    def __init__(self, sessionId: str):
        self._sessionId = sessionId

    def upload(self, video: TikTokVideo) -> bool:
        failedUploads = upload_video(filename=video.getFilename(),
                                     description=video.getDescription(),
                                     sessionid=self._sessionId,
                                     headless=True)

        return len(failedUploads) == 0
