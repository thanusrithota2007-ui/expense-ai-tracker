import hashlib
import hmac
import re


def is_valid_signature(raw_body: bytes, signature_header, app_secret) -> bool:
    if not app_secret or not signature_header or not signature_header.startswith("sha256="):
        return False
    supplied = signature_header[7:]
    if not re.fullmatch(r"[0-9a-fA-F]{64}", supplied):
        return False
    expected = hmac.new(app_secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, supplied)
