from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CalendarEventCreateDTO(BaseModel):
    title: str
    user_id: UUID 
    event_start_datetime: datetime
    description: Optional[str] = None
    event_end_datetime: Optional[datetime] = None
    is_all_day: bool = False
    location: Optional[str] = None
    notify_before_minutes: Optional[int] = None
    color_tag: Optional[str] = None
    recurring_pattern: Optional[str] = None
    created_by_tool: Optional[str] = Field(default="manual")

    class Config:
        from_attributes = True 



class CalendarEventUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_start_datetime: Optional[datetime] = None
    event_end_datetime: Optional[datetime] = None
    is_all_day: Optional[bool] = None
    location: Optional[str] = None
    notify_before_minutes: Optional[int] = None
    color_tag: Optional[str] = None
    recurring_pattern: Optional[str] = None

    class Config:
        from_attributes = True



class CalendarEventResponseDTO(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    event_start_datetime: datetime
    event_end_datetime: Optional[datetime]
    is_all_day: bool
    location: Optional[str]
    notify_before_minutes: Optional[int]
    user_id: UUID
    color_tag: Optional[str]
    recurring_pattern: Optional[str]
    created_at: datetime
    created_by_tool: Optional[str]

    class Config:
        from_attributes = True