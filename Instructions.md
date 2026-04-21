## Overview

This project is a Python Flask web application that allows users to upload a `.txt` file and receive a summarized version of its contents using the Groq LLM API.

The application focuses on integrating file handling, backend processing, and AI-powered text summarization into a simple, user-friendly interface.

## Core Functionalities

1. **File upload** — Users upload a `.txt` file to the application.
2. **Text extraction** — The application reads and validates the uploaded file (plain text only).
3. **Text summarization** — The application sends the text to Groq; the model returns a summarized version.
4. **Display results** — The original text appears in one scrollable area; the summary appears in another.

## Technical Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **API:** [Groq](https://console.groq.com/) LLM API (OpenAI-compatible HTTP API)

## Project Structure

```text
capstoneproject/
├── app.py                 # Flask app: routes, upload handling, Groq client calls
├── requirements.txt     # Pinned dependencies (flask, requests or groq SDK, python-dotenv, etc.)
├── .env                 # Local secrets (NOT committed): GROQ_API_KEY
├── .env.example         # Template showing required variables (safe to commit)
├── .gitignore           # Ignore .env, __pycache__, venv/, uploads/, etc.
├── Instructions.md      # This document
├── README.md            # Short project intro + link to setup steps
├── static/              # CSS, client JS, optional assets
│   ├── style.css
│   └── script.js
├── templates/           # Jinja2 HTML pages
│   └── index.html
└── uploads/             # Optional: temporary storage for uploads (gitignored)
```


## Setup Instructions

### Prerequisites

- **Python 3.10+** (or the version your instructor requires) installed and on your `PATH`.
- A **Groq account** and an **API key** from the [Groq Console](https://console.groq.com/).

### 1. Clone or open the project

Open a terminal in the project root folder (`capstoneproject`).

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

After the virtual environment is active:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*(Create `requirements.txt` when you add packages; typical entries include `flask`, `python-dotenv`, and either the official `groq` client or `requests` if you call the REST API directly.)*

### 4. Configure environment variables

1. Copy `.env.example` to `.env` (once you add those files).
2. Set your key, for example:

   ```text
   GROQ_API_KEY=your_key_here
   ```

3. In code, read `os.environ["GROQ_API_KEY"]` (and fail clearly if it is missing).

Never commit `.env`.

### 5. Run the application

From the project root, with the virtual environment active:

```bash
flask run
```

Or, if your entry point uses `app.run()` for local development:

```bash
python app.py
```

Open the URL shown in the terminal (often `http://127.0.0.1:5000`) in a browser.

### 6. Verify behavior

- Upload a small `.txt` file and confirm original + summary areas update.
- Confirm non-`.txt` uploads are rejected with a clear message.
- Confirm errors (network failure, invalid key, empty file) show a user-friendly error instead of a raw stack trace in production.