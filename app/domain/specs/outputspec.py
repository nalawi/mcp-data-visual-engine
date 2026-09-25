"""Output specification for VizSpec - defines export format and quality."""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class OutputFormat(str, Enum):
    """Supported output formats."""

    PNG = "png"
    SVG = "svg"
    PDF = "pdf"
    HTML = "html"
    JSON = "json"
    WEBP = "webp"
    JPEG = "jpeg"
    BASE64 = "base64"
    ZIP = "zip"


class ExportQuality(str, Enum):
    """Export quality presets."""

    DRAFT = "draft"
    STANDARD = "standard"
    HIGH = "high"
    RETINA = "retina"


class OutputSpec(BaseModel):
    """Output specification controlling export format and quality."""

    format: OutputFormat = Field(default=OutputFormat.PNG, description="Output format.")
    quality: ExportQuality = Field(default=ExportQuality.STANDARD, description="Export quality.")
    dpi: int = Field(default=150, ge=72, le=600, description="Output DPI (72-600).")
    scale: float = Field(default=1.0, ge=0.5, le=4.0, description="Output scale factor.")
    background_color: Optional[str] = Field(default=None, description="Output background color.")
    transparent: bool = Field(default=False, description="Transparent background.")
    include_plotlyjs: bool = Field(default=True, description="Include Plotly JS for HTML output.")
    full_html: bool = Field(default=True, description="Full HTML page vs. div-only.")
    max_width: Optional[int] = Field(default=None, description="Maximum output width.")
    max_height: Optional[int] = Field(default=None, description="Maximum output height.")
    file_name: Optional[str] = Field(default=None, description="Output file name (without extension).")
    compression: Optional[int] = Field(default=None, ge=0, le=9, description="Compression level (0-9).")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Output metadata.")
    custom: Dict[str, Any] = Field(default_factory=dict, description="Custom output properties.")