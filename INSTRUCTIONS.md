# ROLE

You are a Principal Software Architect, Staff Python Engineer, Enterprise Platform Architect, AI Infrastructure Engineer, DevOps Engineer, Security Engineer, Technical Writer, and Visualization Expert.

Your task is to design and implement a COMPLETE PRODUCTION-READY Enterprise AI Visualization Platform.

This is NOT a dashboard application.

This is NOT a Plotly wrapper.

This is an Enterprise Visualization Platform that receives structured visualization specifications (VizSpec) from AI agents, LLMs, applications, REST clients, and MCP clients, then generates high-quality visualizations using interchangeable rendering engines.

The initial renderer is Plotly.

The architecture MUST allow adding future renderers without modifying APIs or business logic.

==========================================================
PROJECT NAME
==========================================================

DV1 Visualization Engine

==========================================================
MAIN OBJECTIVES
==========================================================

Develop an enterprise visualization platform that:

• Receives JSON visualization specifications
• Validates requests
• Transforms data
• Selects renderer
• Generates charts
• Returns images or interactive HTML
• Supports REST API
• Supports MCP
• Supports Python SDK
• Supports batch rendering
• Supports future plugins

Never execute arbitrary Python code.

Never accept executable scripts.

Only accept declarative visualization specifications.

==========================================================
ARCHITECTURE
==========================================================

Use Clean Architecture.

Use Domain Driven Design.

Use SOLID principles.

Use Hexagonal Architecture.

Use CQRS where appropriate.

Use Dependency Injection.

Use Strategy Pattern.

Use Factory Pattern.

Use Builder Pattern.

Use Adapter Pattern.

Use Plugin Architecture.

Application Flow

Client

↓

REST API / MCP

↓

Application Service

↓

VizSpec Validator

↓

Transformation Pipeline

↓

Renderer Factory

↓

Plotly Renderer

↓

Export Engine

↓

PNG / SVG / PDF / HTML / JSON

==========================================================
PROJECT STRUCTURE
==========================================================

Generate complete source code.

dv1_visualization/

app/

api/

v1/

charts.py

dashboard.py

themes.py

templates.py

health.py

metrics.py

application/

commands/

queries/

services/

builders/

factories/

transformers/

domain/

models/

specs/

vizspec.py

dataspec.py

visualspec.py

themespec.py

layoutspec.py

outputspec.py

annotationspec.py

interfaces/

events/

exceptions/

infrastructure/

renderers/

plotly/

base/

plugins/

themes/

storage/

cache/

security/

telemetry/

mcp/

server.py

tools.py

sdk/

python/

tests/

docs/

docker/

scripts/

examples/

==========================================================
CORE DESIGN
==========================================================

Everything is driven by VizSpec.

VizSpec represents visualization intent.

Renderers convert VizSpec into output.

Application layer must never import Plotly directly.

Only renderer adapters may use Plotly.

==========================================================
VIZSPEC
==========================================================

Design a renderer-independent specification.

VizSpec

metadata

data

transforms

encoding

visual

layout

annotations

theme

interaction

output

accessibility

Example

{
    "metadata": {

        "title":"Monthly Revenue",

        "subtitle":"2026"

    },

    "data":{

        "source":"inline",

        "records":[...]

    },

    "transforms":[

        {

            "type":"aggregate"

        }

    ],

    "visual":{

        "type":"line"

    },

    "encoding":{

        "x":"month",

        "y":"revenue",

        "color":"department"

    },

    "layout":{

        "legend":"right"

    },

    "theme":"corporate",

    "output":{

        "format":"png",

        "dpi":300

    }

}

==========================================================
DATA TRANSFORMATION ENGINE
==========================================================

Implement transformation pipeline.

Supported transformations:

Filter

Sort

Group

Aggregate

Window

Pivot

Unpivot

Join

Merge

Normalize

Scale

Log Scale

Rolling Average

Moving Average

Forecast Placeholder

Derived Columns

Calculated Fields

Date Parsing

Missing Value Handling

Outlier Detection

==========================================================
VISUAL ENCODING
==========================================================

Implement grammar of graphics concepts.

Encoding channels

x

y

color

size

shape

opacity

text

tooltip

facet_row

facet_column

animation_frame

animation_group

==========================================================
SUPPORTED CHARTS
==========================================================

Implement using Plotly.

Line

Spline

Area

Stacked Area

Bar

Grouped Bar

Stacked Bar

Horizontal Bar

Pie

Donut

Treemap

Sunburst

Scatter

Bubble

Histogram

Density

Box Plot

Violin

Strip

Heatmap

Correlation Matrix

Hexbin

Contour

Radar

Polar

Waterfall

Funnel

Gauge

Indicator

Timeline

Gantt

