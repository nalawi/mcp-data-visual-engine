"""Plotly renderer implementation - converts VizSpec to Plotly figures."""

import base64
import io
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app.domain.specs.vizspec import VizSpec
from app.domain.specs.visualspec import ChartType
from app.domain.exceptions.base import RendererError
from app.infrastructure.renderers.base.base_renderer import BaseRenderer
from app.infrastructure.themes.theme_engine import theme_engine

logger = logging.getLogger(__name__)


class PlotlyRenderer(BaseRenderer):
    """Plotly-based renderer that converts VizSpec to interactive visualizations.

    This is the initial renderer implementation. It supports all 50+ chart types
    defined in ChartType enum. The application layer never imports this directly -
    only through the Renderer interface.
    """

    def __init__(self) -> None:
        """Initialize the Plotly renderer."""
        super().__init__()
        self._name = "plotly"
        self._version = "5.18.0"

    def render(self, spec: VizSpec) -> go.Figure:
        """Generate a Plotly figure from a VizSpec.

        Args:
            spec: The validated VizSpec to render.

        Returns:
            Plotly Figure object.

        Raises:
            RendererError: If rendering fails.
        """
        try:
            chart_type = spec.visual.type
            if chart_type is None:
                raise RendererError(
                    message="Chart type is required. Please call tool 'see_spec_schema_reference' to see all references",
                    renderer_name=self._name,
                )

            # Dispatch to the appropriate chart builder
            figure = self._build_chart(spec, chart_type)
            self._apply_layout(spec, figure)
            self._apply_annotations(spec, figure)
            self._apply_theme(spec, figure)
            return figure
        except RendererError:
            raise
        except Exception as e:
            raise RendererError(
                message=f"Failed to render chart: {str(e)}",
                renderer_name=self._name,
                details={"chart_type": spec.visual.type.value if spec.visual.type else "unknown"},
            ) from e

    def render_png(self, spec: VizSpec, **kwargs: Any) -> bytes:
        """Render and export as PNG bytes.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            PNG image bytes.
        """
        figure = self.render(spec)
        width = kwargs.get("width", spec.layout.width or 800)
        height = kwargs.get("height", spec.layout.height or 600)
        scale = kwargs.get("scale", spec.output.scale)
        img_bytes = figure.to_image(format="png", width=width, height=height, scale=scale)
        return img_bytes

    def render_svg(self, spec: VizSpec, **kwargs: Any) -> str:
        """Render and export as SVG string.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            SVG XML string.
        """
        figure = self.render(spec)
        width = kwargs.get("width", spec.layout.width or 800)
        height = kwargs.get("height", spec.layout.height or 600)
        svg_str = figure.to_image(format="svg", width=width, height=height)
        return svg_str.decode("utf-8") if isinstance(svg_str, bytes) else svg_str

    def render_pdf(self, spec: VizSpec, **kwargs: Any) -> bytes:
        """Render and export as PDF bytes.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            PDF bytes.
        """
        figure = self.render(spec)
        width = kwargs.get("width", spec.layout.width or 800)
        height = kwargs.get("height", spec.layout.height or 600)
        pdf_bytes = figure.to_image(format="pdf", width=width, height=height)
        return pdf_bytes

    def render_html(self, spec: VizSpec, **kwargs: Any) -> str:
        """Render and export as HTML string.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            HTML string.
        """
        figure = self.render(spec)
        include_plotlyjs = kwargs.get("include_plotlyjs", spec.output.include_plotlyjs)
        full_html = kwargs.get("full_html", spec.output.full_html)
        html_str = figure.to_html(
            include_plotlyjs=include_plotlyjs,
            full_html=full_html,
            config={"responsive": spec.layout.responsive},
        )
        return html_str

    def render_json(self, spec: VizSpec, **kwargs: Any) -> str:
        """Render and export as JSON string (Plotly JSON format).

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            JSON string of the figure data.
        """
        figure = self.render(spec)
        return figure.to_json()

    def render_base64(self, spec: VizSpec, **kwargs: Any) -> str:
        """Render and export as base64-encoded PNG string.

        Args:
            spec: The VizSpec to render.
            **kwargs: Additional export options.

        Returns:
            Base64-encoded PNG data URI.
        """
        png_bytes = self.render_png(spec, **kwargs)
        return self._encode_base64(png_bytes, "image/png")

    def get_supported_chart_types(self) -> List[str]:
        """Get list of chart types supported by this renderer.

        Returns:
            List of all chart type strings.
        """
        return [ct.value for ct in ChartType]

    def _build_chart(self, spec: VizSpec, chart_type: ChartType) -> go.Figure:
        """Build a Plotly figure based on chart type.

        Args:
            spec: The VizSpec to render.
            chart_type: The type of chart to build.

        Returns:
            Plotly Figure object.
        """
        chart_builders = {
            ChartType.LINE: self._build_line_chart,
            ChartType.SPLINE: self._build_spline_chart,
            ChartType.AREA: self._build_area_chart,
            ChartType.STACKED_AREA: self._build_stacked_area_chart,
            ChartType.BAR: self._build_bar_chart,
            ChartType.GROUPED_BAR: self._build_grouped_bar_chart,
            ChartType.STACKED_BAR: self._build_stacked_bar_chart,
            ChartType.HORIZONTAL_BAR: self._build_horizontal_bar_chart,
            ChartType.PIE: self._build_pie_chart,
            ChartType.DONUT: self._build_donut_chart,
            ChartType.TREEMAP: self._build_treemap,
            ChartType.SUNBURST: self._build_sunburst,
            ChartType.SCATTER: self._build_scatter_chart,
            ChartType.BUBBLE: self._build_bubble_chart,
            ChartType.HISTOGRAM: self._build_histogram,
            ChartType.DENSITY: self._build_density_chart,
            ChartType.BOX_PLOT: self._build_box_plot,
            ChartType.VIOLIN: self._build_violin,
            ChartType.STRIP: self._build_strip,
            ChartType.HEATMAP: self._build_heatmap,
            ChartType.CORRELATION_MATRIX: self._build_correlation_matrix,
            ChartType.HEXBIN: self._build_hexbin,
            ChartType.CONTOUR: self._build_contour,
            ChartType.RADAR: self._build_radar,
            ChartType.POLAR: self._build_polar,
            ChartType.WATERFALL: self._build_waterfall,
            ChartType.FUNNEL: self._build_funnel,
            ChartType.GAUGE: self._build_gauge,
            ChartType.INDICATOR: self._build_indicator,
            ChartType.TIMELINE: self._build_timeline,
            ChartType.GANTT: self._build_gantt,
            ChartType.CANDLESTICK: self._build_candlestick,
            ChartType.OHLC: self._build_ohlc,
            ChartType.FINANCIAL_VOLUME: self._build_financial_volume,
            ChartType.SCATTER_3D: self._build_scatter_3d,
            ChartType.SURFACE_3D: self._build_surface_3d,
            ChartType.MESH_3D: self._build_mesh_3d,
            ChartType.PARALLEL_COORDINATES: self._build_parallel_coordinates,
            ChartType.PARALLEL_CATEGORIES: self._build_parallel_categories,
            ChartType.NETWORK_GRAPH: self._build_network_graph,
            ChartType.SANKEY: self._build_sankey,
            ChartType.CHORD_DIAGRAM: self._build_chord_diagram,
            ChartType.CALENDAR_HEATMAP: self._build_calendar_heatmap,
            ChartType.MAP_SCATTER: self._build_map_scatter,
            ChartType.MAP_BUBBLE: self._build_map_bubble,
            ChartType.CHOROPLETH: self._build_choropleth,
            ChartType.FLOW_DIAGRAM: self._build_flow_diagram,
        }

        builder = chart_builders.get(chart_type)
        if builder is None:
            raise RendererError(
                message=f"Unsupported chart type: {chart_type.value}",
                renderer_name=self._name,
            )
        return builder(spec)

    def _prepare_dataframe(self, spec: VizSpec) -> pd.DataFrame:
        """Convert VizSpec data records to a pandas DataFrame.

        Args:
            spec: The VizSpec containing data.

        Returns:
            pandas DataFrame.
        """
        records = self._extract_data(spec)
        if not records:
            return pd.DataFrame()
        return pd.DataFrame(records)

    def _get_encoding_fields(self, spec: VizSpec) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        """Extract encoding field names from VizSpec.

        Args:
            spec: The VizSpec containing encoding.

        Returns:
            Tuple of (x, y, color, size) field names.
        """
        encoding = spec.encoding or {}
        return (
            encoding.get("x"),
            encoding.get("y"),
            encoding.get("color"),
            encoding.get("size"),
        )

    def _build_line_chart(self, spec: VizSpec) -> go.Figure:
        """Build a line chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        if color and color in df.columns:
            fig = px.line(
                df, x=x, y=y, color=color,
                color_discrete_sequence=palette,
                line_shape="linear" if not spec.visual.smooth else "spline",
            )
        else:
            fig = px.line(
                df, x=x, y=y,
                color_discrete_sequence=palette,
                line_shape="linear" if not spec.visual.smooth else "spline",
            )
        return fig

    def _build_spline_chart(self, spec: VizSpec) -> go.Figure:
        """Build a spline chart (smoothed line)."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        if color and color in df.columns:
            fig = px.line(
                df, x=x, y=y, color=color,
                color_discrete_sequence=palette,
                line_shape="spline",
            )
        else:
            fig = px.line(
                df, x=x, y=y,
                color_discrete_sequence=palette,
                line_shape="spline",
            )
        return fig

    def _build_area_chart(self, spec: VizSpec) -> go.Figure:
        """Build an area chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        if color and color in df.columns:
            fig = px.area(
                df, x=x, y=y, color=color,
                color_discrete_sequence=palette,
                line_shape="linear" if not spec.visual.smooth else "spline",
            )
        else:
            fig = px.area(
                df, x=x, y=y,
                color_discrete_sequence=palette,
                line_shape="linear" if not spec.visual.smooth else "spline",
            )
        return fig

    def _build_stacked_area_chart(self, spec: VizSpec) -> go.Figure:
        """Build a stacked area chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.area(
            df, x=x, y=y, color=color,
            color_discrete_sequence=palette,
            line_shape="linear" if not spec.visual.smooth else "spline",
            groupnorm=None,
        )
        return fig

    def _build_bar_chart(self, spec: VizSpec) -> go.Figure:
        """Build a bar chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        if color and color in df.columns:
            fig = px.bar(
                df, x=x, y=y, color=color,
                color_discrete_sequence=palette,
                barmode="relative",
            )
        else:
            fig = px.bar(
                df, x=x, y=y,
                color_discrete_sequence=palette,
            )
        return fig

    def _build_grouped_bar_chart(self, spec: VizSpec) -> go.Figure:
        """Build a grouped bar chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.bar(
            df, x=x, y=y, color=color,
            color_discrete_sequence=palette,
            barmode="group",
        )
        return fig

    def _build_stacked_bar_chart(self, spec: VizSpec) -> go.Figure:
        """Build a stacked bar chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.bar(
            df, x=x, y=y, color=color,
            color_discrete_sequence=palette,
            barmode="stack",
        )
        return fig

    def _build_horizontal_bar_chart(self, spec: VizSpec) -> go.Figure:
        """Build a horizontal bar chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        if color and color in df.columns:
            fig = px.bar(
                df, x=x, y=y, color=color,
                color_discrete_sequence=palette,
                orientation="h",
            )
        else:
            fig = px.bar(
                df, x=x, y=y,
                color_discrete_sequence=palette,
                orientation="h",
            )
        return fig

    def _build_pie_chart(self, spec: VizSpec) -> go.Figure:
        """Build a pie chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        names = color or x
        values = y or x

        fig = px.pie(
            df, names=names, values=values,
            color_discrete_sequence=palette,
        )
        return fig

    def _build_donut_chart(self, spec: VizSpec) -> go.Figure:
        """Build a donut chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        names = color or x
        values = y or x

        fig = px.pie(
            df, names=names, values=values,
            color_discrete_sequence=palette,
            hole=0.4,
        )
        return fig

    def _build_treemap(self, spec: VizSpec) -> go.Figure:
        """Build a treemap."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.treemap(
            df, path=[x] if x else [], values=y,
            color=color,
            color_discrete_sequence=palette,
        )
        return fig

    def _build_sunburst(self, spec: VizSpec) -> go.Figure:
        """Build a sunburst chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.sunburst(
            df, path=[x] if x else [], values=y,
            color=color,
            color_discrete_sequence=palette,
        )
        return fig

    def _build_scatter_chart(self, spec: VizSpec) -> go.Figure:
        """Build a scatter plot."""
        df = self._prepare_dataframe(spec)
        x, y, color, size = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.scatter(
            df, x=x, y=y, color=color, size=size,
            color_discrete_sequence=palette,
            opacity=spec.visual.opacity,
        )
        return fig

    def _build_bubble_chart(self, spec: VizSpec) -> go.Figure:
        """Build a bubble chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, size = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        if not size:
            size = y
        fig = px.scatter(
            df, x=x, y=y, color=color, size=size,
            color_discrete_sequence=palette,
            size_max=60,
            opacity=spec.visual.opacity,
        )
        return fig

    def _build_histogram(self, spec: VizSpec) -> go.Figure:
        """Build a histogram."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.histogram(
            df, x=x, y=y, color=color,
            color_discrete_sequence=palette,
            nbins=spec.visual.bin_size,
            histnorm="percent" if spec.visual.normalize else None,
            cumulative=spec.visual.cumulative,
        )
        return fig

    def _build_density_chart(self, spec: VizSpec) -> go.Figure:
        """Build a density plot."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.density_contour(
            df, x=x, y=y, color=color,
            color_discrete_sequence=palette,
        )
        return fig

    def _build_box_plot(self, spec: VizSpec) -> go.Figure:
        """Build a box plot."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.box(
            df, x=x, y=y, color=color,
            color_discrete_sequence=palette,
        )
        return fig

    def _build_violin(self, spec: VizSpec) -> go.Figure:
        """Build a violin plot."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.violin(
            df, x=x, y=y, color=color,
            color_discrete_sequence=palette,
            box=True,
        )
        return fig

    def _build_strip(self, spec: VizSpec) -> go.Figure:
        """Build a strip plot."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.strip(
            df, x=x, y=y, color=color,
            color_discrete_sequence=palette,
        )
        return fig

    def _build_heatmap(self, spec: VizSpec) -> go.Figure:
        """Build a heatmap."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)

        if x and y and color:
            pivot = df.pivot_table(index=y, columns=x, values=color, aggfunc="mean")
            fig = px.imshow(
                pivot.values,
                x=pivot.columns.tolist(),
                y=pivot.index.tolist(),
                color_continuous_scale="Viridis",
                aspect="auto",
            )
        else:
            fig = px.imshow(
                df.select_dtypes(include="number").values,
                aspect="auto",
            )
        return fig

    def _build_correlation_matrix(self, spec: VizSpec) -> go.Figure:
        """Build a correlation matrix heatmap."""
        df = self._prepare_dataframe(spec)
        numeric_df = df.select_dtypes(include="number")
        corr = numeric_df.corr()

        fig = px.imshow(
            corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            color_continuous_scale="RdBu_r",
            aspect="auto",
            text_auto=".2f",
            title="Correlation Matrix",
        )
        return fig

    def _build_hexbin(self, spec: VizSpec) -> go.Figure:
        """Build a hexbin plot."""
        df = self._prepare_dataframe(spec)
        x, y, _, _ = self._get_encoding_fields(spec)

        fig = px.density_heatmap(
            df, x=x, y=y,
            marginal_x="histogram",
            marginal_y="histogram",
        )
        return fig

    def _build_contour(self, spec: VizSpec) -> go.Figure:
        """Build a contour plot."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)

        if x and y and color:
            pivot = df.pivot_table(index=y, columns=x, values=color, aggfunc="mean")
            fig = go.Figure(data=go.Contour(
                z=pivot.values,
                x=pivot.columns.tolist(),
                y=pivot.index.tolist(),
                colorscale="Viridis",
            ))
        else:
            fig = go.Figure(data=go.Contour(
                z=df.select_dtypes(include="number").values,
                colorscale="Viridis",
            ))
        return fig

    def _build_radar(self, spec: VizSpec) -> go.Figure:
        """Build a radar chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.line_polar(
            df, r=y, theta=x, color=color,
            color_discrete_sequence=palette,
            line_close=True,
        )
        return fig

    def _build_polar(self, spec: VizSpec) -> go.Figure:
        """Build a polar chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.scatter_polar(
            df, r=y, theta=x, color=color,
            color_discrete_sequence=palette,
        )
        return fig

    def _build_waterfall(self, spec: VizSpec) -> go.Figure:
        """Build a waterfall chart."""
        df = self._prepare_dataframe(spec)
        x, y, _, _ = self._get_encoding_fields(spec)

        if x and y:
            values = df[y].tolist()
            text = [f"{v:+,}" for v in values]
            fig = go.Figure(data=go.Waterfall(
                x=df[x].tolist(),
                y=values,
                text=text,
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
        else:
            fig = go.Figure()
        return fig

    def _build_funnel(self, spec: VizSpec) -> go.Figure:
        """Build a funnel chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.funnel(
            df, x=y, y=x, color=color,
            color_discrete_sequence=palette,
        )
        return fig

    def _build_gauge(self, spec: VizSpec) -> go.Figure:
        """Build a gauge chart."""
        df = self._prepare_dataframe(spec)
        _, y, _, _ = self._get_encoding_fields(spec)

        value = df[y].iloc[0] if y is not None and not df.empty else 0
        fig = go.Figure(data=go.Indicator(
            mode="gauge+number",
            value=float(value),
            gauge={"axis": {"range": [None, 100]}},
        ))
        return fig

    def _build_indicator(self, spec: VizSpec) -> go.Figure:
        """Build an indicator chart."""
        df = self._prepare_dataframe(spec)
        _, y, _, _ = self._get_encoding_fields(spec)

        value = df[y].iloc[0] if y is not None and not df.empty else 0
        title = spec.metadata.get("title", "")

        fig = go.Figure(data=go.Indicator(
            mode="number+delta",
            value=float(value),
            title={"text": title},
            number={"font": {"size": 60}},
        ))
        return fig

    def _build_timeline(self, spec: VizSpec) -> go.Figure:
        """Build a timeline chart."""
        df = self._prepare_dataframe(spec)
        x, y, color, _ = self._get_encoding_fields(spec)
        palette = self._get_color_palette(spec)

        fig = px.timeline(
            df, x_start=x, x_end=y, y=color,
            color=color,
            color_discrete_sequence=palette,
        )
        return fig

    def _build_gantt(self, spec: VizSpec) -> go.Figure:
        """Build a Gantt chart."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        task = encoding.get("task", encoding.get("y"))
        start = encoding.get("start", encoding.get("x"))
        end = encoding.get("end")
        resource = encoding.get("resource", encoding.get("color"))
        palette = self._get_color_palette(spec)

        if end:
            fig = px.timeline(
                df, x_start=start, x_end=end, y=task, color=resource,
                color_discrete_sequence=palette,
            )
        else:
            fig = px.timeline(
                df, x_start=start, y=task, color=resource,
                color_discrete_sequence=palette,
            )
        return fig

    def _build_candlestick(self, spec: VizSpec) -> go.Figure:
        """Build a candlestick chart."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        x = encoding.get("x")
        open_f = encoding.get("open", encoding.get("y"))
        high = encoding.get("high")
        low = encoding.get("low")
        close = encoding.get("close")

        if x and open_f and high and low and close:
            fig = go.Figure(data=go.Candlestick(
                x=df[x].tolist(),
                open=df[open_f].tolist(),
                high=df[high].tolist(),
                low=df[low].tolist(),
                close=df[close].tolist(),
            ))
        else:
            fig = go.Figure()
        return fig

    def _build_ohlc(self, spec: VizSpec) -> go.Figure:
        """Build an OHLC chart."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        x = encoding.get("x")
        open_f = encoding.get("open", encoding.get("y"))
        high = encoding.get("high")
        low = encoding.get("low")
        close = encoding.get("close")

        if x and open_f and high and low and close:
            fig = go.Figure(data=go.Ohlc(
                x=df[x].tolist(),
                open=df[open_f].tolist(),
                high=df[high].tolist(),
                low=df[low].tolist(),
                close=df[close].tolist(),
            ))
        else:
            fig = go.Figure()
        return fig

    def _build_financial_volume(self, spec: VizSpec) -> go.Figure:
        """Build a financial volume chart (candlestick + volume)."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        x = encoding.get("x")
        open_f = encoding.get("open", encoding.get("y"))
        high = encoding.get("high")
        low = encoding.get("low")
        close = encoding.get("close")
        volume = encoding.get("volume")

        if x and open_f and high and low and close:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                row_heights=[0.7, 0.3],
            )
            fig.add_trace(
                go.Candlestick(
                    x=df[x].tolist(),
                    open=df[open_f].tolist(),
                    high=df[high].tolist(),
                    low=df[low].tolist(),
                    close=df[close].tolist(),
                    name="Price",
                ),
                row=1, col=1,
            )
            if volume and volume in df.columns:
                fig.add_trace(
                    go.Bar(
                        x=df[x].tolist(),
                        y=df[volume].tolist(),
                        name="Volume",
                        marker_color="rgba(0,150,255,0.5)",
                    ),
                    row=2, col=1,
                )
            fig.update_layout(xaxis_rangeslider_visible=False)
        else:
            fig = go.Figure()
        return fig

    def _build_scatter_3d(self, spec: VizSpec) -> go.Figure:
        """Build a 3D scatter plot."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        x = encoding.get("x")
        y = encoding.get("y")
        z = encoding.get("z")
        color = encoding.get("color")
        size = encoding.get("size")
        palette = self._get_color_palette(spec)

        fig = px.scatter_3d(
            df, x=x, y=y, z=z, color=color, size=size,
            color_discrete_sequence=palette,
            opacity=spec.visual.opacity,
        )
        return fig

    def _build_surface_3d(self, spec: VizSpec) -> go.Figure:
        """Build a 3D surface plot."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        x = encoding.get("x")
        y = encoding.get("y")
        z = encoding.get("z", encoding.get("color"))

        if x and y and z:
            pivot = df.pivot_table(index=y, columns=x, values=z, aggfunc="mean")
            fig = go.Figure(data=go.Surface(
                z=pivot.values,
                x=pivot.columns.tolist(),
                y=pivot.index.tolist(),
                colorscale="Viridis",
            ))
        else:
            fig = go.Figure()
        return fig

    def _build_mesh_3d(self, spec: VizSpec) -> go.Figure:
        """Build a 3D mesh plot."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        x = encoding.get("x")
        y = encoding.get("y")
        z = encoding.get("z")
        color = encoding.get("color")

        if x and y and z:
            fig = go.Figure(data=go.Mesh3d(
                x=df[x].tolist(),
                y=df[y].tolist(),
                z=df[z].tolist(),
                color=color if color and color in df.columns else "lightblue",
                opacity=spec.visual.opacity,
            ))
        else:
            fig = go.Figure()
        return fig

    def _build_parallel_coordinates(self, spec: VizSpec) -> go.Figure:
        """Build a parallel coordinates plot."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        color = encoding.get("color")
        dimensions = [c for c in df.select_dtypes(include="number").columns if c != color]

        fig = px.parallel_coordinates(
            df, dimensions=dimensions, color=color,
            color_continuous_scale="Viridis",
        )
        return fig

    def _build_parallel_categories(self, spec: VizSpec) -> go.Figure:
        """Build a parallel categories plot."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        color = encoding.get("color")
        dimensions = [c for c in df.columns if c != color]

        fig = px.parallel_categories(
            df, dimensions=dimensions, color=color,
        )
        return fig

    def _build_network_graph(self, spec: VizSpec) -> go.Figure:
        """Build a network graph."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        source = encoding.get("source", encoding.get("x"))
        target = encoding.get("target", encoding.get("y"))
        value = encoding.get("value", encoding.get("color"))

        if source and target and source in df.columns and target in df.columns:
            fig = go.Figure(data=go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=list(set(df[source].tolist() + df[target].tolist())),
                ),
                link=dict(
                    source=[list(set(df[source].tolist() + df[target].tolist())).index(s) for s in df[source]],
                    target=[list(set(df[source].tolist() + df[target].tolist())).index(t) for t in df[target]],
                    value=df[value].tolist() if value and value in df.columns else [1] * len(df),
                ),
            ))
        else:
            fig = go.Figure()
        return fig

    def _build_sankey(self, spec: VizSpec) -> go.Figure:
        """Build a Sankey diagram."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        source = encoding.get("source", encoding.get("x"))
        target = encoding.get("target", encoding.get("y"))
        value = encoding.get("value", encoding.get("color"))

        if source and target and source in df.columns and target in df.columns:
            all_nodes = list(set(df[source].tolist() + df[target].tolist()))
            node_indices = {node: i for i, node in enumerate(all_nodes)}

            fig = go.Figure(data=go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=all_nodes,
                ),
                link=dict(
                    source=[node_indices[s] for s in df[source]],
                    target=[node_indices[t] for t in df[target]],
                    value=df[value].tolist() if value and value in df.columns else [1] * len(df),
                ),
            ))
        else:
            fig = go.Figure()
        return fig

    def _build_chord_diagram(self, spec: VizSpec) -> go.Figure:
        """Build a chord diagram (using Sankey with circular layout)."""
        return self._build_sankey(spec)

    def _build_calendar_heatmap(self, spec: VizSpec) -> go.Figure:
        """Build a calendar heatmap."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        date_col = encoding.get("date", encoding.get("x"))
        value_col = encoding.get("value", encoding.get("y"))

        if date_col and value_col and date_col in df.columns and value_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col])
            df["year"] = df[date_col].dt.year
            df["month"] = df[date_col].dt.month
            df["day"] = df[date_col].dt.day

            fig = px.density_heatmap(
                df, x="month", y="day", z=value_col,
                facet_col="year" if df["year"].nunique() > 1 else None,
                color_continuous_scale="Viridis",
            )
        else:
            fig = go.Figure()
        return fig

    def _build_map_scatter(self, spec: VizSpec) -> go.Figure:
        """Build a map scatter plot."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        lat = encoding.get("lat", encoding.get("latitude"))
        lon = encoding.get("lon", encoding.get("longitude"))
        color = encoding.get("color")
        size = encoding.get("size")
        palette = self._get_color_palette(spec)

        if lat and lon and lat in df.columns and lon in df.columns:
            fig = px.scatter_mapbox(
                df, lat=lat, lon=lon, color=color, size=size,
                color_discrete_sequence=palette,
                zoom=3,
                mapbox_style="open-street-map",
            )
        else:
            fig = go.Figure()
        return fig

    def _build_map_bubble(self, spec: VizSpec) -> go.Figure:
        """Build a map bubble chart."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        lat = encoding.get("lat", encoding.get("latitude"))
        lon = encoding.get("lon", encoding.get("longitude"))
        color = encoding.get("color")
        size = encoding.get("size")
        palette = self._get_color_palette(spec)

        if lat and lon and lat in df.columns and lon in df.columns:
            fig = px.scatter_mapbox(
                df, lat=lat, lon=lon, color=color, size=size,
                color_discrete_sequence=palette,
                size_max=50,
                zoom=3,
                mapbox_style="open-street-map",
            )
        else:
            fig = go.Figure()
        return fig

    def _build_choropleth(self, spec: VizSpec) -> go.Figure:
        """Build a choropleth map."""
        df = self._prepare_dataframe(spec)
        encoding = spec.encoding or {}
        locations = encoding.get("locations", encoding.get("x"))
        color = encoding.get("color", encoding.get("y"))
        location_mode = encoding.get("location_mode", "country names")

        if locations and color and locations in df.columns and color in df.columns:
            fig = px.choropleth(
                df, locations=locations, color=color,
                locationmode=location_mode,
                color_continuous_scale="Viridis",
            )
        else:
            fig = go.Figure()
        return fig

    def _build_flow_diagram(self, spec: VizSpec) -> go.Figure:
        """Build a flow diagram (using Sankey)."""
        return self._build_sankey(spec)

    def _apply_layout(self, spec: VizSpec, figure: go.Figure) -> None:
        """Apply layout configuration to a Plotly figure.

        Args:
            spec: The VizSpec containing layout configuration.
            figure: The Plotly figure to modify.
        """
        layout = spec.layout
        metadata = spec.metadata

        # Title
        title_text = metadata.get("title", "")
        subtitle = metadata.get("subtitle", "")
        if subtitle:
            title_text = f"{title_text}<br><sub>{subtitle}</sub>"

        # Build layout dict
        layout_kwargs: Dict[str, Any] = {
            "title": title_text if title_text else None,
            "showlegend": spec.visual.show_legend,
            "hovermode": "closest" if spec.interaction.get("tooltip", True) else False,
            "dragmode": "zoom" if spec.interaction.get("zoom", True) else False,
        }

        # Dimensions
        if layout.width:
            layout_kwargs["width"] = layout.width
        if layout.height:
            layout_kwargs["height"] = layout.height

        # Margins
        layout_kwargs["margin"] = dict(
            t=layout.margin_top,
            b=layout.margin_bottom,
            l=layout.margin_left,
            r=layout.margin_right,
            pad=layout.padding,
        )

        # Legend
        if layout.legend_position != "right":
            layout_kwargs["legend"] = {"orientation": layout.legend_orientation}
            if layout.legend_position in ("top", "bottom"):
                layout_kwargs["legend"]["yanchor"] = "bottom" if layout.legend_position == "top" else "top"
                layout_kwargs["legend"]["y"] = 1.02 if layout.legend_position == "top" else -0.1
                layout_kwargs["legend"]["xanchor"] = "center"
                layout_kwargs["legend"]["x"] = 0.5
            elif layout.legend_position in ("left",):
                layout_kwargs["legend"]["xanchor"] = "right"
                layout_kwargs["legend"]["x"] = -0.1

        # Axis titles
        xaxis: Dict[str, Any] = {}
        yaxis: Dict[str, Any] = {}
        if layout.xaxis_title:
            xaxis["title"] = layout.xaxis_title
        if layout.yaxis_title:
            yaxis["title"] = layout.yaxis_title
        if layout.xaxis_type:
            xaxis["type"] = layout.xaxis_type
        if layout.yaxis_type:
            yaxis["type"] = layout.yaxis_type
        if layout.xaxis_range:
            xaxis["range"] = layout.xaxis_range
        if layout.yaxis_range:
            yaxis["range"] = layout.yaxis_range
        if layout.xaxis_tickangle is not None:
            xaxis["tickangle"] = layout.xaxis_tickangle
        if layout.yaxis_tickangle is not None:
            yaxis["tickangle"] = layout.yaxis_tickangle

        # Grid
        xaxis["showgrid"] = layout.grid_x and layout.show_grid
        yaxis["showgrid"] = layout.grid_y and layout.show_grid

        if xaxis:
            layout_kwargs["xaxis"] = xaxis
        if yaxis:
            layout_kwargs["yaxis"] = yaxis

        # Responsive
        if layout.responsive:
            layout_kwargs["autosize"] = True

        figure.update_layout(**layout_kwargs)

    def _apply_annotations(self, spec: VizSpec, figure: go.Figure) -> None:
        """Apply annotations to a Plotly figure.

        Args:
            spec: The VizSpec containing annotations.
            figure: The Plotly figure to modify.
        """
        for annotation in spec.annotations:
            if annotation.type.value == "text":
                figure.add_annotation(
                    x=annotation.x,
                    y=annotation.y,
                    text=annotation.label or "",
                    xref=annotation.xref,
                    yref=annotation.yref,
                    showarrow=annotation.type.value == "arrow",
                    arrowhead=2 if annotation.type.value == "arrow" else 0,
                    ax=annotation.ax,
                    ay=annotation.ay,
                    font=dict(
                        color=annotation.color,
                        size=annotation.font_size,
                    ),
                    opacity=annotation.opacity,
                    align=annotation.align,
                    bgcolor=annotation.background_color,
                    bordercolor=annotation.border_color,
                    borderwidth=annotation.border_width,
                )
            elif annotation.type.value in ("reference_line", "target_line"):
                if annotation.y is not None:
                    figure.add_hline(
                        y=annotation.y,
                        line_dash=annotation.line_dash or "dash",
                        line_color=annotation.color or "red",
                        line_width=annotation.line_width,
                        annotation_text=annotation.label or "",
                        annotation_position="right",
                    )
                if annotation.x is not None:
                    figure.add_vline(
                        x=annotation.x,
                        line_dash=annotation.line_dash or "dash",
                        line_color=annotation.color or "red",
                        line_width=annotation.line_width,
                        annotation_text=annotation.label or "",
                        annotation_position="top",
                    )

    def _apply_theme(self, spec: VizSpec, figure: go.Figure) -> None:
        """Apply theme styling to a Plotly figure.

        Args:
            spec: The VizSpec containing theme configuration.
            figure: The Plotly figure to modify.
        """
        theme_config = self._resolve_theme(spec)

        # Apply theme colors to layout
        layout_updates: Dict[str, Any] = {}

        if theme_config.get("background_color"):
            layout_updates["plot_bgcolor"] = theme_config["background_color"]
            layout_updates["paper_bgcolor"] = theme_config["background_color"]

        if theme_config.get("font_family"):
            layout_updates["font"] = {"family": theme_config["font_family"]}

        if theme_config.get("font_size"):
            layout_updates.setdefault("font", {})
            layout_updates["font"]["size"] = theme_config["font_size"]

        if theme_config.get("title_font_size") or theme_config.get("title_color"):
            layout_updates["title"] = layout_updates.get("title", {})
            if isinstance(layout_updates["title"], dict):
                if theme_config.get("title_font_size"):
                    layout_updates["title"]["font"] = {"size": theme_config["title_font_size"]}
                if theme_config.get("title_color"):
                    layout_updates["title"]["font"] = layout_updates["title"].get("font", {})
                    layout_updates["title"]["font"]["color"] = theme_config["title_color"]

        if theme_config.get("grid_color"):
            layout_updates["xaxis"] = layout_updates.get("xaxis", {})
            layout_updates["xaxis"]["gridcolor"] = theme_config["grid_color"]
            layout_updates["yaxis"] = layout_updates.get("yaxis", {})
            layout_updates["yaxis"]["gridcolor"] = theme_config["grid_color"]

        if theme_config.get("axis_color"):
            layout_updates["xaxis"] = layout_updates.get("xaxis", {})
            layout_updates["xaxis"]["linecolor"] = theme_config["axis_color"]
            layout_updates["yaxis"] = layout_updates.get("yaxis", {})
            layout_updates["yaxis"]["linecolor"] = theme_config["axis_color"]

        if theme_config.get("tick_color"):
            layout_updates["xaxis"] = layout_updates.get("xaxis", {})
            layout_updates["xaxis"]["tickcolor"] = theme_config["tick_color"]
            layout_updates["xaxis"]["tickfont"] = {"color": theme_config["tick_color"]}
            layout_updates["yaxis"] = layout_updates.get("yaxis", {})
            layout_updates["yaxis"]["tickcolor"] = theme_config["tick_color"]
            layout_updates["yaxis"]["tickfont"] = {"color": theme_config["tick_color"]}

        if theme_config.get("tick_font_size"):
            layout_updates["xaxis"] = layout_updates.get("xaxis", {})
            layout_updates["xaxis"]["tickfont"] = layout_updates["xaxis"].get("tickfont", {})
            layout_updates["xaxis"]["tickfont"]["size"] = theme_config["tick_font_size"]
            layout_updates["yaxis"] = layout_updates.get("yaxis", {})
            layout_updates["yaxis"]["tickfont"] = layout_updates["yaxis"].get("tickfont", {})
            layout_updates["yaxis"]["tickfont"]["size"] = theme_config["tick_font_size"]

        if theme_config.get("legend_font_size"):
            layout_updates["legend"] = layout_updates.get("legend", {})
            layout_updates["legend"]["font"] = {"size": theme_config["legend_font_size"]}

        if theme_config.get("legend_background"):
            layout_updates["legend"] = layout_updates.get("legend", {})
            layout_updates["legend"]["bgcolor"] = theme_config["legend_background"]

        figure.update_layout(**layout_updates)