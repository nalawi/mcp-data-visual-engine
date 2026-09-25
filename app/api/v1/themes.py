"""Themes API endpoints."""

import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.infrastructure.themes.theme_engine import theme_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["themes"])


@router.get("/themes")
async def list_themes() -> JSONResponse:
    """List all available themes.

    Returns:
        JSON response with theme names and metadata.
    """
    themes = theme_engine.list_themes()
    theme_details = {}
    for name in themes:
        try:
            theme_details[name] = theme_engine.get_theme(name)
        except KeyError:
            theme_details[name] = {"name": name}
    return JSONResponse(content={"themes": themes, "details": theme_details})


@router.get("/themes/{theme_name}")
async def get_theme(theme_name: str) -> JSONResponse:
    """Get a specific theme by name.

    Args:
        theme_name: Name of the theme.

    Returns:
        JSON response with theme details.
    """
    try:
        theme = theme_engine.get_theme(theme_name)
        palette = theme_engine.get_palette(theme_name)
        return JSONResponse(content={"theme": theme, "palette": palette})
    except KeyError as e:
        raise HTTPException(status_code=404, detail={"error": True, "message": str(e)})