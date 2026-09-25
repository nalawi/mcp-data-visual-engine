"""Tests for VizSpec domain model."""

import pytest
from app.domain.specs.vizspec import VizSpec
from app.domain.specs.dataspec import DataSpec, DataSource
from app.domain.specs.visualspec import VisualSpec, ChartType
from app.domain.specs.themespec import ThemeSpec
from app.domain.specs.layoutspec import LayoutSpec
from app.domain.specs.outputspec import OutputSpec, OutputFormat
from app.domain.specs.annotationspec import AnnotationSpec, AnnotationType


class TestVizSpec:
    """Test suite for VizSpec creation and validation."""

    def test_create_minimal_vizspec(self):
        """Test creating a minimal VizSpec with defaults."""
        spec = VizSpec(
            data={"source": "inline", "records": [{"x": 1}]}
        )
        assert spec.metadata["title"] == "Untitled Visualization"
        assert spec.data.source == DataSource.INLINE
        assert spec.visual.type is None
        assert spec.theme.name == "light"
        assert spec.output.format == OutputFormat.PNG
        assert spec.spec_version == "1.0"
        assert spec.id is not None

    def test_create_vizspec_from_dict(self):
        """Test creating VizSpec from a dictionary."""
        data = {
            "metadata": {"title": "Test Chart", "subtitle": "Test"},
            "data": {
                "source": "inline",
                "records": [{"x": 1, "y": 2}, {"x": 3, "y": 4}],
            },
            "visual": {"type": "line"},
            "encoding": {"x": "x", "y": "y"},
            "theme": {"name": "dark"},
            "output": {"format": "html"},
        }
        spec = VizSpec.from_dict(data)
        assert spec.metadata["title"] == "Test Chart"
        assert spec.visual.type == ChartType.LINE
        assert spec.theme.name == "dark"
        assert spec.output.format == OutputFormat.HTML
        assert len(spec.data.records) == 2

    def test_vizspec_to_dict(self):
        """Test converting VizSpec to dictionary."""
        spec = VizSpec(
            metadata={"title": "Export Test"},
            data={"source": "inline", "records": [{"category": "A", "value": 1}]},
            visual=VisualSpec(type=ChartType.BAR),
            encoding={"x": "category", "y": "value"},
        )
        d = spec.to_dict()
        assert d["metadata"]["title"] == "Export Test"
        assert d["visual"]["type"] == "bar"
        assert d["encoding"]["x"] == "category"

    def test_vizspec_validation_line_chart_requires_encoding(self):
        """Test that line charts require encoding."""
        with pytest.raises(ValueError, match="requires at minimum"):
            VizSpec(
                data={"source": "inline", "records": [{"x": 1, "y": 2}]},
                visual=VisualSpec(type=ChartType.LINE),
                encoding={},
            )

    def test_vizspec_validation_bar_chart_requires_encoding(self):
        """Test that bar charts require encoding."""
        with pytest.raises(ValueError, match="requires at minimum"):
            VizSpec(
                data={"source": "inline", "records": [{"x": 1, "y": 2}]},
                visual=VisualSpec(type=ChartType.BAR),
                encoding={},
            )

    def test_vizspec_with_annotations(self):
        """Test VizSpec with annotations."""
        spec = VizSpec(
            data={"source": "inline", "records": [{"x": 1}]},
            annotations=[
                AnnotationSpec(
                    type=AnnotationType.TEXT,
                    label="Peak Value",
                    x=5,
                    y=100,
                )
            ]
        )
        assert len(spec.annotations) == 1
        assert spec.annotations[0].label == "Peak Value"
        assert spec.annotations[0].type == AnnotationType.TEXT

    def test_vizspec_with_custom_theme(self):
        """Test VizSpec with custom theme overrides."""
        spec = VizSpec(
            data={"source": "inline", "records": [{"x": 1}]},
            theme=ThemeSpec(
                name="corporate",
                background_color="#f0f0f0",
                font_family="Helvetica",
            )
        )
        assert spec.theme.name == "corporate"
        assert spec.theme.background_color == "#f0f0f0"

    def test_vizspec_with_transforms(self):
        """Test VizSpec with data transforms."""
        spec = VizSpec(
            data={"source": "inline", "records": [{"x": 1}]},
            transforms=[
                {"type": "filter", "field": "value", "operator": "gt", "value": 10},
                {"type": "sort", "field": "date", "ascending": False},
            ]
        )
        assert len(spec.transforms) == 2
        assert spec.transforms[0]["type"] == "filter"

    def test_vizspec_with_interaction(self):
        """Test VizSpec with interaction config."""
        spec = VizSpec(
            data={"source": "inline", "records": [{"x": 1}]},
            interaction={"tooltip": True, "zoom": False, "pan": True, "selection": True}
        )
        assert spec.interaction["tooltip"] is True
        assert spec.interaction["zoom"] is False

    def test_vizspec_with_accessibility(self):
        """Test VizSpec with accessibility config."""
        spec = VizSpec(
            data={"source": "inline", "records": [{"x": 1}]},
            accessibility={
                "description": "Chart showing quarterly revenue",
                "aria_label": "Revenue chart",
                "keyboard_nav": True,
            }
        )
        assert spec.accessibility["description"] == "Chart showing quarterly revenue"

    def test_vizspec_serialization_roundtrip(self):
        """Test that serialization roundtrip preserves data."""
        original = VizSpec(
            metadata={"title": "Roundtrip Test"},
            data=DataSpec(
                source=DataSource.INLINE,
                records=[{"a": 1, "b": 2}],
            ),
            visual=VisualSpec(type=ChartType.SCATTER),
            encoding={"x": "a", "y": "b", "color": "c"},
        )
        d = original.to_dict()
        restored = VizSpec.from_dict(d)
        assert restored.metadata["title"] == original.metadata["title"]
        assert restored.visual.type == original.visual.type
        assert restored.encoding["x"] == original.encoding["x"]


class TestDataSpec:
    """Test suite for DataSpec."""

    def test_inline_data_default(self):
        """Test that inline data source can be created without records."""
        spec = DataSpec(source=DataSource.INLINE)
        assert spec.source == DataSource.INLINE
        assert spec.records is None

    def test_url_data_requires_url(self):
        """Test that URL data source requires URL."""
        with pytest.raises(ValueError, match="requires 'url' field"):
            DataSpec(source=DataSource.URL)

    def test_file_data_requires_path(self):
        """Test that file data source requires file_path."""
        with pytest.raises(ValueError, match="requires 'file_path' field"):
            DataSpec(source=DataSource.FILE)

    def test_valid_inline_data(self):
        """Test valid inline data spec."""
        spec = DataSpec(
            source=DataSource.INLINE,
            records=[{"x": 1, "y": 2}],
        )
        assert spec.records[0]["x"] == 1


class TestOutputSpec:
    """Test suite for OutputSpec."""

    def test_default_output(self):
        """Test default output configuration."""
        spec = OutputSpec()
        assert spec.format == OutputFormat.PNG
        assert spec.dpi == 150
        assert spec.scale == 1.0

    def test_high_quality_export(self):
        """Test high quality export configuration."""
        spec = OutputSpec(format=OutputFormat.PDF, dpi=300, scale=2.0)
        assert spec.format == OutputFormat.PDF
        assert spec.dpi == 300
        assert spec.scale == 2.0

    def test_html_output(self):
        """Test HTML output configuration."""
        spec = OutputSpec(
            format=OutputFormat.HTML,
            include_plotlyjs=True,
            full_html=True,
        )
        assert spec.format == OutputFormat.HTML
        assert spec.include_plotlyjs is True