from fastapi import APIRouter
from app.API.Controllers.UserController import router as user_router
from app.API.Controllers.HR.EmployeeController import router as employee_router
from app.API.Controllers.HR.PayrollController import router as payroll_router
from app.API.Controllers.HR.SalaryRateController import router as salary_rate_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/auth", tags=["users"])
api_router.include_router(employee_router, prefix="/hr/employees", tags=["HR - Employees"])
api_router.include_router(payroll_router, prefix="/hr/payrolls", tags=["HR - Payroll"])
api_router.include_router(salary_rate_router, prefix="/hr/salary-rates", tags=["HR - Salary Rates"])