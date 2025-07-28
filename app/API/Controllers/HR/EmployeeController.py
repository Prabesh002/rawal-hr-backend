from uuid import UUID
from fastapi import APIRouter
from app.API.Dependencies.container import container
from app.API.Utilities.ApiResponse import ApiResponseHelper
from app.HR.Services.EmployeeService import EmployeeService
from app.HR.DTOs.EmployeeDTO import EmployeeCreateDTO, EmployeeUpdateDTO
from app.HR.API.Requests.EmployeeCreateRequest import EmployeeCreateRequest
from app.HR.API.Requests.EmployeeUpdateRequest import EmployeeUpdateRequest
from app.HR.API.Response.EmployeeResponse import EmployeeResponse

router = APIRouter()

def get_employee_service() -> EmployeeService:
    return container.resolve(EmployeeService)


@router.post("/")
async def create_employee(request: EmployeeCreateRequest):
    try:
        employee_service = get_employee_service()
        employee_dto = EmployeeCreateDTO(**request.model_dump())
        created_employee = employee_service.create_employee(employee_dto)
        response = EmployeeResponse.model_validate(created_employee)
        return ApiResponseHelper.success(response, "Employee created successfully.")
    except ValueError as ve:
        return ApiResponseHelper.error(str(ve), status_code=400)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)



@router.put("/{employee_id}")
async def update_employee(employee_id: UUID, request: EmployeeUpdateRequest):
    try:
        employee_service = get_employee_service()
        employee_dto = EmployeeUpdateDTO(**request.model_dump(exclude_unset=True))
        if not employee_dto.model_dump(exclude_unset=True):
            return ApiResponseHelper.error("No update data provided.", status_code=400)
        updated_employee = employee_service.update_employee(employee_id, employee_dto)
        if updated_employee is None:
            return ApiResponseHelper.error("Employee not found.", status_code=404)
        response = EmployeeResponse.model_validate(updated_employee)
        return ApiResponseHelper.success(response, "Employee updated successfully.")
    except ValueError as ve:
        return ApiResponseHelper.error(str(ve), status_code=400)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)


@router.delete("/{employee_id}")
async def delete_employee(employee_id: UUID):
    try:
        employee_service = get_employee_service()
        success = employee_service.delete_employee(employee_id)
        if not success:
            return ApiResponseHelper.error("Employee not found.", status_code=404)
        return ApiResponseHelper.success(message="Employee deleted successfully.")
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)
