from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class TimeLogCreateDTO(BaseModel):
    employee_id: UUID
    start_time: datetime
    end_time: Optional[datetime] = None

class TimeLogUpdateDTO(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
