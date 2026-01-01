"""Screenshot export functionality."""

from __future__ import annotations

from pathlib import Path

from terminal_state.capture.frame import Frame
from terminal_state.export.gif import GifExporter


class ScreenshotExporter:
    """Export single frame as PNG screenshot."""

    def __init__(self, gif_exporter: GifExporter | None = None) -> None:
        self.gif_exporter = gif_exporter or GifExporter()

    def export_frame(self, frame: Frame, path: Path) -> None:
        """Export frame as PNG image."""
        image = self.gif_exporter._render_frame(frame)
        image.save(path, format="PNG")
