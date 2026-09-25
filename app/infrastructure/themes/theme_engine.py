"""Theme engine - manages built-in and custom themes."""

from typing import Any, Dict, List, Optional

from app.domain.specs.themespec import ThemeSpec


# Built-in theme definitions
BUILTIN_THEMES: Dict[str, Dict[str, Any]] = {
    "light": {
        "name": "light",
        "background_color": "#ffffff",
        "font_family": "Arial, sans-serif",
        "font_size": 14,
        "grid_color": "#e0e0e0",
        "grid_width": 1,
        "axis_color": "#333333",
        "axis_width": 1,
        "tick_color": "#666666",
        "tick_font_size": 12,
        "title_font_size": 20,
        "title_color": "#1a1a1a",
        "legend_font_size": 12,
        "legend_background": "#ffffff",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 12,
        "border_radius": 4,
        "shadow": "0 2px 4px rgba(0,0,0,0.1)",
    },
    "dark": {
        "name": "dark",
        "background_color": "#1a1a2e",
        "font_family": "Arial, sans-serif",
        "font_size": 14,
        "grid_color": "#2d2d44",
        "grid_width": 1,
        "axis_color": "#a0a0b8",
        "axis_width": 1,
        "tick_color": "#8888aa",
        "tick_font_size": 12,
        "title_font_size": 20,
        "title_color": "#e0e0ff",
        "legend_font_size": 12,
        "legend_background": "#1a1a2e",
        "tooltip_background": "#16213e",
        "tooltip_font_size": 12,
        "border_radius": 4,
        "shadow": "0 2px 4px rgba(0,0,0,0.3)",
    },
    "corporate": {
        "name": "corporate",
        "background_color": "#ffffff",
        "font_family": "Segoe UI, Arial, sans-serif",
        "font_size": 13,
        "grid_color": "#d0d0d0",
        "grid_width": 1,
        "axis_color": "#2b5797",
        "axis_width": 2,
        "tick_color": "#555555",
        "tick_font_size": 11,
        "title_font_size": 22,
        "title_color": "#1e3a5f",
        "legend_font_size": 11,
        "legend_background": "#f8f9fa",
        "tooltip_background": "#f8f9fa",
        "tooltip_font_size": 11,
        "border_radius": 2,
        "shadow": "0 1px 3px rgba(0,0,0,0.12)",
    },
    "government": {
        "name": "government",
        "background_color": "#f8f9fa",
        "font_family": "Georgia, Times New Roman, serif",
        "font_size": 13,
        "grid_color": "#cccccc",
        "grid_width": 1,
        "axis_color": "#333333",
        "axis_width": 1,
        "tick_color": "#555555",
        "tick_font_size": 11,
        "title_font_size": 18,
        "title_color": "#1a1a1a",
        "legend_font_size": 11,
        "legend_background": "#f8f9fa",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 11,
        "border_radius": 0,
        "shadow": "none",
    },
    "finance": {
        "name": "finance",
        "background_color": "#0d1117",
        "font_family": "Consolas, Courier New, monospace",
        "font_size": 13,
        "grid_color": "#21262d",
        "grid_width": 1,
        "axis_color": "#58a6ff",
        "axis_width": 1,
        "tick_color": "#8b949e",
        "tick_font_size": 11,
        "title_font_size": 20,
        "title_color": "#c9d1d9",
        "legend_font_size": 11,
        "legend_background": "#0d1117",
        "tooltip_background": "#161b22",
        "tooltip_font_size": 11,
        "border_radius": 0,
        "shadow": "none",
    },
    "healthcare": {
        "name": "healthcare",
        "background_color": "#f0f8ff",
        "font_family": "Helvetica, Arial, sans-serif",
        "font_size": 14,
        "grid_color": "#d8e8f0",
        "grid_width": 1,
        "axis_color": "#0066a1",
        "axis_width": 1,
        "tick_color": "#444444",
        "tick_font_size": 12,
        "title_font_size": 22,
        "title_color": "#003b5c",
        "legend_font_size": 12,
        "legend_background": "#f0f8ff",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 12,
        "border_radius": 8,
        "shadow": "0 2px 8px rgba(0,102,161,0.15)",
    },
    "transportation": {
        "name": "transportation",
        "background_color": "#fffbf0",
        "font_family": "Futura, Arial, sans-serif",
        "font_size": 14,
        "grid_color": "#e8ddd0",
        "grid_width": 1,
        "axis_color": "#cc5500",
        "axis_width": 2,
        "tick_color": "#666666",
        "tick_font_size": 12,
        "title_font_size": 20,
        "title_color": "#8b3a00",
        "legend_font_size": 12,
        "legend_background": "#fffbf0",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 12,
        "border_radius": 4,
        "shadow": "0 2px 6px rgba(204,85,0,0.2)",
    },
    "energy": {
        "name": "energy",
        "background_color": "#001a00",
        "font_family": "Arial, sans-serif",
        "font_size": 14,
        "grid_color": "#003300",
        "grid_width": 1,
        "axis_color": "#00cc66",
        "axis_width": 1,
        "tick_color": "#66cc99",
        "tick_font_size": 12,
        "title_font_size": 22,
        "title_color": "#00ff88",
        "legend_font_size": 12,
        "legend_background": "#001a00",
        "tooltip_background": "#002200",
        "tooltip_font_size": 12,
        "border_radius": 0,
        "shadow": "0 0 10px rgba(0,255,136,0.3)",
    },
    "presentation": {
        "name": "presentation",
        "background_color": "#ffffff",
        "font_family": "Calibri, Arial, sans-serif",
        "font_size": 16,
        "grid_color": "#cccccc",
        "grid_width": 1,
        "axis_color": "#333333",
        "axis_width": 2,
        "tick_color": "#555555",
        "tick_font_size": 14,
        "title_font_size": 28,
        "title_color": "#000000",
        "legend_font_size": 14,
        "legend_background": "#ffffff",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 14,
        "border_radius": 0,
        "shadow": "0 4px 12px rgba(0,0,0,0.15)",
    },
    "scientific": {
        "name": "scientific",
        "background_color": "#ffffff",
        "font_family": "Arial, sans-serif",
        "font_size": 12,
        "grid_color": "#b0b0b0",
        "grid_width": 1,
        "axis_color": "#000000",
        "axis_width": 1,
        "tick_color": "#000000",
        "tick_font_size": 10,
        "title_font_size": 16,
        "title_color": "#000000",
        "legend_font_size": 10,
        "legend_background": "#ffffff",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 10,
        "border_radius": 0,
        "shadow": "none",
    },
    "ieee": {
        "name": "ieee",
        "background_color": "#ffffff",
        "font_family": "Times New Roman, serif",
        "font_size": 10,
        "grid_color": "#cccccc",
        "grid_width": 0.5,
        "axis_color": "#000000",
        "axis_width": 1,
        "tick_color": "#000000",
        "tick_font_size": 9,
        "title_font_size": 12,
        "title_color": "#000000",
        "legend_font_size": 9,
        "legend_background": "#ffffff",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 9,
        "border_radius": 0,
        "shadow": "none",
    },
    "nature": {
        "name": "nature",
        "background_color": "#fafaf5",
        "font_family": "Georgia, serif",
        "font_size": 12,
        "grid_color": "#e0ddd0",
        "grid_width": 0.5,
        "axis_color": "#3a3a3a",
        "axis_width": 1,
        "tick_color": "#5a5a5a",
        "tick_font_size": 10,
        "title_font_size": 18,
        "title_color": "#2d5016",
        "legend_font_size": 10,
        "legend_background": "#fafaf5",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 10,
        "border_radius": 0,
        "shadow": "none",
    },
    "minimal": {
        "name": "minimal",
        "background_color": "#ffffff",
        "font_family": "Helvetica, Arial, sans-serif",
        "font_size": 12,
        "grid_color": "#eeeeee",
        "grid_width": 0.5,
        "axis_color": "#999999",
        "axis_width": 1,
        "tick_color": "#999999",
        "tick_font_size": 10,
        "title_font_size": 16,
        "title_color": "#333333",
        "legend_font_size": 10,
        "legend_background": "#ffffff",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 10,
        "border_radius": 0,
        "shadow": "none",
    },
    "instagram": {
        "name": "instagram",
        "background_color": "#ffffff",
        "font_family": "Helvetica Neue, Arial, sans-serif",
        "font_size": 14,
        "grid_color": "#f0f0f0",
        "grid_width": 0.5,
        "axis_color": "#262626",
        "axis_width": 1,
        "tick_color": "#8e8e8e",
        "tick_font_size": 12,
        "title_font_size": 22,
        "title_color": "#262626",
        "legend_font_size": 12,
        "legend_background": "#ffffff",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 12,
        "border_radius": 12,
        "shadow": "0 4px 16px rgba(0,0,0,0.1)",
        "custom_css": "font-weight: 600; letter-spacing: 0.5px;",
    },
    "linkedin": {
        "name": "linkedin",
        "background_color": "#ffffff",
        "font_family": "Arial, sans-serif",
        "font_size": 14,
        "grid_color": "#e0e0e0",
        "grid_width": 1,
        "axis_color": "#0a66c2",
        "axis_width": 1,
        "tick_color": "#555555",
        "tick_font_size": 12,
        "title_font_size": 20,
        "title_color": "#0a66c2",
        "legend_font_size": 12,
        "legend_background": "#ffffff",
        "tooltip_background": "#ffffff",
        "tooltip_font_size": 12,
        "border_radius": 4,
        "shadow": "0 1px 3px rgba(0,0,0,0.08)",
    },
}

