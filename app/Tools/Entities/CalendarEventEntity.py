from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.Entities.BaseEntity import BaseEntity

class CalendarEventEntity(BaseEntity):
    __tablename__ = "calendar_events"
    __table_args__ = {"schema": "tools"} 

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    event_start_datetime = Column(DateTime(timezone=True), nullable=False)
    event_end_datetime = Column(DateTime(timezone=True), nullable=True)
    is_all_day = Column(Boolean, default=False, nullable=False)
    location = Column(String, nullable=True)
    notify_before_minutes = Column(Integer, nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.users.id"), nullable=False)

    color_tag = Column(String, nullable=True)
    recurring_pattern = Column(String, nullable=True) 
    created_by_tool = Column(String, nullable=True, default="manual") 

    def __repr__(self):
        return f"<CalendarEventEntity(id={self.id}, title='{self.title}', user_id='{self.user_id}')>"