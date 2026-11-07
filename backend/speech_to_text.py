import json
import requests
from backend.config import settings
from backend.models import STTResult

def transcribe_audio(audio_bytes: bytes, filename: str, language: str) -> STTResult:
    """
    Calls the configured STT endpoint using a conventional multipart request.
    Confirm the exact payload and response format in your Gnani AI API docs.
    This adapter is intentionally configurable; provider APIs can differ.
    """
    if not settings.gnani_stt_url:
        return STTResult(
            ok=False,
            error="Gnani STT is not configured. Add GNANI_STT_URL and credentials to .env, or use the text question box."
        )
    if not settings.gnani_api_key:
        return STTResult(ok=False, error="GNANI_API_KEY is missing from .env.")

    language_code = settings.hindi_stt_language if language == "hi" else settings.bengali_stt_language
    headers = {
        settings.gnani_auth_header: f"{settings.gnani_auth_prefix}{settings.gnani_api_key}".strip()
    }
    files = {settings.stt_file_field: (filename, audio_bytes)}
    data = {settings.stt_language_field: language_code}
    try:
        response = requests.post(
            settings.gnani_stt_url, headers=headers, files=files, data=data,
            timeout=settings.request_timeout_seconds
        )
        response.raise_for_status()
        payload = response.json()
        key = settings.stt_response_text_key
        text = payload.get(key, "") if isinstance(payload, dict) else ""
        if not text and isinstance(payload, dict):
            # Common response shapes; adjust this to match the provider documentation.
            for candidate in ("transcript", "transcription", "recognized_text", "result"):
                value = payload.get(candidate)
                if isinstance(value, str) and value.strip():
                    text = value
                    break
        if not text:
            return STTResult(ok=False, error=f"Could not find transcript in API response. Check GNANI_STT_RESPONSE_TEXT_KEY. Response keys: {list(payload.keys()) if isinstance(payload, dict) else type(payload).__name__}")
        return STTResult(ok=True, text=text.strip())
    except requests.RequestException as exc:
        return STTResult(ok=False, error=f"STT request failed: {exc}")
    except (ValueError, json.JSONDecodeError) as exc:
        return STTResult(ok=False, error=f"STT endpoint did not return valid JSON: {exc}")
