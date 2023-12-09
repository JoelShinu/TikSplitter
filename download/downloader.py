from pathlib import Path
from abc import ABC, abstractmethod
from pytube import YouTube


class Downloader(ABC):
    def __init__(self, output_path='videos'):
        self.output_path = Path(__file__).resolve().parent.parent / output_path

    @abstractmethod
    def download_video(self, url):
        pass


class YouTubeDownloader(Downloader):
    def download_video(self, url):
        try:
            output_directory = str(self.output_path)  # Convert Path to string
            output_directory_path = Path(output_directory)
            output_directory_path.mkdir(parents=True, exist_ok=True)

            youtube = YouTube(url)
            video_stream = youtube.streams.get_highest_resolution()

            print(f"Downloading YouTube video: {youtube.title}")
            video_stream.download(output_directory)
            print("Download Complete!")

        except Exception as e:
            print(f"An error occurred while downloading YouTube video: {e}")


if __name__ == "__main__":
    youtube_downloader = YouTubeDownloader()
    youtube_video_url = input("Enter the YouTube video URL: ")
    youtube_downloader.download_video(youtube_video_url)
