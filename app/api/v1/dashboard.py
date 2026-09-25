"""Dashboard API endpoints."""

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse

from app.application.services.visualization_service import visualization_service
from app.domain.exceptions.base import DV1Error

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["dashboards"])


@router.post("/dashboard")
async def create_dashboard(
    specs: List[Dict[str, Any]] = Body(..., description="List of VizSpec JSONs for dashboard panels"),
    layout: Optional[Dict[str, Any]] = Body(None, description="Dashboard layout configuration"),
    renderer: Optional[str] = Query(None, description="Renderer name override"),
) -> HTMLResponse:
    """Create a dashboard with multiple visualizations.

    Args:
        specs: List of VizSpec JSONs, one per dashboard panel.
        layout: Dashboard layout configuration (rows, cols, etc.).
        renderer: Optional renderer name.

    Returns:
        HTML dashboard with all visualizations.
    """
    try:
        rows = (layout or {}).get("rows", 1)
        cols = (layout or {}).get("cols", len(specs))

        html_parts = [
            "<!DOCTYPE html>",
            '<html><head><meta charset="utf-8">',
            "<title>DV1 Dashboard</title>",
            '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>',
            '<style>',
            "* { box-sizing: border-box; }",
            "body { margin: 0; padding: 20px; font-family: Arial, sans-serif; background: #f5f5f5; }",
            ".dashboard { display: grid; grid-template-columns: repeat(%d, 1fr); gap: 16px; }" % cols,
            ".panel { background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 16px; display: flex; flex-direction: column; min-height: 400px; }",
            ".panel h3 { margin: 0 0 8px 0; color: #333; flex-shrink: 0; }",
            ".panel .chart-wrapper { flex: 1; min-height: 0; position: relative; }",
            ".panel .chart-wrapper .js-plotly-plot, .panel .chart-wrapper .plot-container { width: 100%% !important; height: 100%% !important; }",
            "</style></head><body>",
            "<div class='dashboard'>",
        ]

        for i, spec_data in enumerate(specs):
            try:
                html = visualization_service.render_html(spec_data, renderer)
                title = spec_data.get("metadata", {}).get("title", f"Panel {i + 1}")
                html_parts.append(f"<div class='panel'><h3>{title}</h3><div class='chart-wrapper'>{html}</div></div>")
            except Exception as e:
                html_parts.append(
                    f"<div class='panel'><h3>Panel {i + 1}</h3>"
                    f"<p style='color: red;'>Error: {str(e)}</p></div>"
                )

        html_parts.append("</div></body></html>")
        return HTMLResponse(content="\n".join(html_parts))

    except DV1Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})