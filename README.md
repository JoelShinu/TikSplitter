# YouTube to TikTok Video Converter

## 🎥 Overview

This Python-based project serves as a YouTube to TikTok video converter. It allows users to input a YouTube URL, download the video, combine it with a sample video, and generate segmented clips suitable for posting on TikTok. Before using the project, ensure that you have the required prerequisites installed and configured.

## 📋 Prerequisites

1. **Python**: Make sure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **ffmpeg Executable**: Download the ffmpeg executable from the official website: [ffmpeg Download](https://ffmpeg.org/download.html). Add the directory containing the ffmpeg executable to your system's PATH.

3. **ImageMagick**: Download the ImageMagick executable and update the policy.xml file. Change the rights to "read, write" for the policy domain="Undefined". Set the location of the ImageMagick binary executable in the `Merger` class of the project.

   **Note**: Ensure that both ffmpeg and ImageMagick executables are accessible from the command line.

## 💾 Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/youtube-to-tiktok-converter.git
   
2. Install Dependencies:

   ```bash
   To be added...

3. Run the program:

   ```bash
   To be added...
   
## 🔧 Configuration

To be added...
   
## Video Output
The program will download the specified YouTube video, combine it with a sample video, and generate segmented clips suitable for TikTok. The output files will be available in the output directory.

To be added... (.mp4)

## 📺 How to Use

Note that the downloaded and merged videos will be in the folder `videos` and `merged` directories respectively. The folder structure is as follows:
```
data  
  ├── captions  
  ├── merged  
  ├── sample
  └── videos 
```
The `videos` folder holds the downloaded Youtube clips, the `sample` folder has the sample videos and the `merged` folder contains the output video which will be the Youtube and sample video.

## 🤝 Contributing
If you want to contribute to this project, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

## 🤔 WIP
Here are some ideas for contributions:

- Improvement #1

## ⚠️ Disclaimer
Please comply with the terms of service of YouTube and TikTok APIs. Respect content creators' rights and platform policies.

## 📜 License
This project is licensed under the MIT License.