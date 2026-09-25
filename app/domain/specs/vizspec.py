"""Core VizSpec model - the central specification for all visualizations."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator

from app.domain.specs.dataspec import DataSpec
from app.domain.specs.visualspec import VisualSpec
from app.domain.specs.themespec import ThemeSpec
from app.domain.specs.layoutspec import LayoutSpec
from app.domain.specs.outputspec import OutputSpec
from app.domain.specs.annotationspec import AnnotationSpec


class VizSpec(BaseModel):
    """Visualization Specification - the universal input for all renderers.

    VizSpec represents the complete intent of a visualization in a
    renderer-independent format. It is validated, transformed, and
    passed to a renderer for output generation.

    Attributes:
        metadata: Descriptive information about the visualization.
        data: Data source specification (inline, URL, reference).
        transforms: Ordered list of data transformation operations.
        encoding: Visual encoding channels mapping data to visual properties.
        visual: Visual configuration including chart type and styling.
        layout: Layout configuration for the visualization.
        annotations: Annotations to overlay on the visualization.
        theme: Theme configuration for styling.
        interaction: Interaction configuration.
        output: Output format and export configuration.
        accessibility: Accessibility configuration.
        spec_version: Version of the VizSpec format.
        id: Unique identifier for this specification.
        created_at: Timestamp when this spec was created.
    """

    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {"title": "Untitled Visualization", "subtitle": ""},
        description="Metadata including title, subtitle, description, author.",
    )
    data: DataSpec = Field(default_factory=DataSpec, description="Data source specification.")
    transforms: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Ordered list of data transformation specifications.",
    )
    encoding: Dict[str, Any] = Field(
        default_factory=dict,
        description="Visual encoding channels (x, y, color, size, shape, etc.).",
    )
    visual: VisualSpec = Field(default_factory=VisualSpec, description="Visual configuration.")
    layout: LayoutSpec = Field(default_factory=LayoutSpec, description="Layout configuration.")
    annotations: List[AnnotationSpec] = Field(
        default_factory=list,
        description="Annotations to overlay on the visualization.",
    )
    theme: ThemeSpec = Field(default_factory=ThemeSpec, description="Theme configuration.")
    interaction: Dict[str, Any] = Field(
        default_factory=lambda: {"tooltip": True, "zoom": True, "pan": True, "selection": False},
        description="Interaction configuration (tooltips, zoom, pan, selection).",
    )
    output: OutputSpec = Field(default_factory=OutputSpec, description="Output configuration.")
    accessibility: Dict[str, Any] = Field(
        default_factory=lambda: {
            "description": "",
            "aria_label": "",
            "keyboard_nav": False,
        },
        description="Accessibility configuration.",
    )
    spec_version: str = Field(default="1.0", description="VizSpec format version.")
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique spec identifier.")
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Creation timestamp.",
    )

    @model_validator(mode="after")
    def validate_visual_type_encoding(self) -> "VizSpec":
        """Validate that encoding is appropriate for the visual type."""
        visual_type = self.visual.type.value if self.visual.type else ""
        encoding_keys = set(self.encoding.keys())

        # Ensure basic encoding for non-trivial charts
        if visual_type in ("line", "bar", "area", "scatter") and not encoding_keys:
            raise ValueError(
                f"Visual type '{visual_type}' requires at minimum an 'x' encoding channel."
            )
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert VizSpec to a serializable dictionary."""
        return self.model_dump(mode="json")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VizSpec":
        """Create VizSpec from a dictionary."""
        return cls.model_validate(data)