import os
import re

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


def clean_string(input_string: str) -> str:
    # Remove invalid characters
    regex_string = re.sub(r'[^a-zA-Z0-9\s]', '', input_string)
    # Replace consecutive spaces with a single space
    regex_string = re.sub(r'\s+', ' ', regex_string)
    # Replace spaces with underscores
    regex_string = regex_string.replace(' ', '_')
    return regex_string


def get_sec(time_str: str) -> int:
    # Converts MM:SS to an integer value of seconds
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)
