"""Data specification for VizSpec."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, model_validator


class DataSource(str, Enum):
    """Types of data sources supported."""

    INLINE = "inline"
    URL = "url"
    FILE = "file"
    DATABASE = "database"
    REFERENCE = "reference"
    S3 = "s3"
    AZURE = "azure"
    GCS = "gcs"


class DataRecord(BaseModel):
    """A single data record as a key-value mapping."""

    model_config = {"extra": "allow", "populate_by_name": True}

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)


class DataSpec(BaseModel):
    """Specification for data used in a visualization.

    Supports inline records, URL references, file paths,
    database queries, and cloud storage references.
    """

    source: DataSource = Field(default=DataSource.INLINE, description="Type of data source.")
    records: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Inline data records as list of dicts."
    )
    url: Optional[str] = Field(default=None, description="URL to fetch data from.")
    file_path: Optional[str] = Field(default=None, description="Path to local data file.")
    query: Optional[str] = Field(default=None, description="Database query string.")
    connection_string: Optional[str] = Field(
        default=None, description="Database connection string."
    )
    storage_bucket: Optional[str] = Field(
        default=None, description="Cloud storage bucket name."
    )
    storage_key: Optional[str] = Field(
        default=None, description="Cloud storage object key/path."
    )
    format: Optional[str] = Field(default="json", description="Data format (json, csv, parquet).")
    data_schema: Optional[Dict[str, Any]] = Field(
        default=None, alias="schema", description="Optional schema definition for the data."
    )
    reference_id: Optional[str] = Field(
        default=None, description="Reference ID for stored/pre-registered data."
    )

    @model_validator(mode="after")
    def validate_source_has_data(self) -> "DataSpec":
        """Validate that the data source has the required fields."""
        if self.source == DataSource.URL and not self.url:
            raise ValueError("URL data source requires 'url' field.")
        if self.source == DataSource.FILE and not self.file_path:
            raise ValueError("File data source requires 'file_path' field.")
        return self
