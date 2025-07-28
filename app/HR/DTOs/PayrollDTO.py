from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel, Field

class PayrollCreateDTO(BaseModel):
    employee_id: UUID
    pay_period_start: date
    pay_period_end: date
    total_hours: float = Field(..., ge=0)
    gross_pay: float = Field(..., ge=0)
    deductions: float = Field(0.0, ge=0)
    net_pay: float = Field(..., ge=0)

class PayrollUpdateDTO(BaseModel):
    payment_date: Optional[date] = None
    status: Optional[str] = None

class PayrollResponseDTO(BaseModel):
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

    class Config:
        from_attributes = True