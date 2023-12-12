import asyncio
from typing import Optional

from pytube import Channel, YouTube


class ChannelClient:
    def __init__(self, channel: Channel):
        self.channel = channel

        self.previous_latest_video: Optional[YouTube] = None

    def is_new_video(self) -> bool:
        return self.latest_video != self.previous_latest_video

    def get_new_video(self) -> Optional[YouTube]:
        if self.is_new_video:
            self.previous_latest_video = self.latest_video
            return self.latest_video

        else:
            return None

    @property
    def latest_video(self) -> YouTube:
        return next(iter(self.channel.videos))


class ChannelWatcher(ChannelClient):
    def __init__(self, channel: Channel, timeout: int = 3600):
        super().__init__(channel)

        # in seconds
        self.timeout = timeout

    async def watch_channel(self):
        while True:
            video: YouTube = self.get_new_video()

            if video:
                yield video

            # sleep for the given timeout, before checking youtube again
            await asyncio.sleep(self.timeout)
