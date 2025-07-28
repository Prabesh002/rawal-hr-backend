from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel, EmailStr

class EmployeeCreateDTO(BaseModel):
    user_id: Optional[UUID] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    position: str
    hire_date: date

class EmployeeUpdateDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    termination_date: Optional[date] = None


class EmployeeResponseDTO(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    position: str
    hire_date: date
    termination_date: Optional[date] = None
    created_at: date

    class Config:
        from_attributes = True