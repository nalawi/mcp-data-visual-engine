"""Renderer interface - the core abstraction for all renderers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from app.domain.specs.vizspec import VizSpec


class Renderer(ABC):
    """Abstract base class for all visualization renderers.

    All renderers must implement this interface. The application layer
    never imports renderer implementations directly - only this interface.

    This enables adding new renderers (Matplotlib, Altair, Bokeh, etc.)
    without modifying any application or API code.
    """

    @abstractmethod
    def render(self, spec: VizSpec) -> Any:
        """Generate a visualization from a VizSpec.

        Args:
            spec: The validated VizSpec to render.

        Returns:
            The rendered visualization object (renderer-specific).

        Raises:
            RendererError: If rendering fails.
        """
        ...

    @abstractmethod
    def render_png(self, spec: VizSpec, **kwargs: Any) -> bytes:
        """Render and export as PNG bytes.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            PNG image bytes.

        Raises:
            RendererError: If rendering or export fails.
        """
        ...

    @abstractmethod
    def render_svg(self, spec: VizSpec, **kwargs: Any) -> str:
        """Render and export as SVG string.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            SVG XML string.

        Raises:
            RendererError: If rendering or export fails.
        """
        ...

    @abstractmethod
    def render_pdf(self, spec: VizSpec, **kwargs: Any) -> bytes:
        """Render and export as PDF bytes.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            PDF bytes.

        Raises:
            RendererError: If rendering or export fails.
        """
        ...

    @abstractmethod
    def render_html(self, spec: VizSpec, **kwargs: Any) -> str:
        """Render and export as HTML string.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options (include_plotlyjs, full_html, etc.).

        Returns:
            HTML string.

        Raises:
            RendererError: If rendering or export fails.
        """
        ...

    @abstractmethod
    def render_json(self, spec: VizSpec, **kwargs: Any) -> str:
        """Render and export as JSON string (plotly JSON format).

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            JSON string of the figure data.

        Raises:
            RendererError: If rendering or export fails.
        """
        ...

    @abstractmethod
    def render_base64(self, spec: VizSpec, **kwargs: Any) -> str:
        """Render and export as base64-encoded image string.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            Base64-encoded image string with data URI prefix.

        Raises:
            RendererError: If rendering or export fails.
        """
        ...

    @abstractmethod
    def get_supported_chart_types(self) -> List[str]:
        """Get list of chart types supported by this renderer.

        Returns:
            List of chart type strings.
        """
        ...

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about this renderer.

        Returns:
            Dict with renderer name, version, capabilities, etc.
        """
        ...


class RendererPlugin(ABC):
    """Interface for renderer plugins that can be registered dynamically."""

    @abstractmethod
    def create_renderer(self) -> Renderer:
        """Create and return a renderer instance.

        Returns:
            A Renderer implementation.
        """
        ...

    @abstractmethod
    def get_plugin_metadata(self) -> Dict[str, Any]:
        """Get metadata about this plugin.

        Returns:
            Dict with plugin name, version, author, etc.
        """
        ...