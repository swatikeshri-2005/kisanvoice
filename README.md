# KisanVoice 🌾

A Hindi-first bilingual agricultural voice-assistant starter project with Bengali support. The repository includes a Streamlit interface, FastAPI backend, small local agriculture FAQ dataset, configurable Gnani AI STT/TTS adapters, safe fallback responses, and basic tests.

> **Important:** The Gnani integration is a configurable adapter, not a claim that the sample request format matches every Gnani API product/account. Before using live speech, confirm endpoint URLs, authentication, accepted language codes, request fields, and response schema in the documentation supplied with your Gnani account. Update `backend/speech_to_text.py` and `backend/text_to_speech.py` if needed.

## Features

- Hindi and Bengali language selector
- Text-based agricultural question input
- Audio upload and configurable STT call
- FAQ retrieval with source labels and conservative fallback
- Configurable TTS call and in-browser audio playback
- FastAPI endpoints for health, answer, transcription, and speech generation
- Unit tests for both languages and fallback behavior

## Requirements

- Python 3.10+ (Python 3.11 recommended)
- VS Code
- Gnani API credentials and API documentation for live STT/TTS (optional for the local FAQ demo)

## Setup in VS Code

### 1. Open the project

Extract the ZIP, then open the `KisanVoice` folder in VS Code.

### 2. Create a virtual environment

**Windows PowerShell**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Gnani API

Copy `.env.example` to `.env`. Add your key and the exact STT/TTS endpoints from your official Gnani documentation.

Do not upload `.env` to GitHub. The included `.gitignore` excludes it.

The example adapter assumes:
- STT accepts a multipart audio file and a language field.
- TTS accepts JSON with `text` and `language`.
- Authentication can be sent in a configurable header.
- TTS may return audio bytes or base64 audio in JSON.

These are configurable assumptions only. If your API uses another payload, token method, voice field, or response structure, adapt the two integration modules accordingly.

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

The local FAQ and text-question workflow work without Gnani credentials. Live STT/TTS will show a clear setup error until configured.

### 5. Run the API separately (optional)

Open another terminal in the project folder:
```bash
uvicorn backend.api:app --reload
```

Then open `http://127.0.0.1:8000/docs` to try the API. Health endpoint: `http://127.0.0.1:8000/health`.

### 6. Run tests

```bash
pytest -q
```

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/answer` | Retrieve a grounded FAQ answer |
| POST | `/transcribe` | Send an audio upload to configured STT |
| POST | `/speak` | Send text to configured TTS |

Example `/answer` body:
```json
{
  "question": "धान की पत्तियाँ पीली क्यों हो रही हैं?",
  "language": "hi"
}
```

## Suggested development order

1. Verify Hindi STT with one short, clean audio sample.
2. Verify Hindi TTS with a short text sentence.
3. Complete the Hindi voice → transcription → retrieval → answer → audio loop.
4. Add Bengali and test STT and TTS separately.
5. Evaluate transcription accuracy, grounded answer correctness, end-to-end latency, audio playback, and fallback behavior.
6. Record one complete Hindi demo and one complete Bengali demo.

## Evaluation checklist

Create a small test set with at least 10 recorded questions per language. For each sample, record:
- Expected transcription and actual transcription
- Word error rate (or a documented manual accuracy score)
- Whether the response is supported by a cited knowledge-base entry
- End-to-end latency in seconds
- Whether TTS audio played successfully
- Whether unknown questions triggered a safe fallback

Do not report invented accuracy or latency numbers. Record results from actual tests.

## Current limitations

- The bundled agriculture FAQ is a starter dataset, not an authoritative or exhaustive agronomy database.
- Keyword retrieval is a baseline, not semantic search. Consider a reviewed retrieval system and trusted official sources before public deployment.
- No generative model is called. Answers are selected from the local FAQ, helping keep the initial workflow grounded.
- Browser audio capture is not implemented; this version uses audio-file upload. Add microphone recording only after the core audio pipeline is reliable.
- Do not give exact pesticide/fertilizer doses without crop, region, diagnosis, and verified local recommendations.

## Suggested VS Code extensions

- Python (Microsoft)
- Pylance
- Python Debugger

## License

For internship prototype and learning use. Add a license before public redistribution.
