from typing import TypeVar, Generic, List, Optional, Callable
from uuid import UUID
from sqlalchemy.orm import Session
from app.Entities.BaseEntity import BaseEntity

T = TypeVar('T', bound=BaseEntity)

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, entity_type: type[T]):
        self.db = db
        self.entity_type = entity_type
    
    def find_by_id(self, id: UUID) -> Optional[T]:
        return self.db.query(self.entity_type).filter(self.entity_type.id == id).first()
    
    def find_all(self) -> List[T]:
        return self.db.query(self.entity_type).all()
    
    def find_by_lambda(self, lambda_expression: Callable[[T], bool]) -> List[T]:
        return list(filter(lambda_expression, self.find_all()))