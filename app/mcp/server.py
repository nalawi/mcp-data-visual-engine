"""MCP Server for DV1 Visualization Engine.

Provides MCP tools for AI agents and LLMs to create visualizations.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from app.application.services.visualization_service import visualization_service
from app.core.config import settings
from app.domain.specs.vizspec import VizSpec
from app.domain.specs.visualspec import ChartType
from app.infrastructure.storage.output_storage import output_storage

logger = logging.getLogger(__name__)


class MCPTool:
    """Represents an MCP tool definition."""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: callable,
    ) -> None:
        """Initialize an MCP tool.

        Args:
            name: Tool name.
            description: Tool description.
            input_schema: JSON Schema for tool inputs.
            handler: Async function to handle tool calls.
        """
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler


class MCPServer:
    """MCP Server implementation for the DV1 Visualization Engine.

    Provides tools that AI agents and LLMs can use to create,
    render, and export visualizations.
    """

    def __init__(self) -> None:
        """Initialize the MCP server with available tools."""
        self._tools: Dict[str, MCPTool] = {}
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all MCP tools."""

        # self._tools["render_chart"] = MCPTool(
        #     name="render_chart",
        #     description="Render a visualization from a VizSpec and return the figure as JSON.",
        #     input_schema={
        #         "type": "object",
        #         "properties": {
        #             "spec": {
        #                 "type": "object",
        #                 "description": "VizSpec JSON object defining the visualization.",
        #             },
        #             "renderer": {
        #                 "type": "string",
        #                 "description": "Optional renderer name (default: plotly).",
        #             },
        #         },
        #         "required": ["spec"],
        #     },
        #     handler=self._handle_render_chart,
        # )

        self._tools["render_html"] = MCPTool(
            name="render_html",
            description="Render a visualization and return interactive HTML.",
            input_schema={
                "type": "object",
                "properties": {
                    "spec": {
                        "type": "object",
                        "description": "VizSpec JSON object.",
                    },
                },
                "required": ["spec"],
            },
            handler=self._handle_render_html,
        )

        self._tools["render_png"] = MCPTool(
            name="render_png",
            description="Render a visualization and return base64-encoded PNG.",
            input_schema={
                "type": "object",
                "properties": {
                    "spec": {
                        "type": "object",
                        "description": "VizSpec JSON object.",
                    },
                },
                "required": ["spec"],
            },
            handler=self._handle_render_png,
        )

        self._tools["render_svg"] = MCPTool(
            name="render_svg",
            description="Render a visualization and return SVG string.",
            input_schema={
                "type": "object",
                "properties": {
                    "spec": {
                        "type": "object",
                        "description": "VizSpec JSON object.",
                    },
                },
                "required": ["spec"],
            },
            handler=self._handle_render_svg,
        )

        self._tools["render_pdf"] = MCPTool(
            name="render_pdf",
            description="Render a visualization and return base64-encoded PDF.",
            input_schema={
                "type": "object",
                "properties": {
                    "spec": {
                        "type": "object",
                        "description": "VizSpec JSON object.",
                    },
                },
                "required": ["spec"],
            },
            handler=self._handle_render_pdf,
        )

        # self._tools["render_batch"] = MCPTool(
        #     name="render_batch",
        #     description="Render multiple visualizations in batch.",
        #     input_schema={
        #         "type": "object",
        #         "properties": {
        #             "specs": {
        #                 "type": "array",
        #                 "items": {"type": "object"},
        #                 "description": "List of VizSpec JSON objects.",
        #             },
        #         },
        #         "required": ["specs"],
        #     },
        #     handler=self._handle_render_batch,
        # )

        self._tools["validate_spec"] = MCPTool(
            name="validate_spec",
            description="Validate a VizSpec without rendering.",
            input_schema={
                "type": "object",
                "properties": {
                    "spec": {
                        "type": "object",
                        "description": "VizSpec JSON object to validate.",
                    },
                },
                "required": ["spec"],
            },
            handler=self._handle_validate_spec,
        )

        # self._tools["recommend_chart"] = MCPTool(
        #     name="recommend_chart",
        #     description="Get AI chart recommendations based on data characteristics.",
        #     input_schema={
        #         "type": "object",
        #         "properties": {
        #             "data": {
        #                 "type": "object",
        #                 "description": "Data description with fields, types, cardinality, etc.",
        #             },
        #         },
        #         "required": ["data"],
        #     },
        #     handler=self._handle_recommend_chart,
        # )

        self._tools["list_themes"] = MCPTool(
            name="list_themes",
            description="List all available visualization themes.",
            input_schema={
                "type": "object",
                "properties": {},
            },
            handler=self._handle_list_themes,
        )

        # self._tools["list_renderers"] = MCPTool(
        #     name="list_renderers",
        #     description="List all available renderers.",
        #     input_schema={
        #         "type": "object",
        #         "properties": {},
        #     },
        #     handler=self._handle_list_renderers,
        # )

        # self._tools["list_templates"] = MCPTool(
        #     name="list_templates",
        #     description="List all available chart templates.",
        #     input_schema={
        #         "type": "object",
        #         "properties": {},
        #     },
        #     handler=self._handle_list_templates,
        # )

        # self._tools["preview_chart"] = MCPTool(
        #     name="preview_chart",
        #     description="Render a chart and return a preview (HTML).",
        #     input_schema={
        #         "type": "object",
        #         "properties": {
        #             "spec": {
        #                 "type": "object",
        #                 "description": "VizSpec JSON object.",
        #             },
        #         },
        #         "required": ["spec"],
        #     },
        #     handler=self._handle_preview_chart,
        # )

        # self._tools["export_chart"] = MCPTool(
        #     name="export_chart",
        #     description="Render and export a chart in the specified format.",
        #     input_schema={
        #         "type": "object",
        #         "properties": {
        #             "spec": {
        #                 "type": "object",
        #                 "description": "VizSpec JSON object.",
        #             },
        #             "format": {
        #                 "type": "string",
        #                 "enum": ["png", "svg", "pdf", "html", "json"],
        #                 "description": "Export format.",
        #             },
        #         },
        #         "required": ["spec", "format"],
        #     },
        #     handler=self._handle_export_chart,
        # )

        # self._tools["transform_data"] = MCPTool(
        #     name="transform_data",
        #     description="Apply data transformations to a dataset.",
        #     input_schema={
        #         "type": "object",
        #         "properties": {
        #             "data": {
        #                 "type": "array",
        #                 "items": {"type": "object"},
        #                 "description": "Data records as list of objects.",
        #             },
        #             "transforms": {
        #                 "type": "array",
        #                 "items": {"type": "object"},
        #                 "description": "List of transformation specifications.",
        #             },
        #         },
        #         "required": ["data", "transforms"],
        #     },
        #     handler=self._handle_transform_data,
        # )

        # ------------------------------------------------------------------
        # 00_FIRST tool – AI agents MUST call this to learn the spec format
        # before calling any render_* tool. Registered first so it appears
        # at the top of the tools list.
        # ------------------------------------------------------------------

        self._tools["see_spec_schema_reference"] = MCPTool(
            name="see_spec_schema_reference",
            description="[See the VizSpec JSON schema with a working example. CALL THIS FIRST before any render_* tool to learn the exact format expected. Returns the full schema, an example spec, all 47 supported chart types, and usage notes.",
            input_schema={
                "type": "object",
                "properties": {},
            },
            handler=self._handle_get_spec_schema,
        )

        # self._tools["simplified_render"] = MCPTool(
        #     name="simplified_render",
        #     description="Render a chart from a SIMPLIFIED spec format. This tool auto-converts common shorthand formats into the full VizSpec. Use this if you are unsure about the exact VizSpec structure.",
        #     input_schema={
        #         "type": "object",
        #         "properties": {
        #             "chart_type": {
        #                 "type": "string",
        #                 "description": "Type of chart (bar, line, scatter, pie, area, histogram, box_plot, heatmap, etc.).",
        #             },
        #             "data": {
        #                 "type": "object",
        #                 "description": "Data specification. Can be: {'values': [{'x': 'A', 'y': 10}, ...]} or {'records': [{'x': 'A', 'y': 10}, ...]} or {'url': '...'}.",
        #             },
        #             "x": {
        #                 "type": "string",
        #                 "description": "Field name for the x-axis (e.g. 'month', 'category', 'date').",
        #             },
        #             "y": {
        #                 "type": "string",
        #                 "description": "Field name for the y-axis (e.g. 'revenue', 'count', 'value').",
        #             },
        #             "color": {
        #                 "type": "string",
        #                 "description": "Optional field name for color encoding (e.g. 'region', 'product').",
        #             },
        #             "title": {
        #                 "type": "string",
        #                 "description": "Optional chart title.",
        #             },
        #             "output_format": {
        #                 "type": "string",
        #                 "enum": ["svg", "png", "html", "pdf", "json"],
        #                 "description": "Output format (default: svg).",
        #             },
        #         },
        #         "required": ["chart_type", "data", "x", "y"],
        #     },
        #     handler=self._handle_simplified_render,
        # )

    # ------------------------------------------------------------------
    # Spec normalisation: converts Vega-Lite & other common formats
    # into the internal VizSpec format.
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
        """Normalise a spec dict into the internal VizSpec format.

        Handles these incoming formats:
          - Vega-Lite:  {chart: {type: "bar"}, data: {values: [...]}, encoding: {x: {field: ...}, y: {field: ...}}}
          - Flat:       {type: "bar", data: {values: [...]}, x: "field", y: "field"}
          - Native:     {visual: {type: "bar"}, data: {records: [...]}, encoding: {x: "field", y: "field"}}
        """
        if not isinstance(spec, dict):
            return spec

        normalized: Dict[str, Any] = dict(spec)  # shallow copy

        # ---- 1. chart.type → visual.type (Vega-Lite style) ----
        chart_block = normalized.pop("chart", None)
        if isinstance(chart_block, dict):
            chart_type = chart_block.get("type")
            if chart_type:
                if "visual" not in normalized or not isinstance(normalized["visual"], dict):
                    normalized["visual"] = {}
                if "type" not in normalized["visual"]:
                    normalized["visual"]["type"] = chart_type

        # ---- 2. top-level type → visual.type (flat style) ----
        top_type = normalized.pop("type", None)
        if top_type and not normalized.get("visual", {}).get("type"):
            if "visual" not in normalized or not isinstance(normalized["visual"], dict):
                normalized["visual"] = {}
            normalized["visual"]["type"] = top_type

        # ---- 3. raw array data → data.records ----
        raw_data = normalized.get("data")
        if isinstance(raw_data, list):
            # data is a raw array: [{"name": "Jan", "value": 45}, ...]
            normalized["data"] = {
                "source": "inline",
                "records": raw_data,
            }
        elif isinstance(raw_data, dict):
            # ---- 3a. data.values → data.records (Vega-Lite style) ----
            values = raw_data.pop("values", None)
            if values is not None and "records" not in raw_data:
                raw_data["records"] = values
            if "source" not in raw_data:
                raw_data["source"] = "inline"

        # ---- 4. encoding.x/y as objects → encoding.x/y as strings (Vega-Lite style) ----
        encoding = normalized.get("encoding")
        if isinstance(encoding, dict):
            for channel in ("x", "y", "color", "size", "shape", "text", "detail", "tooltip"):
                val = encoding.get(channel)
                if isinstance(val, dict):
                    field_name = val.get("field") or val.get("value")
                    if field_name is not None:
                        encoding[channel] = field_name

        # ---- 5. top-level x/y → encoding.x/y (flat style) ----
        for channel in ("x", "y", "color"):
            top_val = normalized.pop(channel, None)
            if top_val is not None:
                if "encoding" not in normalized or not isinstance(normalized["encoding"], dict):
                    normalized["encoding"] = {}
                if channel not in normalized["encoding"]:
                    normalized["encoding"][channel] = top_val

        # ---- 6. title → metadata.title ----
        top_title = normalized.pop("title", None)
        if top_title:
            if "metadata" not in normalized or not isinstance(normalized["metadata"], dict):
                normalized["metadata"] = {}
            if "title" not in normalized["metadata"]:
                normalized["metadata"]["title"] = top_title

        return normalized

    # ------------------------------------------------------------------
    # Output mode helper
    # ------------------------------------------------------------------

    @staticmethod
    def _output_response(
        *,
        fmt: str,
        mime_type: str,
        raw_bytes: Optional[bytes] = None,
        text: Optional[str] = None,
        spec_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Build a response dict respecting the MCP_OUTPUT_MODE setting.

        When MCP_OUTPUT_MODE=inline  → embed the full data in the response.
        When MCP_OUTPUT_MODE=url     → save to disk and return a URL only.

        Args:
            fmt: File format extension (png, svg, pdf, html, json).
            mime_type: MIME type string.
            raw_bytes: Raw binary data (for png, pdf).
            text: Text content (for svg, html, json).
            spec_id: Optional spec identifier for file naming.

        Returns:
            Response dict with either inline data or a URL.
        """
        if settings.MCP_OUTPUT_MODE == "url":
            # Save to disk and return URL
            if raw_bytes is not None:
                url = output_storage.save(raw_bytes, fmt, spec_id)
            elif text is not None:
                url = output_storage.save_text(text, fmt, spec_id)
            else:
                return {"success": False, "error": "No data to save."}

            return {
                "success": True,
                "data": {
                    "url": url,
                    "format": fmt,
                    "mime_type": mime_type,
                },
            }

        # Inline mode – embed data in response
        if raw_bytes is not None:
            import base64
            b64 = base64.b64encode(raw_bytes).decode("utf-8")
            if fmt == "png":
                return {
                    "success": True,
                    "data": {
                        "base64": f"data:image/png;base64,{b64}",
                        "format": "png",
                        "mime_type": "image/png",
                    },
                }
            elif fmt == "pdf":
                return {
                    "success": True,
                    "data": {
                        "base64": f"data:application/pdf;base64,{b64}",
                        "format": "pdf",
                        "mime_type": "application/pdf",
                    },
                }

        if text is not None:
            if fmt == "svg":
                return {
                    "success": True,
                    "data": {
                        "svg": text,
                        "format": "svg",
                        "mime_type": "image/svg+xml",
                    },
                }
            elif fmt == "html":
                return {
                    "success": True,
                    "data": {
                        "html": text,
                        "format": "html",
                        "mime_type": "text/html",
                    },
                }
            elif fmt == "json":
                return {
                    "success": True,
                    "data": {
                        "json": text,
                        "format": "json",
                        "mime_type": "application/json",
                    },
                }

        return {"success": False, "error": f"Unsupported format: {fmt}"}

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    async def _handle_render_chart(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle render_chart tool call."""
        try:
            spec = self._normalize_spec(args["spec"])
            result = visualization_service.render(spec, args.get("renderer"))
            return {"success": True, "data": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_render_html(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle render_html tool call."""
        try:
            spec = self._normalize_spec(args["spec"])
            html = visualization_service.render_html(spec)
            return self._output_response(fmt="html", mime_type="text/html", text=html)
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_render_png(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle render_png tool call."""
        try:
            spec = self._normalize_spec(args["spec"])
            png_bytes = visualization_service.render_png(spec)
            return self._output_response(fmt="png", mime_type="image/png", raw_bytes=png_bytes)
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_render_svg(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle render_svg tool call."""
        try:
            spec = self._normalize_spec(args["spec"])
            svg = visualization_service.render_svg(spec)
            return self._output_response(fmt="svg", mime_type="image/svg+xml", text=svg)
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_render_pdf(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle render_pdf tool call."""
        try:
            spec = self._normalize_spec(args["spec"])
            pdf_bytes = visualization_service.render_pdf(spec)
            return self._output_response(fmt="pdf", mime_type="application/pdf", raw_bytes=pdf_bytes)
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_render_batch(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle render_batch tool call."""
        try:
            specs = [self._normalize_spec(s) for s in args["specs"]]
            results = visualization_service.render_batch(specs)
            return {"success": True, "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_validate_spec(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle validate_spec tool call."""
        spec = self._normalize_spec(args["spec"])
        result = visualization_service.validate_spec(spec)
        return result

    async def _handle_recommend_chart(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle recommend_chart tool call."""
        try:
            recommendations = visualization_service.recommend_chart(args["data"])
            return {"success": True, "recommendations": recommendations}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_list_themes(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_themes tool call."""
        themes = visualization_service.list_themes()
        return {"success": True, "themes": themes}

    async def _handle_list_renderers(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_renderers tool call."""
        renderers = visualization_service.list_renderers()
        return {"success": True, "renderers": renderers}

    async def _handle_list_templates(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_templates tool call."""
        from app.api.v1.templates import CHART_TEMPLATES
        templates = [
            {"id": k, "name": v["name"], "description": v["description"]}
            for k, v in CHART_TEMPLATES.items()
        ]
        return {"success": True, "templates": templates}

    async def _handle_preview_chart(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle preview_chart tool call."""
        try:
            spec = self._normalize_spec(args["spec"])
            html = visualization_service.render_html(spec)
            return self._output_response(fmt="html", mime_type="text/html", text=html)
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_export_chart(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle export_chart tool call."""
        try:
            spec = self._normalize_spec(args["spec"])
            fmt = args.get("format", "png")
            if fmt == "png":
                data = visualization_service.render_png(spec)
                return self._output_response(fmt="png", mime_type="image/png", raw_bytes=data)
            elif fmt == "svg":
                data = visualization_service.render_svg(spec)
                return self._output_response(fmt="svg", mime_type="image/svg+xml", text=data)
            elif fmt == "pdf":
                data = visualization_service.render_pdf(spec)
                return self._output_response(fmt="pdf", mime_type="application/pdf", raw_bytes=data)
            elif fmt == "html":
                data = visualization_service.render_html(spec)
                return self._output_response(fmt="html", mime_type="text/html", text=data)
            elif fmt == "json":
                data = visualization_service.render_json(spec)
                return self._output_response(fmt="json", mime_type="application/json", text=data)
            else:
                return {"success": False, "error": f"Unsupported format: {fmt}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_transform_data(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle transform_data tool call."""
        try:
            import pandas as pd
            df = pd.DataFrame(args["data"])
            transforms = args.get("transforms", [])

            for transform in transforms:
                t_type = transform.get("type", "")
                if t_type == "filter":
                    field = transform.get("field")
                    operator = transform.get("operator", "eq")
                    value = transform.get("value")
                    if operator == "eq":
                        df = df[df[field] == value]
                    elif operator == "gt":
                        df = df[df[field] > value]
                    elif operator == "lt":
                        df = df[df[field] < value]
                    elif operator == "gte":
                        df = df[df[field] >= value]
                    elif operator == "lte":
                        df = df[df[field] <= value]
                elif t_type == "sort":
                    field = transform.get("field")
                    ascending = transform.get("ascending", True)
                    df = df.sort_values(by=field, ascending=ascending)
                elif t_type == "aggregate":
                    group_by = transform.get("group_by", [])
                    agg_field = transform.get("field")
                    agg_func = transform.get("function", "sum")
                    if group_by and agg_field:
                        df = df.groupby(group_by).agg({agg_field: agg_func}).reset_index()
                elif t_type == "select":
                    fields = transform.get("fields", [])
                    if fields:
                        df = df[fields]

            return {
                "success": True,
                "data": df.to_dict(orient="records"),
                "row_count": len(df),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ------------------------------------------------------------------
    # Handler: get_spec_schema
    # ------------------------------------------------------------------

    async def _handle_get_spec_schema(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Return the full VizSpec JSON schema and a working example."""
        schema = VizSpec.model_json_schema()
        example = {
            "metadata": {"title": "Monthly Revenue", "subtitle": "2026 Fiscal Year"},
            "data": {
                "source": "inline",
                "records": [
                    {"month": "Jan", "revenue": 120000, "cost": 80000},
                    {"month": "Feb", "revenue": 135000, "cost": 85000},
                    {"month": "Mar", "revenue": 142000, "cost": 90000},
                ],
            },
            "visual": {"type": "bar", "show_values": True},
            "encoding": {"x": "month", "y": "revenue", "color": "cost"},
            "layout": {"width": 800, "height": 500, "xaxis_title": "Month", "yaxis_title": "Revenue ($)"},
            "theme": {"name": "corporate"},
            "output": {"format": "svg"},
        }
        chart_types = [e.value for e in ChartType]
        return {
            "success": True,
            "schema": schema,
            "example": example,
            "supported_chart_types": chart_types,
            "notes": [
                "The 'spec' field passed to render_* tools must be a JSON object matching the VizSpec schema above.",
                "Use 'visual.type' (not top-level 'type') to set the chart type.",
                "Use 'data.records' (not 'data.values') for inline data.",
                "Use 'encoding.x' and 'encoding.y' (not top-level 'x'/'y') for axis mappings.",
                "If you are unsure, use the 'simplified_render' tool instead — it accepts a flat format.",
            ],
        }

    # ------------------------------------------------------------------
    # Handler: simplified_render
    # ------------------------------------------------------------------

    async def _handle_simplified_render(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a simplified spec into a full VizSpec and render it."""
        try:
            chart_type = args.get("chart_type", "bar")
            data_arg = args.get("data", {})
            x_field = args.get("x", "")
            y_field = args.get("y", "")
            color_field = args.get("color")
            title = args.get("title", "")
            output_format = args.get("output_format", "svg")

            # --- Normalise data ---
            records = data_arg.get("records") or data_arg.get("values") or []
            if not records and isinstance(data_arg, list):
                records = data_arg

            if not records:
                return {"success": False, "error": "No data records provided. Supply data as {'values': [...]} or {'records': [...]}."}

            # --- Build full VizSpec ---
            spec: Dict[str, Any] = {
                "metadata": {"title": title or f"{chart_type.title()} Chart"},
                "data": {"source": "inline", "records": records},
                "visual": {"type": chart_type},
                "encoding": {"x": x_field, "y": y_field},
                "output": {"format": output_format},
            }

            if color_field:
                spec["encoding"]["color"] = color_field

            # --- Render via the existing service ---
            if output_format == "svg":
                svg = visualization_service.render_svg(spec)
                return {"success": True, "format": "svg", "data": svg}
            elif output_format == "png":
                png_bytes = visualization_service.render_png(spec)
                import base64
                encoded = base64.b64encode(png_bytes).decode("utf-8")
                return {"success": True, "format": "png", "data": f"data:image/png;base64,{encoded}"}
            elif output_format == "html":
                html = visualization_service.render_html(spec)
                return {"success": True, "format": "html", "data": html}
            elif output_format == "pdf":
                pdf_bytes = visualization_service.render_pdf(spec)
                import base64
                encoded = base64.b64encode(pdf_bytes).decode("utf-8")
                return {"success": True, "format": "pdf", "data": f"data:application/pdf;base64,{encoded}"}
            elif output_format == "json":
                result = visualization_service.render(spec)
                return {"success": True, "format": "json", "data": str(result)}
            else:
                svg = visualization_service.render_svg(spec)
                return {"success": True, "format": "svg", "data": svg}

        except Exception as e:
            return {"success": False, "error": str(e), "hint": "Use 'see_spec_schema_reference' to see the full VizSpec format, or check your field names match the data records."}

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get MCP tool definitions in the standard format.

        Returns:
            List of tool definition dictionaries.
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema,
            }
            for tool in self._tools.values()
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an MCP tool call.

        Args:
            tool_name: Name of the tool to call.
            arguments: Tool arguments.

        Returns:
            Tool result.

        Raises:
            ValueError: If the tool is not found.
        """
        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        tool = self._tools[tool_name]
        return await tool.handler(arguments)


# Singleton instance
mcp_server = MCPServer()