# DV1 Visualization Engine

**Enterprise AI Visualization Platform**

DV1 Visualization Engine is a production-ready enterprise platform that receives structured visualization specifications (VizSpec) from AI agents, LLMs, applications, REST clients, and MCP clients, then generates high-quality visualizations using interchangeable rendering engines.

## Architecture

```
Client → REST API / MCP → Application Service → VizSpec Validator → Transformation Pipeline → Renderer Factory → Plotly Renderer → Export Engine → PNG / SVG / PDF / HTML / JSON
```

### Clean Architecture Layers

- **Domain Layer**: Core business logic, VizSpec models, interfaces
- **Application Layer**: Services, factories, transformers, commands/queries
- **Infrastructure Layer**: Renderers (Plotly), themes, storage, cache, security
- **API Layer**: REST endpoints, MCP server
- **SDK Layer**: Python client SDK

## Quick Start

### Using Docker Compose

```bash
docker compose up
```

The API will be available at `http://localhost:8000`.

### Using Uvicorn

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Render
- `POST /api/v1/render` - Render a visualization
- `POST /api/v1/render/html` - Render as HTML
- `POST /api/v1/render/png` - Render as PNG
- `POST /api/v1/render/svg` - Render as SVG
- `POST /api/v1/render/pdf` - Render as PDF
- `POST /api/v1/render/json` - Render as JSON
- `POST /api/v1/render/batch` - Batch render

### Dashboard
- `POST /api/v1/dashboard` - Create a dashboard

### Management
- `GET /api/v1/themes` - List themes
- `GET /api/v1/renderers` - List renderers
- `GET /api/v1/templates` - List templates
- `POST /api/v1/validate` - Validate a VizSpec

### System
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

## VizSpec Example

```json
{
  "metadata": {
    "title": "Monthly Revenue",
    "subtitle": "2026"
  },
  "data": {
    "source": "inline",
    "records": [
      {"month": "Jan", "revenue": 120000},
      {"month": "Feb", "revenue": 135000}
    ]
  },
  "visual": {
    "type": "line"
  },
  "encoding": {
    "x": "month",
    "y": "revenue"
  },
  "theme": {
    "name": "corporate"
  },
  "output": {
    "format": "html"
  }
}
```

## Supported Chart Types (50+)

Line, Spline, Area, Stacked Area, Bar, Grouped Bar, Stacked Bar, Horizontal Bar, Pie, Donut, Treemap, Sunburst, Scatter, Bubble, Histogram, Density, Box Plot, Violin, Strip, Heatmap, Correlation Matrix, Hexbin, Contour, Radar, Polar, Waterfall, Funnel, Gauge, Indicator, Timeline, Gantt, Candlestick, OHLC, Financial Volume, 3D Scatter, 3D Surface, 3D Mesh, Parallel Coordinates, Parallel Categories, Network Graph, Sankey, Chord Diagram, Calendar Heatmap, Map Scatter, Map Bubble, Choropleth, Flow Diagram

## Themes (16 built-in)

Corporate, Government, Finance, Healthcare, Transportation, Energy, Presentation, Scientific, IEEE, Nature, Minimal, Dark, Light, LinkedIn, Instagram

## Python SDK

```python
from app.sdk.python import DV1Client

client = DV1Client()

# Render a chart
result = client.render(spec)

# Export as PNG
png_bytes = client.render_png(spec)

# Create a dashboard
html = client.dashboard([spec1, spec2, spec3])

# Get chart recommendations
recs = client.recommend_chart({"fields": [...]})
```

## MCP Server

The DV1 Visualization Engine includes a complete MCP (Model Context Protocol) server that exposes all visualization capabilities as tools for AI agents, LLMs, and MCP-compatible clients (Claude Desktop, Cline, etc.).

### MCP Server Endpoint

The MCP server is accessible via the FastAPI application at:

```
GET  /mcp/tools       - List all available MCP tools with their schemas
POST /mcp/tools/{name} - Execute a specific MCP tool
```

### Connecting from MCP Clients

To connect from an MCP-compatible client (e.g., Claude Desktop, Cline), add the following to your MCP configuration:

```json
{
  "mcpServers": {
    "dv1-visualization": {
      "url": "http://localhost:8000/mcp",
      "command": "uvicorn",
      "args": ["app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    }
  }
}
```

### Using MCP Tools via curl

List all available tools:

```bash
curl http://localhost:8000/mcp/tools | python -m json.tool
```

Call a tool (e.g., render a chart):

```bash
curl -X POST http://localhost:8000/mcp/tools/render_chart \
  -H "Content-Type: application/json" \
  -d '{
    "spec": {
      "metadata": {"title": "MCP Chart"},
      "data": {"source": "inline", "records": [{"x": "A", "y": 10}, {"x": "B", "y": 25}]},
      "visual": {"type": "bar"},
      "encoding": {"x": "x", "y": "y"}
    }
  }' | python -m json.tool
```

### Using MCP Tools via Python SDK

```python
from app.mcp.server import mcp_server

# List available tools
tools = mcp_server.get_tool_definitions()
for tool in tools:
    print(f"{tool['name']}: {tool['description']}")

# Call a tool
result = await mcp_server.handle_tool_call("render_chart", {
    "spec": {
        "metadata": {"title": "SDK Chart"},
        "data": {"source": "inline", "records": [{"x": "A", "y": 10}]},
        "visual": {"type": "bar"},
        "encoding": {"x": "x", "y": "y"}
    }
})
```

### Available MCP Tools (14 tools)

| Tool | Description | Input |
|------|-------------|-------|
| `render_chart` | Render a visualization from VizSpec | `spec` (object, required) |
| `render_html` | Render as interactive HTML | `spec` (object, required) |
| `render_png` | Render as base64-encoded PNG | `spec` (object, required) |
| `render_svg` | Render as SVG string | `spec` (object, required) |
| `render_pdf` | Render as base64-encoded PDF | `spec` (object, required) |
| `render_batch` | Batch render multiple charts | `specs` (array, required) |
| `validate_spec` | Validate a VizSpec without rendering | `spec` (object, required) |
| `recommend_chart` | Get AI chart recommendations | `data` (object, required) |
| `list_themes` | List all available themes | None |
| `list_renderers` | List all available renderers | None |
| `list_templates` | List all chart templates | None |
| `preview_chart` | Preview a chart (returns HTML) | `spec` (object, required) |
| `export_chart` | Export chart in specified format | `spec` (object), `format` (string) |
| `transform_data` | Apply data transformations | `data` (array), `transforms` (array) |

## Deployment

### Docker
```bash
docker compose up
```

### Kubernetes
```bash
kubectl apply -f k8s-deployment.yaml
```

## Testing

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## License

MIT