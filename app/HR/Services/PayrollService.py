from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.HR.DTOs.PayrollDTO import PayrollCreateDTO, PayrollUpdateDTO
from app.HR.Entities.PayrollEntity import PayrollEntity
from app.HR.Repositories.PayrollRepository import PayrollRepository

class PayrollService:
    def __init__(self, db: Session, payroll_repository: PayrollRepository):
        self.db = db
        self.payroll_repository = payroll_repository

    def create_payroll(self, payroll_data: PayrollCreateDTO) -> PayrollEntity:
        if payroll_data.pay_period_start > payroll_data.pay_period_end:
            raise ValueError("Pay period start date cannot be after end date.")
        
        db_payroll = PayrollEntity(**payroll_data.model_dump())
        self.db.add(db_payroll)
        self.db.commit()
        self.db.refresh(db_payroll)
        return db_payroll

    def update_payroll(self, payroll_id: UUID, payroll_data: PayrollUpdateDTO) -> Optional[PayrollEntity]:
        db_payroll = self.payroll_repository.find_by_id(payroll_id)
        if not db_payroll:
            return None

        update_data = payroll_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_payroll, key, value)
        
        self.db.commit()
        self.db.refresh(db_payroll)
        return db_payroll

    def delete_payroll(self, payroll_id: UUID) -> bool:
        db_payroll = self.payroll_repository.find_by_id(payroll_id)
        if not db_payroll:
            return False
        
        self.db.delete(db_payroll)
        self.db.commit()
        return True