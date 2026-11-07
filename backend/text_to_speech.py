import base64  # noqa: I001
import requests
from backend.config import settings
from backend.models import TTSResult # type: ignore

def synthesize_speech(text: str, language: str) -> TTSResult:
    """
    Calls a configurable TTS endpoint. The default request is JSON with `text`
    and `language`. If your Gnani endpoint uses different field names or returns
    raw audio rather than JSON/base64, adapt this function using the official docs.
    """
    if not settings.gnani_tts_url:
        return TTSResult(ok=False, error="Gnani TTS is not configured. Add GNANI_TTS_URL to .env.")
    if not settings.gnani_api_key:
        return TTSResult(ok=False, error="GNANI_API_KEY is missing from .env.")

    language_code = settings.hindi_tts_language if language == "hi" else settings.bengali_tts_language
    headers = {
        settings.gnani_auth_header: f"{settings.gnani_auth_prefix}{settings.gnani_api_key}".strip(),
        "Content-Type": "application/json",
    }
    payload = {"text": text, "language": language_code}
    try:
        response = requests.post(
            settings.gnani_tts_url, headers=headers, json=payload,
            timeout=settings.request_timeout_seconds
        )
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "audio/" in content_type or "application/octet-stream" in content_type:
            mime = content_type.split(";")[0] or "audio/mpeg"
            return TTSResult(ok=True, audio_bytes=response.content, mime_type=mime)
        data = response.json()
        audio_value = data.get(settings.tts_response_audio_key)
        if isinstance(audio_value, str) and audio_value:
            # Most APIs return base64 audio in a JSON field. Confirm format in docs.
            try:
                audio_bytes = base64.b64decode(audio_value)
            except Exception:  # noqa: BLE001
                return TTSResult(ok=False, error="TTS audio field was not valid base64. Check provider response format.")
            mime = data.get("mime_type", data.get("content_type", "audio/mpeg"))
            return TTSResult(ok=True, audio_bytes=audio_bytes, mime_type=mime)
        return TTSResult(ok=False, error=f"Could not find audio in API response. Check GNANI_TTS_RESPONSE_AUDIO_KEY. Response keys: {list(data.keys())}")
    except requests.RequestException as exc:
        return TTSResult(ok=False, error=f"TTS request failed: {exc}")
    except ValueError as exc:
        return TTSResult(ok=False, error=f"TTS endpoint response was neither supported audio nor JSON: {exc}")
