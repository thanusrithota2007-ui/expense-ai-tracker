from google import genai
import json
from datetime import date

from app.prompts.expense_prompt import EXPENSE_PROMPT
from app.prompts.retrieval_prompt import RETRIEVAL_PROMPT
from app.prompts.intent_prompt import INTENT_PROMPT
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def _generate_json(prompt: str, message: str):
    today = date.today().isoformat()

    full_prompt = f"""
{prompt}

Today's date is: {today}

IMPORTANT:
- Use today's date above when converting relative dates like
  "today", "yesterday", "this week", "last month", etc.

User Message:
{message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    response_text = response.text.strip()
    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")
    response_text = response_text.strip()

    return json.loads(response_text)


def extract_expense(message: str):
    return _generate_json(EXPENSE_PROMPT, message)


def understand_retrieval(message: str):
    return _generate_json(RETRIEVAL_PROMPT, message)


def understand_intent(message: str):
    return _generate_json(INTENT_PROMPT, message)
