# DV1 Visualization Engine - Quick Start Guide

## Start the Server

```bash
# Using uvicorn (development)
cd dv1_visualization
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Docker Compose
docker compose up
```

The API will be available at `http://localhost:8000`.

Interactive API docs: http://localhost:8000/docs

---

## 1. Health Check

Verify the server is running.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "DV1 Visualization Engine",
  "version": "1.0.0",
  "uptime_seconds": 12.5,
  "timestamp": 1712345678.9
}
```

---

## 2. Render a Line Chart (HTML)

Create a line chart showing monthly revenue.

```bash
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "title": "Monthly Revenue",
      "subtitle": "2026 Fiscal Year"
    },
    "data": {
      "source": "inline",
      "records": [
        {"month": "Jan", "revenue": 120000},
        {"month": "Feb", "revenue": 135000},
        {"month": "Mar", "revenue": 142000},
        {"month": "Apr", "revenue": 158000},
        {"month": "May", "revenue": 165000},
        {"month": "Jun", "revenue": 180000}
      ]
    },
    "visual": {
      "type": "line",
      "smooth": true,
      "line_width": 3
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
  }' -o line_chart.html
```

Open `line_chart.html` in your browser to see the interactive chart.

---

## 3. Render a Bar Chart (PNG Image)

Create a bar chart comparing sales by category and save as PNG.

```bash
curl -X POST http://localhost:8000/api/v1/render/png \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "title": "Sales by Category"
    },
    "data": {
      "source": "inline",
      "records": [
        {"category": "Electronics", "sales": 45000},
        {"category": "Clothing", "sales": 32000},
        {"category": "Food", "sales": 28000},
        {"category": "Books", "sales": 15000}
      ]
    },
    "visual": {
      "type": "bar"
    },
    "encoding": {
      "x": "category",
      "y": "sales"
    },
    "theme": {
      "name": "corporate"
    },
    "output": {
      "format": "png",
      "dpi": 300
    }
  }' -o bar_chart.png
```

---

## 4. Render a Pie Chart (SVG)

Create a donut chart showing market share.

```bash
curl -X POST http://localhost:8000/api/v1/render/svg \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "title": "Market Share Distribution"
    },
    "data": {
      "source": "inline",
      "records": [
        {"product": "Product A", "share": 35},
        {"product": "Product B", "share": 25},
        {"product": "Product C", "share": 20},
        {"product": "Product D", "share": 20}
      ]
    },
    "visual": {
      "type": "donut"
    },
    "encoding": {
      "x": "product",
      "y": "share"
    },
    "theme": {
      "name": "corporate"
    }
  }' -o donut_chart.svg
```

---

## 5. Render a Scatter Plot (JSON Data)

Get the Plotly JSON representation of a scatter plot.

```bash
curl -X POST http://localhost:8000/api/v1/render/json \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "title": "Price vs Demand"
    },
    "data": {
      "source": "inline",
      "records": [
        {"price": 10, "demand": 100},
        {"price": 15, "demand": 85},
        {"price": 20, "demand": 70},
        {"price": 25, "demand": 55},
        {"price": 30, "demand": 40}
      ]
    },
    "visual": {
      "type": "scatter",
      "marker_size": 12
    },
    "encoding": {
      "x": "price",
      "y": "demand"
    }
  }' | python -m json.tool
```

---

## 6. Render a PDF Report

Create a financial candlestick chart as PDF.

```bash
curl -X POST http://localhost:8000/api/v1/render/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "title": "Stock Price - Q1 2026"
    },
    "data": {
      "source": "inline",
      "records": [
        {"date": "2026-01-07", "open": 150, "high": 155, "low": 148, "close": 153},
        {"date": "2026-01-14", "open": 153, "high": 158, "low": 151, "close": 156},
        {"date": "2026-01-21", "open": 156, "high": 162, "low": 154, "close": 160}
      ]
    },
    "visual": {
      "type": "candlestick"
    },
    "encoding": {
      "x": "date",
      "open": "open",
      "high": "high",
      "low": "low",
      "close": "close"
    },
    "output": {
      "format": "pdf",
      "dpi": 150
    }
  }' -o candlestick.pdf
```

---

## 7. Batch Render Multiple Charts

Render multiple charts in a single request.

```bash
curl -X POST http://localhost:8000/api/v1/render/batch \
  -H "Content-Type: application/json" \
  -d '[
    {
      "metadata": {"title": "Chart 1 - Line"},
      "data": {"source": "inline", "records": [{"x": "A", "y": 10}, {"x": "B", "y": 20}]},
      "visual": {"type": "line"},
      "encoding": {"x": "x", "y": "y"},
      "output": {"format": "json"}
    },
    {
      "metadata": {"title": "Chart 2 - Bar"},
      "data": {"source": "inline", "records": [{"cat": "X", "val": 30}, {"cat": "Y", "val": 50}]},
      "visual": {"type": "bar"},
      "encoding": {"x": "cat", "y": "val"},
      "output": {"format": "json"}
    }
  ]' | python -m json.tool
