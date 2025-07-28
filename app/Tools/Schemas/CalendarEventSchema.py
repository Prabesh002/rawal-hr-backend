from typing import Optional
from pydantic import BaseModel, Field

class CalendarEventToolParams(BaseModel):
    title: str = Field(..., description="The title of the calendar event.")
    description: Optional[str] = Field(None)
    event_start_datetime_str: str = Field(
        ...,
        description="The starting date and time of the event in a string format (e.g., 'tomorrow at 2 PM', '2024-07-15 14:00'), should be a ISO format"
    )
    event_end_datetime_str: Optional[str] = Field(
        None,
        description="The ending date and time of the event in a ISO format"
    )
    is_all_day: Optional[bool] = Field(False, description="Whether the event lasts for the entire day.")
    location: Optional[str] = Field(None, description="The location of the event, if any.")
    notify_before_minutes: Optional[int] = Field(
        None,
        description="Number of minutes before the event start time to send a notification."
    )
    color_tag: Optional[str] = Field(
        None,
        description="A color tag or category for the event ('meeting', 'personal', 'urgent')."
    )
    recurring_pattern: Optional[str] = Field(
        None,
        description="Describes the recurrence of the event 'daily', 'weekly on Monday', 'every first Friday of the month' 'none' or null if not recurring."
    )


    class Config:
        extra = "forbid"