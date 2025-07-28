from uuid import UUID
from fastapi import APIRouter
from app.API.Dependencies.container import container
from app.API.Utilities.ApiResponse import ApiResponseHelper
from app.HR.Services.PayrollService import PayrollService
from app.HR.DTOs.PayrollDTO import PayrollCreateDTO, PayrollUpdateDTO
from app.HR.API.Requests.PayrollCreateRequest import PayrollCreateRequest
from app.HR.API.Requests.PayrollUpdateRequest import PayrollUpdateRequest
from app.HR.API.Response.PayrollResponse import PayrollResponse

router = APIRouter()

def get_payroll_service() -> PayrollService:
    return container.resolve(PayrollService)

@router.post("/")
async def create_payroll_record(request: PayrollCreateRequest):
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
async def update_payroll_record(payroll_id: UUID, request: PayrollUpdateRequest):
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
async def delete_payroll_record(payroll_id: UUID):
    try:
        payroll_service = get_payroll_service()
        success = payroll_service.delete_payroll(payroll_id)
        
        if not success:
            return ApiResponseHelper.error("Payroll record not found.", status_code=404)
        
        return ApiResponseHelper.success(message="Payroll record deleted successfully.")
        
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)