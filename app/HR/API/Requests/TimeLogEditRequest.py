from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class TimeLogEditRequest(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None