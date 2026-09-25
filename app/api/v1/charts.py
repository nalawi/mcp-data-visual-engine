"""Chart rendering API endpoints."""

import base64
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, HTTPException, Query, Response
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from app.application.services.visualization_service import visualization_service
from app.domain.exceptions.base import DV1Error

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["charts"])


@router.post("/render")
async def render_chart(
    spec: Dict[str, Any] = Body(..., description="VizSpec JSON"),
    renderer: Optional[str] = Query(None, description="Renderer name override"),
) -> JSONResponse:
    """Render a visualization and return the figure object.

    Args:
        spec: VizSpec JSON body.
        renderer: Optional renderer name.

    Returns:
        JSON response with rendered figure data.
    """
    try:
        result = visualization_service.render(spec, renderer)
        return JSONResponse(content={"success": True, "data": result})
    except DV1Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})


@router.post("/render/html")
async def render_html(
    spec: Dict[str, Any] = Body(..., description="VizSpec JSON"),
    renderer: Optional[str] = Query(None, description="Renderer name override"),
) -> HTMLResponse:
    """Render a visualization and return interactive HTML.

    Args:
        spec: VizSpec JSON body.
        renderer: Optional renderer name.

    Returns:
        HTML response with embedded Plotly chart.
    """
    try:
        html = visualization_service.render_html(spec, renderer)
        return HTMLResponse(content=html)
    except DV1Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})


@router.post("/render/png")
async def render_png(
    spec: Dict[str, Any] = Body(..., description="VizSpec JSON"),
    renderer: Optional[str] = Query(None, description="Renderer name override"),
) -> StreamingResponse:
    """Render a visualization and return PNG image.

    Args:
        spec: VizSpec JSON body.
        renderer: Optional renderer name.

    Returns:
        PNG image response.
    """
    try:
        png_bytes = visualization_service.render_png(spec, renderer)
        return StreamingResponse(
            content=iter([png_bytes]),
            media_type="image/png",
            headers={"Content-Disposition": "inline; filename=chart.png"},
        )
    except DV1Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})


@router.post("/render/svg")
async def render_svg(
    spec: Dict[str, Any] = Body(..., description="VizSpec JSON"),
    renderer: Optional[str] = Query(None, description="Renderer name override"),
) -> Response:
    """Render a visualization and return SVG.

    Args:
        spec: VizSpec JSON body.
        renderer: Optional renderer name.

    Returns:
        SVG response.
    """
    try:
        svg_str = visualization_service.render_svg(spec, renderer)
        return Response(
            content=svg_str,
            media_type="image/svg+xml",
            headers={"Content-Disposition": "inline; filename=chart.svg"},
        )
    except DV1Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})


@router.post("/render/pdf")
async def render_pdf(
    spec: Dict[str, Any] = Body(..., description="VizSpec JSON"),
    renderer: Optional[str] = Query(None, description="Renderer name override"),
) -> StreamingResponse:
    """Render a visualization and return PDF.

    Args:
        spec: VizSpec JSON body.
        renderer: Optional renderer name.

    Returns:
        PDF response.
    """
    try:
        pdf_bytes = visualization_service.render_pdf(spec, renderer)
        return StreamingResponse(
            content=iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=chart.pdf"},
        )
    except DV1Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})


@router.post("/render/json")
async def render_json(
    spec: Dict[str, Any] = Body(..., description="VizSpec JSON"),
    renderer: Optional[str] = Query(None, description="Renderer name override"),
) -> JSONResponse:
    """Render a visualization and return Plotly JSON.

    Args:
        spec: VizSpec JSON body.
        renderer: Optional renderer name.

    Returns:
        JSON response with Plotly figure data.
    """
    try:
        json_str = visualization_service.render_json(spec, renderer)
        return JSONResponse(content={"success": True, "data": json_str})
    except DV1Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})


@router.post("/render/batch")
async def render_batch(
    specs: List[Dict[str, Any]] = Body(..., description="List of VizSpec JSONs"),
    renderer: Optional[str] = Query(None, description="Renderer name override"),
) -> JSONResponse:
    """Render multiple visualizations in batch.

    Args:
        specs: List of VizSpec JSON bodies.
        renderer: Optional renderer name.

    Returns:
        JSON response with batch results.
    """
    try:
        results = visualization_service.render_batch(specs, renderer)
        return JSONResponse(content={"success": True, "results": results})
    except DV1Error as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})


@router.post("/validate")
async def validate_spec(
    spec: Dict[str, Any] = Body(..., description="VizSpec JSON to validate"),
) -> JSONResponse:
    """Validate a VizSpec without rendering.

    Args:
        spec: VizSpec JSON body.

    Returns:
        Validation result.
    """
    result = visualization_service.validate_spec(spec)
    return JSONResponse(content=result)