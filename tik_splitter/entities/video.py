from pathlib import Path


class Video:
    def __init__(self, filename: Path, title: str, description: str):
        self._filename = filename
        self._title = title
        self._description = description

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
