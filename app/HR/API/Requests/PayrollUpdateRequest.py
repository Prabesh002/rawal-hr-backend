from typing import Optional
from datetime import date
from pydantic import BaseModel

class PayrollUpdateRequest(BaseModel):
    payment_date: Optional[date] = None
    status: Optional[str] = None