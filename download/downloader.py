import os
from pytube import YouTube


class YouTubeDownloader:
    def __init__(self, output_path='videos'):
        self.output_path = output_path

    def download_video(self, url):
        try:
            output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', self.output_path)
            os.makedirs(output_directory, exist_ok=True)

            youtube = YouTube(url)
            video_stream = youtube.streams.get_highest_resolution()

            print(f"Downloading: {youtube.title}")
            video_stream.download(output_directory)
            print("Download Complete!")

        except Exception as e:
            print(f"An Error has occurred: {e}")


if __name__ == "__main__":
    downloader = YouTubeDownloader()
    video_url = input("Enter the YouTube video URL: ")
    downloader.download_video(video_url)
