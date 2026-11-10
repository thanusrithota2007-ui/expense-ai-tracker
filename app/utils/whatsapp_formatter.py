from datetime import date, timedelta
from decimal import Decimal

from app.utils.messages import t, MONTHS


def format_whatsapp_response(data, lang="en"):

    if data is None:
        return t("no_records", lang)

    # List of expenses
    if isinstance(data, list):

        if not data:
            return t("no_expenses", lang)

        text = f"{t('expenses_title', lang)}\n\n"

        for expense in data:
            text += (
                f"{expense['item']}        ₹{expense['amount']}\n"
                f"{expense['category']}\n"
                f"{expense['expense_date']}\n\n"
            )

        return text.strip()

    # Dict response (like total, summary, etc.)
    if isinstance(data, dict):

        # Case: total + expenses
        if "expenses" in data and "total" in data:

            text = f"{t('expenses_title', lang)}\n\n"

            for exp in data["expenses"]:
                text += f"{exp['item']}        ₹{exp['amount']}\n"

            text += "\n--------------------\n"
            text += f"{t('total_spent', lang)} ₹{data['total']}"

            return text

        # Single expense
        if "item" in data:
            return (
                f"{data['item']}        ₹{data['amount']}\n"
                f"{data['category']}\n"
                f"{data['expense_date']}"
            )

        # Total response
        if data.get("type") == "total":

            query = data["query"]

            text = t("total_amount_spent", lang)

            if query.get("category"):
                text += f"\n{t('category_label', lang)} {query['category']}"

            if query.get("item"):
                text += f"\n{t('item_label', lang)} {query['item']}"

            if query.get("start_date") and query.get("end_date"):
                text += "\n" + t(
                    "period_label", lang,
                    start=query["start_date"], end=query["end_date"],
                )

            text += f"\n\n₹{data['total']:.2f}"

            return text

    return str(data)


def _format_amount(amount):
    amount = Decimal(amount)
    if amount == amount.to_integral_value():
        return f"{int(amount):,}"
    return f"{amount:,.2f}"


def _format_expense_date(expense_date, lang="en"):
    today = date.today()
    if expense_date == today:
        return t("today", lang)
    if expense_date == today - timedelta(days=1):
        return t("yesterday", lang)
    month = MONTHS.get(lang, MONTHS["en"])[expense_date.month - 1]
    return f"{expense_date.day:02d} {month} {expense_date.year}"


def format_expense_confirmation(expenses, lang="en"):
    """Confirmation text for one or more saved expenses."""
    if len(expenses) == 1:
        e = expenses[0]
        return (
            f"{t('expense_recorded', lang)}\n"
            f"{e.item.capitalize()} — ₹{_format_amount(e.amount)}\n"
            f"{t('date_label', lang)} {_format_expense_date(e.expense_date, lang)}"
        )

    lines = [t("expenses_recorded", lang)]
    for e in expenses:
        lines.append(
            f"{e.item.capitalize()} — ₹{_format_amount(e.amount)} "
            f"({_format_expense_date(e.expense_date, lang)})"
        )
    total = sum((Decimal(e.amount) for e in expenses), Decimal(0))
    lines.append(f"{t('total', lang)} ₹{_format_amount(total)}")
    return "\n".join(lines)
