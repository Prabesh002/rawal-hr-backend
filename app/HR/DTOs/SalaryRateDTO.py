from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel, Field

class SalaryRateCreateDTO(BaseModel):
    employee_id: UUID
    hourly_rate: float = Field(..., gt=0)
    effective_date: date

class SalaryRateUpdateDTO(BaseModel):
    hourly_rate: Optional[float] = Field(None, gt=0)
    effective_date: Optional[date] = None
