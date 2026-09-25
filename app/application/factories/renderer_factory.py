"""Renderer factory - creates renderer instances using the Factory and Strategy patterns."""

import logging
from typing import Any, Dict, List, Optional, Type

from app.domain.interfaces.renderer import Renderer, RendererPlugin
from app.domain.exceptions.base import RendererError
from app.infrastructure.renderers.plotly.plotly_renderer import PlotlyRenderer

logger = logging.getLogger(__name__)


class RendererFactory:
    """Factory for creating and managing renderer instances.

    Uses the Factory pattern to create renderers and the Strategy pattern
    to select the appropriate renderer for a given chart type.

    New renderers can be registered as plugins without modifying this class.
    """

    def __init__(self) -> None:
        """Initialize the renderer factory with default renderers."""
        self._renderers: Dict[str, Renderer] = {}
        self._plugins: Dict[str, RendererPlugin] = {}
        self._default_renderer: Optional[str] = None
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default renderers."""
        plotly = PlotlyRenderer()
        self._renderers["plotly"] = plotly
        self._default_renderer = "plotly"

    def register_renderer(self, name: str, renderer: Renderer) -> None:
        """Register a renderer instance.

        Args:
            name: Unique name for the renderer.
            renderer: Renderer instance.
        """
        self._renderers[name] = renderer
        logger.info(f"Registered renderer: {name}")

    def register_plugin(self, plugin: RendererPlugin) -> None:
        """Register a renderer plugin.

        Args:
            plugin: RendererPlugin instance.
        """
        metadata = plugin.get_plugin_metadata()
        name = metadata.get("name", f"plugin_{len(self._plugins)}")
        self._plugins[name] = plugin
        renderer = plugin.create_renderer()
        self._renderers[name] = renderer
        logger.info(f"Registered renderer plugin: {name} v{metadata.get('version', 'unknown')}")

    def get_renderer(self, name: Optional[str] = None) -> Renderer:
        """Get a renderer by name.

        Args:
            name: Renderer name. If None, returns the default renderer.

        Returns:
            Renderer instance.

        Raises:
            RendererError: If the renderer is not found.
        """
        renderer_name = name or self._default_renderer
        if renderer_name is None:
            raise RendererError(
                message="No renderer available.",
                renderer_name="unknown",
            )
        if renderer_name not in self._renderers:
            raise RendererError(
                message=f"Renderer '{renderer_name}' not found.",
                renderer_name=renderer_name,
            )
        return self._renderers[renderer_name]

    def get_renderer_for_chart(self, chart_type: str) -> Renderer:
        """Get the appropriate renderer for a chart type.

        Args:
            chart_type: The chart type string.

        Returns:
            Renderer instance that supports the chart type.

        Raises:
            RendererError: If no renderer supports the chart type.
        """
        for name, renderer in self._renderers.items():
            supported = renderer.get_supported_chart_types()
            if chart_type in supported:
                return renderer
        raise RendererError(
            message=f"No renderer supports chart type '{chart_type}'.",
            renderer_name="unknown",
        )

    def list_renderers(self) -> List[Dict[str, Any]]:
        """List all registered renderers with metadata.

        Returns:
            List of renderer metadata dictionaries.
        """
        result = []
        for name, renderer in self._renderers.items():
            metadata = renderer.get_metadata()
            metadata["name"] = name
            result.append(metadata)
        return result

    def set_default_renderer(self, name: str) -> None:
        """Set the default renderer.

        Args:
            name: Renderer name to set as default.

        Raises:
            RendererError: If the renderer is not found.
        """
        if name not in self._renderers:
            raise RendererError(
                message=f"Cannot set default: renderer '{name}' not found.",
                renderer_name=name,
            )
        self._default_renderer = name
        logger.info(f"Default renderer set to: {name}")


# Singleton instance
renderer_factory = RendererFactory()