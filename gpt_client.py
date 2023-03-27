import openai
import os

API_KEY = os.environ['API_KEY']
openai.api_key = API_KEY
model_id = 'gpt-3.5-turbo'


def send_message_to_gtp(text):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[{"role": "user", "content": text}]
    )

    return response['choices'][0]['message']['content']
