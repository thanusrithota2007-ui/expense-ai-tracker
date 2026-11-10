"""Gnani (Vachana) speech-to-text for pre-recorded audio.

Uses the documented REST endpoint (POST https://api.vachana.ai/stt/v3,
multipart/form-data, header X-API-Key-ID), NOT the WebSocket streaming API.
Documented limits: formats WAV/MP3/OGG/FLAC/AAC/M4A, max 30 seconds.
"""
import logging
import time

import requests

from app.config import GNANI_API_KEY, GNANI_MODEL, GNANI_LANGUAGE_CODE
from app.utils.messages import t

logger = logging.getLogger(__name__)

GNANI_STT_URL = "https://api.vachana.ai/stt/v3"
REQUEST_TIMEOUT = (5, 30)  # (connect, read) seconds
MAX_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = (1, 2)
_RETRYABLE_STATUS = {429, 500, 502, 503, 504}

# Gnani decides support from the file-name extension, so we must send a
# correct one. WhatsApp voice notes arrive as audio/ogg (Opus).
_EXTENSIONS = {
    "audio/ogg": "ogg",
    "audio/mpeg": "mp3",
    "audio/mp3": "mp3",
    "audio/mp4": "m4a",
    "audio/x-m4a": "m4a",
    "audio/m4a": "m4a",
    "audio/aac": "aac",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/flac": "flac",
    "audio/x-flac": "flac",
}

# Gnani error type -> message key in app.utils.messages
_ERROR_KEYS = {
    "EMPTY_AUDIO": "stt_empty_audio",
    "MAX_AUDIO_DURATION_EXCEEDED": "stt_too_long",
    "UNSUPPORTED_AUDIO_FORMAT": "stt_unsupported_format",
    "AUDIO_CONVERSION_ERROR": "stt_conversion",
}


class TranscriptionError(Exception):
    """`key` selects the user-facing text in app.utils.messages."""

    def __init__(self, detail, key="stt_generic"):
        super().__init__(detail)
        self.key = key

    @property
    def user_message(self):
        return t(self.key, "en")


class EmptyTranscriptError(TranscriptionError):
    def __init__(self):
        super().__init__("empty transcript", "stt_no_speech")


def _error_type(response):
    """Best-effort extraction of Gnani's error code from any documented shape."""
    try:
        body = response.json()
    except ValueError:
        return None
    if not isinstance(body, dict):
        return None
    err = body.get("error")
    if isinstance(err, dict):
        return err.get("type")
    if body.get("code"):  # 504 shape: {"error": "...", "code": "UPSTREAM_TIMEOUT"}
        return body.get("code")
    detail = body.get("detail")
    if isinstance(detail, dict):  # auth / rate limit shape
        return detail.get("error_code")
    return None


def transcribe_audio(audio_bytes, mime_type):
    """Transcribe a short pre-recorded clip and return the transcript text."""
    if not GNANI_API_KEY:
        raise TranscriptionError("GNANI_API_KEY is not configured")
    if not audio_bytes:
        raise TranscriptionError("no audio bytes", "stt_empty_audio")

    mime = (mime_type or "").split(";")[0].strip().lower()
    extension = _EXTENSIONS.get(mime)
    if extension is None:
        raise TranscriptionError(
            f"unsupported mime type {mime or 'unknown'}",
            "stt_unsupported_format",
        )

    form = {
        "language_code": GNANI_LANGUAGE_CODE,
        # numbers/currency written as digits, easier for the expense extractor
        "format": "transcribe",
    }
    if GNANI_MODEL:
        form["model"] = GNANI_MODEL

    response = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.post(
                GNANI_STT_URL,
                headers={"X-API-Key-ID": GNANI_API_KEY},
                files={"audio_file": (f"voice.{extension}", audio_bytes, mime)},
                data=form,
                timeout=REQUEST_TIMEOUT,
            )
        except requests.RequestException as exc:
            if attempt < MAX_ATTEMPTS:
                time.sleep(RETRY_BACKOFF_SECONDS[attempt - 1])
                continue
            raise TranscriptionError(f"Gnani request failed: {type(exc).__name__}")

        if response.status_code in _RETRYABLE_STATUS and attempt < MAX_ATTEMPTS:
            time.sleep(RETRY_BACKOFF_SECONDS[attempt - 1])
            continue
        break

    if response.status_code != 200:
        error_type = _error_type(response)
        logger.warning("Gnani STT failed: HTTP %s %s", response.status_code, error_type)
        raise TranscriptionError(
            f"Gnani HTTP {response.status_code} {error_type}",
            _ERROR_KEYS.get(error_type, "stt_generic"),
        )

    try:
        body = response.json()
    except ValueError:
        raise TranscriptionError("Gnani returned non-JSON on 200")

    if not isinstance(body, dict) or body.get("success") is not True:
        raise TranscriptionError("Gnani 200 without success=true")

    if body.get("truncated") is True:
        # Incomplete transcript = unreliable amounts. Never process it.
        raise TranscriptionError("transcript truncated", "stt_truncated")

    transcript = body.get("transcript")
    if not isinstance(transcript, str) or not transcript.strip():
        raise EmptyTranscriptError()

    return transcript.strip()