Candlestick

OHLC

Financial Volume

3D Scatter

3D Surface

3D Mesh

Parallel Coordinates

Parallel Categories

Network Graph

Sankey

Chord Diagram

Calendar Heatmap

Map Scatter

Map Bubble

Choropleth

Flow Diagram

Every chart inherits from BaseRenderer.

==========================================================
RENDERERS
==========================================================

Implement interface

Renderer

Methods

render()

render_png()

render_svg()

render_pdf()

render_html()

render_json()

render_base64()

Future renderer plugins

Matplotlib

Altair

Bokeh

Vega

Graphviz

Mermaid

NetworkX

==========================================================
THEME ENGINE
==========================================================

Implement reusable themes.

Corporate

Government

Finance

Healthcare

Transportation

Energy

Presentation

Scientific

IEEE

Nature

Minimal

Dark

Light

LinkedIn

Instagram

Users may register custom themes.

==========================================================
ANNOTATION ENGINE
==========================================================

Maximum

Minimum

Average

Median

Regression

Trend Line

Moving Average

Target Line

Reference Line

Forecast

Confidence Interval

Arrow

Callout

Text

Company Logo

Watermark

==========================================================
LAYOUT ENGINE
==========================================================

Automatic spacing

Legend placement

Axis scaling

Label collision detection

Multiple axes

Subplots

Responsive sizing

Print layout

==========================================================
OUTPUT ENGINE
==========================================================

Support

PNG

SVG

PDF

HTML

JSON

WEBP

JPEG

Base64

ZIP

Support high-resolution export

72

150

300

600 DPI

==========================================================
REST API
==========================================================

POST /api/v1/render

POST /api/v1/render/html

POST /api/v1/render/png

POST /api/v1/render/pdf

POST /api/v1/render/svg

POST /api/v1/render/json

POST /api/v1/render/batch

POST /api/v1/dashboard

POST /api/v1/transform

GET /api/v1/themes

GET /api/v1/renderers

GET /api/v1/templates

GET /health

GET /metrics

==========================================================
MCP SERVER
==========================================================

Implement complete MCP Server.

Tools

render_chart

render_dashboard

transform_data

recommend_chart

export_chart

preview_chart

list_themes

list_renderers

list_templates

validate_spec

==========================================================
AI CHART RECOMMENDATION
==========================================================

Implement recommendation engine.

Infer visualization based on:

Data type

Cardinality

Relationships

Time series

Distribution

Composition

Geospatial

Hierarchical

Network

Generate confidence score.

Return reasoning.

==========================================================
PYTHON SDK
==========================================================

Generate SDK.

Example

client.render()

client.dashboard()

client.preview()

client.export()

==========================================================
SECURITY
==========================================================

JWT

OAuth2 Ready

API Keys

RBAC

Rate Limiting

Request Validation

Payload Limits

Timeouts

Audit Logs

Structured Logging

Never execute user code.

==========================================================
OBSERVABILITY
==========================================================

OpenTelemetry

Prometheus

Grafana Metrics

Tracing

Health Checks

Request IDs

==========================================================
CACHE
==========================================================

Redis

Hash VizSpec

Reuse rendered images

TTL

Invalidate cache

==========================================================
STORAGE
==========================================================

Support

Local Storage

S3

Azure Blob

MinIO

Google Cloud Storage

==========================================================
DEPLOYMENT
==========================================================

Docker

Docker Compose

Kubernetes

Helm

NGINX

Traefik

==========================================================
CI/CD
==========================================================

GitHub Actions

Black

Ruff

MyPy

Pytest

Coverage

Bandit

Docker Build

==========================================================
TESTING
==========================================================

Unit Tests

Integration Tests

Golden Image Tests

API Tests

Renderer Tests

Performance Tests

Stress Tests

Target Coverage

>95%

==========================================================
DOCUMENTATION
==========================================================

Generate

README

Architecture Guide

Developer Guide

Plugin Guide

REST API

MCP Guide

Python SDK Guide

Deployment Guide

Theme Guide

Renderer Guide

Examples

==========================================================
CODE QUALITY
==========================================================

Python 3.13

FastAPI

Pydantic v2

Pydantic Settings

Async First

Type Hints

Google Style Docstrings

No placeholder code

No TODOs

No pseudo-code

Every module must be fully implemented.

==========================================================
DELIVERABLES
==========================================================

Generate every source file.

Generate all implementation code.

Generate Docker deployment.

Generate Kubernetes manifests.

Generate MCP server.

Generate REST API.

Generate Python SDK.

Generate complete tests.

Generate example VizSpec files.

Generate example dashboards.

Generate benchmark report.

The project must run successfully with:

docker compose up

or

uvicorn app.main:app

without requiring manual code changes.