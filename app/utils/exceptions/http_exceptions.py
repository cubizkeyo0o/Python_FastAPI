from fastapi import HTTPException, status
from typing import Any

class BadRequestException(HTTPException):
    def __init__(self, detail: Any = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: Any = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: Any = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ConflictException(HTTPException):
    def __init__(self, detail: Any = "Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UnprocessableEntityException(HTTPException):
    def __init__(self, detail: Any = "Unprocessable entity"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class TooManyRequestsException(HTTPException):
    def __init__(self, detail: Any = "Too many requests"):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)


class InternalServerErrorException(HTTPException):
    def __init__(self, detail: Any = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)