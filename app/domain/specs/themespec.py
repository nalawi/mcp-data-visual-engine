"""Theme specification for VizSpec."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ThemeSpec(BaseModel):
    """Theme specification for visualization styling.

    Supports built-in themes and custom theme definitions.
    """

    name: str = Field(default="light", description="Theme name (light, dark, corporate, etc.).")
    colors: Optional[Dict[str, str]] = Field(
        default=None,
        description="Custom color overrides (primary, secondary, background, text, etc.).",
    )
    font_family: Optional[str] = Field(default=None, description="Font family for text.")
    font_size: Optional[int] = Field(default=None, description="Base font size.")
    background_color: Optional[str] = Field(default=None, description="Background color.")
    grid_color: Optional[str] = Field(default=None, description="Grid line color.")
    grid_width: Optional[int] = Field(default=None, description="Grid line width.")
    axis_color: Optional[str] = Field(default=None, description="Axis line color.")
    axis_width: Optional[int] = Field(default=None, description="Axis line width.")
    tick_color: Optional[str] = Field(default=None, description="Tick mark color.")
    tick_font_size: Optional[int] = Field(default=None, description="Tick label font size.")
    title_font_size: Optional[int] = Field(default=None, description="Title font size.")
    title_color: Optional[str] = Field(default=None, description="Title text color.")
    legend_font_size: Optional[int] = Field(default=None, description="Legend font size.")
    legend_background: Optional[str] = Field(default=None, description="Legend background color.")
    tooltip_background: Optional[str] = Field(default=None, description="Tooltip background color.")
    tooltip_font_size: Optional[int] = Field(default=None, description="Tooltip font size.")
    border_radius: Optional[int] = Field(default=None, description="Border radius for elements.")
    shadow: Optional[str] = Field(default=None, description="Box shadow specification.")
    custom_css: Optional[str] = Field(default=None, description="Custom CSS overrides.")
    custom: Dict[str, Any] = Field(
        default_factory=dict, description="Custom theme properties."
    )