from pathlib import Path
import zipfile
import requests
import subprocess
import os


def ffmpeg_install_windows():
    try:
        ffmpeg_url = "https://github.com/GyanD/codexffmpeg/releases/download/6.0/ffmpeg-6.0-full_build.zip"
        ffmpeg_zip_filename = Path("ffmpeg.zip")
        ffmpeg_extracted_folder = Path("ffmpeg")

        # Check if ffmpeg.zip already exists
        if ffmpeg_zip_filename.exists():
            ffmpeg_zip_filename.unlink()

        # Download FFmpeg
        r = requests.get(ffmpeg_url)
        with ffmpeg_zip_filename.open("wb") as f:
            f.write(r.content)

        # Check if the extracted folder already exists
        if ffmpeg_extracted_folder.exists():
            # Remove existing extracted folder and its contents
            for item in ffmpeg_extracted_folder.glob("**/*"):
                item.unlink()
            ffmpeg_extracted_folder.rmdir()

        # Extract FFmpeg
        with zipfile.ZipFile(ffmpeg_zip_filename, "r") as zip_ref:
            zip_ref.extractall()
        ffmpeg_zip_filename.unlink()

        # Rename and move files
        (ffmpeg_extracted_folder / f"{ffmpeg_extracted_folder}-6.0-full_build").rename(ffmpeg_extracted_folder)
        for file in (ffmpeg_extracted_folder / "bin").iterdir():
            file.rename(Path(".") / file.name)
        (ffmpeg_extracted_folder / "bin").rmdir()
        for file in (ffmpeg_extracted_folder / "doc").iterdir():
            file.unlink()
        for file in (ffmpeg_extracted_folder / "presets").iterdir():
            file.unlink()
        (ffmpeg_extracted_folder / "presets").rmdir()
        (ffmpeg_extracted_folder / "doc").rmdir()
        (ffmpeg_extracted_folder / "LICENSE").unlink()
        (ffmpeg_extracted_folder / "README.txt").unlink()
        ffmpeg_extracted_folder.rmdir()

        print("FFmpeg installed successfully! Please restart your computer and then re-run the program.")
    except Exception as e:
        print(
            "An error occurred while trying to install FFmpeg. Please try again. Otherwise, please install FFmpeg manually and try again."
        )
        print(e)
        exit()


def ffmpeg_install_linux():
    try:
        subprocess.run(
            ["sudo", "apt", "install", "ffmpeg"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception as e:
        print(
            "An error occurred while trying to install FFmpeg. Please try again. Otherwise, please install FFmpeg manually and try again."
        )
        print(e)
        exit()
    print("FFmpeg installed successfully! Please re-run the program.")
    exit()


def ffmpeg_install_mac():
    try:
        subprocess.run(
            ["brew", "install", "ffmpeg"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        print(
            "Homebrew is not installed. Please install it and try again. Otherwise, please install FFmpeg manually and try again."
        )
        exit()
    print("FFmpeg installed successfully! Please re-run the program.")
    exit()


def ffmpeg_install():
    try:
        # Try to run the FFmpeg command
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as e:
        # Check if there's ffmpeg.exe in the current directory
        if Path("./ffmpeg.exe").exists():
            print(
                "FFmpeg is installed on this system! If you are seeing this error for the second time, restart your computer."
            )
        print("FFmpeg is not installed on this system.")
        resp = input("We can try to automatically install it for you. Would you like to do that? (y/n): ")
        if resp.lower() == "y":
            print("Installing FFmpeg...")
            if os.name == "nt":
                ffmpeg_install_windows()
            elif os.name == "posix":
                ffmpeg_install_linux()
            elif os.name == "mac":
                ffmpeg_install_mac()
            else:
                print("Your OS is not supported. Please install FFmpeg manually and try again.")
                exit()
        else:
            print("Please install FFmpeg manually and try again.")
            exit()
    except Exception as e:
        print("Some error??!")
        print(e)
    return None
