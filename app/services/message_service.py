import logging

from app.database.database import SessionLocal
from app.database.crud import already_processed
from app.services.intent_service import detect_intent
from app.services.expense_service import process_expense
from app.services.retrieval_service import process_retrieval
from app.services.speech_to_text_service import (
    transcribe_audio,
    TranscriptionError,
)
from app.services.whatsapp_service import (
    download_media,
    MediaDownloadError,
    send_whatsapp_message,
)
from app.utils.messages import t, bilingual, detect_language
from app.utils.whatsapp_formatter import (
    format_whatsapp_response,
    format_expense_confirmation,
)

logger = logging.getLogger(__name__)

GENERIC_ERROR = t("generic_error", "en")


#main entry for message processing
def process_message(message, db, user_id, message_id=None, from_voice=False):
    """Returns the reply text, or None when nothing should be sent
    (a retried message that was already processed)."""

    # Reply in the language the user wrote/spoke in (English or Telugu).
    lang = detect_language(message)

    intent = detect_intent(message)

    if intent == "greeting":
        return t("greeting", lang)

    elif intent == "help":
        return t("help", lang)

    elif intent == "expense":

        outcome = process_expense(message, db, user_id, message_id, lang)

        if outcome.status == "duplicate":
            return None

        if outcome.status == "clarify":
            prefix = f'{t("heard", lang)} "{message}"\n\n' if from_voice else ""
            return f"{prefix}{outcome.clarification}"

        return format_expense_confirmation(outcome.expenses, lang)

    elif intent == "retrieval":

        result = process_retrieval(message, db, user_id)

        if result["success"]:
            return format_whatsapp_response(result["data"], lang)

        return result["message"]

    return t("unknown", lang)


def process_audio_message(audio, db, user_id, message_id=None):
    """WhatsApp audio -> download -> Gnani STT -> existing text pipeline."""
    try:
        audio_bytes, mime_type = download_media(audio.get("id"))
        transcript = transcribe_audio(audio_bytes, mime_type)
    except (MediaDownloadError, TranscriptionError) as exc:
        logger.warning("Voice note not processed: %s", exc)
        # The language is unknown until a transcript exists, so answer in both.
        return bilingual(exc.key)

    return process_message(transcript, db, user_id, message_id, from_voice=True)


def handle_whatsapp_message(message):
    """Process one WhatsApp message dict from the webhook and send the reply."""
    sender = message.get("from")
    message_id = message.get("id")
    message_type = message.get("type")

    if not sender:
        return

    db = SessionLocal()
    try:
        # Cheap early exit for webhook retries; the DB unique key is the
        # real guarantee against duplicate expenses.
        if message_id and already_processed(db, message_id):
            logger.info("Skipping already-processed message")
            return

        if message_type == "text":
            reply = process_message(message["text"]["body"], db, sender, message_id)
        elif message_type == "audio":
            reply = process_audio_message(message.get("audio") or {}, db, sender, message_id)
        else:
            logger.info("Ignoring unsupported message type: %s", message_type)
            return
    except Exception:
        logger.exception("Failed to process incoming message")
        if message_type == "text":
            reply = t("generic_error", detect_language(message["text"]["body"]))
        else:
            reply = bilingual("generic_error")
    finally:
        db.close()

    if reply:
        try:
            send_whatsapp_message(sender, reply)
        except Exception:
            logger.exception("Failed to send WhatsApp reply")
