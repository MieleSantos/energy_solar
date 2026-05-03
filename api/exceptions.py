class ApiError(Exception):
    """Base exception for predictable API failures."""

    def __init__(self, message: str, status_code: int = 400, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class NotFoundError(ApiError):
    """Raised when an entity is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404)
