import logging
import re

import requests

from app.config import ACCESS_TOKEN, PHONE_NUMBER_ID, MAX_AUDIO_BYTES
from app.utils.messages import t

logger = logging.getLogger(__name__)

GRAPH_BASE_URL = "https://graph.facebook.com/v23.0"
MEDIA_TIMEOUT = (5, 20)  # (connect, read) seconds
_MEDIA_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")

class MediaDownloadError(Exception):
    """`key` selects the user-facing text in app.utils.messages."""
    key = "media_download"

    def __init__(self, detail):
        super().__init__(detail)

    @property
    def user_message(self):
        return t(self.key, "en")


class MediaTooLargeError(MediaDownloadError):
    key = "media_too_large"


class UnsupportedMediaError(MediaDownloadError):
    key = "media_unsupported"



def send_whatsapp_message(recipient, text):
    if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
        raise RuntimeError("WhatsApp credentials are missing")

    url = f"{GRAPH_BASE_URL}/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {
            "body": text
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=(5, 20))
    except requests.RequestException:
        logger.exception("WhatsApp send request failed")
        raise

    if not response.ok:
        logger.error("WhatsApp send failed: HTTP %s %s", response.status_code, response.text)
        response.raise_for_status()

    logger.info("WhatsApp message sent: %s", response.text)
    return response.json()



# -------------------------
# Incoming media
# -------------------------

def _auth_headers():
    return {"Authorization": f"Bearer {ACCESS_TOKEN}"}


def _get_media_info(media_id):
    """Step 1: GET /{media-id} -> {url, mime_type, file_size, ...}."""
    try:
        response = requests.get(
            f"{GRAPH_BASE_URL}/{media_id}",
            headers=_auth_headers(),
            params={"phone_number_id": PHONE_NUMBER_ID},
            timeout=MEDIA_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise MediaDownloadError(f"media lookup failed: {type(exc).__name__}")

    if response.status_code != 200:
        raise MediaDownloadError(f"media lookup HTTP {response.status_code}")

    try:
        info = response.json()
    except ValueError:
        raise MediaDownloadError("media lookup returned non-JSON")

    if not isinstance(info, dict):
        raise MediaDownloadError("media lookup returned unexpected body")

    return info


def _download_from_url(url):
    """Step 2: GET the (5-minute) media URL with the access token.

    Returns bytes, or None if the URL has expired / is gone (404).
    """
    if not url or not url.startswith("https://"):
        raise MediaDownloadError("media URL missing or not https")

    try:
        with requests.get(
            url, headers=_auth_headers(), stream=True, timeout=MEDIA_TIMEOUT
        ) as response:
            if response.status_code == 404:
                return None
            if response.status_code != 200:
                raise MediaDownloadError(
                    f"media download HTTP {response.status_code}"
                )

            chunks, total = [], 0
            for chunk in response.iter_content(chunk_size=65536):
                total += len(chunk)
                if total > MAX_AUDIO_BYTES:
                    raise MediaTooLargeError("audio exceeded size cap while streaming")
                chunks.append(chunk)
    except requests.RequestException as exc:
        raise MediaDownloadError(f"media download failed: {type(exc).__name__}")

    return b"".join(chunks)


def download_media(media_id):
    """Download an incoming WhatsApp audio file. Returns (bytes, mime_type).

    Audio is kept in memory only; no temporary files are created.
    """
    if not isinstance(media_id, str) or not _MEDIA_ID_RE.match(media_id):
        raise MediaDownloadError("invalid media id")

    for _attempt in range(2):  # a 404 means the URL expired: re-fetch once
        info = _get_media_info(media_id)

        mime = (info.get("mime_type") or "").split(";")[0].strip().lower()
        if not mime.startswith("audio/"):
            raise UnsupportedMediaError(f"unexpected media type {mime or 'unknown'}")

        try:
            declared_size = int(info.get("file_size"))
        except (TypeError, ValueError):
            declared_size = None
        if declared_size is not None and declared_size > MAX_AUDIO_BYTES:
            raise MediaTooLargeError("declared file_size above cap")

        data = _download_from_url(info.get("url"))
        if data is None:
            logger.info("WhatsApp media URL expired, re-fetching")
            continue
        if not data:
            raise MediaDownloadError("downloaded audio was empty")
        return data, mime

    raise MediaDownloadError("media URL kept expiring")
