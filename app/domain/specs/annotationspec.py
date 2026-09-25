"""Annotation specification for VizSpec."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class AnnotationType(str, Enum):
    """Types of annotations supported."""

    MAXIMUM = "maximum"
    MINIMUM = "minimum"
    AVERAGE = "average"
    MEDIAN = "median"
    REGRESSION = "regression"
    TREND_LINE = "trend_line"
    MOVING_AVERAGE = "moving_average"
    TARGET_LINE = "target_line"
    REFERENCE_LINE = "reference_line"
    FORECAST = "forecast"
    CONFIDENCE_INTERVAL = "confidence_interval"
    ARROW = "arrow"
    CALLOUT = "callout"
    TEXT = "text"
    LOGO = "logo"
    WATERMARK = "watermark"
    SHAPE = "shape"
    HIGHLIGHT = "highlight"


class AnnotationSpec(BaseModel):
    """Specification for a single annotation on a visualization."""

    type: AnnotationType = Field(..., description="Type of annotation.")
    label: Optional[str] = Field(default=None, description="Annotation label text.")
    value: Optional[Union[float, str, Dict[str, Any]]] = Field(
        default=None, description="Annotation value or configuration."
    )
    x: Optional[Union[float, str]] = Field(default=None, description="X position or data reference.")
    y: Optional[Union[float, str]] = Field(default=None, description="Y position or data reference.")
    xref: str = Field(default="x", description="X coordinate reference system.")
    yref: str = Field(default="y", description="Y coordinate reference system.")
    color: Optional[str] = Field(default=None, description="Annotation color.")
    font_size: Optional[int] = Field(default=None, description="Annotation font size.")
    opacity: float = Field(default=0.8, ge=0.0, le=1.0, description="Annotation opacity.")
    line_width: int = Field(default=2, ge=0, description="Annotation line width.")
    line_dash: Optional[str] = Field(default=None, description="Annotation line dash pattern.")
    arrow_head_length: Optional[float] = Field(default=None, description="Arrow head length.")
    arrow_head_width: Optional[float] = Field(default=None, description="Arrow head width.")
    arrow_side: Optional[str] = Field(default=None, description="Arrow side (start, end, both).")
    border_color: Optional[str] = Field(default=None, description="Border color for callout.")
    border_width: int = Field(default=0, ge=0, description="Border width for callout.")
    background_color: Optional[str] = Field(default=None, description="Background color for text.")
    align: str = Field(default="center", description="Text alignment (left, center, right).")
    ax: Optional[float] = Field(default=None, description="Arrow head x offset.")
    ay: Optional[float] = Field(default=None, description="Arrow head y offset.")
    custom: Dict[str, Any] = Field(default_factory=dict, description="Custom annotation properties.")