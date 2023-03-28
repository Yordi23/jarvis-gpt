import uuid
import tempfile
import os
import pyttsx3
import whisper

from enum import Enum

voice_engine = pyttsx3.init()
voice_engine.setProperty('rate', 175)
voices = voice_engine.getProperty('voices')
raul_voice = voices[1].id
sabina_voice = voices[3].id

whisper_model = whisper.load_model("medium")


class Roles(Enum):
    USER = "user"
    ASSISTANT = "assistant"


def generate_uuid():
    return uuid.uuid1()


def generate_temp_path(filename):
    temp_dir = tempfile.mkdtemp()
    return os.path.join(temp_dir, filename)


def generate_audio_from_text(text: str, voice=raul_voice):
    voice_engine.setProperty('voice', voice)

    save_path = generate_temp_path('temp_transcription.wav')
    voice_engine.save_to_file(text, save_path)
    voice_engine.runAndWait()

    return save_path


def transcribe_audio(path):
    return whisper_model.transcribe(path)["text"]
