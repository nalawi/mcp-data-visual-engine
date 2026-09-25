"""Output file storage service.

Saves rendered visualizations to disk and returns accessible URLs.
The output mode (inline vs url) is controlled via the MCP_OUTPUT_MODE
environment variable.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.core.config import settings

# File extension map
FORMAT_EXTENSIONS = {
    "png": "png",
    "svg": "svg",
    "pdf": "pdf",
    "html": "html",
    "json": "json",
}


class OutputStorage:
    """Handles saving rendered output files to disk."""

    def __init__(self) -> None:
        self._output_dir = Path(settings.OUTPUT_DIR)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        data: bytes,
        fmt: str,
        spec_id: Optional[str] = None,
    ) -> str:
        """Save rendered data to disk and return the public URL.

        Args:
            data: Raw bytes of the rendered output.
            fmt: File format (png, svg, pdf, html, json).
            spec_id: Optional spec identifier for naming.

        Returns:
            Absolute URL to the saved file.
        """
        ext = FORMAT_EXTENSIONS.get(fmt, fmt)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = spec_id or str(uuid.uuid4())[:8]
        filename = f"chart_{timestamp}_{unique_id}.{ext}"

        file_path = self._output_dir / filename
        with open(file_path, "wb") as f:
            f.write(data)

        # Build public URL
        base = settings.BASE_URL.rstrip("/")
        prefix = settings.STATIC_URL_PREFIX.strip("/")
        url = f"{base}/{prefix}/{filename}"
        return url

    def save_text(
        self,
        text: str,
        fmt: str,
        spec_id: Optional[str] = None,
    ) -> str:
        """Save text-based rendered output (SVG, HTML, JSON) to disk.

        Args:
            text: String content of the rendered output.
            fmt: File format (svg, html, json).
            spec_id: Optional spec identifier for naming.

        Returns:
            Absolute URL to the saved file.
        """
        return self.save(text.encode("utf-8"), fmt, spec_id)


# Singleton
output_storage = OutputStorage()