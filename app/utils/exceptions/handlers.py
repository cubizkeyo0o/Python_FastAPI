from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

from app.utils.exceptions.common_exceptions import CommonException
from app.utils.exceptions.auth_exceptions import AuthException
from app.utils.exceptions.exception_status_map import exception_status_map

logger = logging.getLogger(__name__)

def build_rest_error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "code": status_code,
            "message": message
        }
    )

async def auth_exception_handler(request: Request, exc: AuthException):
    logger.warning(f"[AuthException] {exc.__class__.__name__}: {exc.message}")
    status_code = exception_status_map.get(type(exc), 401)
    return build_rest_error_response(status_code, exc.message)

async def common_exception_handler(request: Request, exc: CommonException):
    logger.warning(f"[BusinessException] {exc.__class__.__name__}: {exc.message}")
    status_code = exception_status_map.get(type(exc), 400)
    return build_rest_error_response(status_code, exc.message)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.info(f"[ValidationError] {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "Validation failed",
            "errors": exc.errors()
        }
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"[UnhandledException] {str(exc)}")
    return build_rest_error_response(500, "Internal server error")