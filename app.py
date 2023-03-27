from flask import Flask, render_template, request, jsonify, send_file
import tempfile
import os
import whisper
import pyttsx3
import uuid


whisper_model = whisper.load_model("medium")
voice_engine = pyttsx3.init()
voice_engine.setProperty('rate', 170)

app = Flask(__name__)
chat_history = {}


def generate_uuid():
    return uuid.uuid1()


def generate_temp_path(filename):
    temp_dir = tempfile.mkdtemp()
    return os.path.join(temp_dir, filename)


def generate_audio_from_text(text: str):
    voices = voice_engine.getProperty('voices')
    raul_voice = voices[1].id
    sabina_voice = voices[3].id
    voice_engine.setProperty('voice', raul_voice)

    save_path = generate_temp_path('temp_transcription.wav')
    voice_engine.save_to_file(text, save_path)
    voice_engine.runAndWait()

    return save_path


def insert_new_message(text, sender, audio_path=None):
    id = str(generate_uuid())

    message = {"id": id, "sender": sender,
               "text": text, "audio_path": audio_path}
    chat_history[id] = message

    return {"id": message["id"], "sender": message["sender"], "text": message["text"], }


@app.route('/')
def chat():
    return render_template('chat.html', chat_history=chat_history.values())


@app.route('/get_audio/<id>', methods=['GET'])
def get_audio(id):
    message = chat_history[id]

    return send_file(message["audio_path"], mimetype="audio/wav")


@app.route('/send_message', methods=['POST'])
def send_message():
    text = request.json['message']

    insert_new_message(text, "user")

    # Get bot response somewhere
    bot_response = text
    save_path = generate_audio_from_text(bot_response)

    response_message = insert_new_message(bot_response, "bot", save_path)
    print(response_message["id"])

    return jsonify(success=True, response_messages=[response_message])


@app.route('/send_audio', methods=['POST'])
def send_audio():
    record_path = generate_temp_path('temp_record.wav')

    wav_file = request.files['audio']
    wav_file.save(record_path)
    transcribe_text = whisper_model.transcribe(record_path)["text"]

    bot_response = transcribe_text
    save_path = generate_audio_from_text(bot_response)

    transcribe_message = insert_new_message(transcribe_text, "user")
    response_message = insert_new_message(transcribe_text, "bot", save_path)

    return jsonify(success=True, response_messages=[transcribe_message, response_message, ])


if __name__ == '__main__':
    app.run(debug=True)
