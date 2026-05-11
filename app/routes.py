from fastapi import APIRouter, HTTPException, Header
from app.database import supabase
from app.models import UserRegister, UserLogin, CategoryCreate, ExpenseCreate, ExpenseUpdate
from app.auth import hash_password, verify_password, create_access_token, verify_token
from typing import Optional

router = APIRouter()

# ── AUTH ──────────────────────────────────────────

@router.post("/register")
def register(user: UserRegister):
    existing = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    result = supabase.table("users").insert({
        "email": user.email,
        "hashed_password": hashed
    }).execute()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    result = supabase.table("users").select("*").eq("email", user.email).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    db_user = result.data[0]
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": db_user["id"]})
    return {"access_token": token, "token_type": "bearer"}

# ── HELPER ────────────────────────────────────────

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["sub"]

# ── CATEGORIES ────────────────────────────────────

@router.post("/categories")
def create_category(category: CategoryCreate, authorization: Optional[str] = Header(None)):
    user_id = get_current_user(authorization)
    result = supabase.table("categories").insert({
        "user_id": user_id,
        "name": category.name
    }).execute()
    return result.data

@router.get("/categories")
def get_categories(authorization: Optional[str] = Header(None)):
    user_id = get_current_user(authorization)
    result = supabase.table("categories").select("*").eq("user_id", user_id).execute()
    return result.data

# ── EXPENSES ──────────────────────────────────────

@router.post("/expenses")
def create_expense(expense: ExpenseCreate, authorization: Optional[str] = Header(None)):
    user_id = get_current_user(authorization)
    result = supabase.table("expenses").insert({
        "user_id": user_id,
        "title": expense.title,
        "amount": expense.amount,
        "category_id": expense.category_id,
        "date": str(expense.date) if expense.date else None,
        "notes": expense.notes
    }).execute()
    return result.data

@router.get("/expenses")
def get_expenses(authorization: Optional[str] = Header(None)):
    user_id = get_current_user(authorization)
    result = supabase.table("expenses").select("*").eq("user_id", user_id).execute()
    return result.data

@router.put("/expenses/{expense_id}")
def update_expense(expense_id: str, expense: ExpenseUpdate, authorization: Optional[str] = Header(None)):
    user_id = get_current_user(authorization)
    updates = {k: v for k, v in expense.dict().items() if v is not None}
    if expense.date:
        updates["date"] = str(expense.date)
    result = supabase.table("expenses").update(updates).eq("id", expense_id).eq("user_id", user_id).execute()
    return result.data

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str, authorization: Optional[str] = Header(None)):
    user_id = get_current_user(authorization)
    supabase.table("expenses").delete().eq("id", expense_id).eq("user_id", user_id).execute()
    return {"message": "Expense deleted successfully"}

# ── REPORTS ───────────────────────────────────────

@router.get("/reports/summary")
def get_summary(authorization: Optional[str] = Header(None)):
    user_id = get_current_user(authorization)
    result = supabase.table("expenses").select("*").eq("user_id", user_id).execute()
    expenses = result.data
    total = sum(e["amount"] for e in expenses)
    by_category = {}
    for e in expenses:
        cat = e["category_id"] or "Uncategorized"
        by_category[cat] = by_category.get(cat, 0) + e["amount"]
    return {
        "total_spent": total,
        "by_category": by_category,
        "total_expenses": len(expenses)
    }