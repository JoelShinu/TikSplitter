import os

from dotenv import dotenv_values, find_dotenv, load_dotenv


def get_env_details(*keys: str) -> dict[str, str | None] | str | None:
    """
    Attempts to find env file and retrieves specified key: value pairs

    Returns an empty dict if no variables set in env file

    Returns a single value if only one key specified

    Returns all set env variables by default if no keys specified
    """

    envPath = find_dotenv()
    isEnvSet = load_dotenv(envPath)

    if not isEnvSet:
        return dict()

    if len(keys) == 0:
        return dotenv_values(envPath)

    if len(keys) == 1:
        return os.getenv(keys[0])

    return {key: os.getenv(key) for key in keys}
