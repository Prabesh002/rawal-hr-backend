from fastapi import APIRouter, Depends
from typing import List
from app.API.Dependencies.container import container
from app.API.Requests.User.UserCreateRequest import UserCreate
from app.API.Requests.User.UserLoginRequest import UserLogin
from app.API.Response.Users.UserResponse import UserResponse
from app.API.Utilities.ApiResponse import ApiResponseHelper
from app.Dto.User.UserDto import UserDto
from app.Repositories.User.UserRepository import UserRepository
from app.Services.User.UserService import UserService
from sqlalchemy.orm import  Session
from app.Dto.Token.AccessTokenDto import AccessTokenDto
from app.API.Dependencies.Authentication import get_current_admin_user
from app.Entities.Base.User import User


router = APIRouter()


def get_db() -> Session:
    db = container.resolve(Session)
    return db 

def get_user_service() -> UserService:
    user_service = container.resolve(UserService)
    return user_service

def get_user_repository() -> UserRepository:
    repo = container.resolve(UserRepository)
    return repo

@router.post("/login")
async def login(request: UserLogin):
    try:
        user_service = get_user_service()
        result = user_service.authenticate_user(
            UserDto(
                user_name=request.user_name,
                password=request.password
            )
        )
        user_repo = get_user_repository()
        user = user_repo.get_by_username(request.user_name)
        if not result or not user:
            return ApiResponseHelper.error("Invalid username or password", status_code=401)

        response = AccessTokenDto(
            access_token=result.access_token,
            token_type=result.token_type,
            user_response=UserResponse(
                user_name=user.user_name,
                id=user.id,
                is_admin=user.is_admin,
            )
        )

        return ApiResponseHelper.success(response, "Login successful")
    except Exception as e:
         return ApiResponseHelper.error(str(e), status_code=500)

@router.post("/register")
async def register(request: UserCreate):
    try:
        user_service = get_user_service() 
        user = user_service.create_user(
            UserDto(
                user_name=request.user_name,
                password=request.password,
            )
        )

        response = UserResponse(
            id=user.id,
            user_name=user.user_name,
            is_admin=user.is_admin
        )
        return ApiResponseHelper.success(response, "User registered successfully")
    except ValueError as ve:
        return ApiResponseHelper.error(str(ve), status_code=400)
    except Exception as e:
        return ApiResponseHelper.error(str(e), status_code=500)


@router.get("/users")
async def get_all_users(current_admin: User = Depends(get_current_admin_user)):
    try:
        user_repo = get_user_repository()
        users = user_repo.find_all()
        
        response = [UserResponse.model_validate(user) for user in users]
        
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)