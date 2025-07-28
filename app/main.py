from contextlib import asynccontextmanager
from app.API.Middleware.AuthenticationMiddleware import AuthenticationMiddleware
from app.API.Middleware.DbSessionMiddleware import SessionCleanupMiddleware
from app.API.Middleware.DbSessionMiddleware import SessionCleanupMiddleware
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.router import api_router
from app.API.Utilities.exception_handlers import unprocessable_entity_handler, http_exception_handler, generic_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    #starup ya
    yield


app = FastAPI(
    title="Rawal HR",
    description="API",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(
    SessionCleanupMiddleware
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, unprocessable_entity_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}