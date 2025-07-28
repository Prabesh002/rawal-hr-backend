from typing import Optional
from sqlalchemy.orm import Session
from app.Entities.Base.User import User
from app.HR.Entities.EmployeeEntity import EmployeeEntity
from app.Repositories.Base.BaseRepository import BaseRepository

class EmployeeRepository(BaseRepository[EmployeeEntity]):
    def __init__(self, db: Session):
        super().__init__(db, EmployeeEntity)
    
    def find_by_email(self, email: str) -> Optional[EmployeeEntity]:
        return self.db.query(self.entity_type).filter(self.entity_type.email == email).first()