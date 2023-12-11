from pathlib import Path


class TikTokVideo:
    def __init__(self, filename: Path, description: str):
        self._filename = filename
        self._description = description

    def getFilename(self) -> str:
        return str(self._filename)

    def getDescription(self) -> str:
        return self._description
