from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from decimal import Decimal
from datetime import datetime,date


class ExpenseCreate(BaseModel):
    amount: Annotated[Decimal, Field(description="Amount spent")]
    category: Annotated[str, Field(description="Category of the expense")]
    item: Annotated[str, Field(description="Name of the item")]
    description: Annotated[
        Optional[str],
        Field(description="Extra details about the expense")
    ] = None
    expense_date: Annotated[
        date,
        Field(description="Date when the expense occurred")
    ]



class ExpenseResponse(BaseModel):
    id: Annotated[int, Field(description="Unique expense ID")]
    user_id: Annotated[Optional[str], Field(description="User ID")] = None
    amount: Annotated[Decimal, Field(description="Amount spent")]
    category: Annotated[str, Field(description="Category of the expense")]
    item: Annotated[str, Field(description="Name of the item")]
    description: Annotated[
        Optional[str],
        Field(description="Extra details about the expense")
    ] = None
    created_at: Annotated[
        datetime,
        Field(description="Time when expense was created")
    ]

    model_config = ConfigDict(from_attributes=True)
    expense_date: Annotated[
    date,
    Field(description="Date when the expense occurred")
]
    



class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = None
    category: Optional[str] = None
    item: Optional[str] = None
    description: Optional[str] = None
    expense_date: Optional[date] = None


class RetrievalRequest(BaseModel):
    message: str

    