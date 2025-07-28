from typing import TypeVar, Optional, Generic
from fastapi.responses import JSONResponse
from pydantic import BaseModel

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None

class ApiResponseHelper:
    @staticmethod
    def success(data: Optional[T] = None, message: str = "Operation completed successfully") -> ApiResponse[T]:
        return ApiResponse(
            success=True,
            message=message,
            data=data
        )
    
    @staticmethod
    def error(message: str = "An error occurred", data: Optional[T] = None, status_code = 500) -> ApiResponse[T]:
       return JSONResponse(
            content={
                "success": False,
                "message": message,
                "data": data
            },
            status_code=status_code
        )