"""
Custom error classes
"""


class APIError(Exception):
    """Base API error"""
    def __init__(self, message, status_code=500):
        super().__init__()
        self.message = message
        self.status_code = status_code
    
    def __str__(self):
        return self.message


class BadRequestError(APIError):
    """400 Bad Request"""
    def __init__(self, message):
        super().__init__(message, 400)


class UnauthorizedError(APIError):
    """401 Unauthorized"""
    def __init__(self, message):
        super().__init__(message, 401)


class ForbiddenError(APIError):
    """403 Forbidden"""
    def __init__(self, message):
        super().__init__(message, 403)


class NotFoundError(APIError):
    """404 Not Found"""
    def __init__(self, message):
        super().__init__(message, 404)


class ConflictError(APIError):
    """409 Conflict"""
    def __init__(self, message):
        super().__init__(message, 409)


class ValidationError(APIError):
    """422 Unprocessable Entity"""
    def __init__(self, message):
        super().__init__(message, 422)


class InternalServerError(APIError):
    """500 Internal Server Error"""
    def __init__(self, message):
        super().__init__(message, 500)
