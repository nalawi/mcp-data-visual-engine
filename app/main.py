"""DV1 Visualization Engine - Main FastAPI Application."""

import logging
import os
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.charts import router as charts_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.themes import router as themes_router
from app.api.v1.templates import router as templates_router
from app.api.v1.health import router as health_router
from app.api.v1.mcp_endpoints import router as mcp_router
from app.core.config import settings
from app.domain.exceptions.base import DV1Error

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="DV1 Visualization Engine",
    description="Enterprise AI Visualization Platform - Receives VizSpec from AI agents, LLMs, and REST clients, then generates high-quality visualizations.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(DV1Error)
async def dv1_error_handler(request: Request, exc: DV1Error) -> JSONResponse:
    """Handle DV1Error exceptions globally.

    Args:
        request: The request that caused the error.
        exc: The DV1Error exception.

    Returns:
        JSON response with error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions globally.

    Args:
        request: The request that caused the error.
        exc: The exception.

    Returns:
        JSON response with error details.
    """
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "code": "INTERNAL_ERROR",
            "message": "An internal error occurred.",
        },
    )


# Include routers
app.include_router(charts_router)
app.include_router(dashboard_router)
app.include_router(themes_router)
app.include_router(templates_router)
app.include_router(health_router)
app.include_router(mcp_router)


# ------------------------------------------------------------------
# Mount static file serving for saved output files
# ------------------------------------------------------------------
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
app.mount(settings.STATIC_URL_PREFIX, StaticFiles(directory=settings.OUTPUT_DIR), name="static")
logger.info(
    "Static files mounted: %s -> %s (MCP_OUTPUT_MODE=%s)",
    settings.STATIC_URL_PREFIX,
    settings.OUTPUT_DIR,
    settings.MCP_OUTPUT_MODE,
)


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with API information.

    Returns:
        API information and available endpoints.
    """
    return {
        "service": "DV1 Visualization Engine",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "render": "POST /api/v1/render",
            "render_html": "POST /api/v1/render/html",
            "render_png": "POST /api/v1/render/png",
            "render_svg": "POST /api/v1/render/svg",
            "render_pdf": "POST /api/v1/render/pdf",
            "render_json": "POST /api/v1/render/json",
            "render_batch": "POST /api/v1/render/batch",
            "dashboard": "POST /api/v1/dashboard",
            "validate": "POST /api/v1/validate",
            "themes": "GET /api/v1/themes",
            "templates": "GET /api/v1/templates",
            "health": "GET /health",
            "metrics": "GET /metrics",
        },
    }