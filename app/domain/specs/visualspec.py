"""Visual specification for VizSpec - defines chart type and visual properties."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChartType(str, Enum):
    """All supported chart types."""

    LINE = "line"
    SPLINE = "spline"
    AREA = "area"
    STACKED_AREA = "stacked_area"
    BAR = "bar"
    GROUPED_BAR = "grouped_bar"
    STACKED_BAR = "stacked_bar"
    HORIZONTAL_BAR = "horizontal_bar"
    PIE = "pie"
    DONUT = "donut"
    TREEMAP = "treemap"
    SUNBURST = "sunburst"
    SCATTER = "scatter"
    BUBBLE = "bubble"
    HISTOGRAM = "histogram"
    DENSITY = "density"
    BOX_PLOT = "box_plot"
    VIOLIN = "violin"
    STRIP = "strip"
    HEATMAP = "heatmap"
    CORRELATION_MATRIX = "correlation_matrix"
    HEXBIN = "hexbin"
    CONTOUR = "contour"
    RADAR = "radar"
    POLAR = "polar"
    WATERFALL = "waterfall"
    FUNNEL = "funnel"
    GAUGE = "gauge"
    INDICATOR = "indicator"
    TIMELINE = "timeline"
    GANTT = "gantt"
    CANDLESTICK = "candlestick"
    OHLC = "ohlc"
    FINANCIAL_VOLUME = "financial_volume"
    SCATTER_3D = "scatter_3d"
    SURFACE_3D = "surface_3d"
    MESH_3D = "mesh_3d"
    PARALLEL_COORDINATES = "parallel_coordinates"
    PARALLEL_CATEGORIES = "parallel_categories"
    NETWORK_GRAPH = "network_graph"
    SANKEY = "sankey"
    CHORD_DIAGRAM = "chord_diagram"
    CALENDAR_HEATMAP = "calendar_heatmap"
    MAP_SCATTER = "map_scatter"
    MAP_BUBBLE = "map_bubble"
    CHOROPLETH = "choropleth"
    FLOW_DIAGRAM = "flow_diagram"


class VisualSpec(BaseModel):
    """Visual specification defining chart type and visual properties.

    This is a renderer-independent specification of what the
    visualization should look like.
    """

    type: Optional[ChartType] = Field(default=None, description="Chart type to render.")
    subtype: Optional[str] = Field(default=None, description="Chart subtype variant.")
    orientation: str = Field(default="vertical", description="Chart orientation (vertical/horizontal).")
    color_palette: Optional[List[str]] = Field(default=None, description="Custom color palette.")
    opacity: float = Field(default=1.0, ge=0.0, le=1.0, description="Global opacity.")
    border_width: int = Field(default=0, ge=0, description="Border width around visual elements.")
    border_color: Optional[str] = Field(default=None, description="Border color.")
    fill_color: Optional[str] = Field(default=None, description="Fill color for areas.")
    line_width: int = Field(default=2, ge=0, description="Line width for line charts.")
    line_dash: Optional[str] = Field(default=None, description="Line dash pattern.")
    marker_size: int = Field(default=6, ge=0, description="Marker size for scatter/bubble.")
    marker_symbol: Optional[str] = Field(default=None, description="Marker symbol type.")
    smooth: bool = Field(default=False, description="Smooth curves for line charts.")
    stack_mode: Optional[str] = Field(default=None, description="Stack mode (normal, percent).")
    bin_size: Optional[int] = Field(default=None, description="Bin size for histograms.")
    normalize: bool = Field(default=False, description="Normalize data to percentages.")
    cumulative: bool = Field(default=False, description="Show cumulative distribution.")
    show_legend: bool = Field(default=True, description="Show legend.")
    show_values: bool = Field(default=False, description="Show data values on chart.")
    value_format: Optional[str] = Field(default=None, description="Format string for values.")
    custom: Dict[str, Any] = Field(
        default_factory=dict, description="Custom visual properties for extensibility."
    )