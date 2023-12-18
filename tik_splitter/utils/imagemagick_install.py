import os
import requests
from pathlib import Path


def install_imagemagick_windows():
    try:
        imagemagick_url = "https://download.imagemagick.org/archive/binaries/ImageMagick-6.9.13-1-Q8-x64-dll.exe"
        imagemagick_exe_filename = Path("ImageMagick-6.9.13-1-Q8-x64-dll.exe")
        imagemagick_install_folder = Path("ImageMagick")

        # Check if the downloaded installer file already exists
        if imagemagick_exe_filename.exists():
            imagemagick_exe_filename.unlink()

        # Download ImageMagick
        r = requests.get(imagemagick_url)
        with imagemagick_exe_filename.open("wb") as f:
            f.write(r.content)

        # Run the installer silently
        os.system(f"{str(imagemagick_exe_filename)} /SILENT")

        # Wait for the installation to complete
        input("Please wait for the installation to complete, then press Enter to continue...")

        print("ImageMagick installed successfully!")
    except Exception as e:
        print(
            "An error occurred while trying to install ImageMagick. Please try again. Otherwise, please install ImageMagick manually and try again."
        )
        print(e)
        exit()


def install_imagemagick():
    try:
        # Check if ImageMagick is already installed
        os.system("convert -version")
        print("ImageMagick is already installed on this system!")
        exit()
    except FileNotFoundError as e:
        # ImageMagick is not installed, offer to download and install
        resp = input("ImageMagick is not installed on this system. Would you like to download and install it? (y/n): ")
        if resp.lower() == "y":
            print("Downloading and installing ImageMagick...")
            install_imagemagick_windows()
        else:
            print("Please install ImageMagick manually and try again.")
            exit()
