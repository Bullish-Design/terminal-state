"""GIF export functionality."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel, Field

from terminal_state.capture.frame import Frame
from terminal_state.capture.recorder import Recording


class GifConfig(BaseModel):
    """Configuration for GIF export."""

    fps: int = Field(default=10, ge=1, le=60)
    font_path: str = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    font_size: int = 14
    bg_color: tuple[int, int, int] = (0, 0, 0)
    fg_color: tuple[int, int, int] = (200, 200, 200)
    char_width: int = 9
    char_height: int = 18


class GifExporter:
    """Export recordings to animated GIF."""

    def __init__(self, config: GifConfig | None = None, **kwargs: object) -> None:
        self.config = config or GifConfig(**kwargs)  # type: ignore[arg-type]
        try:
            self.font = ImageFont.truetype(self.config.font_path, self.config.font_size)
        except OSError:
            self.font = ImageFont.load_default()

    def export(self, recording: Recording, path: Path) -> None:
        """Export recording as animated GIF."""
        images = [self._render_frame(frame) for frame in recording.frames]

        if not images:
            raise ValueError("No frames to export")

        frame_duration = int(1000 / self.config.fps)

        images[0].save(
            path,
            save_all=True,
            append_images=images[1:],
            duration=frame_duration,
            loop=0,
            optimize=False,
        )

    def _render_frame(self, frame: Frame) -> Image.Image:
        """Render single frame to image."""
        img_width = frame.width * self.config.char_width
        img_height = frame.height * self.config.char_height

        image = Image.new("RGB", (img_width, img_height), self.config.bg_color)
        draw = ImageDraw.Draw(image)

        # Strip ANSI codes (simple version)
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        clean_content = ansi_escape.sub("", frame.content)

        for y, line in enumerate(clean_content.split("\n")[: frame.height]):
            draw.text(
                (0, y * self.config.char_height),
                line,
                font=self.font,
                fill=self.config.fg_color,
            )

        return image
