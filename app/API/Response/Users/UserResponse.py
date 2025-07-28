from pydantic import UUID4, BaseModel


class UserResponse(BaseModel):
    user_name: str
    id: UUID4