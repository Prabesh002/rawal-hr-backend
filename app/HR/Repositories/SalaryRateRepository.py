from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.HR.Entities.SalaryRateEntity import SalaryRateEntity
from app.Repositories.Base.BaseRepository import BaseRepository

class SalaryRateRepository(BaseRepository[SalaryRateEntity]):
    def __init__(self, db: Session):
        super().__init__(db, SalaryRateEntity)

    def find_by_employee_id(self, employee_id: UUID) -> List[SalaryRateEntity]:
        return self.db.query(self.entity_type).filter(self.entity_type.employee_id == employee_id).order_by(self.entity_type.effective_date.desc()).all()