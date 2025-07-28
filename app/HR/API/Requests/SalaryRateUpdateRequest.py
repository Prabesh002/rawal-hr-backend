from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class SalaryRateUpdateRequest(BaseModel):
    hourly_rate: Optional[float] = Field(None, gt=0, description="The updated hourly pay rate.")
    effective_date: Optional[date] = None