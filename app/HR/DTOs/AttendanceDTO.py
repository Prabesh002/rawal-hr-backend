import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class AttendanceCreateDTO(BaseModel):
    employee_id: UUID
    date: datetime.date
    status: str

class AttendanceUpdateDTO(BaseModel):
    date: Optional[datetime.date] = None
    status: Optional[str] = None
