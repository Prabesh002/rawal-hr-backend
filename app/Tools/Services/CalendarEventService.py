# app/Tools/Services/CalendarEventService.py
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from app.Tools.Repositories.CalendarEventRepository import CalendarEventRepository
from app.Tools.Entities.CalendarEventEntity import CalendarEventEntity
from app.Tools.DTOs.CalendarEventDTO import CalendarEventCreateDTO, CalendarEventUpdateDTO

class CalendarEventService:
    def __init__(self, db: Session, calendar_event_repository: CalendarEventRepository):
        self.db = db
        self.calendar_event_repository = calendar_event_repository

    def create_event(self, event_data: CalendarEventCreateDTO) -> CalendarEventEntity:

        if event_data.event_end_datetime and event_data.event_start_datetime > event_data.event_end_datetime:
            raise ValueError("Event start datetime cannot be after end datetime.")

        db_event = CalendarEventEntity(
            title=event_data.title,
            description=event_data.description,
            event_start_datetime=event_data.event_start_datetime,
            event_end_datetime=event_data.event_end_datetime,
            is_all_day=event_data.is_all_day,
            location=event_data.location,
            notify_before_minutes=event_data.notify_before_minutes,
            user_id=event_data.user_id, 
            color_tag=event_data.color_tag,
            recurring_pattern=event_data.recurring_pattern,
            created_by_tool=event_data.created_by_tool
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_event_by_id(self, event_id: UUID, user_id: UUID) -> Optional[CalendarEventEntity]:

        return self.calendar_event_repository.find_by_id_and_user(event_id=event_id, user_id=user_id)

    def get_events_for_user(
        self,
        user_id: UUID,
        start_datetime_filter: Optional[datetime] = None,
        end_datetime_filter: Optional[datetime] = None
    ) -> List[CalendarEventEntity]:

        if start_datetime_filter and end_datetime_filter:
            if start_datetime_filter > end_datetime_filter:
                raise ValueError("Start datetime filter cannot be after end datetime filter.")
            return self.calendar_event_repository.find_by_user_and_date_range(
                user_id=user_id,
                start_datetime=start_datetime_filter,
                end_datetime=end_datetime_filter
            )
        return self.calendar_event_repository.find_by_user(user_id=user_id)

    def update_event(
        self,
        event_id: UUID,
        user_id: UUID, 
        event_data: CalendarEventUpdateDTO
    ) -> Optional[CalendarEventEntity]:

        db_event = self.calendar_event_repository.find_by_id_and_user(event_id=event_id, user_id=user_id)
        if not db_event:
            return None 

        update_data = event_data.model_dump(exclude_unset=True) 


        new_start = update_data.get("event_start_datetime", db_event.event_start_datetime)
        new_end = update_data.get("event_end_datetime", db_event.event_end_datetime)

        if "event_end_datetime" in update_data and update_data["event_end_datetime"] is None:
            new_end = None 

        if new_end is not None and new_start > new_end:
            raise ValueError("Event start datetime cannot be after end datetime.")


        for key, value in update_data.items():
            setattr(db_event, key, value)

        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def delete_event(self, event_id: UUID, user_id: UUID) -> bool:
        db_event = self.calendar_event_repository.find_by_id_and_user(event_id=event_id, user_id=user_id)
        if not db_event:
            return False
        self.db.delete(db_event)
        self.db.commit()
        return True