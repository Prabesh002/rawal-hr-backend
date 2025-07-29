from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from app.API.Dependencies.container import container
from app.API.Utilities.ApiResponse import ApiResponseHelper
from app.Services.User.TokenService import TokenService
from app.Repositories.User.UserRepository import UserRepository

PUBLIC_PATHS = [
    "/api/v1/auth/login",
    "/api/v1/auth/register",
    "/docs",
    "/openapi.json",
    "/health"
]

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.method == "OPTIONS":
            return await call_next(request)

        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return ApiResponseHelper.error(
                "Authentication token is missing or invalid.",
                status_code=401
            )

        token = auth_header.split(" ")[1]

        try:
            token_service : TokenService = container.resolve(TokenService)
            user_repository: UserRepository = container.resolve(UserRepository)

            payload = token_service.verify_token(token)
            if payload is None:
                return ApiResponseHelper.error("Invalid or expired token.", status_code=401)

            username = payload.get("sub")
            if username is None:
                return ApiResponseHelper.error("Invalid token payload.", status_code=401)

            db_user = user_repository.get_by_username(username)
            if db_user is None:
                return ApiResponseHelper.error("User not found.", status_code=401)

            request.state.user = db_user

        except Exception as e:
            return ApiResponseHelper.error(f"Authentication error: {e}", status_code=401)

        return await call_next(request)