```

---

## 8. Create a Dashboard

Create a multi-panel dashboard with several charts.

```bash
curl -X POST http://localhost:8000/api/v1/dashboard \
  -H "Content-Type: application/json" \
  -d '{
    "specs": [
      {
        "metadata": {"title": "Revenue Trend"},
        "data": {"source": "inline", "records": [{"month": "Jan", "value": 100}, {"month": "Feb", "value": 120}, {"month": "Mar", "value": 115}]},
        "visual": {"type": "line"},
        "encoding": {"x": "month", "y": "value"},
        "theme": {"name": "corporate"}
      },
      {
        "metadata": {"title": "Sales by Category"},
        "data": {"source": "inline", "records": [{"cat": "A", "val": 40}, {"cat": "B", "val": 30}, {"cat": "C", "val": 20}]},
        "visual": {"type": "bar"},
        "encoding": {"x": "cat", "y": "val"},
        "theme": {"name": "corporate"}
      },
      {
        "metadata": {"title": "Market Share"},
        "data": {"source": "inline", "records": [{"prod": "X", "pct": 45}, {"prod": "Y", "pct": 30}, {"prod": "Z", "pct": 25}]},
        "visual": {"type": "donut"},
        "encoding": {"x": "prod", "y": "pct"},
        "theme": {"name": "corporate"}
      }
    ],
    "layout": {
      "rows": 2,
      "cols": 2
    }
  }' -o dashboard.html
```

Open `dashboard.html` in your browser.

---

## 9. Validate a VizSpec

Check if a VizSpec is valid before rendering.

```bash
curl -X POST http://localhost:8000/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "Test"},
    "data": {"source": "inline", "records": [{"x": 1, "y": 2}]},
    "visual": {"type": "line"},
    "encoding": {"x": "x", "y": "y"}
  }' | python -m json.tool
```

**Response (valid):**
```json
{
  "valid": true,
  "spec_id": "a1b2c3d4-...",
  "errors": []
}
```

---

## 10. List Available Themes

```bash
curl http://localhost:8000/api/v1/themes | python -m json.tool
```

**Response:**
```json
{
  "themes": ["corporate", "dark", "energy", "finance", "government", "healthcare", "ieee", "instagram", "light", "linkedin", "minimal", "nature", "presentation", "scientific", "transportation"],
  "details": { ... }
}
```

---

## 11. List Chart Templates

```bash
curl http://localhost:8000/api/v1/templates | python -m json.tool
```

---

## 12. Get a Specific Template

```bash
curl http://localhost:8000/api/v1/templates/line_simple | python -m json.tool
```

---

## 13. Render with Different Themes

Compare the same chart with different themes.

```bash
# Dark theme
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "Dark Theme Example"},
    "data": {"source": "inline", "records": [{"x": "A", "y": 10}, {"x": "B", "y": 25}]},
    "visual": {"type": "bar"},
    "encoding": {"x": "x", "y": "y"},
    "theme": {"name": "dark"}
  }' -o dark_chart.html

# Finance theme
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "Finance Theme"},
    "data": {"source": "inline", "records": [{"x": "A", "y": 10}, {"x": "B", "y": 25}]},
    "visual": {"type": "bar"},
    "encoding": {"x": "x", "y": "y"},
    "theme": {"name": "finance"}
  }' -o finance_chart.html
```

---

## 14. Render with Annotations

Add reference lines and text annotations to a chart.

```bash
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "Sales with Target"},
    "data": {
      "source": "inline",
      "records": [
        {"month": "Jan", "sales": 80},
        {"month": "Feb", "sales": 95},
        {"month": "Mar", "sales": 110},
        {"month": "Apr", "sales": 105}
      ]
    },
    "visual": {"type": "bar"},
    "encoding": {"x": "month", "y": "sales"},
    "annotations": [
      {"type": "reference_line", "y": 100, "label": "Target: 100", "line_dash": "dash", "color": "red"},
      {"type": "text", "label": "Above Target", "x": "Mar", "y": 112, "color": "green"}
    ]
  }' -o annotated_chart.html
```

---

## 15. Render a 3D Scatter Plot

```bash
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "3D Data Visualization"},
    "data": {
      "source": "inline",
      "records": [
        {"x": 1, "y": 2, "z": 3, "group": "A"},
        {"x": 2, "y": 3, "z": 1, "group": "A"},
        {"x": 3, "y": 1, "z": 2, "group": "B"},
        {"x": 4, "y": 5, "z": 4, "group": "B"}
      ]
    },
    "visual": {"type": "scatter_3d"},
    "encoding": {"x": "x", "y": "y", "z": "z", "color": "group"}
  }' -o scatter_3d.html
