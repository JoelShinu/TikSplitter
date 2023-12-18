from pathlib import Path
from typing import List

from tik_splitter.utils.utils import clean_string


def convertToHashtags(tags: List[str], author: str) -> str:
    return (
        "#fyp "
        + " ".join(list(map(lambda tag: "#" + str(tag).replace(" ", ""), tags)))
        + " #"
        + clean_string(author).replace("_", "")
    )


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


class SplitVideo(Video):
    def __init__(self, filename: Path, title: str, description: str, duration: int, part: int):
        super().__init__(filename, title, description, duration)
        self._part = part

    def get_part(self) -> int:
        return self._part

    def get_optimised_description(self) -> str:
        desc = super().get_optimised_description()
        return f"#part{self._part} " + desc


def convertVideoToSplitVideo(video: Video, part: int) -> SplitVideo:
    return SplitVideo(
        video.get_filename(),
        video.get_title() + f" (Part {part})",
        video.get_raw_description(),
        video.get_duration(),
        part,
    )
