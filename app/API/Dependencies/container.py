from punq import Container
import punq
from app.Services.User.UserService import UserService
from app.Services.User.TokenService import TokenService
from app.Repositories.User.UserRepository import UserRepository
from app.Core.Database.ApplicationDatabaseContext import ApplicationDatabaseContext
from app.Core.Config.settings import settings
from sqlalchemy.orm import Session
from app.Core.AI.registration import register_ai_providers 
from app.Tools.Services.CalendarEventService import CalendarEventService
from app.Tools.Repositories.CalendarEventRepository import CalendarEventRepository

def create_container() -> Container:
    container = Container()

    register_ai_providers() 

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

    return container


container = create_container()