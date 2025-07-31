import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv

from app.api.routers.index import Tags
from app.api.routers.v1.user import router as user_router
from app.api.routers.v1.auth import router as auth_router
from app.api.routers.v1.openai import router as openai_router
from app.api.routers.v1.role import router as role_router
from app.api.routers.v1.openai import protected_router as openai_protected_router
from app.api.routers.v1.session import protected_router as session_protected_router
from app.api.routers.v1.message import protected_router as message_protected_router
from app.utils.exceptions.handlers import (
    common_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
    auth_exception_handler
)
from app.utils.exceptions.common_exceptions import CommonException
from app.utils.exceptions.auth_exceptions import AuthException
from app.infrastructure.database.database_session import sessionmanager
from app.infrastructure.database.database_init import Base

load_dotenv()  # read file .env

app = FastAPI(
    title=os.getenv("APP_NAME"),
    version=os.getenv("API_VERSION"),
    openapi_tags=Tags,
)

async def startup():
    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Register global exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AuthException, auth_exception_handler)
app.add_exception_handler(CommonException, common_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(user_router)
app.include_router(role_router)
app.include_router(auth_router)
app.include_router(openai_router)
app.include_router(openai_protected_router)
app.include_router(session_protected_router)
app.include_router(message_protected_router)