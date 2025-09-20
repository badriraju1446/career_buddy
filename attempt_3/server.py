from flask import Flask, request, jsonify, render_template
import requests
import os


app = Flask(__name__)

# Gemini API Key (set your key here or use environment variable)
GEMINI_API_KEY = os.environ.get("AIzaSyDhegglS5udhXzWK39Tb3s1oRtvnvMmkCM", "AIzaSyDhegglS5udhXzWK39Tb3s1oRtvnvMmkCM")



# Homepage route serving chatbot UI
@app.route("/")
def home():
    return render_template("index.html")


# Chat endpoint using Gemini REST API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("user_message", "Hello")
    page_context = data.get("page_context", {})

    prompt = f"""
You are CareerBuddy, the chatbot for a career advisor web app.\n\nPage Context: {page_context}\nStudent Message: {user_message}
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        result = r.json()
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        reply = f"Error: {str(e)}"
    return jsonify({"reply": reply})


# Optionally, remove or update /list-models if not needed

if __name__ == "__main__":
    print("Visit http://127.0.0.1:5000/list-models to see available models in the console log.")
    app.run(debug=True, port=5000)
