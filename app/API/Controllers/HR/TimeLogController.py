from uuid import UUID
from fastapi import APIRouter, Depends
from app.API.Dependencies.GetEmployee import get_current_employee
from app.API.Utilities.ApiResponse import ApiResponseHelper
from app.HR.Repositories.TimeLogRepository import TimeLogRepository
from app.HR.Services.TimeLogService import TimeLogService
from app.HR.API.Response.TimeLogResponse import TimeLogResponse

from app.HR.Entities.EmployeeEntity import EmployeeEntity
from app.API.Dependencies.container import container

router = APIRouter()

def get_time_log_service() -> TimeLogService:
    return container.resolve(TimeLogService)

def get_time_log_repository() -> TimeLogRepository:
    return container.resolve(TimeLogRepository)


@router.get("/active")
async def get_active_shift(
    current_employee: EmployeeEntity = Depends(get_current_employee)
):
    try:
        repo = get_time_log_repository()
        active_shift = repo.find_active_by_employee_id(employee_id=current_employee.id)

        if not active_shift:
            return ApiResponseHelper.success(data=None, message="No active shift found.")

        response = TimeLogResponse.model_validate(active_shift)
        return ApiResponseHelper.success(response, "Active shift retrieved successfully.")

    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)


@router.post("/start")
async def start_shift(
    current_employee: EmployeeEntity = Depends(get_current_employee)
):
    try:
        service = get_time_log_service()
        new_log = service.start_shift(employee_id=current_employee.id)
        response = TimeLogResponse.model_validate(new_log)
        return ApiResponseHelper.success(response, "Shift started successfully.")
    except ValueError as ve:
        return ApiResponseHelper.error(str(ve), status_code=400)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.put("/{log_id}/stop")
async def stop_shift(
    log_id: UUID,
    current_employee: EmployeeEntity = Depends(get_current_employee)
):
    try:
        service = get_time_log_service()
        updated_log = service.stop_shift(log_id=log_id, employee_id=current_employee.id)
        
        if updated_log is None:
            return ApiResponseHelper.error("Active shift log not found or does not belong to user.", status_code=404)
            
        response = TimeLogResponse.model_validate(updated_log)
        return ApiResponseHelper.success(response, "Shift stopped successfully.")
    except ValueError as ve:
        return ApiResponseHelper.error(str(ve), status_code=400)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)