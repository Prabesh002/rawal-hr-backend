from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr

class EmployeeUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    termination_date: Optional[date] = None