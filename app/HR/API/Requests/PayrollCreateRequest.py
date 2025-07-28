from uuid import UUID
from datetime import date
from pydantic import BaseModel, Field

class PayrollCreateRequest(BaseModel):
    employee_id: UUID
    pay_period_start: date
    pay_period_end: date
    total_hours: float = Field(..., ge=0, description="Total hours worked in the pay period.")
    gross_pay: float = Field(..., ge=0, description="Total gross pay calculated for the period.")
    deductions: float = Field(0.0, ge=0, description="Total deductions for the period.")
    net_pay: float = Field(..., ge=0, description="The final net pay for the employee.")