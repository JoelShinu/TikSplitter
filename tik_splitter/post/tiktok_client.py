from requests import Session

from tik_splitter.configs.utils import get_env_details


class TiktokClient:
    def __init__(self):
        env = get_env_details("API_KEY", "SECRET_KEY")
        self._session = self._login(api=env["API_KEY"], secret=env["SECRET_KEY"])

    def _login(self, api: str, secret: str) -> Session:
        # login to TikTok client and return the session
        pass
