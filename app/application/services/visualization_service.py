"""Core visualization service - the main application service for rendering."""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from app.domain.specs.vizspec import VizSpec
from app.domain.specs.outputspec import OutputFormat
from app.domain.exceptions.base import ValidationError, RendererError
from app.application.factories.renderer_factory import renderer_factory
from app.infrastructure.themes.theme_engine import theme_engine

logger = logging.getLogger(__name__)


class VisualizationService:
    """Core application service for visualization operations.

    This service orchestrates the entire visualization pipeline:
    1. Validate VizSpec
    2. Select renderer
    3. Render visualization
    4. Export in requested format

    The service never imports renderer implementations directly.
    """

    def __init__(self) -> None:
        """Initialize the visualization service."""
        self._renderer_factory = renderer_factory

    def validate_spec(self, spec_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a VizSpec dictionary.

        Args:
            spec_data: Raw VizSpec dictionary.

        Returns:
            Validation result with status and any errors.
        """
        try:
            spec = VizSpec.from_dict(spec_data)
            return {
                "valid": True,
                "spec_id": spec.id,
                "errors": [],
            }
        except Exception as e:
            return {
                "valid": False,
                "spec_id": None,
                "errors": [{"message": str(e), "field": getattr(e, "field_name", None)}],
            }

    def render(
        self,
        spec_data: Dict[str, Any],
        renderer_name: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Render a visualization from a VizSpec dictionary.

        Args:
            spec_data: Raw VizSpec dictionary.
            renderer_name: Optional renderer name override.
            **kwargs: Additional render options.

        Returns:
            Rendered visualization object.

        Raises:
            ValidationError: If the VizSpec is invalid.
            RendererError: If rendering fails.
        """
        try:
            spec = VizSpec.from_dict(spec_data)
        except Exception as e:
            raise ValidationError(
                message=f"Invalid VizSpec: {str(e)}",
                details={"spec_data": spec_data},
            ) from e

        renderer = self._renderer_factory.get_renderer(renderer_name)
        return renderer.render(spec)

    def render_png(
        self,
        spec_data: Dict[str, Any],
        renderer_name: Optional[str] = None,
        **kwargs: Any,
    ) -> bytes:
        """Render and export as PNG.

        Args:
            spec_data: Raw VizSpec dictionary.
            renderer_name: Optional renderer name override.
            **kwargs: Additional render options.

        Returns:
            PNG image bytes.
        """
        spec = VizSpec.from_dict(spec_data)
        renderer = self._renderer_factory.get_renderer(renderer_name)
        return renderer.render_png(spec, **kwargs)

    def render_svg(
        self,
        spec_data: Dict[str, Any],
        renderer_name: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Render and export as SVG.

        Args:
            spec_data: Raw VizSpec dictionary.
            renderer_name: Optional renderer name override.
            **kwargs: Additional render options.

        Returns:
            SVG string.
        """
        spec = VizSpec.from_dict(spec_data)
        renderer = self._renderer_factory.get_renderer(renderer_name)
        return renderer.render_svg(spec, **kwargs)

    def render_pdf(
        self,
        spec_data: Dict[str, Any],
        renderer_name: Optional[str] = None,
        **kwargs: Any,
    ) -> bytes:
        """Render and export as PDF.

        Args:
            spec_data: Raw VizSpec dictionary.
            renderer_name: Optional renderer name override.
            **kwargs: Additional render options.

        Returns:
            PDF bytes.
        """
        spec = VizSpec.from_dict(spec_data)
        renderer = self._renderer_factory.get_renderer(renderer_name)
        return renderer.render_pdf(spec, **kwargs)

    def render_html(
        self,
        spec_data: Dict[str, Any],
        renderer_name: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Render and export as HTML.

        Args:
            spec_data: Raw VizSpec dictionary.
            renderer_name: Optional renderer name override.
            **kwargs: Additional render options.

        Returns:
            HTML string.
        """
        spec = VizSpec.from_dict(spec_data)
        renderer = self._renderer_factory.get_renderer(renderer_name)
        return renderer.render_html(spec, **kwargs)

    def render_json(
        self,
        spec_data: Dict[str, Any],
        renderer_name: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Render and export as JSON.

        Args:
            spec_data: Raw VizSpec dictionary.
            renderer_name: Optional renderer name override.
            **kwargs: Additional render options.

        Returns:
            JSON string.
        """
        spec = VizSpec.from_dict(spec_data)
        renderer = self._renderer_factory.get_renderer(renderer_name)
        return renderer.render_json(spec, **kwargs)

    def render_base64(
        self,
        spec_data: Dict[str, Any],
        renderer_name: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Render and export as base64.

        Args:
            spec_data: Raw VizSpec dictionary.
            renderer_name: Optional renderer name override.
            **kwargs: Additional render options.

        Returns:
            Base64-encoded data URI.
        """
        spec = VizSpec.from_dict(spec_data)
        renderer = self._renderer_factory.get_renderer(renderer_name)
        return renderer.render_base64(spec, **kwargs)

    def render_batch(
        self,
        specs: List[Dict[str, Any]],
        renderer_name: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """Render multiple visualizations in batch.

        Args:
            specs: List of VizSpec dictionaries.
            renderer_name: Optional renderer name override.
            **kwargs: Additional render options.

        Returns:
            List of render results with spec_id and output.
        """
        results = []
        for spec_data in specs:
            try:
                spec = VizSpec.from_dict(spec_data)
                renderer = self._renderer_factory.get_renderer(renderer_name)
                output_format = spec.output.format.value

                if output_format == "png":
                    output = renderer.render_png(spec, **kwargs)
                elif output_format == "svg":
                    output = renderer.render_svg(spec, **kwargs)
                elif output_format == "pdf":
                    output = renderer.render_pdf(spec, **kwargs)
                elif output_format == "html":
                    output = renderer.render_html(spec, **kwargs)
                elif output_format == "json":
                    output = renderer.render_json(spec, **kwargs)
                elif output_format == "base64":
                    output = renderer.render_base64(spec, **kwargs)
                else:
                    output = renderer.render(spec)

                results.append({
                    "spec_id": spec.id,
                    "success": True,
                    "format": output_format,
                    "output": output,
                })
            except Exception as e:
                results.append({
                    "spec_id": spec_data.get("id", "unknown"),
                    "success": False,
                    "error": str(e),
                })

        return results

    def list_renderers(self) -> List[Dict[str, Any]]:
        """List all available renderers.

        Returns:
            List of renderer metadata.
        """
        return self._renderer_factory.list_renderers()

    def list_themes(self) -> List[str]:
        """List all available themes.

        Returns:
            List of theme names.
        """
        return theme_engine.list_themes()

    def recommend_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend a chart type based on data analysis.

        Args:
            data: Data description including field types and cardinality.

        Returns:
            Recommendation with chart type, confidence, and reasoning.
        """
        return ChartRecommender.recommend(data)


class ChartRecommender:
    """AI chart recommendation engine.

    Analyzes data characteristics and recommends the most appropriate
    visualization type based on data type, cardinality, relationships,
    and other factors.
    """

    @staticmethod
    def recommend(data: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend a chart type based on data analysis.

        Args:
            data: Data description with fields, types, cardinality, etc.

        Returns:
            Recommendation with chart type, confidence, and reasoning.
        """
        fields = data.get("fields", [])
        relationships = data.get("relationships", [])
        data_type = data.get("type", "tabular")

        recommendations = []

        # Analyze fields
        numeric_fields = [f for f in fields if f.get("type") in ("number", "integer", "float")]
        categorical_fields = [f for f in fields if f.get("type") in ("string", "category", "text")]
        date_fields = [f for f in fields if f.get("type") in ("date", "datetime", "time")]
        geospatial_fields = [f for f in fields if f.get("lat") or f.get("lon") or f.get("type") == "geospatial"]

        num_numeric = len(numeric_fields)
        num_categorical = len(categorical_fields)
        num_dates = len(date_fields)
        num_geo = len(geospatial_fields)

        # Time series detection
        if num_dates >= 1 and num_numeric >= 1:
            recommendations.append({
                "chart_type": "line",
                "confidence": 0.95,
                "reasoning": f"Time series detected: {num_dates} date field(s) and {num_numeric} numeric field(s). Line chart is optimal for temporal trends.",
            })
            recommendations.append({
                "chart_type": "area",
                "confidence": 0.80,
                "reasoning": "Area chart can show magnitude changes over time.",
            })

        # Categorical comparison
        if num_categorical >= 1 and num_numeric >= 1:
            cardinality = categorical_fields[0].get("cardinality", 0)
            if cardinality <= 10:
                recommendations.append({
                    "chart_type": "bar",
                    "confidence": 0.90,
                    "reasoning": f"Bar chart for comparing {num_numeric} metric(s) across {cardinality} categories.",
                })
            else:
                recommendations.append({
                    "chart_type": "horizontal_bar",
                    "confidence": 0.75,
                    "reasoning": f"Horizontal bar chart for {cardinality} categories to improve readability.",
                })

        # Composition
        if num_categorical >= 1 and num_numeric == 1:
            cardinality = categorical_fields[0].get("cardinality", 0)
            if cardinality <= 7:
                recommendations.append({
                    "chart_type": "pie",
                    "confidence": 0.70,
                    "reasoning": f"Pie chart for composition of {cardinality} parts.",
                })
                recommendations.append({
                    "chart_type": "donut",
                    "confidence": 0.75,
                    "reasoning": f"Donut chart for composition of {cardinality} parts with better readability.",
                })

        # Distribution
        if num_numeric >= 1 and num_categorical == 0:
            recommendations.append({
                "chart_type": "histogram",
                "confidence": 0.85,
                "reasoning": f"Histogram for distribution of {num_numeric} numeric field(s).",
            })
            recommendations.append({
                "chart_type": "density",
                "confidence": 0.70,
                "reasoning": "Density plot for smoothed distribution visualization.",
            })

        # Relationship / Correlation
        if num_numeric >= 2:
            recommendations.append({
                "chart_type": "scatter",
                "confidence": 0.85,
                "reasoning": f"Scatter plot for relationship between {num_numeric} numeric fields.",
            })
            if num_numeric >= 3:
                recommendations.append({
                    "chart_type": "scatter_3d",
                    "confidence": 0.60,
                    "reasoning": "3D scatter plot for exploring multi-dimensional relationships.",
                })
            recommendations.append({
                "chart_type": "correlation_matrix",
                "confidence": 0.80,
                "reasoning": "Correlation matrix to show relationships between all numeric fields.",
            })

        # Geospatial
        if num_geo >= 1:
            recommendations.append({
                "chart_type": "map_scatter",
                "confidence": 0.90,
                "reasoning": "Map scatter plot for geospatial data distribution.",
            })

        # Hierarchical
        if num_categorical >= 2:
            recommendations.append({
                "chart_type": "treemap",
                "confidence": 0.65,
                "reasoning": f"Treemap for hierarchical data with {num_categorical} categorical levels.",
            })
            recommendations.append({
                "chart_type": "sunburst",
                "confidence": 0.60,
                "reasoning": f"Sunburst chart for hierarchical composition with {num_categorical} levels.",
            })

        # Network
        if relationships:
            recommendations.append({
                "chart_type": "sankey",
                "confidence": 0.75,
                "reasoning": f"Sankey diagram for flow between {len(relationships)} relationships.",
            })
            recommendations.append({
                "chart_type": "network_graph",
                "confidence": 0.70,
                "reasoning": "Network graph for relationship visualization.",
            })

        # Sort by confidence
        recommendations.sort(key=lambda r: r["confidence"], reverse=True)

        return {
            "recommendations": recommendations[:5],
            "data_profile": {
                "type": data_type,
                "numeric_fields": num_numeric,
                "categorical_fields": num_categorical,
                "date_fields": num_dates,
                "geospatial_fields": num_geo,
                "total_fields": len(fields),
                "has_relationships": len(relationships) > 0,
            },
        }


# Singleton instance
visualization_service = VisualizationService()