"""Custom exceptions for the portfolio application"""


class PortfolioException(Exception):
    """Base exception for all portfolio-related errors"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(PortfolioException):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, 400)


class DatabaseError(PortfolioException):
    """Raised when database operations fail"""
    def __init__(self, message: str):
        super().__init__(message, 500)


class AuthenticationError(PortfolioException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class AuthorizationError(PortfolioException):
    """Raised when user lacks permission for an action"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403)


class NotFoundError(PortfolioException):
    """Raised when a resource is not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class RateLimitError(PortfolioException):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, 429)


class FileUploadError(PortfolioException):
    """Raised when file upload fails"""
    def __init__(self, message: str):
        super().__init__(message, 400)
