"""
Flask app: upload a .txt file, summarize with Groq, return JSON for the front end.
Run with: python app.py
"""

from __future__ import annotations

import logging
import os
import threading
import webbrowser
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from groq import Groq
from groq import GroqError
from werkzeug.exceptions import RequestEntityTooLarge

_PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(_PROJECT_ROOT / ".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Limits (see Instructions.md optional section)
MAX_UPLOAD_BYTES = 256 * 1024
MAX_CHARS_FOR_MODEL = 48_000

DEFAULT_MODEL = "llama-3.1-8b-instant"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES


def _allowed_txt(filename: str | None) -> bool:
    if not filename or "." not in filename:
        return False
    return filename.rsplit(".", 1)[1].lower() == "txt"


def _read_text_from_storage(file_storage) -> Tuple[str | None, str | None]:
    """Returns (text, error_message)."""
    if not file_storage or file_storage.filename == "":
        return None, "No file was uploaded."

    if not _allowed_txt(file_storage.filename):
        return None, "Only .txt files are allowed."

    raw = file_storage.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES:
        return None, "That file is too large for this app."

    if not raw.strip():
        return None, "That file is empty."

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "Could not read the file as UTF-8 text. Save it as UTF-8 and try again."

    text = text.strip()
    if not text:
        return None, "That file is empty."

    if len(text) > MAX_CHARS_FOR_MODEL:
        text = text[:MAX_CHARS_FOR_MODEL]

    return text, None


def _summarize(text: str) -> Tuple[str | None, str | None]:
    """Returns (summary, error_message)."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None, "Missing GROQ_API_KEY. Copy .env.example to .env and add your key."

    model = os.environ.get("GROQ_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL

    client = Groq(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You summarize user-supplied text clearly and concisely. "
                        "Preserve important facts. Use plain paragraphs; no markdown unless the "
                        "source already uses it."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n\n{text}",
                },
            ],
            temperature=0.3,
        )
    except GroqError as exc:
        logger.warning("Groq API error: %s", type(exc).__name__)
        return None, "The summarization service returned an error. Check your API key and try again."
    except OSError:
        logger.exception("Network error calling Groq")
        return None, "Could not reach the summarization service. Check your internet connection."

    choice = completion.choices[0].message
    summary = (choice.content or "").strip()
    if not summary:
        return None, "The model returned an empty summary. Try again with different text."

    return summary, None


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/summarize")
def api_summarize():
    if "file" not in request.files:
        return jsonify({"error": "No file field in the request."}), 400

    text, err = _read_text_from_storage(request.files["file"])
    if err:
        return jsonify({"error": err}), 400

    summary, err = _summarize(text)
    if err:
        return jsonify({"error": err}), 502

    return jsonify({"original": text, "summary": summary})


@app.errorhandler(RequestEntityTooLarge)
def handle_too_large(_e):
    return jsonify({"error": "That file is too large for this app."}), 413


@app.errorhandler(413)
def handle_413(_e):
    return jsonify({"error": "That file is too large for this app."}), 413


def _open_browser() -> None:
    webbrowser.open("http://127.0.0.1:5000/")


if __name__ == "__main__":
    # Single process: avoid reloader so the browser opens once and behavior is predictable.
    threading.Timer(1.0, _open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
