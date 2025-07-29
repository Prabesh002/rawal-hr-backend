from uuid import UUID
from fastapi import APIRouter
from app.API.Dependencies.container import container
from app.API.Utilities.ApiResponse import ApiResponseHelper
from app.HR.Repositories.EmployeeRepository import EmployeeRepository
from app.HR.Services.EmployeeService import EmployeeService
from app.HR.DTOs.EmployeeDTO import EmployeeCreateDTO, EmployeeUpdateDTO
from app.HR.API.Requests.EmployeeCreateRequest import EmployeeCreateRequest
from app.HR.API.Requests.EmployeeUpdateRequest import EmployeeUpdateRequest
from app.HR.API.Response.EmployeeResponse import EmployeeResponse

router = APIRouter()

def get_employee_service() -> EmployeeService:
    return container.resolve(EmployeeService)

def get_employee_repository() -> EmployeeRepository:
    return container.resolve(EmployeeRepository)

@router.get("/{employee_id}")
async def get_employee_by_id(employee_id: UUID):
    try:
        employee_repo = get_employee_repository()
        employee = employee_repo.find_by_id(employee_id)
        if not employee:
            return ApiResponseHelper.error("Employee not found.", status_code=404)
        
        response = EmployeeResponse.model_validate(employee)
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)

@router.get("/")
async def get_all_employees():
    try:
        employee_repo = get_employee_repository()
        employees = employee_repo.find_all()
        response = [EmployeeResponse.model_validate(emp) for emp in employees]
        return ApiResponseHelper.success(response)
    except Exception as e:
        return ApiResponseHelper.error(f"An unexpected error occurred: {e}", status_code=500)


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
