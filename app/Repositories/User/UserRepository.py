from typing import Optional
from sqlalchemy.orm import Session
from app.Entities.Base.User import User
from app.Repositories.Base.BaseRepository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.user_name == username).first()