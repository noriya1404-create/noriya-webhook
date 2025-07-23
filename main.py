from flask import Flask, request
from transformers import pipeline
import requests
import os

app = Flask(__name__)
generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    user_input = data['message']['text']
    result = generator(user_input, max_length=200, do_sample=True, temperature=0.8)
    answer = result[0]['generated_text']

    token = os.environ.get("BOT_TOKEN", "توکن_مثالی")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": answer})
    return "ok"
