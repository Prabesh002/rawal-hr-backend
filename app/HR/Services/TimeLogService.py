from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from app.HR.Entities.TimeLogEntity import TimeLogEntity
from app.HR.Repositories.TimeLogRepository import TimeLogRepository
from app.HR.DTOs.TimeLogDTO import TimeLogUpdateDTO

class TimeLogService:
    def __init__(self, db: Session, time_log_repository: TimeLogRepository):
        self.db = db
        self.time_log_repository = time_log_repository

    def start_shift(self, employee_id: UUID) -> TimeLogEntity:
        active_shift = self.time_log_repository.find_active_by_employee_id(employee_id)
        if active_shift:
            raise ValueError("An active shift is already in progress. Please stop the current shift before starting a new one.")

        new_log = TimeLogEntity(
            employee_id=employee_id,
            start_time=datetime.now().astimezone() 
        )
        self.db.add(new_log)
        self.db.commit()
        self.db.refresh(new_log)
        return new_log

    def stop_shift(self, log_id: UUID, employee_id: UUID) -> Optional[TimeLogEntity]:
        db_log = self.time_log_repository.find_by_id_and_employee_id(log_id, employee_id)
        
        if not db_log:
            return None

        if db_log.end_time is not None:
            raise ValueError("This shift has already been completed.")
            
        db_log.end_time = datetime.now().astimezone()

        if db_log.start_time > db_log.end_time:
            raise ValueError("Clock-out time cannot be before clock-in time.")

        self.db.commit()
        self.db.refresh(db_log)
        return db_log
        
    def edit_time_log(self, log_id: UUID, time_log_data: TimeLogUpdateDTO) -> Optional[TimeLogEntity]:
        db_log = self.time_log_repository.find_by_id(log_id)
        if not db_log:
            return None

        update_data = time_log_data.model_dump(exclude_unset=True)
        
        new_start = update_data.get('start_time', db_log.start_time)
        new_end = update_data.get('end_time', db_log.end_time)

        if 'end_time' in update_data and update_data['end_time'] is None:
            new_end = None

        if new_end is not None and new_start > new_end:
            raise ValueError("End time cannot be before start time.")

        for key, value in update_data.items():
            setattr(db_log, key, value)
        
        self.db.commit()
        self.db.refresh(db_log)
        return db_log

    def delete_time_log(self, log_id: UUID, employee_id: UUID) -> bool:
        """Deletes a time log record, ensuring ownership."""
        db_log = self.time_log_repository.find_by_id_and_employee_id(log_id, employee_id)
        if not db_log:
            return False
        
        self.db.delete(db_log)
        self.db.commit()
        return True