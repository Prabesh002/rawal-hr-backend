from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.HR.Entities.TimeLogEntity import TimeLogEntity
from app.Repositories.Base.BaseRepository import BaseRepository

class TimeLogRepository(BaseRepository[TimeLogEntity]):
    def __init__(self, db: Session):
        super().__init__(db, TimeLogEntity)

    def find_by_employee_id(self, employee_id: UUID) -> List[TimeLogEntity]:
        return self.db.query(self.entity_type).filter(self.entity_type.employee_id == employee_id).order_by(self.entity_type.start_time).all()
    
    def find_active_by_employee_id(self, employee_id: UUID) -> Optional[TimeLogEntity]:
        return self.db.query(self.entity_type).filter(
            self.entity_type.employee_id == employee_id,
            self.entity_type.end_time == None
        ).first()