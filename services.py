
from datetime import datetime, date
from sqlalchemy import select

from .database import LocalSession
from .models import Expense, Budget


## ----------- Utils ----------
def _month_or_current(month:str) -> str:
    if month.strip():
        return month.strip()
    else:
        return date.today().strftime("%Y-%m")
        
        
def _month_bounds(month:str) -> tuple[date, date]:
    year, month = map(int, month.split("-"))
    start = date(year, month, 1)
    end = date(year, month + 1, 1)
    return start, end


## ----------- Expenses ----------
def add_expense(amount:float, category:str, note:str = "", spent_on:str = ""):
    when = datetime.strftime(spent_on, "%Y-%m-%d").date() if spent_on.strip() else date.today()
    with LocalSession() as session:
        exp = Expense(
            amount=amount,
            category = category.strip().lower(),
            note = note,
            spent_on = when
        )
        session.add(exp)
        session.commit()
        session.refresh(exp)
        return "✅ Added Expense"
        
        
def list_expenses(month:str = "", category:str = "") -> str:
    month = _month_or_current(month)
    start, end = _month_bounds(month)
    with LocalSession() as session:
        query = select(Expense).where(Expense.spent_on >= start, Expense.spent_on < end)
        if category.strip():
            query = query.where(Expense.category == category.strip().lower())
    
        expenses = session.scalars(query.order_by(Expense.spent_on)).all()
        
    if not expenses:
        return f"No Expenses found for {month}"
    
    lines = []
    total = 0
    for exp in expenses:
        lines.append(exp.to_string())
        total += exp.amount
        
    lines.append(f"Total Expanse is: {total}")
    return "\n\n".join(lines)




def delete_expense(expense_id:int) -> str:
    with LocalSession() as session:
        
        exp = session.get(Expense, expense_id)
        if not exp:
            return f"Expense #{expense_id} not found"

        session.delete(exp)
        session.commit()
        
        return f"Expense Deleted Successfully.."
            
            