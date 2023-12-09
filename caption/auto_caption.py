import os
import moviepy.editor as mp
import speech_recognition as sr


def transcribe_audio(video_path):
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_path = "transcribed_audio.wav"
    audio_clip.write_audiofile(audio_path)
    audio_clip.close()

    speech_recogniser = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = speech_recogniser.record(source)

    try:
        text = speech_recogniser.recognize_google_cloud(audio)
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition Service: {e}")
    except sr.WaitTimeoutError:
        print("Timeout Error")
    finally:
        os.remove(audio_path)

    return None


def auto_caption(video_file, output_file="auto_caption.txt"):
    video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videos', video_file)
    captions = transcribe_audio(video_path)

    if captions:
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
        with open(output_path, 'w') as file:
            file.write(captions)
        print(f"Auto-caption save to: {output_file}")
    else:
        print("Auto-captioning failed.")
