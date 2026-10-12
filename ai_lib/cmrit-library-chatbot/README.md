# CMRIT Library Chatbot

A small Flask web application that answers common questions about the CMR Institute of Technology library.

## Setup

```bash
cd cmrit-library-chatbot
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

For PowerShell from the `ai_lib` directory:

```powershell
cd .\cmrit-library-chatbot
python app.py
```

The API also exposes `GET /health` and validates chat requests at `POST /chat`.

## Test

```bash
python -m unittest discover -s tests
```

## Project structure

- `app.py` - Flask application and chat API
- `library_data.py` - Sample library information
- `chatbot.py` - Response logic
- `templates/index.html` - Chatbot webpage
- `static/style.css` - Website styling
- `static/script.js` - Browser chat functionality
