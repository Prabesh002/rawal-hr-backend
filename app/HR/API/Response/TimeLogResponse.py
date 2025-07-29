from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class TimeLogResponse(BaseModel):
    id: UUID
    employee_id: UUID
    start_time: datetime
    end_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True