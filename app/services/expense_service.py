#Receive Expense - validate - call crud - return response

from app.services.gemini_service import extract_expense
from app.database.crud import create_expense
from app.models.schemas import ExpenseCreate

def process_expense(message, db):
    expense_data = extract_expense(message)
    print("Expense Data:", expense_data)
    expense = ExpenseCreate(**expense_data)

    saved_expense = create_expense(db, expense)

    return saved_expense