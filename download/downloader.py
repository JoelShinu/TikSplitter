import os
from pytube import YouTube


def download_youtube(url, output_path="videos"):
    try:
        output_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", output_path
        )
        os.makedirs(output_directory, exist_ok=True)

        youtube = YouTube(url)
        video_stream = youtube.streams.get_highest_resolution()

        print(f"Downloading: {youtube.title}")
        video_stream.download(output_directory)
        print("Download Complete!")

    except Exception as e:
        print(f"An Error has occurred: {e}")
