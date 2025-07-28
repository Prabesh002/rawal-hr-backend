from fastapi import Depends, HTTPException, status
from app.Entities.Base.User import User
from app.HR.Entities.EmployeeEntity import EmployeeEntity
from app.HR.Repositories.EmployeeRepository import EmployeeRepository
from app.API.Dependencies.Authentication import get_current_user
from app.API.Dependencies.container import container

def get_current_employee(current_user: User = Depends(get_current_user)) -> EmployeeEntity:
    repo : EmployeeRepository = container.resolve(EmployeeRepository)
    employee = repo.find_by_id(current_user.id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The current user does not have an associated employee profile."
        )
    return employee