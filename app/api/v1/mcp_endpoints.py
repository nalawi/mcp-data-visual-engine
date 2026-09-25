"""MCP HTTP endpoints for DV1 Visualization Engine.

Exposes MCP tools as HTTP endpoints for AI agents and clients.
Supports both JSON-RPC 2.0 protocol and REST-style endpoints.
"""

import logging
from typing import Any, Dict, Optional, Union

from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.responses import JSONResponse

from app.mcp.server import mcp_server

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mcp", tags=["mcp"])


# ---------------------------------------------------------------------------
# JSON-RPC 2.0 endpoint
# ---------------------------------------------------------------------------

def _make_jsonrpc_error(
    code: int,
    message: str,
    data: Optional[Any] = None,
    id: Optional[Union[str, int, None]] = None,
) -> Dict[str, Any]:
    """Build a JSON-RPC 2.0 error response.

    Args:
        code: Error code (follows JSON-RPC 2.0 spec).
        message: Error message.
        data: Optional additional error data.
        id: Request identifier.

    Returns:
        JSON-RPC 2.0 error response dict.
    """
    error: Dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "error": error, "id": id}


def _make_jsonrpc_success(
    result: Any,
    id: Optional[Union[str, int, None]] = None,
) -> Dict[str, Any]:
    """Build a JSON-RPC 2.0 success response.

    Args:
        result: The result payload.
        id: Request identifier.

    Returns:
        JSON-RPC 2.0 success response dict.
    """
    return {"jsonrpc": "2.0", "result": result, "id": id}


@router.post("")
async def jsonrpc_endpoint(request: Request) -> JSONResponse:
    """JSON-RPC 2.0 entry point for MCP protocol.

    Accepts JSON-RPC 2.0 requests where the method is one of:
      - "tools/list"   – list available tools with their input schemas
      - "tools/call"   – call a specific tool with arguments

    Request format (per JSON-RPC 2.0):
      {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
          "name": "render_chart",
          "arguments": { ... }
        }
      }

    Returns:
        JSON-RPC 2.0 response.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content=_make_jsonrpc_error(
                code=-32700,
                message="Parse error: invalid JSON",
                id=None,
            ),
        )

    # ---- Validate JSON-RPC 2.0 envelope ----
    jsonrpc_version = body.get("jsonrpc")
    if jsonrpc_version != "2.0":
        return JSONResponse(
            status_code=400,
            content=_make_jsonrpc_error(
                code=-32600,
                message=f"Invalid JSON-RPC version: {jsonrpc_version!r}",
                id=body.get("id"),
            ),
        )

    method: str = body.get("method", "")
    req_id = body.get("id")
    params: Dict[str, Any] = body.get("params", {})

    if not method:
        return JSONResponse(
            status_code=400,
            content=_make_jsonrpc_error(
                code=-32600,
                message="Method not specified",
                id=req_id,
            ),
        )

    # ---- Route method ----
    if method == "tools/list":
        try:
            tools = mcp_server.get_tool_definitions()
            return JSONResponse(
                content=_make_jsonrpc_success(
                    result={"tools": tools},
                    id=req_id,
                )
            )
        except Exception as e:
            logger.exception("tools/list failed")
            return JSONResponse(
                status_code=500,
                content=_make_jsonrpc_error(
                    code=-32603,
                    message=f"Internal error: {e}",
                    id=req_id,
                ),
            )

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if not tool_name:
            return JSONResponse(
                status_code=400,
                content=_make_jsonrpc_error(
                    code=-32602,
                    message="Missing required parameter: 'name'",
                    id=req_id,
                ),
            )

        try:
            result = await mcp_server.handle_tool_call(tool_name, arguments)
            return JSONResponse(
                content=_make_jsonrpc_success(
                    result=result,
                    id=req_id,
                )
            )
        except ValueError as e:
            return JSONResponse(
                status_code=404,
                content=_make_jsonrpc_error(
                    code=-32602,
                    message=f"Tool not found: {tool_name}",
                    data=str(e),
                    id=req_id,
                ),
            )
        except Exception as e:
            logger.exception(f"tools/call '{tool_name}' failed")
            return JSONResponse(
                status_code=500,
                content=_make_jsonrpc_error(
                    code=-32603,
                    message=f"Internal error executing '{tool_name}': {e}",
                    id=req_id,
                ),
            )

    else:
        return JSONResponse(
            status_code=400,
            content=_make_jsonrpc_error(
                code=-32601,
                message=f"Method not found: {method}",
                id=req_id,
            ),
        )


# ---------------------------------------------------------------------------
# Existing REST-style endpoints (kept for backward-compatibility)
# ---------------------------------------------------------------------------

@router.get("/tools")
async def list_mcp_tools_get() -> JSONResponse:
    """List all available MCP tools with their schemas.

    Returns:
        JSON response with tool definitions.
    """
    tools = mcp_server.get_tool_definitions()
    return JSONResponse(content={"tools": tools})


@router.post("/tools")
async def list_mcp_tools_post() -> JSONResponse:
    """List all available MCP tools with their schemas.

    Returns:
        JSON response with tool definitions.
    """
    tools = mcp_server.get_tool_definitions()
    return JSONResponse(content={"tools": tools})


@router.post("/tools/{tool_name}")
async def call_mcp_tool(
    tool_name: str,
    arguments: Dict[str, Any] = Body(..., description="Tool arguments"),
) -> JSONResponse:
    """Execute an MCP tool by name.

    Args:
        tool_name: Name of the tool to execute.
        arguments: Tool arguments matching the tool's input schema.

    Returns:
        JSON response with tool execution result.
    """
    try:
        result = await mcp_server.handle_tool_call(tool_name, arguments)
        return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": True, "message": str(e)})
    except Exception as e:
        logger.exception(f"MCP tool '{tool_name}' failed")
        raise HTTPException(status_code=500, detail={"error": True, "message": str(e)})


@router.get("/tools/{tool_name}")
async def get_mcp_tool(tool_name: str) -> JSONResponse:
    """Get the schema for a specific MCP tool.

    Args:
        tool_name: Name of the tool.

    Returns:
        JSON response with the tool's input schema.
    """
    tools = mcp_server.get_tool_definitions()
    for tool in tools:
        if tool["name"] == tool_name:
            return JSONResponse(content={"tool": tool})
    raise HTTPException(
        status_code=404,
        detail={"error": True, "message": f"Tool '{tool_name}' not found."},
    )