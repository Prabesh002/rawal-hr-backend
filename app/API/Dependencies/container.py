from punq import Container
import punq
from app.Services.User.UserService import UserService
from app.Services.User.TokenService import TokenService
from app.Repositories.User.UserRepository import UserRepository
from app.Core.Database.ApplicationDatabaseContext import ApplicationDatabaseContext
from app.Core.Config.settings import settings
from sqlalchemy.orm import Session
from app.HR.Repositories.EmployeeRepository import EmployeeRepository
from app.HR.Repositories.AttendanceRepository import AttendanceRepository
from app.HR.Repositories.TimeLogRepository import TimeLogRepository
from app.HR.Repositories.SalaryRateRepository import SalaryRateRepository
from app.HR.Repositories.PayrollRepository import PayrollRepository
from app.HR.Services.EmployeeService import EmployeeService
from app.HR.Services.AttendanceService import AttendanceService
from app.HR.Services.TimeLogService import TimeLogService
from app.HR.Services.SalaryRateService import SalaryRateService
from app.HR.Services.PayrollService import PayrollService
from app.Tools.Services.CalendarEventService import CalendarEventService
from app.Tools.Repositories.CalendarEventRepository import CalendarEventRepository

def create_container() -> Container:
    container = Container()


    db_context = ApplicationDatabaseContext(settings.database_url)
    container.register(ApplicationDatabaseContext, instance=db_context)
    def session_factory() -> Session:
        return next(db_context.get_db())


    container.register(Session, factory=session_factory, scope=punq.Scope.transient)

    container.register(UserRepository)

    container.register(TokenService)
    container.register(UserService)

    container.register(CalendarEventRepository, scope=punq.Scope.transient)
    container.register(CalendarEventService, scope=punq.Scope.transient)

    #hr

    container.register(EmployeeRepository, scope=punq.Scope.transient)
    container.register(AttendanceRepository, scope=punq.Scope.transient)
    container.register(TimeLogRepository, scope=punq.Scope.transient)
    container.register(SalaryRateRepository, scope=punq.Scope.transient)
    container.register(PayrollRepository, scope=punq.Scope.transient)

    container.register(EmployeeService, scope=punq.Scope.transient)
    container.register(AttendanceService, scope=punq.Scope.transient)
    container.register(TimeLogService, scope=punq.Scope.transient)
    container.register(SalaryRateService, scope=punq.Scope.transient)
    container.register(PayrollService, scope=punq.Scope.transient)


    return container


container = create_container()