# Color palettes for built-in themes
THEME_COLOR_PALETTES: Dict[str, List[str]] = {
    "light": [
        "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
        "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac",
    ],
    "dark": [
        "#00bcd4", "#ff5722", "#8bc34a", "#ffeb3b", "#e91e63",
        "#9c27b0", "#3f51b5", "#00acc1", "#ff9800", "#4caf50",
    ],
    "corporate": [
        "#2b5797", "#1e3a5f", "#00a4ef", "#0078d4", "#50e6ff",
        "#106ebe", "#5c2d91", "#e81123", "#ff8c00", "#107c10",
    ],
    "government": [
        "#4a6fa5", "#8b4513", "#556b2f", "#708090", "#2f4f4f",
        "#191970", "#006400", "#8b0000", "#ff8c00", "#9400d3",
    ],
    "finance": [
        "#00ff00", "#ff4444", "#00ccff", "#ffff00", "#ff00ff",
        "#00ff88", "#ff8800", "#8888ff", "#ff0088", "#88ff00",
    ],
    "healthcare": [
        "#0066a1", "#0099cc", "#66c2e0", "#003b5c", "#00a1b2",
        "#7eb8da", "#005a8c", "#b3ddf2", "#2b7a78", "#3aafa9",
    ],
    "transportation": [
        "#cc5500", "#ff8800", "#ffaa44", "#8b3a00", "#ffcc88",
        "#e07000", "#ff6600", "#ff9933", "#cc4400", "#aa5500",
    ],
    "energy": [
        "#00ff88", "#00cc66", "#66ff99", "#009944", "#33ff77",
        "#00bb55", "#99ffbb", "#007733", "#ccffdd", "#005522",
    ],
    "presentation": [
        "#4472c4", "#ed7d31", "#a5a5a5", "#ffc000", "#5b9bd5",
        "#70ad47", "#264478", "#9b57a4", "#636363", "#e88a3a",
    ],
    "scientific": [
        "#000000", "#404040", "#808080", "#b0b0b0", "#d0d0d0",
        "#1a1a1a", "#606060", "#a0a0a0", "#c0c0c0", "#e0e0e0",
    ],
    "ieee": [
        "#000000", "#444444", "#888888", "#bbbbbb", "#cccccc",
        "#222222", "#666666", "#aaaaaa", "#dddddd", "#eeeeee",
    ],
    "nature": [
        "#2d5016", "#5a8f3c", "#8db86a", "#bbddaa", "#d4e8c0",
        "#3a6b1f", "#6aa84f", "#a0c685", "#c4dbb4", "#e2efd6",
    ],
    "minimal": [
        "#333333", "#666666", "#999999", "#bbbbbb", "#cccccc",
        "#555555", "#777777", "#aaaaaa", "#dddddd", "#eeeeee",
    ],
    "instagram": [
        "#405de6", "#5851db", "#833ab4", "#c13584", "#e1306c",
        "#fd1d1d", "#f56040", "#f77737", "#fcaf45", "#ffdc80",
    ],
    "linkedin": [
        "#0a66c2", "#004182", "#7fc15e", "#e0a800", "#f5f5f5",
        "#057642", "#d11124", "#86888a", "#000000", "#ffffff",
    ],
}


