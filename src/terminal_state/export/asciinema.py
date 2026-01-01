"""Asciinema format exporter."""

from __future__ import annotations

import json
from pathlib import Path

from terminal_state.capture.recorder import Recording


class AsciinemaExporter:
    """Export recordings to asciinema format (v2).

    Format spec: https://docs.asciinema.org/manual/asciicast/v2/
    """

    def export(self, recording: Recording, path: Path) -> None:
        """Export recording to asciinema format."""
        with open(path, "w") as f:
            # Header
            header = {
                "version": 2,
                "width": recording.width,
                "height": recording.height,
                "timestamp": int(recording.started_at),
                "title": recording.title or "Terminal Recording",
                "env": recording.environment or {"TERM": "xterm-256color"},
            }
            f.write(json.dumps(header) + "\n")

            # Events
            for frame in recording.frames:
                timestamp = frame.timestamp - recording.started_at
                event = [timestamp, "o", frame.content]
                f.write(json.dumps(event) + "\n")
