from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends
from app.API.Dependencies.container import container
from app.API.Utilities.ApiResponse import ApiResponseHelper
from app.HR.Services.SalaryRateService import SalaryRateService
from app.HR.Repositories.SalaryRateRepository import SalaryRateRepository
from app.HR.Repositories.EmployeeRepository import EmployeeRepository
from app.HR.DTOs.SalaryRateDTO import SalaryRateCreateDTO, SalaryRateUpdateDTO
from app.HR.API.Requests.SalaryRateCreateRequest import SalaryRateCreateRequest
from app.HR.API.Requests.SalaryRateUpdateRequest import SalaryRateUpdateRequest
from app.HR.API.Response.SalaryRateResponse import SalaryRateResponse
from app.API.Dependencies.Authentication import get_current_user, get_current_admin_user
from app.Entities.Base.User import User

router = APIRouter()

def get_salary_rate_service() -> SalaryRateService:
    return container.resolve(SalaryRateService)

def get_salary_rate_repository() -> SalaryRateRepository:
    return container.resolve(SalaryRateRepository)

def get_employee_repository() -> EmployeeRepository:
    return container.resolve(EmployeeRepository)

@router.get("/employee/{employee_id}")
async def get_salary_rates_by_employee_id(employee_id: UUID, current_user: User = Depends(get_current_user)):
    try:
        if not current_user.is_admin:
            employee_repo = get_employee_repository()
            employee_profile_list = employee_repo.find_by_lambda(lambda e: e.user_id == current_user.id)
            
            if not employee_profile_list or employee_profile_list[0].id != employee_id:
                return ApiResponseHelper.error("You do not have permission to view these salary rates.", status_code=403)

        repo = get_salary_rate_repository()
        rates = repo.find_by_employee_id(employee_id)
        
        response = [SalaryRateResponse.model_validate(rate) for rate in rates]
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.post("/")
async def create_salary_rate(request: SalaryRateCreateRequest, current_admin: User = Depends(get_current_admin_user)):
    try:
        salary_rate_service = get_salary_rate_service()
        rate_dto = SalaryRateCreateDTO(**request.model_dump())
        
        created_rate = salary_rate_service.create_salary_rate(rate_dto)
        
        response = SalaryRateResponse.model_validate(created_rate)
        return ApiResponseHelper.success(response, "Salary rate created successfully.")
        
    except ValueError as ve:
        return ApiResponseHelper.error(str(ve), status_code=400)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.put("/{rate_id}")
async def update_salary_rate(rate_id: UUID, request: SalaryRateUpdateRequest, current_admin: User = Depends(get_current_admin_user)):
    try:
        salary_rate_service = get_salary_rate_service()
        rate_dto = SalaryRateUpdateDTO(**request.model_dump(exclude_unset=True))

        if not rate_dto.model_dump(exclude_unset=True):
             return ApiResponseHelper.error("No update data provided.", status_code=400)

        updated_rate = salary_rate_service.update_salary_rate(rate_id, rate_dto)
        
        if updated_rate is None:
            return ApiResponseHelper.error("Salary rate not found.", status_code=404)
            
        response = SalaryRateResponse.model_validate(updated_rate)
        return ApiResponseHelper.success(response, "Salary rate updated successfully.")

    except ValueError as ve:
        return ApiResponseHelper.error(str(ve), status_code=400)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.delete("/{rate_id}")
async def delete_salary_rate(rate_id: UUID, current_admin: User = Depends(get_current_admin_user)):
    try:
        salary_rate_service = get_salary_rate_service()
        success = salary_rate_service.delete_salary_rate(rate_id)
        
        if not success:
            return ApiResponseHelper.error("Salary rate not found.", status_code=404)
        
        return ApiResponseHelper.success(message="Salary rate deleted successfully.")
        
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)