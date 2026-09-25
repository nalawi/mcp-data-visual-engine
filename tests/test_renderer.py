"""Tests for the Plotly renderer."""

import pytest
from app.domain.specs.vizspec import VizSpec
from app.domain.specs.visualspec import VisualSpec, ChartType
from app.infrastructure.renderers.plotly.plotly_renderer import PlotlyRenderer
from app.application.factories.renderer_factory import renderer_factory


class TestPlotlyRenderer:
    """Test suite for the Plotly renderer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.renderer = PlotlyRenderer()

    def test_renderer_metadata(self):
        """Test renderer metadata."""
        metadata = self.renderer.get_metadata()
        assert metadata["name"] == "plotly"
        assert "plotly" in metadata["name"]

    def test_supported_chart_types(self):
        """Test that all chart types are supported."""
        types = self.renderer.get_supported_chart_types()
        assert "line" in types
        assert "bar" in types
        assert "scatter" in types
        assert "pie" in types
        assert "heatmap" in types
        assert len(types) > 40  # Should support 50+ chart types

    def test_render_line_chart(self):
        """Test rendering a line chart."""
        spec = VizSpec(
            metadata={"title": "Test Line"},
            data={
                "source": "inline",
                "records": [
                    {"x": "Jan", "y": 10},
                    {"x": "Feb", "y": 25},
                    {"x": "Mar", "y": 15},
                ],
            },
            visual=VisualSpec(type=ChartType.LINE),
            encoding={"x": "x", "y": "y"},
        )
        figure = self.renderer.render(spec)
        assert figure is not None
        assert len(figure.data) > 0

    def test_render_bar_chart(self):
        """Test rendering a bar chart."""
        spec = VizSpec(
            metadata={"title": "Test Bar"},
            data={
                "source": "inline",
                "records": [
                    {"category": "A", "value": 30},
                    {"category": "B", "value": 45},
                    {"category": "C", "value": 25},
                ],
            },
            visual=VisualSpec(type=ChartType.BAR),
            encoding={"x": "category", "y": "value"},
        )
        figure = self.renderer.render(spec)
        assert figure is not None

    def test_render_pie_chart(self):
        """Test rendering a pie chart."""
        spec = VizSpec(
            metadata={"title": "Test Pie"},
            data={
                "source": "inline",
                "records": [
                    {"label": "A", "value": 30},
                    {"label": "B", "value": 45},
                    {"label": "C", "value": 25},
                ],
            },
            visual=VisualSpec(type=ChartType.PIE),
            encoding={"x": "label", "y": "value"},
        )
        figure = self.renderer.render(spec)
        assert figure is not None

    def test_render_scatter_chart(self):
        """Test rendering a scatter chart."""
        spec = VizSpec(
            metadata={"title": "Test Scatter"},
            data={
                "source": "inline",
                "records": [
                    {"x": 1, "y": 2},
                    {"x": 2, "y": 4},
                    {"x": 3, "y": 1},
                ],
            },
            visual=VisualSpec(type=ChartType.SCATTER),
            encoding={"x": "x", "y": "y"},
        )
        figure = self.renderer.render(spec)
        assert figure is not None

    def test_render_html_export(self):
        """Test HTML export."""
        spec = VizSpec(
            metadata={"title": "HTML Test"},
            data={
                "source": "inline",
                "records": [{"x": "A", "y": 10}],
            },
            visual=VisualSpec(type=ChartType.BAR),
            encoding={"x": "x", "y": "y"},
        )
        html = self.renderer.render_html(spec)
        assert html is not None
        assert "<html" in html or "<div" in html

    def test_render_json_export(self):
        """Test JSON export."""
        spec = VizSpec(
            metadata={"title": "JSON Test"},
            data={
                "source": "inline",
                "records": [{"x": "A", "y": 10}],
            },
            visual=VisualSpec(type=ChartType.BAR),
            encoding={"x": "x", "y": "y"},
        )
        json_str = self.renderer.render_json(spec)
        assert json_str is not None
        assert '"data"' in json_str or len(json_str) > 0

    def test_renderer_factory(self):
        """Test renderer factory."""
        renderer = renderer_factory.get_renderer()
        assert renderer is not None
        renderers = renderer_factory.list_renderers()
        assert len(renderers) > 0

    def test_render_with_theme(self):
        """Test rendering with a theme."""
        spec = VizSpec(
            metadata={"title": "Themed Chart"},
            data={
                "source": "inline",
                "records": [{"x": "A", "y": 10}],
            },
            visual=VisualSpec(type=ChartType.BAR),
            encoding={"x": "x", "y": "y"},
            theme={"name": "dark"},
        )
        figure = self.renderer.render(spec)
        assert figure is not None

    def test_render_with_annotations(self):
        """Test rendering with annotations."""
        spec = VizSpec(
            metadata={"title": "Annotated Chart"},
            data={
                "source": "inline",
                "records": [{"x": "A", "y": 10}, {"x": "B", "y": 20}],
            },
            visual=VisualSpec(type=ChartType.LINE),
            encoding={"x": "x", "y": "y"},
            annotations=[
                {"type": "text", "label": "Peak", "x": "B", "y": 20}
            ],
        )
        figure = self.renderer.render(spec)
        assert figure is not None