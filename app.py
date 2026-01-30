#!/usr/bin/env python3
"""
Watch Insurance Advisor - Web Application
A beautiful web-based chatbot for watch insurance decisions.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the system prompt
PROMPT_FILE = Path(__file__).parent / "watch_insurance_prompt.txt"


def load_system_prompt() -> str:
    """Load the system prompt from file."""
    try:
        with open(PROMPT_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "You are a helpful watch insurance advisor."


SYSTEM_PROMPT = load_system_prompt()


@app.route("/")
def index():
    """Serve the main chat interface."""
    # Reset conversation on page load
    session["messages"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages."""
    data = request.json
    user_message = data.get("message", "").strip()
    
    # Initialize or get conversation history
    if "messages" not in session:
        session["messages"] = []
    
    messages = session["messages"]
    
    # If this is the first message, get the opening
    if not messages and not user_message:
        # Get initial greeting
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT}
                ],
                temperature=0.8,
                max_tokens=400
            )
            assistant_message = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_message})
            session["messages"] = messages
            return jsonify({"response": assistant_message})
        except Exception as e:
            return jsonify({"response": f"I apologize, but I'm having trouble connecting. Please try again.", "error": str(e)})
    
    # Add user message
    if user_message:
        messages.append({"role": "user", "content": user_message})
    
    # Get AI response
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.8,
            max_tokens=500
        )
        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        session["messages"] = messages
        return jsonify({"response": assistant_message})
    except Exception as e:
        return jsonify({"response": "I apologize, but I encountered an issue. Please try again.", "error": str(e)})


@app.route("/reset", methods=["POST"])
def reset():
    """Reset the conversation."""
    session["messages"] = []
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
