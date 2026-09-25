"""Base domain exceptions for the DV1 Visualization Engine."""

from typing import Any, Dict, List, Optional


class DV1Error(Exception):
    """Base exception for all DV1 Visualization Engine errors."""

    def __init__(
        self,
        message: str,
        code: str = "UNKNOWN_ERROR",
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            code: Machine-readable error code.
            details: Additional error details.
            status_code: HTTP status code for API responses.
        """
        self.message = message
        self.code = code
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to a serializable dictionary.

        Returns:
            Dict with error information.
        """
        return {
            "error": True,
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class ValidationError(DV1Error):
    """Raised when VizSpec validation fails."""

    def __init__(
        self,
        message: str,
        field_errors: Optional[List[Dict[str, Any]]] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize validation error.

        Args:
            message: Error message.
            field_errors: List of field-specific validation errors.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details={**(details or {}), "field_errors": field_errors or []},
            status_code=422,
        )


class RendererError(DV1Error):
    """Raised when a renderer fails to render a visualization."""

    def __init__(
        self,
        message: str,
        renderer_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize renderer error.

        Args:
            message: Error message.
            renderer_name: Name of the renderer that failed.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="RENDERER_ERROR",
            details={**(details or {}), "renderer": renderer_name or "unknown"},
            status_code=500,
        )


class TransformationError(DV1Error):
    """Raised when a data transformation fails."""

    def __init__(
        self,
        message: str,
        transform_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize transformation error.

        Args:
            message: Error message.
            transform_name: Name of the transformation that failed.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="TRANSFORMATION_ERROR",
            details={**(details or {}), "transform": transform_name or "unknown"},
            status_code=422,
        )


class StorageError(DV1Error):
    """Raised when a storage operation fails."""

    def __init__(
        self,
        message: str,
        storage_backend: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize storage error.

        Args:
            message: Error message.
            storage_backend: Name of the storage backend.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="STORAGE_ERROR",
            details={**(details or {}), "backend": storage_backend or "unknown"},
            status_code=500,
        )


class CacheError(DV1Error):
    """Raised when a cache operation fails."""

    def __init__(
        self,
        message: str,
        cache_backend: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize cache error.

        Args:
            message: Error message.
            cache_backend: Name of the cache backend.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="CACHE_ERROR",
            details={**(details or {}), "backend": cache_backend or "unknown"},
            status_code=500,
        )


class AuthenticationError(DV1Error):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize authentication error.

        Args:
            message: Error message.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            details=details or {},
            status_code=401,
        )


class AuthorizationError(DV1Error):
    """Raised when authorization fails."""

    def __init__(
        self,
        message: str = "Not authorized",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize authorization error.

        Args:
            message: Error message.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            details=details or {},
            status_code=403,
        )


class RateLimitError(DV1Error):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize rate limit error.

        Args:
            message: Error message.
            retry_after: Seconds to wait before retrying.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="RATE_LIMIT_ERROR",
            details={**(details or {}), "retry_after": retry_after or 60},
            status_code=429,
        )


class NotFoundError(DV1Error):
    """Raised when a requested resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize not found error.

        Args:
            message: Error message.
            resource_type: Type of resource not found.
            resource_id: ID of resource not found.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="NOT_FOUND",
            details={
                **(details or {}),
                "resource_type": resource_type or "unknown",
                "resource_id": resource_id or "unknown",
            },
            status_code=404,
        )