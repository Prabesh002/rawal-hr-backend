from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.HR.DTOs.TimeLogDTO import TimeLogCreateDTO, TimeLogUpdateDTO
from app.HR.Entities.TimeLogEntity import TimeLogEntity
from app.HR.Repositories.TimeLogRepository import TimeLogRepository

class TimeLogService:
    def __init__(self, db: Session, time_log_repository: TimeLogRepository):
        self.db = db
        self.time_log_repository = time_log_repository

    def create_time_log(self, time_log_data: TimeLogCreateDTO) -> TimeLogEntity:
        if time_log_data.end_time and time_log_data.start_time > time_log_data.end_time:
            raise ValueError("Start time cannot be after end time.")

        db_time_log = TimeLogEntity(**time_log_data.model_dump())
        self.db.add(db_time_log)
        self.db.commit()
        self.db.refresh(db_time_log)
        return db_time_log

    def update_time_log(self, time_log_id: UUID, time_log_data: TimeLogUpdateDTO) -> Optional[TimeLogEntity]:
        db_time_log = self.time_log_repository.find_by_id(time_log_id)
        if not db_time_log:
            return None
        
        update_data = time_log_data.model_dump(exclude_unset=True)
        start_time = update_data.get('start_time', db_time_log.start_time)
        end_time = update_data.get('end_time', db_time_log.end_time)

        if end_time and start_time > end_time:
            raise ValueError("Start time cannot be after end time.")

        for key, value in update_data.items():
            setattr(db_time_log, key, value)
            
        self.db.commit()
        self.db.refresh(db_time_log)
        return db_time_log

    def delete_time_log(self, time_log_id: UUID) -> bool:
        db_time_log = self.time_log_repository.find_by_id(time_log_id)
        if not db_time_log:
            return False
        
        self.db.delete(db_time_log)
        self.db.commit()
        return True