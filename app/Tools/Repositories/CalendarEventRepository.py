from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, datetime

from app.Repositories.Base.BaseRepository import BaseRepository
from app.Tools.Entities.CalendarEventEntity import CalendarEventEntity

class CalendarEventRepository(BaseRepository[CalendarEventEntity]):
    def __init__(self, db: Session):
        super().__init__(db, CalendarEventEntity)

    def find_by_id_and_user(self, event_id: UUID, user_id: UUID) -> Optional[CalendarEventEntity]:
        return self.db.query(self.entity_type).filter(
            self.entity_type.id == event_id,
            self.entity_type.user_id == user_id
        ).first()

    def find_by_user(self, user_id: UUID) -> List[CalendarEventEntity]:
        return self.db.query(self.entity_type).filter(
            self.entity_type.user_id == user_id
        ).order_by(self.entity_type.event_start_datetime).all()

    def find_by_user_and_date_range(
        self,
        user_id: UUID,
        start_datetime: datetime,
        end_datetime: datetime
    ) -> List[CalendarEventEntity]:

        return self.db.query(self.entity_type).filter(
            self.entity_type.user_id == user_id,
            or_(

                and_(self.entity_type.event_start_datetime >= start_datetime, self.entity_type.event_start_datetime < end_datetime),

                and_(self.entity_type.event_end_datetime > start_datetime, self.entity_type.event_end_datetime <= end_datetime),

                and_(self.entity_type.event_start_datetime < start_datetime, self.entity_type.event_end_datetime > end_datetime)
            )
        ).order_by(self.entity_type.event_start_datetime).all()

    def find_by_user_and_title_for_a_day(
        self,
        user_id: UUID,
        title: str,
        day: date
    ) -> List[CalendarEventEntity]:

        start_of_day = datetime.combine(day, datetime.min.time())
        end_of_day = datetime.combine(day, datetime.max.time())

        return self.db.query(self.entity_type).filter(
            self.entity_type.user_id == user_id,
            self.entity_type.title == title,
            self.entity_type.event_start_datetime >= start_of_day,
            self.entity_type.event_start_datetime <= end_of_day
        ).all()