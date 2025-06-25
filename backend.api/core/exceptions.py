# AI-Generated
"""
Custom Exception Classes

Defines custom exceptions for HealthRankDash API with proper
HTTP status codes and error messaging.
"""

from typing import Optional, Dict, Any


class HealthRankException(Exception):
    """Base exception class for HealthRankDash API."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_type: str = "internal_error",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(HealthRankException):
    """Raised when request validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=422,
            error_type="validation_error",
            details=details
        )


class NotFoundError(HealthRankException):
    """Raised when requested resource is not found."""
    
    def __init__(self, message: str, resource_type: str = "resource"):
        super().__init__(
            message=message,
            status_code=404,
            error_type="not_found",
            details={"resource_type": resource_type}
        )


class BadRequestError(HealthRankException):
    """Raised when request parameters are invalid."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=400,
            error_type="bad_request",
            details=details
        )


class DataProcessingError(HealthRankException):
    """Raised when data processing fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_type="data_processing_error",
            details=details
        )