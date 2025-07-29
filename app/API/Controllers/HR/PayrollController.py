from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends
from app.API.Dependencies.container import container
from app.API.Utilities.ApiResponse import ApiResponseHelper
from app.HR.Services.PayrollService import PayrollService
from app.HR.Repositories.PayrollRepository import PayrollRepository
from app.HR.Repositories.EmployeeRepository import EmployeeRepository
from app.HR.DTOs.PayrollDTO import PayrollCreateDTO, PayrollUpdateDTO
from app.HR.API.Requests.PayrollCreateRequest import PayrollCreateRequest
from app.HR.API.Requests.PayrollUpdateRequest import PayrollUpdateRequest
from app.HR.API.Response.PayrollResponse import PayrollResponse
from app.API.Dependencies.Authentication import get_current_user, get_current_admin_user
from app.Entities.Base.User import User

router = APIRouter()

def get_payroll_service() -> PayrollService:
    return container.resolve(PayrollService)

def get_payroll_repository() -> PayrollRepository:
    return container.resolve(PayrollRepository)

def get_employee_repository() -> EmployeeRepository:
    return container.resolve(EmployeeRepository)

@router.get("/")
async def get_all_payrolls(current_user: User = Depends(get_current_user)):
    try:
        payroll_repo = get_payroll_repository()
        
        if current_user.is_admin:
            payrolls = payroll_repo.find_all()
        else:
            employee_repo = get_employee_repository()
            employee_profile_list = employee_repo.find_by_lambda(lambda e: e.user_id == current_user.id)
            
            if not employee_profile_list:
                return ApiResponseHelper.success([], "User has no associated employee profile.")
                
            employee_profile = employee_profile_list[0]
            payrolls = payroll_repo.find_by_employee_id(employee_profile.id)

        response = [PayrollResponse.model_validate(p) for p in payrolls]
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.get("/{payroll_id}")
async def get_payroll_by_id(payroll_id: UUID, current_user: User = Depends(get_current_user)):
    try:
        repo = get_payroll_repository()
        payroll = repo.find_by_id(payroll_id)
        if not payroll:
            return ApiResponseHelper.error("Payroll record not found.", status_code=404)
        
        if not current_user.is_admin:
            employee_repo = get_employee_repository()
            employee_profile_list = employee_repo.find_by_lambda(lambda e: e.user_id == current_user.id)
            if not employee_profile_list or payroll.employee_id != employee_profile_list[0].id:
                return ApiResponseHelper.error("You do not have permission to view this payroll record.", status_code=403)
        
        response = PayrollResponse.model_validate(payroll)
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.post("/")
async def create_payroll_record(request: PayrollCreateRequest, current_admin: User = Depends(get_current_admin_user)):
    try:
        payroll_service = get_payroll_service()
        payroll_dto = PayrollCreateDTO(**request.model_dump())
        
        created_payroll = payroll_service.create_payroll(payroll_dto)
        
        response = PayrollResponse.model_validate(created_payroll)
        return ApiResponseHelper.success(response, "Payroll record created successfully.")
        
    except ValueError as ve:
        return ApiResponseHelper.error(str(ve), status_code=400)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.put("/{payroll_id}")
async def update_payroll_record(payroll_id: UUID, request: PayrollUpdateRequest, current_admin: User = Depends(get_current_admin_user)):
    try:
        payroll_service = get_payroll_service()
        payroll_dto = PayrollUpdateDTO(**request.model_dump(exclude_unset=True))

        if not payroll_dto.model_dump(exclude_unset=True):
             return ApiResponseHelper.error("No update data provided.", status_code=400)

        updated_payroll = payroll_service.update_payroll(payroll_id, payroll_dto)
        
        if updated_payroll is None:
            return ApiResponseHelper.error("Payroll record not found.", status_code=404)
            
        response = PayrollResponse.model_validate(updated_payroll)
        return ApiResponseHelper.success(response, "Payroll record updated successfully.")

    except ValueError as ve:
        return ApiResponseHelper.error(str(ve), status_code=400)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.delete("/{payroll_id}")
async def delete_payroll_record(payroll_id: UUID, current_admin: User = Depends(get_current_admin_user)):
    try:
        payroll_service = get_payroll_service()
        success = payroll_service.delete_payroll(payroll_id)
        
        if not success:
            return ApiResponseHelper.error("Payroll record not found.", status_code=404)
        
        return ApiResponseHelper.success(message="Payroll record deleted successfully.")
        
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)