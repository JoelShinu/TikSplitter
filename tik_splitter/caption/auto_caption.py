import logging
import os

import speech_recognition as sr


def transcribe_wav(audio_path, output_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_sphinx(audio)
        save_path = os.path.join(os.getcwd(), output_file)

        with open(save_path, "w") as file:
            file.write(text)

        logging.info(f"Transcription saved to: {output_file}")
        return text
    except sr.UnknownValueError:
        logging.warning("Speech recognition could not recognize audio")
    except sr.RequestError as e:
        logging.warning(f"Could not request results from Google Speech Recognition service: {e}")
    except sr.WaitTimeoutError:
        logging.warning("Timeout Error")

    return None
