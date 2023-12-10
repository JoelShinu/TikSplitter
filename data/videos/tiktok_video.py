class TikTokVideo:
    def __init__(self, filename: str, description: str):
        self._filename = filename
        self._description = description

    def getFilename(self) -> str:
        return self._filename

    def getDescription(self) -> str:
        return self._description