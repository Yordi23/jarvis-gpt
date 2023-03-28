import openai
import os

openai.api_key = os.environ['API_KEY']
model_id = 'gpt-3.5-turbo'


def parse_chat_history(chat_history):
    parsed_chat_history = []
    for message in chat_history:
        parsed_chat_history.append({
            "role": message["sender"],
            "content": message["text"]
        })

    return parsed_chat_history


def send_message_to_gtp(chat_history):
    system_message = {"role": "system",
                      "content": "You are a helpful assistant."}
    parsed_chat_history = parse_chat_history(chat_history.values())
    messages = [system_message] + parsed_chat_history

    response = openai.ChatCompletion.create(
        model=model_id,
        messages=messages
    )

    print(messages)
    print('Tokens usage: ' + str(response['usage']))

    return response['choices'][0]['message']['content']
