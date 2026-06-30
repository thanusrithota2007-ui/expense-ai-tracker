from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, func,Date
# Base -> To tell the database this is the schema
from app.database.database  import Base 


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    # If you're using Supabase auth later, this links to user
    user_id = Column(String, nullable=True, index=True)

    amount = Column(Numeric(10, 2), nullable=False)

    category = Column(String(50), nullable=False)

    item = Column(String(255), nullable=False)

    description = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    expense_date = Column(Date, nullable=False)

