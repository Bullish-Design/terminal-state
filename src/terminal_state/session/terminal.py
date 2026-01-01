"""High-level terminal session interface."""

from __future__ import annotations

import re
import time
from typing import Self

from terminal_state.capture.frame import Frame
from terminal_state.capture.recorder import Recording
from terminal_state.input.keys import KeySequence, Keys
from terminal_state.models.config import SessionConfig
from terminal_state.session.backend import TmuxBackend


class TerminalSession:
    """High-level terminal session interface."""

    def __init__(self, config: SessionConfig) -> None:
        self.config = config
        self.backend = TmuxBackend(config)
        self.recording = Recording(width=config.width, height=config.height)
        self._started = False

    @classmethod
    def create(cls, **kwargs) -> Self:  # type: ignore[misc]
        """Create and start a new session."""
        config = SessionConfig(**kwargs)
        session = cls(config)
        session.start()
        return session

    def start(self) -> None:
        """Start the terminal session."""
        if not self._started:
            self.backend.create()
            self._started = True

    def send_keys(self, keys: str | KeySequence, record: bool = True) -> None:
        """Send key sequence to terminal."""
        if isinstance(keys, str):
            keys = KeySequence(keys=keys, literal=True)

        self.backend.send_keys(keys)

        if record:
            time.sleep(0.1)  # Brief delay for output
            self.recording.add_frame(self.capture())

    def send_command(self, command: str, record: bool = True) -> None:
        """Send command and press enter."""
        self.send_keys(KeySequence(keys=command, literal=True), record=False)
        self.send_keys(Keys.ENTER, record=record)

    def capture(self) -> Frame:
        """Capture current terminal state."""
        return self.backend.capture()

    def expect_text(self, pattern: str, timeout: float = 5.0) -> bool:
        """Wait for text to appear in terminal output."""
        start_time = time.time()

        while (time.time() - start_time) < timeout:
            frame = self.capture()
            if re.search(pattern, frame.content):
                return True
            time.sleep(0.1)

        return False

    def destroy(self) -> None:
        """Destroy the terminal session."""
        if self._started:
            self.backend.destroy()
            self._started = False

    def __enter__(self) -> Self:
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, *args: object) -> None:
        """Context manager exit."""
        self.destroy()
