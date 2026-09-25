"""Base renderer implementation providing common functionality."""

import base64
import io
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from app.domain.interfaces.renderer import Renderer
from app.domain.specs.vizspec import VizSpec
from app.domain.exceptions.base import RendererError
from app.infrastructure.themes.theme_engine import theme_engine

logger = logging.getLogger(__name__)


class BaseRenderer(Renderer, ABC):
    """Abstract base renderer with common export functionality.

    Provides shared logic for theme resolution, encoding extraction,
    and export format handling. Subclasses implement the actual
    chart rendering logic.
    """

    def __init__(self) -> None:
        """Initialize the base renderer."""
        self._name = self.__class__.__name__
        self._version = "1.0.0"

    def _resolve_theme(self, spec: VizSpec) -> Dict[str, Any]:
        """Resolve theme configuration from a VizSpec.

        Args:
            spec: The VizSpec containing theme information.

        Returns:
            Resolved theme configuration dictionary.
        """
        return theme_engine.resolve_theme(spec.theme)

    def _get_color_palette(self, spec: VizSpec) -> List[str]:
        """Get the color palette for a VizSpec.

        Args:
            spec: The VizSpec containing theme information.

        Returns:
            List of color hex strings.
        """
        palette = theme_engine.get_palette_for_spec(spec.theme)
        if spec.visual.color_palette:
            palette = spec.visual.color_palette
        return palette

    def _extract_data(self, spec: VizSpec) -> List[Dict[str, Any]]:
        """Extract data records from a VizSpec.

        Args:
            spec: The VizSpec containing data.

        Returns:
            List of data record dictionaries.

        Raises:
            RendererError: If data source is not inline or no records found.
        """
        if spec.data.source.value == "inline" and spec.data.records:
            return spec.data.records
        raise RendererError(
            message="Only inline data source is currently supported.",
            renderer_name=self._name,
            details={"data_source": spec.data.source.value},
        )

    def _get_encoding(self, spec: VizSpec) -> Dict[str, Any]:
        """Get encoding channels from a VizSpec.

        Args:
            spec: The VizSpec containing encoding.

        Returns:
            Encoding channels dictionary.
        """
        return spec.encoding or {}

    def _get_output_config(self, spec: VizSpec) -> Dict[str, Any]:
        """Get output configuration from a VizSpec.

        Args:
            spec: The VizSpec containing output config.

        Returns:
            Output configuration dictionary.
        """
        output = spec.output
        return {
            "format": output.format.value,
            "dpi": output.dpi,
            "scale": output.scale,
            "width": spec.layout.width,
            "height": spec.layout.height,
            "background_color": output.background_color or "#ffffff",
            "transparent": output.transparent,
        }

    def _encode_base64(self, data: bytes, mime_type: str = "image/png") -> str:
        """Encode binary data as a base64 data URI.

        Args:
            data: Binary data to encode.
            mime_type: MIME type of the data.

        Returns:
            Base64 data URI string.
        """
        encoded = base64.b64encode(data).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"

    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about this renderer.

        Returns:
            Dict with renderer name, version, and capabilities.
        """
        return {
            "name": self._name,
            "version": self._version,
            "supported_chart_types": self.get_supported_chart_types(),
            "supported_formats": ["png", "svg", "pdf", "html", "json", "base64"],
        }