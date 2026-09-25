"""Storage interface for persisting visualization outputs."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class StorageBackend(ABC):
    """Interface for storage backends (local, S3, Azure, GCS, MinIO)."""

    @abstractmethod
    async def save(self, key: str, data: bytes, content_type: str, **kwargs: Any) -> str:
        """Save data to storage.

        Args:
            key: Storage key/path.
            data: Binary data to store.
            content_type: MIME type of the data.
            **kwargs: Additional storage options.

        Returns:
            URL or path to the stored data.

        Raises:
            StorageError: If save fails.
        """
        ...

    @abstractmethod
    async def load(self, key: str) -> Tuple[bytes, str]:
        """Load data from storage.

        Args:
            key: Storage key/path.

        Returns:
            Tuple of (data bytes, content type).

        Raises:
            StorageError: If load fails or key not found.
        """
        ...

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete data from storage.

        Args:
            key: Storage key/path.

        Returns:
            True if deleted, False if not found.

        Raises:
            StorageError: If delete fails.
        """
        ...

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists in storage.

        Args:
            key: Storage key/path.

        Returns:
            True if key exists.
        """
        ...

    @abstractmethod
    async def list_keys(self, prefix: str) -> List[str]:
        """List all keys with a given prefix.

        Args:
            prefix: Key prefix to filter by.

        Returns:
            List of matching keys.
        """
        ...


class CacheBackend(ABC):
    """Interface for cache backends (Redis, in-memory, etc.)."""

    @abstractmethod
    async def get(self, key: str) -> Optional[bytes]:
        """Get cached data.

        Args:
            key: Cache key.

        Returns:
            Cached bytes or None if not found.
        """
        ...

    @abstractmethod
    async def set(self, key: str, data: bytes, ttl: Optional[int] = None) -> None:
        """Set cached data.

        Args:
            key: Cache key.
            data: Data to cache.
            ttl: Time-to-live in seconds.
        """
        ...

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete cached data.

        Args:
            key: Cache key.

        Returns:
            True if deleted.
        """
        ...

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cached data."""
        ...

    @abstractmethod
    async def get_ttl(self, key: str) -> Optional[int]:
        """Get remaining TTL for a cached key.

        Args:
            key: Cache key.

        Returns:
            Remaining TTL in seconds, or None if key doesn't exist.
        """
        ...