# Python script for posting the final video to TikTok.
from tiktok_client import TiktokClient


class Poster:
    def __init__(self, client: TiktokClient):
        self._client = client
