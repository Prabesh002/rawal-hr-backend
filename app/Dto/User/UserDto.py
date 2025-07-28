from pydantic import BaseModel


class UserDto(BaseModel):
    user_name: str
    password: str