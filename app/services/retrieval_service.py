from app.services.gemini_service import understand_retrieval
from app.database import crud
from app.utils.formatter import (
    expenses_to_list,
    single_expense,
    total_response
)


def process_retrieval(message, db, user_id):

    query = understand_retrieval(message)

    operation = query["operation"]

    handlers = {

        # Show all expenses
        "all": lambda: expenses_to_list(
            crud.get_all_expenses(db, user_id)
        ),

        # Show expenses by category
        "category": lambda: expenses_to_list(
            crud.get_expenses(
                db=db,
                user_id=user_id,
                category=query["category"]
            )
        ),

        # Calculate total
        "sum": lambda: total_response(
            query,
            crud.get_total(
                db=db,
                user_id=user_id,
                category=query["category"],
                item=query["item"],
                start_date=query["start_date"],
                end_date=query["end_date"]
            )
        ),

        # Latest expense
        "latest": lambda: single_expense(
            crud.get_latest_expense(db, user_id)
        ),

        # Highest expense
        "highest": lambda: single_expense(
            crud.get_highest_expense(db, user_id)
        ),

        # Expenses above amount
        "above_amount": lambda: expenses_to_list(
            crud.get_expenses(
                db=db,
                user_id=user_id,
                amount=query["amount"]
            )
        ),

        # Expenses between dates
        "between_dates": lambda: expenses_to_list(
            crud.get_expenses(
                db=db,
                user_id=user_id,
                start_date=query["start_date"],
                end_date=query["end_date"]
            )
        ),

        # Expenses by item
        "item": lambda: expenses_to_list(
            crud.get_expenses(
                db=db,
                user_id=user_id,
                item=query["item"]
            )
        ),
    }

    handler = handlers.get(operation)

    if handler is None:
        return {
            "success": False,
            "message": f"Unsupported operation: {operation}"
        }

    return {
        "success": True,
        "operation": operation,
        "data": handler()
    }
