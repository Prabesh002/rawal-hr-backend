from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from app.API.Utilities.ApiResponse import ApiResponseHelper

async def unprocessable_entity_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_messages = [f"{error['loc'][1]}: {error['msg']}" for error in errors]
    return ApiResponseHelper.error(
        message="Validation error",
        data=error_messages,
        status_code=422
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return ApiResponseHelper.error(
        message=exc.detail,
        status_code=exc.status_code
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return ApiResponseHelper.error(
        message="An unexpected internal server error occurred.",
        status_code=500
    )