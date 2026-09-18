
from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


### Expenses - Budget - Tasks
### amount, category, note, spent_on, created_at


class Expense(Base):
    __tablename__ = "expenses"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    amount : Mapped[float] = mapped_column(Float)
    category : Mapped[str] = mapped_column(String(60)) 
    note: Mapped[str] = mapped_column(String(300), default="")
    spent_on : Mapped[date] = mapped_column(Date, default=date.today)
    created_at : Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    
    def to_string(self) -> str:
        note = self.note if self.note else ""
        return f"{self.id} | {self.spent_on} | {self.category} | {self.amount} | {note}"
        
    

class Budget(Base):
    __tablename__ = "budget"
        
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    monthly_limit : Mapped[float] = mapped_column(Float)
    category : Mapped[str] = mapped_column(String(60), unique=True) 

