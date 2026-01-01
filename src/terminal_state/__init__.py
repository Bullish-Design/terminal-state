"""Terminal State - Terminal automation with state capture and export."""

from terminal_state.capture import Frame, Recording
from terminal_state.export import (
    AsciinemaExporter,
    GifConfig,
    GifExporter,
    ScreenshotExporter,
)
from terminal_state.input import KeySequence, Keys
from terminal_state.models import SessionConfig
from terminal_state.session import TerminalSession, TmuxBackend

__version__ = "0.1.0"

__all__ = [
    # Core session
    "TerminalSession",
    "TmuxBackend",
    "SessionConfig",
    # Capture
    "Frame",
    "Recording",
    # Input
    "KeySequence",
    "Keys",
    # Export
    "AsciinemaExporter",
    "GifExporter",
    "GifConfig",
    "ScreenshotExporter",
]
