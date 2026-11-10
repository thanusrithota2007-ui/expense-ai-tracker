import json
import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request, Response

from app.config import APP_SECRET, VERIFY_TOKEN
from app.services.message_service import handle_whatsapp_message
from app.utils.webhook_security import is_valid_signature

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if (hub_mode == "subscribe" and VERIFY_TOKEN and hub_verify_token == VERIFY_TOKEN
            and hub_challenge is not None):
        return Response(content=hub_challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Invalid verify token")


@router.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    raw_body = await request.body()
    if not is_valid_signature(raw_body, request.headers.get("X-Hub-Signature-256"), APP_SECRET):
        logger.warning(
            "Rejected webhook POST: signature invalid or APP_SECRET missing (secret set: %s)",
            bool(APP_SECRET),
        )
        raise HTTPException(status_code=403, detail="Invalid signature")
    logger.info("Webhook POST accepted, %d bytes", len(raw_body))
    if not is_valid_signature(raw_body, request.headers.get("X-Hub-Signature-256"), APP_SECRET):
        logger.warning("Rejected webhook POST with missing or invalid signature")
        raise HTTPException(status_code=403, detail="Invalid signature")
    try:
        data = json.loads(raw_body)
    except (ValueError, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if not isinstance(data, dict) or not isinstance(data.get("entry"), list):
        raise HTTPException(status_code=400, detail="Malformed webhook payload")
    count = 0
    for entry in data["entry"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("changes", []), list):
            continue
        for change in (entry.get("changes") or []):
            if not isinstance(change, dict):
                continue
            value = change.get("value") or {}
            if not isinstance(value, dict) or not isinstance(value.get("messages", []), list):
                continue
            messages = value.get("messages") or []
            for message in messages:
                if isinstance(message, dict):
                    background_tasks.add_task(handle_whatsapp_message, message)
                    count += 1
                    logger.info("Webhook processed. Messages received: %s", count)
    return {"status": "accepted" if count else "ignored", "messages": count}
