"""Layout specification for VizSpec."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LayoutSpec(BaseModel):
    """Layout specification for visualization positioning and sizing."""

    width: Optional[int] = Field(default=None, description="Chart width in pixels.")
    height: Optional[int] = Field(default=None, description="Chart height in pixels.")
    margin_top: int = Field(default=50, description="Top margin in pixels.")
    margin_bottom: int = Field(default=50, description="Bottom margin in pixels.")
    margin_left: int = Field(default=50, description="Left margin in pixels.")
    margin_right: int = Field(default=50, description="Right margin in pixels.")
    padding: int = Field(default=10, description="Padding around chart area.")
    legend_position: str = Field(default="right", description="Legend position (top, bottom, left, right, none).")
    legend_orientation: str = Field(default="v", description="Legend orientation (h, v).")
    title_position: str = Field(default="top", description="Title position (top, bottom).")
    xaxis_title: Optional[str] = Field(default=None, description="X-axis title.")
    yaxis_title: Optional[str] = Field(default=None, description="Y-axis title.")
    xaxis_type: Optional[str] = Field(default=None, description="X-axis type (linear, log, date, category).")
    yaxis_type: Optional[str] = Field(default=None, description="Y-axis type (linear, log, date, category).")
    xaxis_range: Optional[List[Any]] = Field(default=None, description="X-axis range [min, max].")
    yaxis_range: Optional[List[Any]] = Field(default=None, description="Y-axis range [min, max].")
    xaxis_tickangle: Optional[int] = Field(default=None, description="X-axis tick angle.")
    yaxis_tickangle: Optional[int] = Field(default=None, description="Y-axis tick angle.")
    show_grid: bool = Field(default=True, description="Show grid lines.")
    grid_x: bool = Field(default=True, description="Show x-axis grid lines.")
    grid_y: bool = Field(default=True, description="Show y-axis grid lines.")
    subplots: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Subplot definitions for multi-chart layouts."
    )
    subplot_rows: int = Field(default=1, description="Number of subplot rows.")
    subplot_cols: int = Field(default=1, description="Number of subplot columns.")
    subplot_titles: Optional[List[str]] = Field(default=None, description="Subplot titles.")
    responsive: bool = Field(default=True, description="Responsive sizing.")
    print_layout: bool = Field(default=False, description="Optimize for print layout.")
    custom: Dict[str, Any] = Field(default_factory=dict, description="Custom layout properties.")