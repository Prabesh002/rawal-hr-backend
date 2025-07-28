from uuid import UUID
from datetime import date
from pydantic import BaseModel, Field

class SalaryRateCreateRequest(BaseModel):
    employee_id: UUID
    hourly_rate: float = Field(..., gt=0, description="The hourly pay rate for the employee.")
    effective_date: date