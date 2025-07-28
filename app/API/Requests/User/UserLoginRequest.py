from pydantic import BaseModel


class UserLogin(BaseModel):
    user_name: str
    password: str