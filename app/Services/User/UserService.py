from passlib.context import CryptContext
from sqlalchemy.orm import Session
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
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
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