"""All user-facing bot text, in English and Telugu, plus language detection.

Replies use fixed templates (not machine translation) so amounts and dates
can never be altered. To add a language, add a dict to MESSAGES with the same
keys and extend detect_language().
"""

TELUGU_MONTHS = [
    "జనవరి", "ఫిబ్రవరి", "మార్చి", "ఏప్రిల్", "మే", "జూన్",
    "జూలై", "ఆగస్టు", "సెప్టెంబర్", "అక్టోబర్", "నవంబర్", "డిసెంబర్",
]
ENGLISH_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHS = {"en": ENGLISH_MONTHS, "te": TELUGU_MONTHS}

MESSAGES = {
    "en": {
        "greeting": "Hello! 👋 How can I help you today?",
        "help": (
            "I can:\n"
            "• Save expenses\n"
            "• Show all expenses\n"
            "• Calculate totals\n"
            "• Find your latest expense"
        ),
        "unknown": "Sorry, I didn't understand that.",
        "generic_error": "Sorry, something went wrong on my side. Please try again.",
        "clarify_default": (
            "I couldn't find a clear amount and item. "
            "Could you tell me exactly how much you spent and on what?"
        ),
        "heard": "I heard:",
        "expense_recorded": "Expense recorded:",
        "expenses_recorded": "Expenses recorded:",
        "date_label": "Date:",
        "today": "Today",
        "yesterday": "Yesterday",
        "total": "Total:",
        # retrieval
        "no_records": "No records found.",
        "no_expenses": "No expenses found.",
        "expenses_title": "Expenses",
        "total_spent": "Total Spent:",
        "total_amount_spent": "Total Amount Spent",
        "category_label": "Category:",
        "item_label": "Item:",
        "period_label": "Period: {start} to {end}",
        # voice-note errors
        "media_download": "Sorry, I couldn't download that voice note. Please try sending it again.",
        "media_too_large": "That voice note is too large. Please send a shorter one.",
        "media_unsupported": "I can only read voice notes and audio messages right now.",
        "stt_generic": (
            "Sorry, I couldn't transcribe that voice note. "
            "Please try again or type the expense."
        ),
        "stt_empty_audio": "That voice note seems to be empty. Please try again.",
        "stt_too_long": "That voice note is too long. Please keep it under 30 seconds.",
        "stt_unsupported_format": "I couldn't read that audio format. Please try recording again.",
        "stt_conversion": "I couldn't read that audio. Please try recording it again.",
        "stt_no_speech": (
            "I couldn't hear any speech in that voice note. "
            "Please try again a bit louder or type the expense."
        ),
        "stt_truncated": (
            "That voice note was too long for me to read fully. "
            "Please send a shorter one."
        ),
    },
    "te": {
        "greeting": "నమస్తే! 👋 నేను మీకు ఎలా సహాయం చేయగలను?",
        "help": (
            "నేను ఇవి చేయగలను:\n"
            "• ఖర్చులను నమోదు చేయడం\n"
            "• అన్ని ఖర్చులను చూపించడం\n"
            "• మొత్తాలను లెక్కించడం\n"
            "• మీ తాజా ఖర్చును కనుగొనడం"
        ),
        "unknown": "క్షమించండి, నాకు అర్థం కాలేదు.",
        "generic_error": "క్షమించండి, ఏదో తప్పు జరిగింది. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "clarify_default": (
            "నాకు స్పష్టమైన మొత్తం, వస్తువు తెలియలేదు. "
            "మీరు ఎంత ఖర్చు చేశారో, దేనికోసమో ఖచ్చితంగా చెప్పగలరా?"
        ),
        "heard": "నాకు వినిపించింది:",
        "expense_recorded": "ఖర్చు నమోదైంది:",
        "expenses_recorded": "ఖర్చులు నమోదయ్యాయి:",
        "date_label": "తేదీ:",
        "today": "ఈ రోజు",
        "yesterday": "నిన్న",
        "total": "మొత్తం:",
        "no_records": "రికార్డులు ఏవీ కనిపించలేదు.",
        "no_expenses": "ఖర్చులు ఏవీ కనిపించలేదు.",
        "expenses_title": "ఖర్చులు",
        "total_spent": "మొత్తం ఖర్చు:",
        "total_amount_spent": "ఖర్చు చేసిన మొత్తం",
        "category_label": "వర్గం:",
        "item_label": "వస్తువు:",
        "period_label": "కాలం: {start} నుండి {end} వరకు",
        "media_download": "క్షమించండి, ఆ వాయిస్ నోట్‌ను డౌన్‌లోడ్ చేయలేకపోయాను. దయచేసి మళ్లీ పంపండి.",
        "media_too_large": "ఆ వాయిస్ నోట్ చాలా పెద్దది. దయచేసి చిన్నది పంపండి.",
        "media_unsupported": "నేను ప్రస్తుతం వాయిస్ నోట్లు, ఆడియో సందేశాలు మాత్రమే చదవగలను.",
        "stt_generic": (
            "క్షమించండి, ఆ వాయిస్ నోట్‌ను టెక్స్ట్‌గా మార్చలేకపోయాను. "
            "దయచేసి మళ్లీ ప్రయత్నించండి లేదా ఖర్చును టైప్ చేయండి."
        ),
        "stt_empty_audio": "ఆ వాయిస్ నోట్ ఖాళీగా ఉన్నట్లుంది. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "stt_too_long": "ఆ వాయిస్ నోట్ చాలా పొడవుగా ఉంది. దయచేసి 30 సెకన్లలోపు ఉంచండి.",
        "stt_unsupported_format": "ఆ ఆడియో ఫార్మాట్‌ను చదవలేకపోయాను. దయచేసి మళ్లీ రికార్డ్ చేయండి.",
        "stt_conversion": "ఆ ఆడియోను చదవలేకపోయాను. దయచేసి మళ్లీ రికార్డ్ చేయండి.",
        "stt_no_speech": (
            "ఆ వాయిస్ నోట్‌లో మాటలు వినిపించలేదు. "
            "దయచేసి కొంచెం గట్టిగా మళ్లీ ప్రయత్నించండి లేదా ఖర్చును టైప్ చేయండి."
        ),
        "stt_truncated": (
            "ఆ వాయిస్ నోట్ పూర్తిగా చదవడానికి చాలా పొడవుగా ఉంది. "
            "దయచేసి చిన్నది పంపండి."
        ),
    },
}


def t(key, lang="en", **fmt):
    """Look up a message; unknown language or key falls back to English."""
    text = MESSAGES.get(lang, MESSAGES["en"]).get(key) or MESSAGES["en"][key]
    return text.format(**fmt) if fmt else text


def bilingual(key):
    """English + Telugu together, for when the user's language is not known
    yet (e.g. a voice note that failed before it could be transcribed)."""
    return f"{t(key, 'en')}\n\n{t(key, 'te')}"


def detect_language(text):
    """'te' if the text is mostly Telugu script, otherwise 'en'.

    Works on typed messages and on voice transcripts (Gnani returns Telugu
    speech in Telugu script). Telugu typed in English letters counts as 'en'.
    """
    letters = [c for c in (text or "") if c.isalpha()]
    if not letters:
        return "en"
    telugu = sum(1 for c in letters if "\u0c00" <= c <= "\u0c7f")
    return "te" if telugu / len(letters) >= 0.3 else "en"
