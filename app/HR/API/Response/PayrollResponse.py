from typing import Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

class PayrollResponse(BaseModel):
    id: UUID
    employee_id: UUID
    pay_period_start: date
    pay_period_end: date
    payment_date: Optional[date]
    total_hours: float
    gross_pay: float
    deductions: float
    net_pay: float
    status: str
    created_at: datetime