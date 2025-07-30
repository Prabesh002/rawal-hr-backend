from pydantic import UUID4, BaseModel


class UserResponse(BaseModel):
    user_name: str
    id: UUID4
    is_admin: bool

    class Config:
        from_attributes = True