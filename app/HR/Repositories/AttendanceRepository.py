from typing import List
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from app.HR.Entities.AttendanceEntity import AttendanceEntity
from app.Repositories.Base.BaseRepository import BaseRepository

class AttendanceRepository(BaseRepository[AttendanceEntity]):
    def __init__(self, db: Session):
        super().__init__(db, AttendanceEntity)

    def find_by_employee_id(self, employee_id: UUID) -> List[AttendanceEntity]:
        return self.db.query(self.entity_type).filter(self.entity_type.employee_id == employee_id).all()

    def find_by_employee_and_date(self, employee_id: UUID, attendance_date: date) -> List[AttendanceEntity]:
        return self.db.query(self.entity_type).filter(
            self.entity_type.employee_id == employee_id,
            self.entity_type.date == attendance_date
        ).first()