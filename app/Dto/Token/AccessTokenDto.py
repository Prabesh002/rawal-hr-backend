from typing import Optional
from pydantic import BaseModel

from app.API.Response.Users.UserResponse import UserResponse

class AccessTokenDto(BaseModel):
    access_token: str
    token_type: str
    user_response: Optional[UserResponse] = None