"""Example: Creating a dashboard with multiple visualizations using the DV1 SDK."""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.sdk.python import DV1Client


def main():
    """Create a sample dashboard with multiple charts."""
    client = DV1Client(use_direct=True)

    # Define chart specs
    line_spec = {
        "metadata": {"title": "Revenue Trend", "subtitle": "Monthly"},
        "data": {
            "source": "inline",
            "records": [
                {"month": "Jan", "value": 100},
                {"month": "Feb", "value": 120},
                {"month": "Mar", "value": 115},
                {"month": "Apr", "value": 140},
                {"month": "May", "value": 155},
                {"month": "Jun", "value": 170},
            ],
        },
        "visual": {"type": "line", "smooth": True},
        "encoding": {"x": "month", "y": "value"},
        "theme": {"name": "corporate"},
    }

    bar_spec = {
        "metadata": {"title": "Sales by Category"},
        "data": {
            "source": "inline",
            "records": [
                {"category": "Electronics", "sales": 45000},
                {"category": "Clothing", "sales": 32000},
                {"category": "Food", "sales": 28000},
                {"category": "Books", "sales": 15000},
            ],
        },
        "visual": {"type": "bar"},
        "encoding": {"x": "category", "y": "sales"},
        "theme": {"name": "corporate"},
    }

    pie_spec = {
        "metadata": {"title": "Market Share"},
        "data": {
            "source": "inline",
            "records": [
                {"product": "Product A", "share": 35},
                {"product": "Product B", "share": 25},
                {"product": "Product C", "share": 20},
                {"product": "Product D", "share": 20},
            ],
        },
        "visual": {"type": "donut"},
        "encoding": {"x": "product", "y": "share"},
        "theme": {"name": "corporate"},
    }

    # Render individual charts
    print("Rendering line chart...")
    line_html = client.render_html(line_spec)
    print(f"  HTML length: {len(line_html)} chars")

    print("Rendering bar chart...")
    bar_html = client.render_html(bar_spec)
    print(f"  HTML length: {len(bar_html)} chars")

    print("Rendering pie chart...")
    pie_html = client.render_html(pie_spec)
    print(f"  HTML length: {len(pie_html)} chars")

    # Create dashboard
    print("\nCreating dashboard...")
    dashboard_html = client.dashboard([line_spec, bar_spec, pie_spec])

    # Save dashboard
    output_path = os.path.join(
        os.path.dirname(__file__), "..", "output", "dashboard_example.html"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(dashboard_html)
    print(f"Dashboard saved to: {output_path}")

    # Get chart recommendations
    print("\nGetting chart recommendations...")
    recommendations = client.recommend_chart({
        "fields": [
            {"name": "date", "type": "date"},
            {"name": "revenue", "type": "number"},
            {"name": "category", "type": "string", "cardinality": 5},
        ],
    })
    print(f"  Top recommendation: {recommendations['recommendations'][0]['chart_type']}")
    print(f"  Confidence: {recommendations['recommendations'][0]['confidence']}")

    # List themes
    print("\nAvailable themes:")
    themes = client.list_themes()
    for theme in themes:
        print(f"  - {theme}")

    print("\nDone!")


if __name__ == "__main__":
    main()