class ThemeEngine:
    """Manages theme resolution, registration, and application.

    Supports built-in themes and custom user-registered themes.
    """

    def __init__(self) -> None:
        """Initialize the theme engine with built-in themes."""
        self._themes: Dict[str, Dict[str, Any]] = dict(BUILTIN_THEMES)
        self._palettes: Dict[str, List[str]] = dict(THEME_COLOR_PALETTES)

    def get_theme(self, name: str) -> Dict[str, Any]:
        """Get a theme definition by name.

        Args:
            name: Theme name.

        Returns:
            Theme definition dictionary.

        Raises:
            KeyError: If theme is not found.
        """
        if name not in self._themes:
            raise KeyError(f"Theme '{name}' not found. Available themes: {self.list_themes()}")
        return dict(self._themes[name])

    def get_palette(self, name: str) -> List[str]:
        """Get a color palette by theme name.

        Args:
            name: Theme name.

        Returns:
            List of color hex strings.
        """
        if name in self._palettes:
            return list(self._palettes[name])
        return list(THEME_COLOR_PALETTES.get("light", []))

    def register_theme(self, name: str, theme: Dict[str, Any]) -> None:
        """Register a custom theme.

        Args:
            name: Theme name.
            theme: Theme definition dictionary.
        """
        self._themes[name] = theme

    def register_palette(self, name: str, palette: List[str]) -> None:
        """Register a custom color palette.

        Args:
            name: Palette/theme name.
            palette: List of color hex strings.
        """
        self._palettes[name] = palette

    def remove_theme(self, name: str) -> None:
        """Remove a registered theme.

        Args:
            name: Theme name. Cannot remove built-in themes.
        """
        if name in BUILTIN_THEMES:
            raise ValueError(f"Cannot remove built-in theme '{name}'.")
        self._themes.pop(name, None)
        self._palettes.pop(name, None)

    def list_themes(self) -> List[str]:
        """List all available theme names.

        Returns:
            Sorted list of theme names.
        """
        return sorted(self._themes.keys())

    def resolve_theme(self, spec: ThemeSpec) -> Dict[str, Any]:
        """Resolve a ThemeSpec into a complete theme configuration.

        Merges the base theme with any custom overrides from the spec.

        Args:
            spec: Theme specification.

        Returns:
            Complete resolved theme configuration.
        """
        base_name = spec.name or "light"
        try:
            base = self.get_theme(base_name)
        except KeyError:
            base = self.get_theme("light")

        # Override with spec values if provided
        resolved = dict(base)
        override_map = {
            "colors": "colors",
            "font_family": "font_family",
            "font_size": "font_size",
            "background_color": "background_color",
            "grid_color": "grid_color",
            "grid_width": "grid_width",
            "axis_color": "axis_color",
            "axis_width": "axis_width",
            "tick_color": "tick_color",
            "tick_font_size": "tick_font_size",
            "title_font_size": "title_font_size",
            "title_color": "title_color",
            "legend_font_size": "legend_font_size",
            "legend_background": "legend_background",
            "tooltip_background": "tooltip_background",
            "tooltip_font_size": "tooltip_font_size",
            "border_radius": "border_radius",
            "shadow": "shadow",
            "custom_css": "custom_css",
        }

        for spec_attr, resolved_key in override_map.items():
            spec_value = getattr(spec, spec_attr, None)
            if spec_value is not None:
                resolved[resolved_key] = spec_value

        # Merge custom properties
        if spec.custom:
            resolved.setdefault("custom", {}).update(spec.custom)

        return resolved

    def get_palette_for_spec(self, spec: ThemeSpec) -> List[str]:
        """Get the color palette for a ThemeSpec.

        Args:
            spec: Theme specification.

        Returns:
            List of color hex strings.
        """
        name = spec.name or "light"
        palette = self.get_palette(name)
        if spec.colors:
            # If spec has custom colors, use those as overrides
            custom_colors = spec.colors
            if isinstance(custom_colors, dict):
                # Convert dict to list if needed
                pass
            elif isinstance(custom_colors, list):
                palette = custom_colors + palette[len(custom_colors):]
        return palette


# Singleton instance
theme_engine = ThemeEngine()