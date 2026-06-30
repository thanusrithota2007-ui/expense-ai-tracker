def format_whatsapp_response(data):

    if data is None:
        return "No records found."

    # List of expenses
    if isinstance(data, list):

        if not data:
            return "No expenses found."

        text = "Expenses\n\n"

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

            text = "Expenses\n\n"

            for exp in data["expenses"]:
                text += f"{exp['item']}        ₹{exp['amount']}\n"

            text += "\n--------------------\n"
            text += f"Total Spent: ₹{data['total']}"

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

            text = "Total Amount Spent"

            if query.get("category"):
                text += f"\nCategory: {query['category']}"

            if query.get("item"):
                text += f"\nItem: {query['item']}"

            if query.get("start_date") and query.get("end_date"):
                text += (
                    f"\nPeriod: {query['start_date']} to {query['end_date']}"
                )

            text += f"\n\n₹{data['total']:.2f}"

            return text

    return str(data)