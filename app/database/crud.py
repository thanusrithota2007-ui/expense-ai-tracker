from sqlalchemy.orm import Session
from sqlalchemy import func

from sqlalchemy.exc import IntegrityError

from app.database.database_models import Expense, ProcessedMessage
from app.models.schemas import ExpenseCreate


# -------------------------
# CREATE
# -------------------------

def _owned_by(user_id):
    """Row filter for one user. user_id is mandatory so a missing id can never
    silently widen a query to every user's data."""
    if not user_id:
        raise ValueError("user_id is required")
    return Expense.user_id == user_id


def create_expense(db: Session, expense: ExpenseCreate, user_id):
    if not user_id:
        raise ValueError("user_id is required")
    new_expense = Expense(**expense.model_dump(), user_id=user_id)

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# -------------------------
# READ
# -------------------------

def _user_filter(user_id):
    if not user_id:
        raise ValueError("user_id is required")
    return Expense.user_id == user_id


def already_processed(db: Session, message_id: str) -> bool:
    return db.query(ProcessedMessage).filter_by(message_id=message_id).first() is not None


def save_expenses_once(db: Session, expenses, user_id, message_id=None):
    """Atomically write a message marker and all its expense rows."""
    if not user_id:
        raise ValueError("user_id is required")
    rows = [Expense(**e.model_dump(), user_id=user_id) for e in expenses]
    try:
        if message_id:
            db.add(ProcessedMessage(message_id=message_id))
        db.add_all(rows)
        db.commit()
    except IntegrityError:
        db.rollback()
        if message_id and already_processed(db, message_id):
            return None
        raise
    for row in rows:
        db.refresh(row)
    return rows


def get_all_expenses(db: Session, user_id):
    return db.query(Expense).filter(_user_filter(user_id)).all()


def get_latest_expense(db: Session, user_id):
    return (
        db.query(Expense).filter(_user_filter(user_id))
        .order_by(Expense.expense_date.desc())
        .first()
    )


def get_highest_expense(db: Session, user_id):
    return (
        db.query(Expense).filter(_user_filter(user_id))
        .order_by(Expense.amount.desc())
        .first()
    )


# -------------------------
# Generic Expense Query
# -------------------------

def get_expenses(
    db: Session,
    user_id,
    category=None,
    item=None,
    amount=None,
    start_date=None,
    end_date=None,
):
    query = db.query(Expense).filter(_user_filter(user_id))

    if category:
        query = query.filter(
            Expense.category.ilike(f"%{category}%")
        )

    if item:
        query = query.filter(
            Expense.item.ilike(f"%{item}%")
        )

    if amount is not None:
        query = query.filter(
            Expense.amount > amount
        )

    if start_date:
        query = query.filter(
            Expense.expense_date >= start_date
        )

    if end_date:
        query = query.filter(
            Expense.expense_date <= end_date
        )

    return query.all()


# -------------------------
# Generic Sum Query
# -------------------------

def get_total(
    db: Session,
    user_id,
    category=None,
    item=None,
    start_date=None,
    end_date=None,
):
    query = db.query(func.sum(Expense.amount)).filter(_user_filter(user_id))

    if category:
        query = query.filter(
            Expense.category.ilike(f"%{category}%")
        )

    if item:
        query = query.filter(
            Expense.item.ilike(f"%{item}%")
        )

    if start_date:
        query = query.filter(
            Expense.expense_date >= start_date
        )

    if end_date:
        query = query.filter(
            Expense.expense_date <= end_date
        )

    total = query.scalar()

    return total or 0
