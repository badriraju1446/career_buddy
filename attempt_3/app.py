# backend/app.py

from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# 🔑 Place your Gemini API key here
GEMINI_API_KEY = "AIzaSyCQST6IsSyYhSy70sfM2jPeGBmEXXe35-Q"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# System Prompt (the bot's brain)
SYSTEM_PROMPT = """
You are CareerBuddy, the official assistant of a career advisor web application...
<<< paste the full system prompt I gave you earlier >>>
"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("user_message")
    page_context = data.get("page_context", {})

    # Combine context into prompt
    full_prompt = f"""
{SYSTEM_PROMPT}

Current Page Context: {page_context}
Student Message: {user_message}
"""

    # Send to Gemini
    response = model.generate_content(full_prompt)

    return jsonify({"reply": response.text})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
