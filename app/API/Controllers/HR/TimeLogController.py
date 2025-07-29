from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/")
async def get_all_shifts(current_employee: EmployeeEntity = Depends(get_current_employee)):
    try:
        repo = get_time_log_repository()
        all_logs = repo.find_all()
        response = [TimeLogResponse.model_validate(log) for log in all_logs]
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.get("/employee/{employee_id}")
async def get_shifts_by_employee_id(employee_id: UUID, current_employee: EmployeeEntity = Depends(get_current_employee)):
    try:
        repo = get_time_log_repository()
        employee_logs = repo.find_by_lambda(lambda log: log.employee_id == employee_id)
        response = [TimeLogResponse.model_validate(log) for log in employee_logs]
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.get("/{log_id}")
async def get_shift_by_id(log_id: UUID, current_employee: EmployeeEntity = Depends(get_current_employee)):
    try:
        repo = get_time_log_repository()
        log = repo.find_by_id(log_id)
        if not log:
            return ApiResponseHelper.error("Time log not found.", status_code=404)
        if log.employee_id != current_employee.id:
            return ApiResponseHelper.error("You do not have permission to view this time log.", status_code=403)

        response = TimeLogResponse.model_validate(log)
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.get("/active")
async def get_active_shift(current_employee: EmployeeEntity = Depends(get_current_employee)):
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
async def start_shift(current_employee: EmployeeEntity = Depends(get_current_employee)):
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
async def stop_shift(log_id: UUID, current_employee: EmployeeEntity = Depends(get_current_employee)):
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

@router.delete("/{log_id}")
async def delete_shift(log_id: UUID, current_employee: EmployeeEntity = Depends(get_current_employee)):
    try:
        service = get_time_log_service()
        success = service.delete_time_log(log_id=log_id, employee_id=current_employee.id)
        if not success:
            return ApiResponseHelper.error("Time log not found or you do not have permission to delete it.", status_code=404)
        return ApiResponseHelper.success(message="Time log deleted successfully.")
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)