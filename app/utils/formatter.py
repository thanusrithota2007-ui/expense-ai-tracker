from app.database.database_models import Expense


def expense_to_dict(expense: Expense):

    return {
        "id": expense.id,
        "item": expense.item,
        "category": expense.category,
        "amount": float(expense.amount),
        "expense_date": expense.expense_date.isoformat(),
        "description": expense.description
    }


def expenses_to_list(expenses):

    return [
        expense_to_dict(expense)
        for expense in expenses
    ]


def single_expense(expense):

    if expense is None:
        return None

    return expense_to_dict(expense)

def total_response(query, total):

    return {
        "type": "total",
        "query": query,
        "total": float(total)
    }