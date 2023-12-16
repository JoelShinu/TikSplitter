from pathlib import Path
from typing import List


def convertTagsToHashtags(tags: List[str]) -> str:
    return "#fyp " + " ".join(list(map(lambda tag: "#" + str(tag).replace(" ", ""), tags)))


class Video:
    def __init__(self, filename: Path, title: str, description: str, duration: int):
        self._filename = filename
        self._title = title
        self._description = description
        self._duration = duration

    def get_filename_as_string(self) -> str:
        return str(self._filename)

    def get_filename(self) -> Path:
        return self._filename

    def get_title(self) -> str:
        return self._title.strip()

    def get_raw_description(self) -> str:
        return self._description

    def get_optimised_description(self) -> str:
        tags = set(self._description.split(" "))
        return " ".join(tags)

    def get_duration(self) -> int:
        return self._duration
