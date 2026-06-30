from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database_models import Expense
from app.models.schemas import ExpenseCreate


# -------------------------
# CREATE
# -------------------------

def create_expense(db: Session, expense: ExpenseCreate):
    new_expense = Expense(**expense.model_dump())

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# -------------------------
# READ
# -------------------------

def get_all_expenses(db: Session):
    return db.query(Expense).all()


def get_latest_expense(db: Session):
    return (
        db.query(Expense)
        .order_by(Expense.expense_date.desc())
        .first()
    )


def get_highest_expense(db: Session):
    return (
        db.query(Expense)
        .order_by(Expense.amount.desc())
        .first()
    )


# -------------------------
# Generic Expense Query
# -------------------------

def get_expenses(
    db: Session,
    category=None,
    item=None,
    amount=None,
    start_date=None,
    end_date=None,
):
    query = db.query(Expense)

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
    category=None,
    item=None,
    start_date=None,
    end_date=None,
):
    query = db.query(func.sum(Expense.amount))

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