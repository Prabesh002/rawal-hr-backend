from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.HR.DTOs.AttendanceDTO import AttendanceCreateDTO, AttendanceUpdateDTO
from app.HR.Entities.AttendanceEntity import AttendanceEntity
from app.HR.Repositories.AttendanceRepository import AttendanceRepository

class AttendanceService:
    def __init__(self, db: Session, attendance_repository: AttendanceRepository):
        self.db = db
        self.attendance_repository = attendance_repository

    def create_attendance(self, attendance_data: AttendanceCreateDTO) -> AttendanceEntity:
        if self.attendance_repository.find_by_employee_and_date(attendance_data.employee_id, attendance_data.date):
            raise ValueError("Attendance for this employee on this date already recorded.")

        db_attendance = AttendanceEntity(**attendance_data.model_dump())
        self.db.add(db_attendance)
        self.db.commit()
        self.db.refresh(db_attendance)
        return db_attendance

    def update_attendance(self, attendance_id: UUID, attendance_data: AttendanceUpdateDTO) -> Optional[AttendanceEntity]:
        db_attendance = self.attendance_repository.find_by_id(attendance_id)
        if not db_attendance:
            return None

        update_data = attendance_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_attendance, key, value)
        
        self.db.commit()
        self.db.refresh(db_attendance)
        return db_attendance

    def delete_attendance(self, attendance_id: UUID) -> bool:
        db_attendance = self.attendance_repository.find_by_id(attendance_id)
        if not db_attendance:
            return False
        
        self.db.delete(db_attendance)
        self.db.commit()
        return True