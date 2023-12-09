import os

from dotenv import load_dotenv, find_dotenv, dotenv_values


def get_env_details(*keys: str) -> dict[str, str | None]:
    """
    Attempts to find env file and retrieves specified key: value pairs

    Returns an empty dict if no variables set in env file

    Returns all set env variables by default if no keys specified
    """

    envPath = find_dotenv()
    isEnvSet = load_dotenv(envPath)

    if not isEnvSet:
        return dict()

    if len(keys) == 0:
        return dotenv_values(envPath)

    return {key: os.getenv(key) for key in keys}

