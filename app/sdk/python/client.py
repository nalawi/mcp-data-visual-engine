"""DV1 Python SDK Client.

Provides a high-level interface for interacting with the DV1 Visualization Engine.
Can be used both as a direct client (importing the service) or as an HTTP client.
"""

import base64
import json
import logging
from typing import Any, Dict, List, Optional, Union

from app.domain.specs.vizspec import VizSpec
from app.application.services.visualization_service import visualization_service

logger = logging.getLogger(__name__)


class DV1Client:
    """High-level Python SDK client for the DV1 Visualization Engine.

    Provides convenient methods for rendering, exporting, and managing
    visualizations. Can be used directly (in-process) or via HTTP.

    Examples:
        ```python
        from app.sdk.python import DV1Client

        client = DV1Client()

        # Render a chart
        result = client.render({
            "metadata": {"title": "Sales"},
            "data": {"source": "inline", "records": [...]},
            "visual": {"type": "bar"},
            "encoding": {"x": "month", "y": "revenue"},
        })

        # Export as PNG
        png_bytes = client.render_png(spec)

        # Get chart recommendations
        recommendations = client.recommend_chart({
            "fields": [{"name": "date", "type": "date"}, {"name": "value", "type": "number"}]
        })
        ```
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        use_direct: bool = True,
    ) -> None:
        """Initialize the DV1 client.

        Args:
            base_url: Base URL for the DV1 API (e.g., http://localhost:8000).
            api_key: API key for authentication.
            use_direct: If True, use in-process service (no HTTP).
        """
        self._base_url = base_url
        self._api_key = api_key
        self._use_direct = use_direct

    def render(
        self,
        spec: Union[Dict[str, Any], VizSpec],
        renderer: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Render a visualization.

        Args:
            spec: VizSpec dictionary or VizSpec object.
            renderer: Optional renderer name.
            **kwargs: Additional options.

        Returns:
            Rendered visualization.
        """
        spec_data = spec if isinstance(spec, dict) else spec.to_dict()
        if self._use_direct:
            return visualization_service.render(spec_data, renderer, **kwargs)
        return self._http_post("/api/v1/render", {"spec": spec_data, "renderer": renderer})

    def render_png(
        self,
        spec: Union[Dict[str, Any], VizSpec],
        renderer: Optional[str] = None,
        **kwargs: Any,
    ) -> bytes:
        """Render and export as PNG.

        Args:
            spec: VizSpec dictionary or VizSpec object.
            renderer: Optional renderer name.
            **kwargs: Additional options.

        Returns:
            PNG image bytes.
        """
        spec_data = spec if isinstance(spec, dict) else spec.to_dict()
        if self._use_direct:
            return visualization_service.render_png(spec_data, renderer, **kwargs)
        return self._http_get_bytes("/api/v1/render/png", {"spec": json.dumps(spec_data)})

    def render_svg(
        self,
        spec: Union[Dict[str, Any], VizSpec],
        renderer: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Render and export as SVG.

        Args:
            spec: VizSpec dictionary or VizSpec object.
            renderer: Optional renderer name.
            **kwargs: Additional options.

        Returns:
            SVG string.
        """
        spec_data = spec if isinstance(spec, dict) else spec.to_dict()
        if self._use_direct:
            return visualization_service.render_svg(spec_data, renderer, **kwargs)
        return ""

    def render_pdf(
        self,
        spec: Union[Dict[str, Any], VizSpec],
        renderer: Optional[str] = None,
        **kwargs: Any,
    ) -> bytes:
        """Render and export as PDF.

        Args:
            spec: VizSpec dictionary or VizSpec object.
            renderer: Optional renderer name.
            **kwargs: Additional options.

        Returns:
            PDF bytes.
        """
        spec_data = spec if isinstance(spec, dict) else spec.to_dict()
        if self._use_direct:
            return visualization_service.render_pdf(spec_data, renderer, **kwargs)
        return b""

    def render_html(
        self,
        spec: Union[Dict[str, Any], VizSpec],
        renderer: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Render and export as HTML.

        Args:
            spec: VizSpec dictionary or VizSpec object.
            renderer: Optional renderer name.
            **kwargs: Additional options.

        Returns:
            HTML string.
        """
        spec_data = spec if isinstance(spec, dict) else spec.to_dict()
        if self._use_direct:
            return visualization_service.render_html(spec_data, renderer, **kwargs)
        return ""

    def render_json(
        self,
        spec: Union[Dict[str, Any], VizSpec],
        renderer: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Render and export as JSON.

        Args:
            spec: VizSpec dictionary or VizSpec object.
            renderer: Optional renderer name.
            **kwargs: Additional options.

        Returns:
            JSON string.
        """
        spec_data = spec if isinstance(spec, dict) else spec.to_dict()
        if self._use_direct:
            return visualization_service.render_json(spec_data, renderer, **kwargs)
        return "{}"

    def render_base64(
        self,
        spec: Union[Dict[str, Any], VizSpec],
        renderer: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Render and export as base64-encoded data URI.

        Args:
            spec: VizSpec dictionary or VizSpec object.
            renderer: Optional renderer name.
            **kwargs: Additional options.

        Returns:
            Base64 data URI string.
        """
        spec_data = spec if isinstance(spec, dict) else spec.to_dict()
        if self._use_direct:
            return visualization_service.render_base64(spec_data, renderer, **kwargs)
        return ""

    def render_batch(
        self,
        specs: List[Union[Dict[str, Any], VizSpec]],
        renderer: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """Render multiple visualizations in batch.

        Args:
            specs: List of VizSpec dictionaries or objects.
            renderer: Optional renderer name.
            **kwargs: Additional options.

        Returns:
            List of render results.
        """
        specs_data = [s if isinstance(s, dict) else s.to_dict() for s in specs]
        if self._use_direct:
            return visualization_service.render_batch(specs_data, renderer, **kwargs)
        return []

    def dashboard(
        self,
        specs: List[Union[Dict[str, Any], VizSpec]],
        layout: Optional[Dict[str, Any]] = None,
        renderer: Optional[str] = None,
    ) -> str:
        """Create a dashboard with multiple visualizations.

        Args:
            specs: List of VizSpec dictionaries or objects.
            layout: Dashboard layout configuration.
            renderer: Optional renderer name.

        Returns:
            HTML dashboard string.
        """
        specs_data = [s if isinstance(s, dict) else s.to_dict() for s in specs]
        if self._use_direct:
            from app.api.v1.dashboard import create_dashboard
            import asyncio
            # For simplicity, render each spec as HTML and combine
            html_parts = [
                "<!DOCTYPE html>",
                '<html><head><meta charset="utf-8">',
                "<title>DV1 Dashboard</title>",
                '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>',
                '<style>',
                "* { box-sizing: border-box; }",
                "body { margin: 0; padding: 20px; font-family: Arial, sans-serif; background: #f5f5f5; }",
                ".dashboard { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }",
                ".panel { background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 16px; display: flex; flex-direction: column; min-height: 400px; }",
                ".panel h3 { margin: 0 0 8px 0; color: #333; flex-shrink: 0; }",
                ".panel .chart-wrapper { flex: 1; min-height: 0; position: relative; }",
                ".panel .chart-wrapper .js-plotly-plot, .panel .chart-wrapper .plot-container { width: 100% !important; height: 100% !important; }",
                "</style></head><body><div class='dashboard'>",
            ]
            for sd in specs_data:
                try:
                    html = visualization_service.render_html(sd, renderer)
                    title = sd.get("metadata", {}).get("title", "Panel")
                    html_parts.append(f"<div class='panel'><h3>{title}</h3><div class='chart-wrapper'>{html}</div></div>")
                except Exception as e:
                    html_parts.append(f"<div class='panel'><p>Error: {e}</p></div>")
            html_parts.append("</div></body></html>")
            return "\n".join(html_parts)
        return ""

    def preview(
        self,
        spec: Union[Dict[str, Any], VizSpec],
        renderer: Optional[str] = None,
    ) -> str:
        """Preview a chart (returns HTML).

        Args:
            spec: VizSpec dictionary or VizSpec object.
            renderer: Optional renderer name.

        Returns:
            HTML preview string.
        """
        return self.render_html(spec, renderer)

    def export(
        self,
        spec: Union[Dict[str, Any], VizSpec],
        format: str = "png",
        renderer: Optional[str] = None,
    ) -> Union[bytes, str]:
        """Export a chart in the specified format.

        Args:
            spec: VizSpec dictionary or VizSpec object.
            format: Export format (png, svg, pdf, html, json).
            renderer: Optional renderer name.

        Returns:
            Exported data (bytes for binary formats, str for text formats).
        """
        if format == "png":
            return self.render_png(spec, renderer)
        elif format == "svg":
            return self.render_svg(spec, renderer)
        elif format == "pdf":
            return self.render_pdf(spec, renderer)
        elif format == "html":
            return self.render_html(spec, renderer)
        elif format == "json":
            return self.render_json(spec, renderer)
        elif format == "base64":
            return self.render_base64(spec, renderer)
        raise ValueError(f"Unsupported format: {format}")

    def validate_spec(self, spec: Union[Dict[str, Any], VizSpec]) -> Dict[str, Any]:
        """Validate a VizSpec.

        Args:
            spec: VizSpec dictionary or VizSpec object.

        Returns:
            Validation result.
        """
        spec_data = spec if isinstance(spec, dict) else spec.to_dict()
        if self._use_direct:
            return visualization_service.validate_spec(spec_data)
        return {"valid": False, "errors": ["HTTP mode not implemented"]}

    def recommend_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI chart recommendations.

        Args:
            data: Data description with fields, types, cardinality.

        Returns:
            Recommendations with chart types and confidence scores.
        """
        if self._use_direct:
            return visualization_service.recommend_chart(data)
        return {"recommendations": []}

    def list_themes(self) -> List[str]:
        """List all available themes.

        Returns:
            List of theme names.
        """
        if self._use_direct:
            return visualization_service.list_themes()
        return []

    def list_renderers(self) -> List[Dict[str, Any]]:
        """List all available renderers.

        Returns:
            List of renderer metadata.
        """
        if self._use_direct:
            return visualization_service.list_renderers()
        return []

    def _http_post(self, path: str, data: Dict[str, Any]) -> Any:
        """Make an HTTP POST request.

        Args:
            path: API path.
            data: Request data.

        Returns:
            Response data.
        """
        import requests
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        url = f"{self._base_url}{path}"
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def _http_get_bytes(self, path: str, params: Dict[str, str]) -> bytes:
        """Make an HTTP GET request returning bytes.

        Args:
            path: API path.
            params: Query parameters.

        Returns:
            Response bytes.
        """
        import requests
        headers = {}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        url = f"{self._base_url}{path}"
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.content