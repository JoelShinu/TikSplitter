from tik_splitter.entities.username import Username
from tik_splitter.utils.utils import get_env_details


class Account:
    def __init__(self, username: Username):
        self._username = username

    def get_user(self) -> Username:
        return self._username

    def get_user_as_string(self) -> str:
        return self._username.value

    def get_session_id(self) -> str:
        return get_env_details(f"{self._username.value}_SESSION_ID")
