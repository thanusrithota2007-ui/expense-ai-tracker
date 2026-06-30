from app.services.intent_service import detect_intent
from app.services.expense_service import process_expense
from app.services.retrieval_service import process_retrieval
from app.utils.whatsapp_formatter import format_whatsapp_response
#main entry for message processing
def process_message(message, db):

    intent = detect_intent(message)

    if intent == "greeting":
        return "Hello! 👋 How can I help you today?"

    elif intent == "help":
        return (
            "I can:\n"
            "• Save expenses\n"
            "• Show all expenses\n"
            "• Calculate totals\n"
            "• Find your latest expense"
        )

    elif intent == "expense":

        expense = process_expense(message, db)

        return (
            f"Expense saved! ₹{expense.amount} "
            f"for {expense.item}"
        )

    elif intent == "retrieval":

        result = process_retrieval(message, db)

        if result["success"]:
            return format_whatsapp_response(result["data"])

        return result["message"]

    return "Sorry, I didn't understand that."