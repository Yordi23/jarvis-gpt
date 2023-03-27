from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, send_file
from gpt_client import send_message_to_gtp
from helpers import generate_audio_from_text, generate_temp_path, generate_uuid, transcribe_audio


app = Flask(__name__)
chat_history = {}


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

    bot_response = send_message_to_gtp(text)
    save_path = generate_audio_from_text(bot_response)

    response_message = insert_new_message(bot_response, "bot", save_path)

    return jsonify(success=True, response_messages=[response_message])


@app.route('/send_audio', methods=['POST'])
def send_audio():
    audio_path = generate_temp_path('temp_record.wav')

    wav_file = request.files['audio']
    wav_file.save(audio_path)
    transcribed_text = transcribe_audio(audio_path)

    bot_response = send_message_to_gtp(transcribed_text)
    response_audio_path = generate_audio_from_text(bot_response)

    transcribe_message = insert_new_message(transcribed_text, "user")
    response_message = insert_new_message(
        bot_response, "bot", response_audio_path)

    return jsonify(success=True, response_messages=[transcribe_message, response_message, ])


if __name__ == '__main__':
    app.run(debug=True)
