from fastapi import APIRouter, Request, Query
from app.database.database import get_db
from app.services.message_service import process_message
from app.services.whatsapp_service import send_whatsapp_message
from app.config import VERIFY_TOKEN
from app.database.database import SessionLocal

router = APIRouter()

@router.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    if hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)

    return {"error": "Invalid verify token"}

@router.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return {"status": "ignored"}

        message = value["messages"][0]["text"]["body"]
        sender = value["messages"][0]["from"]

        db = SessionLocal()

        try:
            response = process_message(message, db)
        finally:
            db.close()

        send_whatsapp_message(sender, response)

    except Exception as e:
        print("ERROR:", e)
        print(data)

    return {"status": "ok"}