```

---

## 16. Render a Heatmap

```bash
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "Correlation Heatmap"},
    "data": {
      "source": "inline",
      "records": [
        {"x": "A", "y": "X", "value": 0.9},
        {"x": "A", "y": "Y", "value": 0.3},
        {"x": "B", "y": "X", "value": 0.4},
        {"x": "B", "y": "Y", "value": 0.8}
      ]
    },
    "visual": {"type": "heatmap"},
    "encoding": {"x": "x", "y": "y", "color": "value"}
  }' -o heatmap.html
```

---

## 17. Render a Sankey Diagram

```bash
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "Energy Flow"},
    "data": {
      "source": "inline",
      "records": [
        {"source": "Solar", "target": "Grid", "value": 40},
        {"source": "Wind", "target": "Grid", "value": 30},
        {"source": "Grid", "target": "Residential", "value": 35},
        {"source": "Grid", "target": "Commercial", "value": 25},
        {"source": "Grid", "target": "Industrial", "value": 10}
      ]
    },
    "visual": {"type": "sankey"},
    "encoding": {"source": "source", "target": "target", "value": "value"}
  }' -o sankey.html
```

---

## 18. Render a Map Scatter Plot

```bash
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "Store Locations"},
    "data": {
      "source": "inline",
      "records": [
        {"city": "NYC", "lat": 40.7128, "lon": -74.0060, "sales": 500},
        {"city": "LA", "lat": 34.0522, "lon": -118.2437, "sales": 400},
        {"city": "Chicago", "lat": 41.8781, "lon": -87.6298, "sales": 300}
      ]
    },
    "visual": {"type": "map_scatter"},
    "encoding": {"lat": "lat", "lon": "lon", "color": "sales", "size": "sales"}
  }' -o map.html
```

---

## 19. Render a Gantt Chart

```bash
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "Project Timeline"},
    "data": {
      "source": "inline",
      "records": [
        {"task": "Design", "start": "2026-01-01", "end": "2026-01-15", "resource": "Team A"},
        {"task": "Development", "start": "2026-01-16", "end": "2026-02-15", "resource": "Team B"},
        {"task": "Testing", "start": "2026-02-16", "end": "2026-03-01", "resource": "Team A"}
      ]
    },
    "visual": {"type": "gantt"},
    "encoding": {"task": "task", "start": "start", "end": "end", "resource": "resource"}
  }' -o gantt.html
```

---

## 20. Render a Waterfall Chart

```bash
curl -X POST http://localhost:8000/api/v1/render/html \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"title": "P&L Waterfall"},
    "data": {
      "source": "inline",
      "records": [
        {"item": "Revenue", "amount": 1000},
        {"item": "COGS", "amount": -400},
        {"item": "OpEx", "amount": -300},
        {"item": "Tax", "amount": -100},
        {"item": "Net Profit", "amount": 200}
      ]
    },
    "visual": {"type": "waterfall"},
    "encoding": {"x": "item", "y": "amount"}
  }' -o waterfall.html
```

---

## VizSpec Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `metadata.title` | string | No | Chart title |
| `metadata.subtitle` | string | No | Chart subtitle |
| `data.source` | string | Yes | `"inline"`, `"url"`, `"file"` |
| `data.records` | array | Yes (for inline) | Array of data objects |
| `visual.type` | string | Yes | Chart type (see below) |
| `visual.smooth` | bool | No | Smooth curves for line charts |
| `encoding.x` | string | Depends | X-axis field name |
| `encoding.y` | string | Depends | Y-axis field name |
| `encoding.color` | string | No | Color grouping field |
| `encoding.size` | string | No | Size field (bubble charts) |
| `theme.name` | string | No | Theme name |
| `output.format` | string | No | `"html"`, `"png"`, `"svg"`, `"pdf"`, `"json"` |
| `output.dpi` | int | No | Image resolution (72-600) |

## Supported Chart Types (50+)

`line`, `spline`, `area`, `stacked_area`, `bar`, `grouped_bar`, `stacked_bar`, `horizontal_bar`, `pie`, `donut`, `treemap`, `sunburst`, `scatter`, `bubble`, `histogram`, `density`, `box_plot`, `violin`, `strip`, `heatmap`, `correlation_matrix`, `hexbin`, `contour`, `radar`, `polar`, `waterfall`, `funnel`, `gauge`, `indicator`, `timeline`, `gantt`, `candlestick`, `ohlc`, `financial_volume`, `scatter_3d`, `surface_3d`, `mesh_3d`, `parallel_coordinates`, `parallel_categories`, `network_graph`, `sankey`, `chord_diagram`, `calendar_heatmap`, `map_scatter`, `map_bubble`, `choropleth`, `flow_diagram`

## Available Themes (16)

`corporate`, `government`, `finance`, `healthcare`, `transportation`, `energy`, `presentation`, `scientific`, `ieee`, `nature`, `minimal`, `dark`, `light`, `linkedin`, `instagram`