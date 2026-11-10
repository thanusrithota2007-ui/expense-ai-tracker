#Receive Expense - validate - call crud - return response
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from pydantic import ValidationError

from app.services.gemini_service import extract_expense
from app.database.crud import save_expenses_once
from app.models.schemas import ExpenseCreate
from app.utils.messages import t

_MAX_AMOUNT = Decimal(10) ** 8  # Numeric(10, 2) column


@dataclass
class ExpenseOutcome:
    status: str  # "saved" | "clarify" | "duplicate"
    expenses: List = field(default_factory=list)
    clarification: Optional[str] = None


def _normalize(raw):
    """Accept the new {"expenses": [...], "clarification": ...} shape and the
    legacy single flat expense object. Returns (items, clarification)."""
    if isinstance(raw, dict) and "expenses" in raw:
        items = raw.get("expenses") or []
        clarification = raw.get("clarification")
    elif isinstance(raw, dict):
        items, clarification = [raw], None
    elif isinstance(raw, list):
        items, clarification = raw, None
    else:
        items, clarification = [], None

    if not isinstance(items, list):
        items = []
    if not isinstance(clarification, str) or not clarification.strip():
        clarification = None
    return items, clarification


def _validate(item):
    """Return a validated ExpenseCreate, or None if anything is missing/invalid."""
    if not isinstance(item, dict):
        return None
    try:
        expense = ExpenseCreate(**item)
    except (ValidationError, TypeError, ValueError):
        return None

    if not expense.amount.is_finite() or not (0 < expense.amount < _MAX_AMOUNT):
        return None

    expense.item = (expense.item or "").strip()
    expense.category = (expense.category or "").strip()
    if expense.description is not None:
        expense.description = expense.description.strip() or None

    if not expense.item or len(expense.item) > 255:
        return None
    if not expense.category or len(expense.category) > 50:
        return None
    if expense.description and len(expense.description) > 255:
        return None
    return expense


def process_expense(message, db, user_id, message_id=None, lang="en"):
    raw = extract_expense(message)
    items, clarification = _normalize(raw)

    # Any doubt -> ask, never save a partial or guessed result.
    if clarification or not items:
        return ExpenseOutcome("clarify", clarification=clarification or t("clarify_default", lang))

    validated = [_validate(item) for item in items]
    if any(v is None for v in validated):
        return ExpenseOutcome("clarify", clarification=t("clarify_default", lang))

    saved = save_expenses_once(db, validated, user_id, message_id)
    if saved is None:
        return ExpenseOutcome("duplicate")

    return ExpenseOutcome("saved", expenses=saved)
