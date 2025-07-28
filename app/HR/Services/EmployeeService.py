from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.HR.DTOs.EmployeeDTO import EmployeeCreateDTO, EmployeeUpdateDTO
from app.HR.Entities.EmployeeEntity import EmployeeEntity
from app.HR.Repositories.EmployeeRepository import EmployeeRepository

class EmployeeService:
    def __init__(self, db: Session, employee_repository: EmployeeRepository):
        self.db = db
        self.employee_repository = employee_repository

    def create_employee(self, employee_data: EmployeeCreateDTO) -> EmployeeEntity:
        if self.employee_repository.find_by_email(employee_data.email):
            raise ValueError("Employee with this email already exists.")
        
        db_employee = EmployeeEntity(**employee_data.model_dump())
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def update_employee(self, employee_id: UUID, employee_data: EmployeeUpdateDTO) -> Optional[EmployeeEntity]:
        db_employee = self.employee_repository.find_by_id(employee_id)
        if not db_employee:
            return None

        update_data = employee_data.model_dump(exclude_unset=True)
        if 'email' in update_data and self.employee_repository.find_by_email(update_data['email']):
             raise ValueError("Another employee with this email already exists.")

        for key, value in update_data.items():
            setattr(db_employee, key, value)
        
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def delete_employee(self, employee_id: UUID) -> bool:
        db_employee = self.employee_repository.find_by_id(employee_id)
        if not db_employee:
            return False
        
        self.db.delete(db_employee)
        self.db.commit()
        return True