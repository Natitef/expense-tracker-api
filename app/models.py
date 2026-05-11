from pydantic import BaseModel
from typing import Optional
from datetime import date

# Auth models
class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Category models
class CategoryCreate(BaseModel):
    name: str

# Expense models
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category_id: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None

class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None