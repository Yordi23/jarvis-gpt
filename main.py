import whisper
import pyttsx3

# Voice setup
engine = pyttsx3.init()
engine.setProperty('rate', 170)

voices = engine.getProperty('voices')
raul_voice = voices[1].id
sabina_voice = voices[3].id

engine.setProperty('voice', raul_voice)

# Whisper setup

print("Rendering text...")
model = whisper.load_model("medium")
result = model.transcribe("audio.mp3")

print("Done")
engine.say(result["text"])
engine.runAndWait()
