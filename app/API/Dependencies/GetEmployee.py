from fastapi import Depends, HTTPException, status
from app.Entities.Base.User import User
from app.HR.Entities.EmployeeEntity import EmployeeEntity
from app.HR.Repositories.EmployeeRepository import EmployeeRepository
from app.API.Dependencies.Authentication import get_current_user
from app.API.Dependencies.container import container
from app.Logger import get_logger

logger = get_logger(__name__)

def get_current_employee(current_user: User = Depends(get_current_user)) -> EmployeeEntity:
    repo : EmployeeRepository = container.resolve(EmployeeRepository)
    employee = repo.find_by_lambda(lambda e: e.user_id == current_user.id)

    employeeOne = employee[0] if employee else None

    if not employeeOne:
        logger.warning(f"User {current_user.id} does not have an associated employee profile.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user does not have an associated employee profile."
        )
    return employeeOne