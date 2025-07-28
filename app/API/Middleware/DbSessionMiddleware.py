from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session
from app.Core.Database.ApplicationDatabaseContext import createdSessions
from app.Logger import get_logger


logger = get_logger(__name__)

class SessionCleanupMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        while createdSessions:
            db:Session = createdSessions.pop()
            if(db.is_active):
                db.close()
        return response