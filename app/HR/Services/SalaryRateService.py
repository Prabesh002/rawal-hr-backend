from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.HR.DTOs.SalaryRateDTO import SalaryRateCreateDTO, SalaryRateUpdateDTO
from app.HR.Entities.SalaryRateEntity import SalaryRateEntity
from app.HR.Repositories.SalaryRateRepository import SalaryRateRepository

class SalaryRateService:
    def __init__(self, db: Session, salary_rate_repository: SalaryRateRepository):
        self.db = db
        self.salary_rate_repository = salary_rate_repository

    def create_salary_rate(self, rate_data: SalaryRateCreateDTO) -> SalaryRateEntity:
        db_rate = SalaryRateEntity(**rate_data.model_dump())
        self.db.add(db_rate)
        self.db.commit()
        self.db.refresh(db_rate)
        return db_rate

    def update_salary_rate(self, rate_id: UUID, rate_data: SalaryRateUpdateDTO) -> Optional[SalaryRateEntity]:
        db_rate = self.salary_rate_repository.find_by_id(rate_id)
        if not db_rate:
            return None

        update_data = rate_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_rate, key, value)
        
        self.db.commit()
        self.db.refresh(db_rate)
        return db_rate

    def delete_salary_rate(self, rate_id: UUID) -> bool:
        db_rate = self.salary_rate_repository.find_by_id(rate_id)
        if not db_rate:
            return False
        
        self.db.delete(db_rate)
        self.db.commit()
        return True