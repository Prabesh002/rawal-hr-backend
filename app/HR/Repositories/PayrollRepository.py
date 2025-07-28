from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.HR.Entities.PayrollEntity import PayrollEntity
from app.Repositories.Base.BaseRepository import BaseRepository

class PayrollRepository(BaseRepository[PayrollEntity]):
    def __init__(self, db: Session):
        super().__init__(db, PayrollEntity)
        
    def find_by_employee_id(self, employee_id: UUID) -> List[PayrollEntity]:
        return self.db.query(self.entity_type).filter(self.entity_type.employee_id == employee_id).order_by(self.entity_type.pay_period_start.desc()).all()