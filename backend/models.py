from dataclasses import dataclass

@dataclass
class STTResult:
    ok: bool
    text: str = ""
    provider: str = "Gnani AI"
    error: str = ""

@dataclass
class TTSResult:
    ok: bool
    audio_bytes: bytes = b""
    mime_type: str = "audio/mpeg"
    provider: str = "Gnani AI"
    error: str = ""

@dataclass
class AnswerResult:
    answer: str
    source: str
    score: float
    mode: str
    is_fallback: bool = False
