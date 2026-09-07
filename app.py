from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-сюда-ключ")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "сюда-ключ")

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def ask_deepseek(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }
    resp = requests.post(DEEPSEEK_URL, json=data, headers=headers)
    return resp.json()["choices"][0]["message"]["content"]

def ask_gemini(prompt):
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    resp = requests.post(GEMINI_URL, json=payload)
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def synthesize(d, g):
   return (
    "**DeepSeek:** " + d + "\n\n" + "**Gemini:** " + g
)
@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    model = data.get("model", "both")

    if model == "deepseek":
        answer = ask_deepseek(question)
    elif model == "gemini":
        answer = ask_gemini(question)
    else:
        d = ask_deepseek(question)
        g = ask_gemini(question)
        answer = synthesize(d, g)

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
