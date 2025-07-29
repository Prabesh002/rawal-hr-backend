from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

class SalaryRateResponse(BaseModel):
    id: UUID
    employee_id: UUID
    hourly_rate: float
    effective_date: date
    created_at: datetime

    class Config:
        from_attributes = True