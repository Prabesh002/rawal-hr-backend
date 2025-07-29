from uuid import UUID
from fastapi import APIRouter, Depends
from app.API.Dependencies.GetEmployee import get_current_employee
from app.API.Utilities.ApiResponse import ApiResponseHelper
from app.HR.Repositories.TimeLogRepository import TimeLogRepository
from app.HR.Repositories.EmployeeRepository import EmployeeRepository
from app.HR.Services.TimeLogService import TimeLogService
from app.HR.API.Response.TimeLogResponse import TimeLogResponse
from app.HR.Entities.EmployeeEntity import EmployeeEntity
from app.Entities.Base.User import User
from app.API.Dependencies.Authentication import get_current_user
from app.API.Dependencies.container import container

router = APIRouter()

def get_time_log_service() -> TimeLogService:
    return container.resolve(TimeLogService)

def get_time_log_repository() -> TimeLogRepository:
    return container.resolve(TimeLogRepository)
    
def get_employee_repository() -> EmployeeRepository:
    return container.resolve(EmployeeRepository)

@router.get("/")
async def get_all_shifts(current_user: User = Depends(get_current_user)):
    try:
        repo = get_time_log_repository()
        logs = []
        if current_user.is_admin:
            logs = repo.find_all()
        else:
            employee_repo = get_employee_repository()
            employee_list = employee_repo.find_by_lambda(lambda e: e.user_id == current_user.id)
            if employee_list:
                employee = employee_list[0]
                logs = repo.find_by_employee_id(employee.id)

        response = [TimeLogResponse.model_validate(log) for log in logs]
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

@router.get("/employee/{employee_id}")
async def get_shifts_by_employee_id(employee_id: UUID, current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin:
            employee_repo = get_employee_repository()
            employee_list = employee_repo.find_by_lambda(lambda e: e.user_id == current_user.id)
            if not employee_list or employee_list[0].id != employee_id:
                 return ApiResponseHelper.error("You do not have permission to view these time logs.", status_code=403)

        repo = get_time_log_repository()
        employee_logs = repo.find_by_employee_id(employee_id)
        response = [TimeLogResponse.model_validate(log) for log in employee_logs]
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.get("/{log_id}")
async def get_shift_by_id(log_id: UUID, current_user: User = Depends(get_current_user)):
    try:
        repo = get_time_log_repository()
        log = repo.find_by_id(log_id)
        if not log:
            return ApiResponseHelper.error("Time log not found.", status_code=404)
        
        if not current_user.is_admin:
            employee_repo = get_employee_repository()
            employee_list = employee_repo.find_by_lambda(lambda e: e.user_id == current_user.id)
            if not employee_list or log.employee_id != employee_list[0].id:
                return ApiResponseHelper.error("You do not have permission to view this time log.", status_code=403)

        response = TimeLogResponse.model_validate(log)
        return ApiResponseHelper.success(response)
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
async def delete_shift(log_id: UUID, current_user: User = Depends(get_current_user)):
    try:
        repo = get_time_log_repository()
        log_to_delete = repo.find_by_id(log_id)
        if not log_to_delete:
            return ApiResponseHelper.error("Time log not found.", status_code=404)

        employee_id_for_delete = log_to_delete.employee_id

        if not current_user.is_admin:
            employee_repo = get_employee_repository()
            employee_list = employee_repo.find_by_lambda(lambda e: e.user_id == current_user.id)
            if not employee_list or log_to_delete.employee_id != employee_list[0].id:
                 return ApiResponseHelper.error("You do not have permission to delete this time log.", status_code=403)

        service = get_time_log_service()
        success = service.delete_time_log(log_id=log_id, employee_id=employee_id_for_delete)
        
        if not success:
            return ApiResponseHelper.error("Failed to delete the time log.", status_code=500)
            
        return ApiResponseHelper.success(message="Time log deleted successfully.")
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)