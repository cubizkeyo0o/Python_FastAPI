class AuthException(Exception):
    def __init__(self, message: str = "Authentication error"):
        self.message = message
        super().__init__(message)


class InvalidCredentialsException(AuthException):
    def __init__(self, message: str = "Invalid username or password"):
        super().__init__(message)


class TokenExpiredException(AuthException):
    def __init__(self, message: str = "Access token has expired"):
        super().__init__(message)


class MissingTokenException(AuthException):
    def __init__(self, message: str = "Missing token"):
        super().__init__(message)

class InvalidTokenException(AuthException):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message)


class UnauthorizedAccessException(AuthException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message)


class ForbiddenAccessException(AuthException):
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message)


class RefreshTokenExpiredException(AuthException):
    def __init__(self, message: str = "Refresh token has expired"):
        super().__init__(message)

class BlackListTokenException(AuthException):
    def __init__(self, message: str = "Token is blacklisted"):
        super().__init__(message)