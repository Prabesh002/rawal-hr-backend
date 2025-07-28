from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel, EmailStr

class EmployeeCreateRequest(BaseModel):
    user_id: Optional[UUID] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    position: str
    hire_date: date