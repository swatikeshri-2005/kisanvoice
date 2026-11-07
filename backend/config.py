import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    gnani_api_key: str = os.getenv("GNANI_API_KEY", "")
    gnani_stt_url: str = os.getenv("GNANI_STT_URL", "")
    gnani_tts_url: str = os.getenv("GNANI_TTS_URL", "")
    gnani_auth_header: str = os.getenv("GNANI_AUTH_HEADER", "Authorization")
    gnani_auth_prefix: str = os.getenv("GNANI_AUTH_PREFIX", "Bearer ")
    stt_file_field: str = os.getenv("GNANI_STT_FILE_FIELD", "file")
    stt_language_field: str = os.getenv("GNANI_STT_LANGUAGE_FIELD", "language")
    stt_response_text_key: str = os.getenv("GNANI_STT_RESPONSE_TEXT_KEY", "text")
    tts_response_audio_key: str = os.getenv("GNANI_TTS_RESPONSE_AUDIO_KEY", "audio")
    hindi_stt_language: str = os.getenv("GNANI_HINDI_STT_LANGUAGE", "hi-IN")
    bengali_stt_language: str = os.getenv("GNANI_BENGALI_STT_LANGUAGE", "bn-IN")
    hindi_tts_language: str = os.getenv("GNANI_HINDI_TTS_LANGUAGE", "hi-IN")
    bengali_tts_language: str = os.getenv("GNANI_BENGALI_TTS_LANGUAGE", "bn-IN")
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "45"))

settings = Settings()
