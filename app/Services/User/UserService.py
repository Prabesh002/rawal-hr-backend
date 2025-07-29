from uuid import UUID
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.Core.Security.PasswordManager import PasswordManager
from app.Dto.Token.AccessTokenDto import AccessTokenDto
from app.Dto.User.UserDto import UserDto
from app.Repositories.User.UserRepository import UserRepository
from app.Services.User.TokenService import TokenService
from app.Entities.Base.User import User
from typing import Optional

class UserService:
    def __init__(self, db: Session, user_repository: UserRepository, token_service: TokenService):
        self.db = db
        self.user_repository = user_repository
        self.token_service = token_service
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
       return PasswordManager.verify_password(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return PasswordManager.get_password_hash(password)
    
    def authenticate_user(self, passed_user : UserDto) -> AccessTokenDto:
        user = self.user_repository.get_by_username(passed_user.user_name)
        if not user:
            return None
        if not self.verify_password(passed_user.password, user.hashed_password):
            return None
        
        access_token = self.token_service.create_access_token(
            data={"sub": user.user_name}
        )
        return AccessTokenDto(
            access_token=access_token,
            token_type="bearer"
        )
    
    def create_user(self, user : UserDto) -> User:
        if self.user_repository.get_by_username(user.user_name):
            raise ValueError("Username already exists")
            
        user = User(
            user_name=user.user_name,
            hashed_password=self.get_password_hash(user.password)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    

def set_user_admin_status(self, user_id: UUID, is_admin: bool) -> Optional[User]:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return None 
        user.is_admin = is_admin
        self.db.commit()
        self.db.refresh(user)
        return user