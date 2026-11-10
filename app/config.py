from dotenv import load_dotenv
import os

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# WhatsApp voice notes (Gnani/Vachana STT)
GNANI_API_KEY = os.getenv("GNANI_API_KEY")
GNANI_MODEL = os.getenv("GNANI_MODEL", "prisma-v3.0")
GNANI_LANGUAGE_CODE = os.getenv("GNANI_LANGUAGE_CODE", "indic-auto")
MAX_AUDIO_BYTES = int(os.getenv("MAX_AUDIO_BYTES", str(5 * 1024 * 1024)))

# Meta App Dashboard > Settings > Basic. Missing secret fails webhook auth closed.
APP_SECRET = os.getenv("APP_SECRET")
