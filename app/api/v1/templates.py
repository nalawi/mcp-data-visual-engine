"""Templates API endpoints."""

import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.application.services.visualization_service import visualization_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["templates"])

# Pre-built chart templates
CHART_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "line_simple": {
        "name": "Simple Line Chart",
        "description": "Basic line chart for time series data.",
        "spec": {
            "metadata": {"title": "Line Chart", "subtitle": "Time Series"},
            "data": {"source": "inline", "records": [{"x": "Jan", "y": 10}, {"x": "Feb", "y": 25}, {"x": "Mar", "y": 15}]},
            "visual": {"type": "line"},
            "encoding": {"x": "x", "y": "y"},
        },
    },
    "bar_simple": {
        "name": "Simple Bar Chart",
        "description": "Basic bar chart for category comparison.",
        "spec": {
            "metadata": {"title": "Bar Chart", "subtitle": "Category Comparison"},
            "data": {"source": "inline", "records": [{"category": "A", "value": 30}, {"category": "B", "value": 45}, {"category": "C", "value": 25}]},
            "visual": {"type": "bar"},
            "encoding": {"x": "category", "y": "value"},
        },
    },
    "pie_simple": {
        "name": "Simple Pie Chart",
        "description": "Basic pie chart for composition.",
        "spec": {
            "metadata": {"title": "Pie Chart", "subtitle": "Distribution"},
            "data": {"source": "inline", "records": [{"label": "Product A", "value": 35}, {"label": "Product B", "value": 25}, {"label": "Product C", "value": 40}]},
            "visual": {"type": "pie"},
            "encoding": {"x": "label", "y": "value"},
        },
    },
    "scatter_simple": {
        "name": "Simple Scatter Plot",
        "description": "Basic scatter plot for correlation.",
        "spec": {
            "metadata": {"title": "Scatter Plot", "subtitle": "Relationship"},
            "data": {"source": "inline", "records": [{"x": 1, "y": 2}, {"x": 2, "y": 4}, {"x": 3, "y": 1}, {"x": 4, "y": 5}]},
            "visual": {"type": "scatter"},
            "encoding": {"x": "x", "y": "y"},
        },
    },
    "area_simple": {
        "name": "Simple Area Chart",
        "description": "Basic area chart for magnitude over time.",
        "spec": {
            "metadata": {"title": "Area Chart", "subtitle": "Cumulative View"},
            "data": {"source": "inline", "records": [{"month": "Q1", "revenue": 100}, {"month": "Q2", "revenue": 150}, {"month": "Q3", "revenue": 130}]},
            "visual": {"type": "area"},
            "encoding": {"x": "month", "y": "revenue"},
        },
    },
    "histogram_simple": {
        "name": "Simple Histogram",
        "description": "Basic histogram for distribution.",
        "spec": {
            "metadata": {"title": "Histogram", "subtitle": "Distribution"},
            "data": {"source": "inline", "records": [{"value": 1}, {"value": 2}, {"value": 2}, {"value": 3}, {"value": 3}, {"value": 3}]},
            "visual": {"type": "histogram"},
            "encoding": {"x": "value"},
        },
    },
    "heatmap_simple": {
        "name": "Simple Heatmap",
        "description": "Basic heatmap for matrix data.",
        "spec": {
            "metadata": {"title": "Heatmap", "subtitle": "Matrix View"},
            "data": {"source": "inline", "records": [{"x": "A", "y": "X", "value": 1}, {"x": "A", "y": "Y", "value": 4}, {"x": "B", "y": "X", "value": 3}]},
            "visual": {"type": "heatmap"},
            "encoding": {"x": "x", "y": "y", "color": "value"},
        },
    },
    "corporate_dashboard": {
        "name": "Corporate Dashboard",
        "description": "Multi-panel corporate dashboard with KPIs.",
        "spec": {
            "metadata": {"title": "Corporate Dashboard", "subtitle": "Q4 2025"},
            "data": {"source": "inline", "records": [{"metric": "Revenue", "Q1": 100, "Q2": 120, "Q3": 110, "Q4": 140}]},
            "visual": {"type": "bar"},
            "encoding": {"x": "metric", "y": "Q4"},
            "theme": {"name": "corporate"},
            "layout": {"width": 600, "height": 400},
        },
    },
}


@router.get("/templates")
async def list_templates() -> JSONResponse:
    """List all available chart templates.

    Returns:
        JSON response with template list.
    """
    templates = []
    for key, template in CHART_TEMPLATES.items():
        templates.append({
            "id": key,
            "name": template["name"],
            "description": template["description"],
        })
    return JSONResponse(content={"templates": templates})


@router.get("/templates/{template_id}")
async def get_template(template_id: str) -> JSONResponse:
    """Get a specific template by ID.

    Args:
        template_id: Template identifier.

    Returns:
        JSON response with template spec.
    """
    if template_id not in CHART_TEMPLATES:
        raise HTTPException(
            status_code=404,
            detail={"error": True, "message": f"Template '{template_id}' not found."},
        )
    return JSONResponse(content=CHART_TEMPLATES[template_id])