class CommonException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotMatchException(CommonException):
    pass

class EntityNotFoundException(CommonException):
    pass

class ConflictException(CommonException):
    pass

class InvalidOperationException(CommonException):
    pass

class BusinessRuleViolationException(CommonException):
    pass

class InternalServerErrorException(CommonException):
    pass

class RequiredException(CommonException):
    pass