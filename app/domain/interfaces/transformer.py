"""Transformer interface for data transformation pipeline."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import pandas as pd


class DataTransformer(ABC):
    """Interface for data transformation operations.

    Each transformation type implements this interface to perform
    a specific data transformation on a pandas DataFrame.
    """

    @abstractmethod
    def transform(self, data: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Apply a transformation to the data.

        Args:
            data: Input DataFrame.
            params: Transformation parameters.

        Returns:
            Transformed DataFrame.

        Raises:
            TransformationError: If the transformation fails.
        """
        ...

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this transformation.

        Returns:
            Transformation type name.
        """
        ...


class TransformerRegistry(ABC):
    """Interface for registering and retrieving data transformers."""

    @abstractmethod
    def register(self, name: str, transformer: DataTransformer) -> None:
        """Register a transformer.

        Args:
            name: Transformation type name.
            transformer: Transformer implementation.
        """
        ...

    @abstractmethod
    def get(self, name: str) -> DataTransformer:
        """Get a transformer by name.

        Args:
            name: Transformation type name.

        Returns:
            Transformer implementation.

        Raises:
            KeyError: If transformer is not registered.
        """
        ...

    @abstractmethod
    def get_all(self) -> Dict[str, DataTransformer]:
        """Get all registered transformers.

        Returns:
            Dict mapping names to transformers.
        """
        ...