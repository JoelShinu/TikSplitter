from typing import Iterable, Optional

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
    def videos(self) -> Iterable[YouTube]:
        return self.channel.videos

    @property
    def latest_video(self) -> YouTube:
        return next(iter(self.channel.videos))


class ChannelWatcher(ChannelClient):

    def __init__(self, channel: Channel):
        super().__init__(channel)



