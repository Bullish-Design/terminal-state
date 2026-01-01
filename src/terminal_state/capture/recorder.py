"""Recording model for collections of frames."""

from __future__ import annotations

import time
from pathlib import Path

from pydantic import BaseModel, Field

from terminal_state.capture.frame import Frame


class Recording(BaseModel):
    """Collection of frames with timing."""

    frames: list[Frame] = Field(default_factory=list)
    started_at: float = Field(default_factory=time.time)
    width: int = 0
    height: int = 0
    title: str = ""
    environment: dict[str, str] = Field(default_factory=dict)

    def add_frame(self, frame: Frame) -> None:
        """Add frame to recording."""
        if not self.frames:
            self.width = frame.width
            self.height = frame.height
        self.frames.append(frame)

    @property
    def duration(self) -> float:
        """Total duration in seconds."""
        if not self.frames:
            return 0.0
        return self.frames[-1].timestamp - self.started_at

    def to_asciinema(self, path: Path | str) -> None:
        """Export to asciinema format."""
        from terminal_state.export.asciinema import AsciinemaExporter

        exporter = AsciinemaExporter()
        exporter.export(self, Path(path))

    def to_gif(self, path: Path | str, fps: int = 10) -> None:
        """Export to animated GIF."""
        from terminal_state.export.gif import GifExporter

        exporter = GifExporter(fps=fps)
        exporter.export(self, Path(path))

    def to_screenshot(self, path: Path | str, frame_index: int = -1) -> None:
        """Export single frame as PNG."""
        from terminal_state.export.screenshot import ScreenshotExporter

        exporter = ScreenshotExporter()
        exporter.export_frame(self.frames[frame_index], Path(path))
