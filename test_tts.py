import os  # noqa: I001
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.getenv("GNANI_TTS_URL")
api_key = os.getenv("GNANI_TTS_API_KEY")

if not url or not api_key:
    raise ValueError("TTS URL or API key missing in .env")

headers = {
    "X-API-Key-ID": api_key,
    "Content-Type": "application/json"
}

payload = {
    "text": "नमस्ते किसान, किसान वॉइस में आपका स्वागत है।",
    "voice": "Nalini",
    "model": "timbre-v2.5",
    "language": "hi-IN",
    "speed": 1.0,
    "audio_config": {
        "sample_rate": 48000,
        "num_channels": 1,
        "sample_width": 2,
        "encoding": "linear_pcm",
        "container": "wav"
    }
}

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=90
    )

    print("Status:", response.status_code)
    print("Content type:", response.headers.get("Content-Type"))

    if response.ok:
        with open("tts_test_output.wav", "wb") as f:
            f.write(response.content)

        print("TTS request successful!")
        print("Audio saved: tts_test_output.wav")
    else:
        print("API Error:", response.text[:1000])

except requests.RequestException as e:
    print("Request failed:", e)