from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from backend.answer_engine import answer_question
from backend.speech_to_text import transcribe_audio
from backend.text_to_speech import synthesize_speech

app = FastAPI(title="KisanVoice API", version="0.1.0")

class QuestionRequest(BaseModel):
    question: str
    language: str = "hi"

@app.get("/health")
def health():
    return {"status": "ok", "app": "KisanVoice"}

@app.post("/answer")
def answer(request: QuestionRequest):
    if request.language not in ("hi", "bn"):
        raise HTTPException(status_code=400, detail="language must be 'hi' or 'bn'")
    return answer_question(request.question, request.language).__dict__

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), language: str = Form("hi")):
    if language not in ("hi", "bn"):
        raise HTTPException(status_code=400, detail="language must be 'hi' or 'bn'")
    result = transcribe_audio(await file.read(), file.filename or "audio.wav", language)
    if not result.ok:
        raise HTTPException(status_code=502, detail=result.error)
    return {"text": result.text, "provider": result.provider}

class SpeechRequest(BaseModel):
    text: str
    language: str = "hi"

@app.post("/speak")
def speak(request: SpeechRequest):
    if request.language not in ("hi", "bn"):
        raise HTTPException(status_code=400, detail="language must be 'hi' or 'bn'")
    result = synthesize_speech(request.text, request.language)
    if not result.ok:
        raise HTTPException(status_code=502, detail=result.error)
    import base64
    return {"audio_base64": base64.b64encode(result.audio_bytes).decode("ascii"), "mime_type": result.mime_type}
