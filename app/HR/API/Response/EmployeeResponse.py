from typing import Optional
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, EmailStr

class EmployeeResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    position: str
    hire_date: date
    termination_date: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True